import os
import re
from core.utils.file_reader import read_text_file


COMPOSABLE_PATTERN = re.compile(r"@Composable\s+fun\s+(\w+)")
XML_LAYOUT_PATTERN = re.compile(r"<layout|<LinearLayout|<ConstraintLayout")


def export_kotlin_ui_map(tree_root):
    composables = []
    xml_layouts = []

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)
            composables.extend(COMPOSABLE_PATTERN.findall(code))

        if node.name.endswith(".xml"):
            code = read_text_file(node.path)
            if XML_LAYOUT_PATTERN.search(code):
                xml_layouts.append(node.name)

        for c in node.children:
            walk(c)

    walk(tree_root)

    lines = []
    lines.append("=" * 32)
    lines.append("KOTLIN UI MAP")
    lines.append("=" * 32)
    lines.append("")

    if composables:
        lines.append("COMPOSABLE SCREENS")
        lines.append("-" * 32)
        for c in sorted(set(composables)):
            lines.append(f"• {c}")
        lines.append("")

    if xml_layouts:
        lines.append("XML LAYOUTS")
        lines.append("-" * 32)
        for x in sorted(set(xml_layouts)):
            lines.append(f"• {x}")
        lines.append("")

    if not composables and not xml_layouts:
        lines.append("No UI components detected.")

    return "\n".join(lines)
