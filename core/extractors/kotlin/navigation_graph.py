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


ROUTE_DEF = re.compile(r'composable(?:\s*<[^>]+>|\s*\(\s*(?:route\s*=\s*)?["\']([^"\'{}]+)["\'])')
ROUTE_NAV = re.compile(r'\.navigate\(\s*["\']([^"\'${}]+)["\']')


def export_kotlin_navigation_graph(tree_root):
    routes = defaultdict(set)
    nav_calls = defaultdict(set)

    def walk(node):
        if not node.is_dir and node.name.endswith(".kt"):
            code = read_text_file(node.path)
            rel = _get_rel_path(node.path)

            for d in ROUTE_DEF.findall(code):
                clean_route = d.strip().split("?")[0]
                routes[clean_route].add(rel)

            for u in ROUTE_NAV.findall(code):
                clean_target = u.strip().split("?")[0]
                nav_calls[rel].add(clean_target)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not routes and not nav_calls:
        return "No explicit Kotlin Compose navigation routes or calls detected."

    lines = []
    lines.append("=" * 60)
    lines.append("KOTLIN NAVIGATION GRAPH (ROUTES & SCREEN TRANSITIONS)")
    lines.append("=" * 60)
    lines.append("")

    if routes:
        lines.append("📍 DEFINED ROUTES:")
        lines.append("-" * 40)
        for r, defining_files in sorted(routes.items()):
            files_str = ", ".join(sorted(defining_files))
            lines.append(f"• Route: {r} (Defined in: {files_str})")
        lines.append("")

    if nav_calls:
        lines.append("🚀 SCREEN TRANSITIONS (CALLER → TARGET):")
        lines.append("-" * 40)
        for caller, targets in sorted(nav_calls.items()):
            lines.append(f"Screen/File: {caller}")
            for t in sorted(targets):
                lines.append(f"   → navigates to: '{t}'")
            lines.append("")

    return "\n".join(lines)

