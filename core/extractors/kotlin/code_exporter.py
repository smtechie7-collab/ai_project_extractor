import os
from collections import defaultdict
from core.utils.file_reader import read_text_file
from core.extractors.kotlin.role_classifier import classify_kotlin_role


def export_kotlin_modules(tree_root):
    layers = defaultdict(list)

    def walk(node):
        if node.name.endswith(".kt"):
            role = classify_kotlin_role(node.name)
            layers[role].append(node.path)

        for child in node.children:
            walk(child)

    walk(tree_root)

    if not layers:
        return "No Kotlin (.kt) files found."

    lines = []
    lines.append("=" * 32)
    lines.append("KOTLIN PROJECT — MODULE EXPORT")
    lines.append("=" * 32)
    lines.append("")

    for layer, files in sorted(layers.items()):
        lines.append(f"LAYER: {layer}")
        lines.append("=" * len(f"LAYER: {layer}"))
        lines.append("")

        for file_path in sorted(files):
            file_name = os.path.basename(file_path)
            lines.append(f"FILE: {file_name}")
            lines.append("-" * 40)
            lines.append(read_text_file(file_path))
            lines.append("\n")

        lines.append("\n")

    return "\n".join(lines)
