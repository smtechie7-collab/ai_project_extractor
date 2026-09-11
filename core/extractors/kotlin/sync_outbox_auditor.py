import re
import os
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


# Sync Patterns
OUTBOX_ENTITY_PATTERN = re.compile(r'\b(SyncOutboxEntity|SyncOutboxDao|OutboxMutation)\b')
SYNC_WORKER_PATTERN = re.compile(r'\b(FirestoreSyncWorker|CoroutineWorker|Worker)\b')
DEPRECATED_SYNC_PATTERN = re.compile(r'\b(SyncDispatcher|SyncOutboxWorker)\b')

# Direct Firestore calls (Illegal outside sync/ per Article 42)
FIRESTORE_WRITE_PATTERN = re.compile(
    r'\b(?:firestore|FirebaseFirestore\.getInstance\(\))\s*\.\s*collection\s*\([^)]+\)\s*\.\s*(?:add|set|update|delete)\b'
)


def audit_sync_outbox(tree_root):
    """
    Audits Write-Ahead Outbox Cloud Sync Engine and verifies Article 42 Single Sync Engine compliance.
    """
    outbox_files = []
    sync_worker_files = []
    deprecated_sync_violations = []
    direct_firestore_violations = []
    all_kt_files = 0

    def walk(node):
        nonlocal all_kt_files
        if not node.is_dir and node.name.endswith(".kt"):
            all_kt_files += 1
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            rel_p = _get_rel_path(node.path)
            is_sync_folder = "sync/" in rel_p.replace("\\", "/").lower()

            if OUTBOX_ENTITY_PATTERN.search(code):
                outbox_files.append(rel_p)

            if "FirestoreSyncWorker" in code or (SYNC_WORKER_PATTERN.search(code) and is_sync_folder):
                sync_worker_files.append(rel_p)

            # Check CRIT-001 Deprecated Dual Sync Engine
            dep_matches = DEPRECATED_SYNC_PATTERN.findall(code)
            if dep_matches:
                # Ignore comments or deprecation annotations
                if "class SyncDispatcher" not in code and "@Deprecated" not in code:
                    deprecated_sync_violations.append((rel_p, list(set(dep_matches))))

            # Check Article 42 Direct Write Violations (outside sync/)
            if not is_sync_folder and "test" not in rel_p.lower():
                if FIRESTORE_WRITE_PATTERN.search(code):
                    direct_firestore_violations.append(rel_p)

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    lines = []
    lines.append("=" * 70)
    lines.append("🔄 CLOUD SYNC & WRITE-AHEAD OUTBOX ENGINE AUDIT")
    lines.append("=" * 70)
    lines.append(f"• Total Kotlin Source Files Analyzed: {all_kt_files}")
    lines.append("")

    # 1. Outbox Architecture Overview
    lines.append("## 1. WRITE-AHEAD OUTBOX COMPONENTS")
    if outbox_files:
        lines.append("Discovered Outbox Entities & Repositories:")
        for f in sorted(outbox_files):
            lines.append(f"  • `{f}`")
    else:
        lines.append("  ⚠ No explicit SyncOutboxEntity detected. Verify outbox queue naming.")
    lines.append("")

    lines.append("Authorized Cloud Sync Workers:")
    if sync_worker_files:
        for f in sorted(sync_worker_files):
            lines.append(f"  • `{f}` (Article 42 Authorized Processor)")
    else:
        lines.append("  ⚠ No authorized FirestoreSyncWorker found.")
    lines.append("")

    # 2. Constitution Article 42 Compliance
    lines.append("## 2. SINGLE SYNC ENGINE COMPLIANCE (ARTICLE 42)")
    if not direct_firestore_violations and not deprecated_sync_violations:
        lines.append("✅ **STATUS: FULLY COMPLIANT**")
        lines.append("All remote mutations route through the Write-Ahead Outbox. Zero rogue direct Firestore writes found.")
    else:
        lines.append("❌ **STATUS: ARCHITECTURAL VIOLATIONS DETECTED**")
        if deprecated_sync_violations:
            lines.append("### 🚨 CRIT-001 Deprecated Dual Sync Engine References:")
            for f, items in deprecated_sync_violations:
                lines.append(f"  • `{f}`: References deprecated engine: {', '.join(items)}")
        if direct_firestore_violations:
            lines.append("### 🚨 Article 42 Direct Firestore Writes (Outside sync/):")
            for f in direct_firestore_violations:
                lines.append(f"  • `{f}`: Direct Firestore write detected! Must route via Outbox.")
    lines.append("")

    # 3. Mermaid Architecture Flow
    lines.append("## 3. OUTBOX SYNCHRONIZATION PIPELINE (MERMAID)")
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    lines.append("    autonumber")
    lines.append("    actor User as User Action")
    lines.append("    participant UI as Feature Screen / ViewModel")
    lines.append("    participant Repo as Repository")
    lines.append("    participant Room as Room Encrypted DB")
    lines.append("    participant Outbox as SyncOutboxQueue")
    lines.append("    participant Worker as FirestoreSyncWorker")
    lines.append("    participant Cloud as Firestore Cloud")
    lines.append("")
    lines.append("    User->>UI: Submit Financial Transaction")
    lines.append("    UI->>Repo: Execute UseCase")
    lines.append("    critical Atomic DB Transaction")
    lines.append("        Repo->>Room: Write Business Entity (Paise)")
    lines.append("        Repo->>Outbox: Enqueue SyncOutboxEntity (PENDING)")
    lines.append("    end")
    lines.append("    Repo-->>UI: Immediate Local UI Success (Offline-First)")
    lines.append("    Worker->>Outbox: Poll PENDING Mutations")
    lines.append("    Worker->>Cloud: Batch Write to Firestore")
    lines.append("    Cloud-->>Worker: Ack Success")
    lines.append("    Worker->>Outbox: Mark Mutation SYNCED")
    lines.append("```")

    return "\n".join(lines)
