"""
core/extractors/generic/ai_code_exporter.py
===========================================
Language-neutral *Full Source (AI)* phase.

Dumps the complete source of every file matching the active profile, grouped by
architectural bucket, in a format optimised for pasting into an LLM.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from core.extractors.generic.code_exporter import _classify
from core.extractors.generic.common import get_rel_path, iter_source_files, read_or_marker
from state.app_state import AppState


def export_generic_ai_code(
    tree_root,
    lang: str | None = None,
    extensions: Iterable[str] | None = None,
) -> str:
    """Full source export for the active (or supplied) language profile."""
    lang = (lang or AppState.selected_language or "all").lower()

    modules: dict[str, list[str]] = defaultdict(list)
    for path in iter_source_files(tree_root, extensions):
        modules[_classify(path)].append(path)

    if not modules:
        return "No source files found for this profile."

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("FULL SOURCE CODE EXPORT (AI READY)")
    lines.append("=" * 70)
    lines.append("")
    lines.append(
        "AI INSTRUCTIONS:\n"
        "- This is the COMPLETE source for the selected profile\n"
        "- Files are grouped by architectural module group\n"
        "- Preserve existing business logic and behavior when proposing edits\n"
    )
    lines.append("")

    total_files = 0
    for category in sorted(modules):
        files = sorted(set(modules[category]))
        total_files += len(files)

        lines.append("")
        lines.append("#" * 70)
        lines.append(f"MODULE GROUP: {category.upper()}")
        lines.append("#" * 70)
        lines.append("")

        for path in files:
            lines.append("=" * 70)
            lines.append(f"FILE: {get_rel_path(path)}")
            lines.append("=" * 70)
            lines.append("")
            lines.append(read_or_marker(path))
            lines.append("\n")

    lines.append("")
    lines.append(f"# TOTAL FILES EXPORTED: {total_files}")
    return "\n".join(lines)
