from core.extractors.js_ts.dependency_graph import export_js_ts_dependency_graph


def build_js_ts_dependency_dot(tree_root):
    raw = export_js_ts_dependency_graph(tree_root)
    lines = ["digraph JS_TS {"]

    for line in raw.splitlines():
        if "→" in line:
            left, right = line.split("→")
            lines.append(f'  "{left.strip()}" -> "{right.strip()}";')

    lines.append("}")
    return "\n".join(lines)
