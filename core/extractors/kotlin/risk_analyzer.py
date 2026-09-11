import os
import re
from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(p: str) -> str:
    try:
        if AppState.project_root:
            return os.path.relpath(p, AppState.project_root).replace("\\", "/")
        return os.path.basename(p)
    except Exception:
        return os.path.basename(p)


# Production-grade Kotlin & Android Architectural Risk Patterns
RISK_PATTERNS = [
    (
        re.compile(r'OR\s*:[a-zA-Z0-9_]+\s*=\s*[\'"][^\'"]+[\'"]', re.IGNORECASE),
        "CRITICAL (Article 4.4)",
        "SQL Parameter Tautology detected! Comparing parameter to literal destroys multi-tenant / frontId isolation"
    ),
    (
        re.compile(r'\bGlobalScope\.(?:launch|async)\b'),
        "HIGH",
        "GlobalScope usage: Bypasses Android lifecycle, potential memory & coroutine leak"
    ),
    (
        re.compile(r'\brunBlocking\s*[\({]'),
        "HIGH",
        "runBlocking detected: May block Android Main Thread and cause ANR (Application Not Responding)"
    ),
    (
        re.compile(r'\b(?:FirebaseFirestore\.getInstance\(\)|firestore)\.collection\s*\([^)]+\)\s*\.\s*(?:set|add|update|delete)\b'),
        "CRITICAL (Article 42)",
        "Direct Firestore write detected outside authorized sync worker! Violates Single Sync Engine rule"
    ),
    (
        re.compile(r'lateinit\s+var\s+'),
        "MEDIUM",
        "lateinit var property: Risk of UninitializedPropertyAccessException if accessed before injection"
    ),
    (
        re.compile(r'!!'),
        "MEDIUM",
        "Force unwrap (!!) detected: Potential NullPointerException at runtime"
    )
]


def analyze_kotlin_risks(tree_root):
    """
    Analyzes Kotlin source code for real architectural violations, SQL tautology bugs,
    lifecycle leaks, and crash vectors with exact line numbers. Zero false positives on 'var' or 'mutableStateOf'.
    """
    findings = []
    total_files = 0

    def walk(node):
        nonlocal total_files
        if not node.is_dir and node.name.endswith(".kt"):
            total_files += 1
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            rel_p = _get_rel_path(node.path)
            file_issues = []
            lines = code.splitlines()

            # Skip test files from strict Article 42 check
            is_test = "test" in rel_p.lower()

            for line_idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                # Skip comments
                if clean_line.startswith(("//", "/*", "*")):
                    continue

                for pattern, severity, desc in RISK_PATTERNS:
                    if "Article 42" in severity and (is_test or "sync/" in rel_p.replace("\\", "/").lower()):
                        continue

                    if pattern.search(line):
                        file_issues.append((line_idx, severity, desc, clean_line[:80]))

            # God class check
            if len(lines) > 800:
                file_issues.append((len(lines), "LOW", f"Large file ({len(lines)} lines) – potential God class / SRP violation", ""))

            if file_issues:
                findings.append((rel_p, file_issues))

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    if not findings:
        return (
            "=" * 60 + "\n"
            "KOTLIN RISK & ARCHITECTURAL STABILITY ANALYSIS\n"
            "=" * 60 + "\n\n"
            "✅ All checked Kotlin files conform to safety standards. No critical risks detected."
        )

    out = []
    out.append("=" * 70)
    out.append("🛡️ KOTLIN RISK & ARCHITECTURAL STABILITY ANALYSIS")
    out.append("=" * 70)
    out.append(f"• Total Kotlin Files Scanned: {total_files}")
    out.append(f"• Files With Findings: {len(findings)}")
    out.append("")

    for rel_p, issues in sorted(findings, key=lambda x: len(x[1]), reverse=True):
        out.append(f"## File: `{rel_p}` ({len(issues)} findings)")
        for line_no, severity, desc, snippet in issues:
            out.append(f"  • [Line {line_no}] [{severity}] {desc}")
            if snippet:
                out.append(f"    Code: `{snippet}`")
        out.append("")

    return "\n".join(out)
