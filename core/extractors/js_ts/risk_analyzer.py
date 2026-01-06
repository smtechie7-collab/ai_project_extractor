from core.utils.file_reader import read_text_file


JS_RISKS = {
    "eval(": "eval() usage — security risk",
    "any": "TypeScript 'any' usage — type safety risk",
    "require(": "CommonJS require — mixed module system",
}


def analyze_js_ts_risks(tree_root):
    findings = []

    def walk(node):
        if node.name.endswith((".js", ".ts", ".jsx", ".tsx")):
            code = read_text_file(node.path)
            issues = []

            for k, v in JS_RISKS.items():
                if k in code:
                    issues.append(v)

            if issues:
                findings.append((node.name, issues))

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not findings:
        return "No major JavaScript / TypeScript risks detected."

    lines = ["JS / TS RISK ANALYSIS", "=" * 30, ""]

    for file, issues in findings:
        lines.append(f"FILE: {file}")
        for i in issues:
            lines.append(f"⚠ {i}")
        lines.append("")

    return "\n".join(lines)
