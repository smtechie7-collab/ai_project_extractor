import os
import re
from collections import defaultdict
from core.utils.file_reader import read_text_file


IMPORT_RE = re.compile(r"import\s+.*?\s+from\s+['\"](.+?)['\"]")


def export_js_ts_modules(tree_root):
    modules = defaultdict(list)
    imports_map = defaultdict(set)

    def walk(node):
        if node.name.endswith((".js", ".ts", ".jsx", ".tsx")):
            folder = os.path.dirname(node.path)
            modules[folder].append(node.path)

            code = read_text_file(node.path)
            for imp in IMPORT_RE.findall(code):
                imports_map[node.name].add(imp)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not modules:
        return "No JavaScript / TypeScript source files found."

    lines = []
    lines.append("=" * 44)
    lines.append("JAVASCRIPT / TYPESCRIPT MODULE EXPORT")
    lines.append("=" * 44)
    lines.append("")

    for folder, files in sorted(modules.items()):
        lines.append(f"MODULE: {folder}")
        lines.append("=" * (8 + len(folder)))
        lines.append("")

        for path in sorted(files):
            name = os.path.basename(path)
            lines.append(f"FILE: {name}")
            lines.append("-" * 40)
            lines.append(read_text_file(path))
            lines.append("")

            if name in imports_map:
                lines.append("IMPORTS:")
                for imp in sorted(imports_map[name]):
                    lines.append(f"  → {imp}")
                lines.append("")

        lines.append("")

    return "\n".join(lines)
