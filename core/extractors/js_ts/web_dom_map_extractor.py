import os
import re
from collections import defaultdict

from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(p: str) -> str:
    try:
        if AppState.project_root:
            return os.path.relpath(p, AppState.project_root).replace("\\", "/")
        return os.path.basename(p)
    except Exception:
        return os.path.basename(p)


# HTML Patterns
VIEW_SECTION_PATTERN = re.compile(
    r'<(?:section|div|main)[^>]+id=["\']([a-zA-Z0-9_-]*(?:view|page|tab|screen|section|container)[a-zA-Z0-9_-]*)["\']',
    re.IGNORECASE
)

MODAL_PATTERN = re.compile(
    r'<(?:div|dialog)[^>]+id=["\']([a-zA-Z0-9_-]*(?:modal|dialog|drawer|popup|sheet)[a-zA-Z0-9_-]*)["\']',
    re.IGNORECASE
)

FORM_PATTERN = re.compile(
    r'<form[^>]+id=["\']([a-zA-Z0-9_-]+)["\']',
    re.IGNORECASE
)

BUTTON_ID_PATTERN = re.compile(
    r'<button[^>]+id=["\']([a-zA-Z0-9_-]+)["\']',
    re.IGNORECASE
)

# JS Binding Patterns
DOM_BIND_PATTERN = re.compile(
    r'(?:getElementById|querySelector(?:All)?)\s*\(\s*["\']#?([a-zA-Z0-9_-]+)["\']',
    re.IGNORECASE
)

EVENT_LISTENER_PATTERN = re.compile(
    r'([a-zA-Z0-9_$.]+)\.addEventListener\s*\(\s*["\']([a-zA-Z0-9_-]+)["\']\s*,\s*([a-zA-Z0-9_]+)?',
    re.IGNORECASE
)


def extract_web_dom_map(tree_root):
    """
    Extracts HTML Views, Modals, Forms, and correlates them with JS Module bindings.
    """
    html_files = []
    js_files = []

    def walk(node):
        if not node.is_dir:
            if node.name.endswith((".html", ".htm")):
                html_files.append(node.path)
            elif node.name.endswith((".js", ".ts", ".jsx", ".tsx")):
                js_files.append(node.path)

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    if not html_files:
        return (
            "=" * 60 + "\n"
            "WEB UI & DOM MAP (NO HTML FILES FOUND)\n"
            "=" * 60 + "\n\n"
            "No .html templates found in the project root. If this is a headless API or React/Vue app,\n"
            "refer to the Component classification in Full Source (AI)."
        )

    # 1. Parse HTML views and modals
    views = set()
    modals = set()
    forms = set()
    interactive_elements = set()

    for h_path in html_files:
        try:
            content = read_text_file(h_path)
        except Exception:
            continue

        for m in VIEW_SECTION_PATTERN.finditer(content):
            views.add(m.group(1))
        for m in MODAL_PATTERN.finditer(content):
            modals.add(m.group(1))
        for m in FORM_PATTERN.finditer(content):
            forms.add(m.group(1))
        for m in BUTTON_ID_PATTERN.finditer(content):
            interactive_elements.add(m.group(1))

    # 2. Correlate with JS handlers
    element_to_js = defaultdict(set)
    for js_path in js_files:
        try:
            code = read_text_file(js_path)
        except Exception:
            continue

        rel_js = _get_rel_path(js_path)
        for m in DOM_BIND_PATTERN.finditer(code):
            elem_id = m.group(1)
            if elem_id in views or elem_id in modals or elem_id in forms or elem_id in interactive_elements:
                element_to_js[elem_id].add(rel_js)

    lines = []
    lines.append("=" * 60)
    lines.append("WEB UI & DOM INTERACTION MAP")
    lines.append("=" * 60)
    lines.append(f"• HTML Templates: {len(html_files)}")
    lines.append(f"• Core Views/Sections: {len(views)}")
    lines.append(f"• Modals & Dialogs: {len(modals)}")
    lines.append(f"• Forms: {len(forms)}")
    lines.append("")

    # Views Table
    lines.append("## 1. PRIMARY VIEWS & SECTIONS")
    if views:
        lines.append("| View / Section ID | Bound JavaScript Handler / Module |")
        lines.append("| :--- | :--- |")
        for v in sorted(views):
            handlers = ", ".join(sorted(element_to_js[v])) if element_to_js[v] else "Static / CSS Routed"
            lines.append(f"| `#{v}` | {handlers} |")
    else:
        lines.append("No primary view sections with standard ID conventions detected.")
    lines.append("")

    # Modals Table
    lines.append("## 2. MODALS & POPUP DIALOGS")
    if modals:
        lines.append("| Modal ID | Interacting JavaScript Modules |")
        lines.append("| :--- | :--- |")
        for m in sorted(modals):
            handlers = ", ".join(sorted(element_to_js[m])) if element_to_js[m] else "Dynamic / Global Modal Trigger"
            lines.append(f"| `#{m}` | {handlers} |")
    else:
        lines.append("No modal dialogs found in HTML templates.")
    lines.append("")

    # Forms Table
    lines.append("## 3. DATA FORMS")
    if forms:
        lines.append("| Form ID | Handling JS Module |")
        lines.append("| :--- | :--- |")
        for f in sorted(forms):
            handlers = ", ".join(sorted(element_to_js[f])) if element_to_js[f] else "Unbound / Inline Handler"
            lines.append(f"| `#{f}` | {handlers} |")
    else:
        lines.append("No explicit form tags detected.")
    lines.append("")

    # Mermaid diagram
    lines.append("## 4. UI STRUCTURE DIAGRAM (MERMAID)")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append("    IndexHTML[index.html Entrypoint]")
    for v in sorted(views)[:12]:
        clean_v = re.sub(r'[^a-zA-Z0-9_]', '_', v)
        lines.append(f"    IndexHTML --> View_{clean_v}[View: #{v}]")
        if element_to_js[v]:
            first_js = list(element_to_js[v])[0]
            clean_js = re.sub(r'[^a-zA-Z0-9_]', '_', os.path.basename(first_js))
            lines.append(f"    View_{clean_v} -.-> {clean_js}")

    for m in sorted(modals)[:8]:
        clean_m = re.sub(r'[^a-zA-Z0-9_]', '_', m)
        lines.append(f"    IndexHTML -. Modal .-> Modal_{clean_m}[Modal: #{m}]")
    lines.append("```")

    return "\n".join(lines)
