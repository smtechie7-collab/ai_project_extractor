from core.utils.file_reader import read_text_file

RISK_PATTERNS = {
    "eval(": "Use of eval() — security risk",
    "exec(": "Use of exec() — security risk",
    "global ": "Global variable usage",
    "except:": "Bare except clause",
    "pickle.load": "Pickle load — unsafe deserialization",
}


def analyze_python_risks(tree_root):
    findings = []

    def walk(node):
        if not node.is_dir and node.name.endswith(".py"):
            code = read_text_file(node.path)
            issues = []

            for k, v in RISK_PATTERNS.items():
                if k in code:
                    issues.append(v)

            if issues:
                findings.append((node.path, issues))

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not findings:
        return "No major Python risks detected."

    lines = []
    lines.append("=" * 60)
    lines.append("PYTHON RISK ANALYSIS")
    lines.append("=" * 60)
    lines.append("")

    for file, issues in findings:
        lines.append(f"FILE: {file}")
        for i in issues:
            lines.append(f"⚠ {i}")
        lines.append("")

    return "\n".join(lines)
