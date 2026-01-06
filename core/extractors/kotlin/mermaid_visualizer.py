import re
from core.utils.file_reader import read_text_file

# --- REGEX PATTERNS ---
# Database
TABLE_NAME_PATTERN = re.compile(r'tableName\s*=\s*"([^"]+)"')
CLASS_NAME_PATTERN = re.compile(r'data\s+class\s+(\w+)')
FIELD_PATTERN = re.compile(r'(val|var)\s+(\w+)\s*:\s*([A-Za-z0-9_<>]+)')

# Navigation - Smart Patterns
# Detect routes defined in NavHost
HOST_ROUTE_PATTERN = re.compile(r'composable\(\s*(?:route\s*=\s*)?["\']([^"\'{}]+)')
# Detect navigation calls ONLY inside lambdas or functions
# Capture: .navigate( "route" )
NAV_CALL_PATTERN = re.compile(r'\.navigate\(\s*["\']([^"\'${}]+)') 

def generate_mermaid_visuals(tree_root):
    """
    Master function to generate all visual diagrams.
    """
    db_diagram = _generate_db_er_diagram(tree_root)
    nav_diagram = _generate_nav_flow_diagram(tree_root)
    
    report = []
    report.append("# VISUAL ARCHITECTURE REPORT (MERMAID)")
    report.append("Copy the code blocks below into https://mermaid.live or ask AI to render them.\n")

    report.append("## 1. DATABASE ER DIAGRAM")
    report.append("Displays entities, fields, and primary keys.\n")
    report.append("```mermaid")
    report.append(db_diagram)
    report.append("```\n")

    report.append("## 2. NAVIGATION FLOWCHART")
    report.append("Displays screen connections and flow.\n")
    report.append("```mermaid")
    report.append(nav_diagram)
    report.append("```\n")

    return "\n".join(report)


def _generate_db_er_diagram(tree_root):
    lines = ["erDiagram"]
    
    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except:
                return

            if "@Entity" in code:
                # Class Name
                class_match = CLASS_NAME_PATTERN.search(code)
                if not class_match: return
                class_name = class_match.group(1)

                # Table Name
                table_match = TABLE_NAME_PATTERN.search(code)
                table_name = table_match.group(1) if table_match else class_name

                lines.append(f"    {table_name} {{")
                
                # Fields
                file_lines = code.splitlines()
                for line in file_lines:
                    field_match = FIELD_PATTERN.search(line)
                    if field_match:
                        col_name = field_match.group(2)
                        col_type = field_match.group(3).replace("<", "~").replace(">", "~") # Escape generic brackets
                        is_pk = "PK" if "@PrimaryKey" in line else ""
                        lines.append(f"        {col_type} {col_name} {is_pk}")
                
                lines.append("    }")

        for child in node.children:
            walk(child)

    walk(tree_root)
    
    if len(lines) == 1:
        return "%% No Room Entities detected"
    
    return "\n".join(lines)


def _generate_nav_flow_diagram(tree_root):
    lines = ["graph TD"]
    lines.append("    classDef screen fill:#f9f,stroke:#333,stroke-width:2px;")
    
    # We will map: File -> [Routes Defined, Routes Called]
    file_map = {}
    all_routes = set()

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except:
                return
            
            # Simple heuristic:
            # If a file has @Composable and calls navigate("route"), it's a source
            # If a file defines composable("route"), it's a destination
            
            defined = set(HOST_ROUTE_PATTERN.findall(code))
            called = set(NAV_CALL_PATTERN.findall(code))
            
            if defined or called:
                file_map[node.name] = {"def": defined, "call": called}
                all_routes.update(defined)

        for child in node.children:
            walk(child)
    
    walk(tree_root)

    # Clean up routes (remove dynamic params like /{id})
    clean_routes = set()
    for r in all_routes:
        base = r.split("/")[0]
        clean_routes.add(base)
        lines.append(f'    {base}:::screen')

    # Build Links
    # Logic: If File A defines Route X, and File B calls Route X -> Link B to A (or usually A to B logic)
    # Actually navigation is: Screen A calls navigate(Route B).
    # So we find files that CALL a route, and link them to the route name.
    
    for filename, data in file_map.items():
        calls = data["call"]
        
        # If this file defines a route (e.g. HomeScreen.kt defines "home"), 
        # use that route name as the source node.
        # Otherwise use filename.
        source_node = filename.replace(".kt", "")
        if data["def"]:
            # Pick first defined route as primary identity
            source_node = list(data["def"])[0].split("/")[0]

        for target_raw in calls:
            target = target_raw.split("/")[0]
            
            # Don't link to self
            if source_node != target and target in clean_routes:
                lines.append(f'    {source_node} --> {target}')

    if len(lines) <= 2:
        return "%% No explicit navigation flows detected"

    return "\n".join(lines)