import os
from core.utils.file_reader import read_text_file


RISK_RULES = {
    "lateinit var": "Lateinit dependency (possible DI fragility)",
    "!!": "Force unwrap (!!) – potential runtime crash",
    "GlobalScope": "GlobalScope usage – lifecycle leak risk",
    "mutableStateOf": "State mutation risk (Compose)",
    "var ": "Mutable state detected (review necessity)",
}


def analyze_kotlin_risks(tree_root):
    findings = []

    def walk(node):
        if node.name.endswith(".kt"):
            code = read_text_file(node.path)
            file_findings = []

            for pattern, description in RISK_RULES.items():
                if pattern in code:
                    file_findings.append(description)

            # Heuristic: Large files = God class risk
            lines = code.count("\n")
            if lines > 600:
                file_findings.append(
                    f"Large file ({lines} lines) – possible God class"
                )

            if file_findings:
                findings.append((node.path, file_findings))

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not findings:
        return "No major Kotlin risks detected."

    lines = []
    lines.append("=" * 36)
    lines.append("KOTLIN RISK & FRAGILITY ANALYSIS")
    lines.append("=" * 36)
    lines.append("")

    for path, issues in findings:
        lines.append(f"FILE: {os.path.basename(path)}")
        lines.append("-" * 40)
        for issue in issues:
            lines.append(f"⚠ {issue}")
        lines.append("")

    return "\n".join(lines)
