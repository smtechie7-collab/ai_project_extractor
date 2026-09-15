import os
from collections import defaultdict

from state.app_state import AppState

CATEGORIES = {
    "routes & api": ["route", "router", "api", "view", "endpoint", "controller"],
    "services & logic": ["service", "manager", "logic", "usecase", "handler"],
    "models & schemas": ["model", "schema", "entity", "dto"],
    "tasks & workers": ["worker", "task", "job", "celery", "cron", "consumer"],
    "configuration": ["config", "setting", "env"],
    "utilities & helpers": ["util", "helper", "common", "tool"],
    "tests": ["test"],
}


def _get_rel_path(path: str) -> str:
    try:
        base = AppState.project_root or os.getcwd()
        return os.path.relpath(path, start=base)
    except Exception:
        return os.path.basename(path)


def classify(path: str) -> str:
    name = os.path.basename(path).lower()
    folder = os.path.dirname(path).lower()

    for cat, keys in CATEGORIES.items():
        for k in keys:
            if k in name or f"/{k}" in folder.replace("\\", "/"):
                return cat
    return "core modules"


def export_python_modules(tree_root):
    buckets = defaultdict(list)

    def walk(node):
        if not node.is_dir and node.name.endswith(".py"):
            cat = classify(node.path)
            buckets[cat].append(node.path)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not buckets:
        return "No Python modules detected."

    lines = []
    lines.append("=" * 60)
    lines.append("PYTHON MODULE CLASSIFICATION (ARCHITECTURAL GROUPS)")
    lines.append("=" * 60)
    lines.append("")

    for cat, files in sorted(buckets.items()):
        lines.append(f"[{cat.upper()}] ({len(files)} files)")
        lines.append("-" * (len(cat) + 12))
        for f in sorted(files):
            lines.append(f"• {_get_rel_path(f)}")
        lines.append("")

    return "\n".join(lines)

