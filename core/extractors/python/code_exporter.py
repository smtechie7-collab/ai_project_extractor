import os
from collections import defaultdict
from core.utils.file_reader import read_text_file


CATEGORIES = {
    "api": ["route", "router", "api", "view"],
    "services": ["service", "manager", "logic"],
    "models": ["model", "schema", "entity"],
    "utils": ["util", "helper", "common"],
    "tests": ["test"],
}


def classify(path: str) -> str:
    name = os.path.basename(path).lower()
    folder = os.path.dirname(path).lower()

    for cat, keys in CATEGORIES.items():
        for k in keys:
            if k in name or k in folder:
                return cat
    return "other"


def export_python_modules(tree_root):
    buckets = defaultdict(list)

    def walk(node):
        if node.name.endswith(".py") and node.name != "__init__.py":
            cat = classify(node.path)
            buckets[cat].append(node.path)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not buckets:
        return "No Python modules detected."

    lines = []
    lines.append("=" * 40)
    lines.append("PYTHON MODULE CLASSIFICATION")
    lines.append("=" * 40)
    lines.append("")

    for cat, files in sorted(buckets.items()):
        lines.append(f"[{cat.upper()}]")
        lines.append("-" * (len(cat) + 2))
        for f in sorted(files):
            lines.append(f"• {os.path.relpath(f)}")
        lines.append("")

    return "\n".join(lines)
