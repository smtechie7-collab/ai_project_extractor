import os
from collections import defaultdict
from core.utils.file_reader import read_text_file
from core.extractors.kotlin.role_classifier import classify_kotlin_role
from state.app_state import AppState


def _get_rel_path(path: str) -> str:
    try:
        base = AppState.project_root or os.getcwd()
        return os.path.relpath(path, start=base)
    except Exception:
        return os.path.basename(path)


def export_kotlin_module_classification(tree_root):
    layers = defaultdict(list)

    def walk(node):
        if not node.is_dir and node.name.endswith((".kt", ".kts")):
            role = classify_kotlin_role(node.name)
            layers[role].append(node.path)

        for child in node.children:
            walk(child)

    walk(tree_root)

    if not layers:
        return "No Kotlin (.kt) files found."

    lines = []
    lines.append("=" * 60)
    lines.append("KOTLIN ARCHITECTURAL MODULE CLASSIFICATION")
    lines.append("=" * 60)
    lines.append("")

    for layer, files in sorted(layers.items()):
        lines.append(f"LAYER: {layer.upper()} ({len(files)} files)")
        lines.append("-" * (len(layer) + 14))
        for file_path in sorted(files):
            lines.append(f"• {_get_rel_path(file_path)}")
        lines.append("")

    return "\n".join(lines)


def export_kotlin_modules(tree_root):
    """Full source code export for Kotlin projects."""
    layers = defaultdict(list)

    def walk(node):
        if not node.is_dir and node.name.endswith((".kt", ".kts")):
            role = classify_kotlin_role(node.name)
            layers[role].append(node.path)

        for child in node.children:
            walk(child)

    walk(tree_root)

    if not layers:
        return "No Kotlin (.kt) files found."

    lines = []
    lines.append("=" * 70)
    lines.append("KOTLIN FULL SOURCE CODE EXPORT (AI READY)")
    lines.append("=" * 70)
    lines.append("")

    total_files = 0
    for layer, files in sorted(layers.items()):
        total_files += len(files)
        lines.append(f"\nLAYER: {layer.upper()}")
        lines.append("=" * 50)
        lines.append("")

        for file_path in sorted(files):
            rel = _get_rel_path(file_path)
            lines.append(f"FILE: {rel}")
            lines.append("-" * 40)
            lines.append(read_text_file(file_path))
            lines.append("\n")

    lines.append(f"\n# TOTAL KOTLIN FILES EXPORTED: {total_files}")
    return "\n".join(lines)

