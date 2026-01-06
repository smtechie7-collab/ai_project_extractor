import re
from collections import defaultdict
from core.utils.file_reader import read_text_file

FUNC_DEF = re.compile(r'^def\s+([a-zA-Z_]\w*)\s*\(', re.MULTILINE)
FUNC_CALL = re.compile(r'([a-zA-Z_]\w*)\s*\(')


def export_python_call_graph(tree_root):
    defined = set()
    calls = defaultdict(set)

    def walk(node):
        if not node.is_dir and node.name.endswith(".py"):
            code = read_text_file(node.path)

            for fn in FUNC_DEF.findall(code):
                defined.add(fn)

            for line in code.splitlines():
                for call in FUNC_CALL.findall(line):
                    if call in defined:
                        calls[node.name].add(call)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not calls:
        return "No Python call relationships detected."

    lines = []
    lines.append("=" * 60)
    lines.append("PYTHON CALL GRAPH")
    lines.append("=" * 60)
    lines.append("")

    for file, funcs in sorted(calls.items()):
        lines.append(f"FILE: {file}")
        for f in sorted(funcs):
            lines.append(f"  → calls {f}()")
        lines.append("")

    return "\n".join(lines)
