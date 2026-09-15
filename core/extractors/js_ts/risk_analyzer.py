import os
import re

from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(path: str) -> str:
    try:
        base = AppState.project_root or os.getcwd()
        return os.path.relpath(path, start=base)
    except Exception:
        return os.path.basename(path)


RISK_PATTERNS = [
    (re.compile(r"\beval\s*\("), "Dynamic code execution via eval() — severe security vulnerability"),
    (re.compile(r":\s*any\b|as\s+any\b|<any>"), "TypeScript 'any' bypass — disables compiler type-safety"),
    (re.compile(r"\bdangerouslySetInnerHTML\b"), "React dangerouslySetInnerHTML — cross-site scripting (XSS) risk"),
    (re.compile(r"\binnerHTML\s*="), "Direct innerHTML assignment — potential DOM XSS vulnerability"),
    (re.compile(r"\bdocument\.write\s*\("), "Legacy document.write() call — performance & injection hazard"),
    (re.compile(r"\brequire\s*\("), "CommonJS require() detected — mixed module system in ESM project"),
]


def analyze_js_ts_risks(tree_root):
    findings = []

    def walk(node):
        if not node.is_dir and node.name.endswith((".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs")):
            code = read_text_file(node.path)
            issues = []
            lines = code.splitlines()

            for line_idx, line in enumerate(lines, 1):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                    continue

                for pattern, desc in RISK_PATTERNS:
                    if pattern.search(line):
                        issues.append(f"[Line {line_idx}] {desc}")

            if issues:
                findings.append((node.path, issues))

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not findings:
        return "✅ No critical JavaScript / TypeScript risks or anti-patterns detected."

    lines = []
    lines.append("=" * 60)
    lines.append("JAVASCRIPT / TYPESCRIPT RISK & QUALITY AUDIT")
    lines.append("=" * 60)
    lines.append("")

    for path, issues in findings:
        rel = _get_rel_path(path)
        lines.append(f"FILE: {rel}")
        lines.append("-" * (len(rel) + 6))
        for i in issues:
            lines.append(f"  ⚠ {i}")
        lines.append("")

    return "\n".join(lines)

