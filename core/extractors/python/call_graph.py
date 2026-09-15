import ast
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


def export_python_call_graph(tree_root):
    """
    Two-pass AST-powered Python Call Graph Extractor.
    Pass 1: Discover all top-level and class functions/methods across the project.
    Pass 2: Map invocations from callers to defined functions.
    """
    files_data = {}  # rel_path -> (ast_tree or None, code, classes_map, functions_set)
    all_defined_funcs = set()
    all_defined_classes = set()

    # --- PASS 1: Collection ---
    def collect(node):
        if not node.is_dir and node.name.endswith(".py"):
            code = read_text_file(node.path)
            rel_name = _get_rel_path(node.path)
            funcs = set()
            classes = defaultdict(list)
            parsed_tree = None

            try:
                parsed_tree = ast.parse(code)
                for item in parsed_tree.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        funcs.add(item.name)
                        all_defined_funcs.add(item.name)
                    elif isinstance(item, ast.ClassDef):
                        all_defined_classes.add(item.name)
                        for sub in item.body:
                            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                funcs.add(f"{item.name}.{sub.name}")
                                funcs.add(sub.name)
                                classes[item.name].append(sub.name)
                                all_defined_funcs.add(sub.name)
                                all_defined_funcs.add(f"{item.name}.{sub.name}")
            except Exception:
                # Regex fallback for files with syntax errors
                for m in re.finditer(r"(?:def|class)\s+([a-zA-Z_]\w*)", code):
                    funcs.add(m.group(1))
                    all_defined_funcs.add(m.group(1))

            files_data[rel_name] = (parsed_tree, code, classes, funcs)

        for c in node.children:
            collect(c)

    collect(tree_root)

    if not files_data:
        return "No Python source files detected."

    # Built-in or standard names to ignore to avoid clutter
    BUILTIN_IGNORE = {
        "print", "len", "range", "str", "int", "float", "bool", "dict", "list",
        "set", "tuple", "isinstance", "issubclass", "getattr", "setattr", "hasattr",
        "super", "enumerate", "zip", "map", "filter", "min", "max", "sum", "abs",
        "open", "type", "repr", "next", "iter", "round", "sorted", "reversed"
    }

    # --- PASS 2: Call Resolution ---
    calls = defaultdict(set)
    defined_summary = {}

    for rel_name, (tree, code, classes, funcs) in files_data.items():
        if classes:
            defined_summary[rel_name] = dict(classes)

        if tree:
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    callee = None
                    if isinstance(node.func, ast.Name):
                        callee = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        callee = node.func.attr

                    if callee and callee in all_defined_funcs and callee not in BUILTIN_IGNORE:
                        calls[rel_name].add(callee)
        else:
            # Fallback text regex
            for token in re.findall(r"([a-zA-Z_]\w*)\s*\(", code):
                if token in all_defined_funcs and token not in BUILTIN_IGNORE:
                    calls[rel_name].add(token)

    lines = []
    lines.append("=" * 60)
    lines.append("PYTHON CALL GRAPH & SYMBOL RESOLUTION (AST-POWERED)")
    lines.append("=" * 60)
    lines.append("")

    if not calls and not defined_summary:
        return "No internal Python function call relationships detected."

    for file in sorted(set(list(calls.keys()) + list(defined_summary.keys()))):
        lines.append(f"FILE: {file}")

        # Display classes & methods defined in file
        if file in defined_summary:
            for cls_name, methods in sorted(defined_summary[file].items()):
                lines.append(f"  class {cls_name}:")
                for m in sorted(methods):
                    lines.append(f"    • def {m}()")

        # Display outward calls
        if file in calls:
            called_list = sorted(calls[file])
            if called_list:
                lines.append("  Invocations:")
                for f in called_list:
                    lines.append(f"    → calls {f}()")

        lines.append("")

    return "\n".join(lines)

