"""
core/extractors/generic/risk_analyzer.py
========================================
Language-neutral *Risk Analysis* phase.

Pattern-based heuristics that work across C/C++, Java, Kotlin, Python, JS/TS and
other C-like languages. Intentionally conservative: it reports candidate risks
with exact line numbers so a human (or the LLM) can confirm.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from core.extractors.generic.common import get_rel_path, iter_source_files, read_or_marker

# (compiled pattern, severity, message)
RISK_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"\beval\s*\("), "HIGH", "Use of eval() — possible arbitrary code execution"),
    (re.compile(r"\bexec\s*\("), "HIGH", "Use of exec() — dynamic code execution"),
    (re.compile(r"shell\s*=\s*True"), "HIGH", "subprocess with shell=True — possible command injection"),
    (re.compile(r"\b(?:system|popen)\s*\("), "HIGH", "C system()/popen() call — possible command injection"),
    (
        re.compile(r"\b(?:strcpy|strcat|sprintf|vsprintf|gets)\s*\("),
        "HIGH",
        "Unsafe C string function (buffer overflow risk)",
    ),
    (re.compile(r"\bmemcpy\s*\("), "MEDIUM", "memcpy() — verify bounds to avoid overflow"),
    (re.compile(r"TODO|FIXME|HACK|XXX"), "LOW", "Unresolved TODO/FIXME/HACK marker"),
    (re.compile(r"@?Suppress(Warnings|Lint)"), "LOW", "Suppressed warnings/lints — verify intentional"),
    (
        re.compile(r"(?i)(password|secret|api[_-]?key|token)\s*[:=]\s*[\"'][^\"']{6,}[\"']"),
        "MEDIUM",
        "Possible hardcoded credential",
    ),
]

ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
MAX_LINE_LEN = 200


def analyze_generic_risks(tree_root, extensions: Iterable[str] | None = None) -> str:
    """Pattern-based risk report for every file in the active profile."""
    findings: list[tuple[str, list[tuple[int, str, str, str]]]] = []
    total_files = 0

    for path in iter_source_files(tree_root, extensions):
        content = read_or_marker(path)
        if content.startswith("[") and content.endswith("]"):
            continue  # binary / too large / unreadable marker

        total_files += 1
        issues: list[tuple[int, str, str, str]] = []

        for line_no, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith(("//", "#", "/*", "*")):
                continue

            for pattern, severity, desc in RISK_PATTERNS:
                if pattern.search(line):
                    issues.append((line_no, severity, desc, stripped[:80]))

            if len(line) > MAX_LINE_LEN:
                issues.append((line_no, "LOW", f"Very long line ({len(line)} chars) — reduced readability", stripped[:80]))

        if issues:
            issues.sort(key=lambda i: ORDER.get(i[1], 9))
            findings.append((get_rel_path(path), issues))

    if not findings:
        border = "=" * 60
        return (
            f"{border}\n"
            "GENERIC RISK & CODE QUALITY ANALYSIS\n"
            f"{border}\n\n"
            "All checked files look clean. No heuristic risks detected."
        )

    out: list[str] = []
    out.append("=" * 70)
    out.append("GENERIC RISK & CODE QUALITY ANALYSIS")
    out.append("=" * 70)
    out.append(f"• Files scanned     : {total_files}")
    out.append(f"• Files with issues : {len(findings)}")
    out.append("")

    for rel_path, issues in sorted(findings, key=lambda x: -len(x[1])):
        out.append(f"## {rel_path}  ({len(issues)} findings)")
        for line_no, severity, desc, snippet in issues:
            out.append(f"  • [Line {line_no}] [{severity}] {desc}")
            if snippet:
                out.append(f"    Code: `{snippet}`")
        out.append("")

    return "\n".join(out)
