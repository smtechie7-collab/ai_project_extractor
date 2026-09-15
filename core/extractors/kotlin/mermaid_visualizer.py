import re

from core.utils.file_reader import read_text_file

# --- REGEX PATTERNS ---
ENTITY_CLASS_RE = re.compile(
    r'@Entity(?:\([^)]*\))?\s*(?:data\s+class|class)\s+(\w+)\s*\(([\s\S]*?)\)',
    re.MULTILINE
)
TABLE_NAME_RE = re.compile(r'tableName\s*=\s*"([^"]+)"')
FIELD_RE = re.compile(r'(?:val|var)\s+(\w+)\s*:\s*([A-Za-z0-9_<>]+)')

HOST_ROUTE_PATTERN = re.compile(r'composable(?:\s*<[^>]+>|\s*\(\s*(?:route\s*=\s*)?["\']([^"\'{}]+)["\'])')
NAV_CALL_PATTERN = re.compile(r'\.navigate\(\s*["\']([^"\'${}]+)["\']')


def generate_mermaid_visuals(tree_root):
    db_diagram = _generate_db_er_diagram(tree_root)
    nav_diagram = _generate_nav_flow_diagram(tree_root)

    report = []
    report.append("# VISUAL ARCHITECTURE REPORT (MERMAID)")
    report.append("Copy the code blocks below into https://mermaid.live or LLM markdown viewers.\n")

    report.append("## 1. DATABASE ER DIAGRAM")
    report.append("```mermaid")
    report.append(db_diagram)
    report.append("```\n")

    report.append("## 2. NAVIGATION FLOWCHART")
    report.append("```mermaid")
    report.append(nav_diagram)
    report.append("```\n")

    return "\n".join(report)


def _clean_mermaid_id(name: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"n_{cleaned}"
    return cleaned


def _generate_db_er_diagram(tree_root):
    lines = ["erDiagram"]
    has_entities = False

    def walk(node):
        nonlocal has_entities
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            if "@Entity" in code:
                for match in ENTITY_CLASS_RE.finditer(code):
                    has_entities = True
                    class_name = match.group(1)
                    body = match.group(2)

                    # Check for explicit tableName
                    table_name = class_name
                    before_class = code[max(0, match.start() - 200):match.start()]
                    t_match = TABLE_NAME_RE.search(before_class)
                    if t_match:
                        table_name = t_match.group(1)

                    safe_table = _clean_mermaid_id(table_name)
                    lines.append(f"    {safe_table} {{")

                    for line in body.splitlines():
                        f_match = FIELD_RE.search(line)
                        if f_match:
                            col_name = f_match.group(1)
                            col_type = f_match.group(2).replace("<", "~").replace(">", "~")
                            is_pk = "PK" if "@PrimaryKey" in line else ""
                            lines.append(f"        {col_type} {col_name} {is_pk}".rstrip())

                    lines.append("    }")

        for child in node.children:
            walk(child)

    walk(tree_root)

    if not has_entities:
        return "%% No Room @Entities detected in codebase"

    return "\n".join(lines)


def _generate_nav_flow_diagram(tree_root):
    lines = ["graph TD"]
    lines.append("    classDef screen fill:#2d3748,stroke:#4fc3f7,stroke-width:2px,color:#fff;")

    file_map = {}
    all_routes = set()

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            defined = set()
            for m in HOST_ROUTE_PATTERN.finditer(code):
                r = m.group(1)
                if r:
                    defined.add(r.strip())

            called = set()
            for m in NAV_CALL_PATTERN.finditer(code):
                r = m.group(1)
                if r:
                    called.add(r.strip())

            if defined or called:
                file_map[node.name] = {"def": defined, "call": called}
                all_routes.update(defined)

        for child in node.children:
            walk(child)

    walk(tree_root)

    clean_routes = {}
    for r in all_routes:
        base = r.split("/")[0].split("?")[0]
        node_id = _clean_mermaid_id(base)
        clean_routes[base] = node_id
        lines.append(f'    {node_id}["{base}"]:::screen')

    for filename, data in file_map.items():
        calls = data["call"]
        source_label = filename.replace(".kt", "")
        if data["def"]:
            source_label = list(data["def"])[0].split("/")[0].split("?")[0]

        source_id = clean_routes.get(source_label, _clean_mermaid_id(source_label))

        for target_raw in calls:
            target_label = target_raw.split("/")[0].split("?")[0]
            target_id = clean_routes.get(target_label, _clean_mermaid_id(target_label))

            if source_id != target_id:
                lines.append(f'    {source_id} --> {target_id}')

    if len(lines) <= 2:
        return "%% No explicit navigation flows detected"

    return "\n".join(lines)