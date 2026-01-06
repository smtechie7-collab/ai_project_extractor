import os
from core.utils.file_reader import read_text_file


def build_kotlin_di_dot(tree_root) -> str:
    nodes = []
    edges = []

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)
            if "@Module" in code:
                mod = node.name.replace(".kt", "")
                nodes.append(mod)

                if "@Provides" in code:
                    edges.append(f'{mod} -> Provides')

        for c in node.children:
            walk(c)

    walk(tree_root)

    lines = ["digraph DI {"]

    for n in set(nodes):
        lines.append(f'  "{n}";')

    for e in edges:
        lines.append(f"  {e};")

    lines.append("}")
    return "\n".join(lines)
