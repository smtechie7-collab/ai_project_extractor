"""
core/extractors/generic/call_graph.py
=====================================
Language-neutral heuristic *Call Graph* phase.

Collects function/method definitions across the active profile and reports
cross-file calls to those definitions. This is a **heuristic** textual analysis
(no compiler/AST), intentionally conservative to avoid noise. Used for Java and
the C/C++ / "All Languages" profiles where no dedicated extractor exists.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable

from core.extractors.generic.common import get_rel_path, iter_source_files, read_or_marker

# Definition patterns across common languages.
DEF_PATTERNS = [
    re.compile(r"\bfun\s+(?:<[^>]+>\s*)?(\w+)\s*\("),                    # Kotlin
    re.compile(r"^\s*def\s+(\w+)\s*\(", re.MULTILINE),                    # Python
    re.compile(r"\bfunction\s+(\w+)\s*\("),                               # JS/TS
    # Java / C-like method or function definition with a body
    re.compile(
        r"^[ \t]*(?:public|private|protected|static|final|abstract|synchronized|native|virtual|inline|extern"
        r"|const|unsigned|signed|long|short|struct|class|template|[\w:<>\[\],\.\*&]+)"
        r"[ \t]+(\w+)[ \t]*\([^;{}]*\)[ \t]*(?:const)?[ \t]*\{",
        re.MULTILINE,
    ),
]

# Function-call site (identifier followed by opening paren).
CALL_RE = re.compile(r"(\w+)\s*\(")

IGNORE_NAMES = {
    "if", "for", "while", "switch", "catch", "return", "sizeof", "new", "delete",
    "print", "println", "printf", "sprintf", "strlen", "main",
    "let", "also", "apply", "run", "with", "takeIf", "takeUnless", "repeat",
    "synchronized", "lazy", "listOf", "setOf", "mapOf", "arrayOf", "toString",
    "equals", "hashCode", "require", "check", "assert", "typeof", "instanceof",
}


def _collect_defs(content: str) -> set[str]:
    names: set[str] = set()
    for pattern in DEF_PATTERNS:
        names.update(pattern.findall(content))
    return names - IGNORE_NAMES


def export_generic_call_graph(tree_root, extensions: Iterable[str] | None = None) -> str:
    """Heuristic cross-file call graph for the active profile."""
    files_data: dict[str, tuple[str, set[str]]] = {}
    all_defs: set[str] = set()

    for path in iter_source_files(tree_root, extensions):
        content = read_or_marker(path)
        if content.startswith("[") and content.endswith("]"):
            continue
        defs = _collect_defs(content)
        all_defs.update(defs)
        files_data[get_rel_path(path)] = (content, defs)

    if not files_data:
        return "No source files detected for this profile."

    calls: dict[str, set[str]] = defaultdict(set)
    for rel_file, (content, defs) in files_data.items():
        for token in CALL_RE.findall(content):
            if token in all_defs and token not in defs and token not in IGNORE_NAMES:
                calls[rel_file].add(token)

    if not calls:
        return "No cross-file call relationships detected (heuristic scan)."

    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("CALL GRAPH & INVOCATION MAP (heuristic, cross-file)")
    lines.append("=" * 60)
    lines.append("")
    for rel_file, funcs in sorted(calls.items()):
        lines.append(f"FILE: {rel_file}")
        for f in sorted(funcs):
            lines.append(f"  → calls {f}()")
        lines.append("")

    return "\n".join(lines)
