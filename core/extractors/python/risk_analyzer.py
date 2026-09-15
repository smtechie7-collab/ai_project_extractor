import ast
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


def analyze_python_risks(tree_root):
    """
    Production AST-powered Python Risk & Fragility Analyzer.
    Reports exact line numbers for security flaws, bare exceptions, and state anti-patterns.
    """
    findings = []

    def walk(node):
        if not node.is_dir and node.name.endswith(".py"):
            code = read_text_file(node.path)
            issues = []

            try:
                tree = ast.parse(code)
                for ast_node in ast.walk(tree):
                    # 1. Bare Except Clauses
                    if isinstance(ast_node, ast.ExceptHandler) and ast_node.type is None:
                        line = getattr(ast_node, 'lineno', '?')
                        issues.append(f"[Line {line}] Bare 'except:' clause suppresses all errors including KeyboardInterrupt and SystemExit")

                    # 2. Dangerous function calls
                    elif isinstance(ast_node, ast.Call):
                        line = getattr(ast_node, 'lineno', '?')
                        if isinstance(ast_node.func, ast.Name):
                            if ast_node.func.id == "eval":
                                issues.append(f"[Line {line}] Dangerous call to eval() — potential arbitrary code execution")
                            elif ast_node.func.id == "exec":
                                issues.append(f"[Line {line}] Dangerous call to exec() — dynamic code execution")
                        elif isinstance(ast_node.func, ast.Attribute):
                            attr = ast_node.func.attr
                            val = getattr(ast_node.func.value, 'id', '')
                            if val == "pickle" and attr in ["load", "loads"]:
                                issues.append(f"[Line {line}] Insecure deserialization via pickle.{attr}()")
                            elif attr in ["call", "Popen", "run", "check_output"]:
                                for kw in ast_node.keywords:
                                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                        issues.append(f"[Line {line}] Subprocess call with shell=True — potential command injection")

                    # 3. Global variable mutation
                    elif isinstance(ast_node, ast.Global):
                        line = getattr(ast_node, 'lineno', '?')
                        names = ", ".join(ast_node.names)
                        issues.append(f"[Line {line}] Global variable mutation ({names}) — tight module coupling")

            except SyntaxError as e:
                issues.append(f"[Line {e.lineno}] Python SyntaxError: {e.msg}")
            except Exception:
                # Fallback simple regex
                if re.search(r"^\s*except\s*:", code, re.MULTILINE):
                    issues.append("Bare 'except:' clause detected")

            if issues:
                findings.append((node.path, issues))

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not findings:
        return "✅ No critical Python code risks or anti-patterns detected."

    lines = []
    lines.append("=" * 60)
    lines.append("PYTHON RISK & CODE QUALITY AUDIT (AST-POWERED)")
    lines.append("=" * 60)
    lines.append("")

    for file_path, issues in findings:
        rel_file = _get_rel_path(file_path)
        lines.append(f"FILE: {rel_file}")
        lines.append("-" * (len(rel_file) + 6))
        for i in issues:
            lines.append(f"  ⚠ {i}")
        lines.append("")

    return "\n".join(lines)

