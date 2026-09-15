"""
core/extractors/generic/code_exporter.py
========================================
Language-neutral *module classification* phase.

Groups source files (for the active language profile) into architectural buckets
using filename/path keyword heuristics. Used by the C/C++ and "All Languages"
profiles, for Java, and as the safe fallback for unmatched profiles.
"""

from __future__ import annotations

import os
from collections import defaultdict
from collections.abc import Iterable

from core.extractors.generic.common import get_rel_path, iter_source_files
from state.app_state import AppState

# Keyword buckets (checked against lower-cased file name and path).
CATEGORIES: dict[str, list[str]] = {
    "ui & views": ["view", "screen", "activity", "fragment", "component", "widget", "window", "dialog"],
    "controllers & routes": ["controller", "route", "router", "api", "endpoint", "handler", "servlet"],
    "services & logic": ["service", "manager", "logic", "usecase", "engine", "processor"],
    "data & models": ["model", "entity", "schema", "dto", "struct", "record", "dao", "repository", "repo"],
    "tasks & workers": ["worker", "task", "job", "scheduler", "consumer", "cron"],
    "configuration": ["config", "setting", "env", "constant", "properties", "manifest"],
    "utilities & helpers": ["util", "helper", "common", "tool", "support"],
    "tests": ["test", "spec", "fixture"],
    "headers": [".h", ".hpp", ".hh", ".hxx"],
}


def _classify(path: str) -> str:
    name = os.path.basename(path).lower()
    folder = os.path.dirname(path).replace("\\", "/").lower()

    for category, keys in CATEGORIES.items():
        for key in keys:
            if key.startswith(".") and name.endswith(key):
                return category
            if key in name or f"/{key}" in folder:
                return category
    return "source files"


def export_generic_modules(
    tree_root,
    lang: str | None = None,
    extensions: Iterable[str] | None = None,
) -> str:
    """Module classification report for the active (or supplied) language profile."""
    lang = (lang or AppState.selected_language or "all").lower()
    buckets: dict[str, list[str]] = defaultdict(list)

    for path in iter_source_files(tree_root, extensions):
        buckets[_classify(path)].append(path)

    if not buckets:
        return (
            "No source files detected for this profile.\n"
            "Tip: pick a language in the toolbar that matches your project, "
            "or use 'All Languages'."
        )

    total = sum(len(v) for v in buckets.values())
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append(f"MODULE CLASSIFICATION — profile: {lang} ({total} files)")
    lines.append("=" * 70)
    lines.append("")

    for category in sorted(buckets, key=lambda c: (-len(buckets[c]), c)):
        files = sorted(set(buckets[category]))
        lines.append(f"[{category.upper()}] ({len(files)} files)")
        lines.append("-" * (len(category) + 14))
        for f in files:
            lines.append(f"• {get_rel_path(f)}")
        lines.append("")

    return "\n".join(lines)
