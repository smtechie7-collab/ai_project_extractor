import os
import re
from collections import defaultdict
from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(path: str) -> str:
    try:
        base = AppState.project_root or os.getcwd()
        return os.path.relpath(path, start=base)
    except Exception:
        return os.path.basename(path)


IMPORT_RE = re.compile(
    r"""(?:import\s+.*?from\s+['"]([^'"]+)['"]|import\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\)|export\s+.*?from\s+['"]([^'"]+)['"])"""
)


def export_js_ts_dependency_graph(tree_root):
    deps = defaultdict(lambda: {"internal": set(), "external": set()})

    def walk(node):
        if not node.is_dir and node.name.endswith((".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs")):
            code = read_text_file(node.path)
            rel_path = _get_rel_path(node.path)

            for m in IMPORT_RE.finditer(code):
                imp = m.group(1) or m.group(2) or m.group(3) or m.group(4)
                if imp:
                    if imp.startswith(".") or imp.startswith("/"):
                        deps[rel_path]["internal"].add(imp)
                    else:
                        deps[rel_path]["external"].add(imp)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not deps:
        return "No JavaScript / TypeScript dependencies detected."

    lines = []
    lines.append("=" * 60)
    lines.append("JAVASCRIPT / TYPESCRIPT DEPENDENCY GRAPH")
    lines.append("=" * 60)
    lines.append("")

    for file, data in sorted(deps.items()):
        lines.append(f"FILE: {file}")
        
        if data["external"]:
            lines.append("  📦 External Packages:")
            for ext in sorted(data["external"]):
                lines.append(f"    • {ext}")

        if data["internal"]:
            lines.append("  🔗 Internal Modules:")
            for internal in sorted(data["internal"]):
                lines.append(f"    → {internal}")

        lines.append("")

    return "\n".join(lines)

