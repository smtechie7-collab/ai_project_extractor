import os
import re
from collections import defaultdict
from core.utils.file_reader import read_text_file

IMPORT_RE = re.compile(
    r'import\s+(?:.+?\s+from\s+)?["\'](.+?)["\']|require\(["\'](.+?)["\']\)'
)


def export_js_ts_dependency_graph(tree_root):
    deps = defaultdict(set)

    def walk(node):
        if node.name.endswith((".js", ".ts", ".jsx", ".tsx")):
            code = read_text_file(node.path)
            for m in IMPORT_RE.findall(code):
                imp = m[0] or m[1]
                if imp:
                    deps[node.name].add(imp)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not deps:
        return "No JS/TS dependencies detected."

    lines = []
    lines.append("=" * 40)
    lines.append("JS / TS DEPENDENCY GRAPH")
    lines.append("=" * 40)
    lines.append("")

    for file, imports in sorted(deps.items()):
        lines.append(f"FILE: {file}")
        for i in sorted(imports):
            lines.append(f"  → {i}")
        lines.append("")

    return "\n".join(lines)
