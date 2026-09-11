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


FUNC_DEF = re.compile(r'fun\s+(?:<[^>]+>\s*)?(\w+)\s*\(')
FUNC_CALL = re.compile(r'(\w+)\s*\(')

KOTLIN_KEYWORD_IGNORE = {
    "let", "also", "apply", "run", "with", "takeIf", "takeUnless",
    "repeat", "synchronized", "lazy", "listOf", "setOf", "mapOf",
    "mutableListOf", "mutableSetOf", "mutableMapOf", "arrayOf",
    "toString", "equals", "hashCode", "println", "print", "require", "check"
}


def export_kotlin_call_graph(tree_root):
    files_data = {}
    all_defined_funcs = set()

    # Pass 1: Collect definitions
    def collect(node):
        if not node.is_dir and node.name.endswith((".kt", ".kts")):
            code = read_text_file(node.path)
            defs = set(FUNC_DEF.findall(code)) - KOTLIN_KEYWORD_IGNORE
            all_defined_funcs.update(defs)
            files_data[_get_rel_path(node.path)] = (code, defs)

        for c in node.children:
            collect(c)

    collect(tree_root)

    if not files_data:
        return "No Kotlin source files detected."

    # Pass 2: Map calls
    calls = defaultdict(set)
    for rel_file, (code, defs) in files_data.items():
        for token in FUNC_CALL.findall(code):
            if token in all_defined_funcs and token not in defs:
                calls[rel_file].add(token)

    if not calls:
        return "No Kotlin cross-component call relationships detected."

    lines = []
    lines.append("=" * 60)
    lines.append("KOTLIN CALL GRAPH & INVOCATION MAP")
    lines.append("=" * 60)
    lines.append("")

    for file, funcs in sorted(calls.items()):
        lines.append(f"FILE: {file}")
        for f in sorted(funcs):
            lines.append(f"  → calls {f}()")
        lines.append("")

    return "\n".join(lines)

