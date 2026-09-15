import os
import re
from collections import defaultdict

from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(p: str) -> str:
    try:
        if AppState.project_root:
            return os.path.relpath(p, AppState.project_root).replace("\\", "/")
        return os.path.basename(p)
    except Exception:
        return os.path.basename(p)


# Regex patterns for Firebase / Firestore
# 1. Modular SDK: collection(db, "users") or collection(firestore, `businesses/${businessId}/.../kyc_records`)
MODULAR_COLLECTION_PATTERN = re.compile(
    r'\bcollection\s*\(\s*(?:[a-zA-Z0-9_$]+(?:\(\))?)\s*,\s*[`\'"]([^`\'"]+)[`\'"]',
    re.IGNORECASE
)

# 2. Compat SDK: db.collection("users") or db.collection(`...`)
COMPAT_COLLECTION_PATTERN = re.compile(
    r'\b(?:db|firestore)\.collection\s*\(\s*[`\'"]([^`\'"]+)[`\'"]',
    re.IGNORECASE
)

# 3. doc(...) references
DOC_PATTERN = re.compile(
    r'\bdoc\s*\(\s*(?:[a-zA-Z0-9_$]+(?:\(\))?)\s*,\s*[`\'"]([^`\'"]+)[`\'"]',
    re.IGNORECASE
)

def _normalize_collection_name(raw_path: str):
    """
    Normalizes a path like 'businesses/${businessId}/shops/${shopId}/kyc_records'
    into clean collection name 'kyc_records' and full path 'businesses/{businessId}/shops/{shopId}/kyc_records'.
    """
    clean_path = re.sub(r'\$\{[^}]+\}', lambda m: '{' + m.group(0)[2:-1].strip() + '}', raw_path)
    segments = [s for s in clean_path.split('/') if s and not (s.startswith('{') and s.endswith('}'))]
    if segments:
        col_name = segments[-1]
    else:
        col_name = clean_path
    return col_name, clean_path

# 4. Queries (where, orderBy)
WHERE_PATTERN = re.compile(
    r'\bwhere\s*\(\s*["\']([a-zA-Z0-9_.]+)["\']\s*,\s*["\']([=><!in\-]+)["\']',
    re.IGNORECASE
)
ORDER_BY_PATTERN = re.compile(
    r'\borderBy\s*\(\s*["\']([a-zA-Z0-9_.]+)["\'](?:\s*,\s*["\'](asc|desc)["\'])?',
    re.IGNORECASE
)

# 5. Realtime Listeners
SNAPSHOT_PATTERN = re.compile(r'\bonSnapshot\s*\(', re.IGNORECASE)

# 6. Writes
WRITE_OPS_PATTERN = re.compile(r'\b(setDoc|updateDoc|addDoc|deleteDoc)\s*\(', re.IGNORECASE)
BATCH_PATTERN = re.compile(r'\b(writeBatch|runTransaction)\b', re.IGNORECASE)


