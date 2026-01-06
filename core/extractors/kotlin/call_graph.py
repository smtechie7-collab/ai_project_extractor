import re
from collections import defaultdict
from core.utils.file_reader import read_text_file


FUNC_DEF = re.compile(r'fun\s+(\w+)\s*\(')
FUNC_CALL = re.compile(r'(\w+)\s*\(')


def export_kotlin_call_graph(tree_root):
    functions = set()
    calls = defaultdict(set)

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)

            defs = FUNC_DEF.findall(code)
            functions.update(defs)

            for line in code.splitlines():
                for call in FUNC_CALL.findall(line):
                    if call in functions:
                        calls[node.name].add(call)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not calls:
        return "No Kotlin call graph detected."

    lines = []
    lines.append("=" * 36)
    lines.append("KOTLIN CALL GRAPH")
    lines.append("=" * 36)
    lines.append("")

    for file, funcs in calls.items():
        lines.append(f"FILE: {file}")
        for f in sorted(funcs):
            lines.append(f"  → calls {f}()")
        lines.append("")

    return "\n".join(lines)
