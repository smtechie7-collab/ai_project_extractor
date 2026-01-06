import re
from core.utils.file_reader import read_text_file


ROUTE_DEF = re.compile(r'composable\("([^"]+)"')
ROUTE_NAV = re.compile(r'navigate\("([^"]+)"')


def export_kotlin_navigation_graph(tree_root):
    routes = set()
    edges = []

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)

            defined = ROUTE_DEF.findall(code)
            used = ROUTE_NAV.findall(code)

            for d in defined:
                routes.add(d)

            for u in used:
                edges.append(u)

        for c in node.children:
            walk(c)

    walk(tree_root)

    lines = []
    lines.append("=" * 36)
    lines.append("KOTLIN NAVIGATION GRAPH")
    lines.append("=" * 36)
    lines.append("")

    if routes:
        lines.append("ROUTES:")
        for r in sorted(routes):
            lines.append(f"• {r}")
        lines.append("")

    if edges:
        lines.append("NAVIGATION CALLS:")
        for e in edges:
            lines.append(f"→ navigate({e})")

    return "\n".join(lines)
