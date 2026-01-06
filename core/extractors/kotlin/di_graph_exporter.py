import os
import re
from core.utils.file_reader import read_text_file


MODULE_PATTERN = re.compile(r"@Module")
PROVIDES_PATTERN = re.compile(r"@Provides|@Binds")


def export_kotlin_di_graph(tree_root):
    modules = {}

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)

            if "@Module" in code:
                provides = PROVIDES_PATTERN.findall(code)
                modules[node.path] = len(provides)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not modules:
        return "No DI modules detected."

    lines = []
    lines.append("=" * 32)
    lines.append("KOTLIN DI GRAPH")
    lines.append("=" * 32)
    lines.append("")

    for path, count in modules.items():
        lines.append(f"MODULE FILE: {os.path.basename(path)}")
        lines.append(f"Provides/Binds count: {count}")
        lines.append("")

    return "\n".join(lines)
