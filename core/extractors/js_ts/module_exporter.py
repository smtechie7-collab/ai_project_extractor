import os
from collections import defaultdict
from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(path: str) -> str:
    try:
        base = AppState.project_root or os.getcwd()
        return os.path.relpath(path, start=base)
    except Exception:
        return os.path.basename(path)


CATEGORIES = {
    "pages & routes": ["pages", "app/routes", "route", "views"],
    "ui components": ["components", "ui", "widgets"],
    "state & stores": ["store", "slice", "reducer", "context"],
    "custom hooks": ["hooks"],
    "services & api clients": ["service", "api", "client", "fetcher"],
    "server & backend": ["server", "controllers", "routes"],
    "types & models": ["types", "models", "interfaces", "schema"],
    "utilities & helpers": ["utils", "helpers", "lib"],
    "configuration": ["config"],
    "tests": ["test", "__tests__", "spec"],
}


def classify_js_ts(path: str) -> str:
    lower = path.replace("\\", "/").lower()
    name = os.path.basename(path).lower()

    if name.endswith((".html", ".htm")) or name in ["sw.js", "manifest.webmanifest", "manifest.json"]:
        return "html & pwa entrypoints"
    if name.endswith(".css"):
        return "styles & themes"
    if "/modules/" in lower:
        return "business modules"
    if "test" in name or ".spec." in name or "/test" in lower:
        return "tests"
    if name.startswith("use") and not name.startswith("user"):
        return "custom hooks"
    if any(k in name or f"/{k}" in lower for k in ["store", "slice", "reducer", "atom"]):
        return "state & stores"
    if "/pages/" in lower or "/app/" in lower and ("page." in name or "route." in name):
        return "pages & routes"
    if any(k in name or f"/{k}" in lower for k in ["service", "api", "client"]):
        return "services & api clients"
    if any(k in name or f"/{k}" in lower for k in ["model", "type", "interface", "schema"]) or path.endswith(".d.ts"):
        return "types & models"
    if "/components/" in lower or path.endswith((".jsx", ".tsx")):
        return "ui components"
    if any(k in name or f"/{k}" in lower for k in ["util", "helper", "lib"]):
        return "utilities & helpers"
    if any(k in name for k in ["config", "package.json", "tsconfig", "webpack", "vite"]):
        return "configuration"

    return "general modules"


def export_js_ts_modules(tree_root):
    buckets = defaultdict(list)

    def walk(node):
        if not node.is_dir and node.name.endswith((".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".html", ".htm", ".css", ".webmanifest")):
            cat = classify_js_ts(node.path)
            buckets[cat].append(node.path)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not buckets:
        return "No JavaScript / TypeScript modules detected."

    lines = []
    lines.append("=" * 60)
    lines.append("JAVASCRIPT / TYPESCRIPT MODULE CLASSIFICATION")
    lines.append("=" * 60)
    lines.append("")

    for cat, files in sorted(buckets.items()):
        lines.append(f"[{cat.upper()}] ({len(files)} files)")
        lines.append("-" * (len(cat) + 12))
        for f in sorted(files):
            lines.append(f"• {_get_rel_path(f)}")
        lines.append("")

    return "\n".join(lines)


def export_js_ts_ai_code(tree_root):
    modules = defaultdict(list)

    def walk(node):
        if not node.is_dir and node.name.endswith((".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".html", ".htm", ".css", ".webmanifest")):
            cat = classify_js_ts(node.path)
            modules[cat].append(node.path)

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not modules:
        return "No JavaScript / TypeScript source files found."

    lines = []
    lines.append("=" * 70)
    lines.append("JAVASCRIPT / TYPESCRIPT FULL SOURCE CODE EXPORT (AI READY)")
    lines.append("=" * 70)
    lines.append("")
    lines.append(
        "AI INSTRUCTIONS:\n"
        "- This is the COMPLETE JavaScript / TypeScript project source code\n"
        "- Files are grouped by architectural role\n"
        "- Preserve existing state management and routing behavior when refactoring\n"
    )
    lines.append("")

    total_files = 0
    for cat in sorted(modules.keys()):
        files = sorted(set(modules[cat]))
        total_files += len(files)

        lines.append("")
        lines.append("#" * 70)
        lines.append(f"MODULE GROUP: {cat.upper()}")
        lines.append("#" * 70)
        lines.append("")

        for path in files:
            rel = _get_rel_path(path)
            lines.append("=" * 70)
            lines.append(f"FILE: {rel}")
            lines.append("=" * 70)
            lines.append("")

            try:
                lines.append(read_text_file(path))
            except Exception as e:
                lines.append(f"// ERROR READING FILE: {e}")

            lines.append("\n")

    lines.append("")
    lines.append(f"// TOTAL FILES EXPORTED: {total_files}")

    return "\n".join(lines)