def extract_firestore_schema(tree_root):
    """
    Extracts complete Firestore Database Schema, Collections, Query Filters,
    CRUD operations, and generates Mermaid ER diagrams for Web Portals.
    """
    collections = defaultdict(lambda: {
        "files": set(),
        "paths": set(),
        "reads": 0,
        "writes": 0,
        "listeners": 0,
        "queries": set(),
        "order_by": set(),
        "operations": set()
    })

    total_files_scanned = 0

    def walk(node):
        nonlocal total_files_scanned
        if not node.is_dir and node.name.endswith((".js", ".ts", ".jsx", ".tsx")):
            total_files_scanned += 1
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            rel_file = _get_rel_path(node.path)

            # Detect collections
            found_cols = {}
            for m in MODULAR_COLLECTION_PATTERN.finditer(code):
                col_name, full_path = _normalize_collection_name(m.group(1))
                if col_name and len(col_name) > 1 and not col_name.startswith('{'):
                    found_cols[col_name] = full_path

            for m in COMPAT_COLLECTION_PATTERN.finditer(code):
                col_name, full_path = _normalize_collection_name(m.group(1))
                if col_name and len(col_name) > 1 and not col_name.startswith('{'):
                    found_cols[col_name] = full_path

            if not found_cols:
                return

            # Analyze operations inside file
            has_snapshot = bool(SNAPSHOT_PATTERN.search(code))
            write_matches = WRITE_OPS_PATTERN.findall(code)
            has_batch = bool(BATCH_PATTERN.search(code))
            where_matches = WHERE_PATTERN.findall(code)
            order_matches = ORDER_BY_PATTERN.findall(code)

            for col, full_path in found_cols.items():
                col_data = collections[col]
                col_data["files"].add(rel_file)
                if full_path:
                    col_data["paths"].add(full_path)

                if has_snapshot:
                    col_data["listeners"] += 1
                    col_data["operations"].add("Realtime onSnapshot")

                if write_matches:
                    col_data["writes"] += len(write_matches)
                    for w in write_matches:
                        col_data["operations"].add(w)

                if has_batch:
                    col_data["operations"].add("Batch/Transaction")

                for field, op in where_matches:
                    col_data["queries"].add(f"{field} {op}")

                for field, direction in order_matches:
                    dir_str = direction or "asc"
                    col_data["order_by"].add(f"{field} ({dir_str})")

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    if not collections:
        return (
            "=" * 60 + "\n"
            "FIRESTORE & BACKEND SCHEMA (WEB PORTAL)\n"
            "=" * 60 + "\n\n"
            "No direct Firestore collection references detected in client source files.\n"
            "If using custom REST/GraphQL endpoints, check service modules."
        )

    lines = []
    lines.append("=" * 60)
    lines.append("FIRESTORE DATABASE SCHEMA & COLLECTION CATALOG")
    lines.append("=" * 60)
    lines.append(f"• Total Collections Detected: {len(collections)}")
    lines.append(f"• Source Files Scanned: {total_files_scanned}")
    lines.append("")

    lines.append("## 1. COLLECTIONS SUMMARY TABLE")
    lines.append("| Collection Name | Interacting Files | Operations | Queries (where) | Order By |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")

    for col in sorted(collections.keys()):
        data = collections[col]
        files_count = len(data["files"])
        ops_str = ", ".join(sorted(data["operations"])) if data["operations"] else "Read/Query"
        queries_str = ", ".join(sorted(data["queries"])) if data["queries"] else "None"
        order_str = ", ".join(sorted(data["order_by"])) if data["order_by"] else "None"
        lines.append(f"| `{col}` | {files_count} files | {ops_str} | {queries_str} | {order_str} |")

    lines.append("")
    lines.append("## 2. DETAILED COLLECTION USAGE & FILES")
    for col in sorted(collections.keys()):
        data = collections[col]
        lines.append(f"### Collection: `{col}`")
        if data["operations"]:
            lines.append(f"  • Operations: {', '.join(sorted(data['operations']))}")
        if data["queries"]:
            lines.append(f"  • Filter Criteria: {', '.join(sorted(data['queries']))}")
        if data["order_by"]:
            lines.append(f"  • Sorting / Indexes: {', '.join(sorted(data['order_by']))}")
        lines.append("  • Active Files:")
        for f in sorted(data["files"]):
            lines.append(f"    - {f}")
        lines.append("")

    lines.append("## 3. MERMAID DATA MODEL DIAGRAM")
    lines.append("```mermaid")
    lines.append("classDiagram")
    lines.append("    class FirestoreDB {")
    lines.append("        <<Firebase>>")
    for col in sorted(collections.keys()):
        lines.append(f"        +Collection {col}")
    lines.append("    }")
    for col in sorted(collections.keys()):
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', col)
        lines.append(f"    FirestoreDB --> {clean_name}")
        lines.append(f"    class {clean_name} {{")
        for q in sorted(collections[col]["queries"]):
            field_name = q.split()[0]
            lines.append(f"        +{field_name}")
        lines.append("    }")
    lines.append("```")

    return "\n".join(lines)
