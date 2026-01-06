import re
from core.utils.file_reader import read_text_file


def build_kotlin_ui_dot(tree_root) -> str:
    composables = []

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)
            matches = re.findall(r"@Composable\s+fun\s+(\w+)", code)
            composables.extend(matches)

        for c in node.children:
            walk(c)

    walk(tree_root)

    lines = ["digraph UI {"]

    for c in set(composables):
        lines.append(f'  "{c}";')

    lines.append("}")
    return "\n".join(lines)
