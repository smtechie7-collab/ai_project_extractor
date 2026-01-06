import os
from collections import defaultdict
from core.utils.file_reader import read_text_file
from core.extractors.python.code_exporter import classify


SKIP_DIR_NAMES = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
}


def export_python_ai_code(tree_root):
    """
    FULL Python source exporter (AI-ready)
    GUARANTEES all .py files are included
    """

    modules = defaultdict(list)

    def walk(node):
        # Skip junk directories only
        if node.is_dir and node.name in SKIP_DIR_NAMES:
            return

        # Collect ALL .py files
        if not node.is_dir and node.name.endswith(".py"):
            category = classify(node.path)
            modules[category].append(node.path)

        # Always continue walking children
        for c in node.children:
            walk(c)

    walk(tree_root)

    if not modules:
        return "No Python source files found."

    lines = []
    lines.append("=" * 70)
    lines.append("PYTHON FULL SOURCE CODE EXPORT (AI READY)")
    lines.append("=" * 70)
    lines.append("")
    lines.append(
        "AI INSTRUCTIONS:\n"
        "- This is the COMPLETE Python project source\n"
        "- Files are grouped by logical module\n"
        "- Preserve behavior while suggesting refactors\n"
    )
    lines.append("")

    total_files = 0

    for category in sorted(modules.keys()):
        files = sorted(set(modules[category]))
        total_files += len(files)

        lines.append("")
        lines.append("#" * 70)
        lines.append(f"MODULE GROUP: {category.upper()}")
        lines.append("#" * 70)
        lines.append("")

        for path in files:
            rel = os.path.relpath(path)
            lines.append("=" * 70)
            lines.append(f"FILE: {rel}")
            lines.append("=" * 70)
            lines.append("")

            try:
                lines.append(read_text_file(path))
            except Exception as e:
                lines.append(f"# ERROR READING FILE: {e}")

            lines.append("\n")

    lines.append("")
    lines.append(f"# TOTAL FILES EXPORTED: {total_files}")

    return "\n".join(lines)
