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


# Hilt Patterns
MODULE_PATTERN = re.compile(r'@Module\b')
INSTALL_IN_PATTERN = re.compile(r'@InstallIn\s*\(\s*([A-Za-z0-9_]+)::class\s*\)')
PROVIDES_METHOD_PATTERN = re.compile(r'@Provides\s+(?:@\w+\s+)*(?:fun|def)\s+([A-Za-z0-9_]+)\s*\([^)]*\)\s*:\s*([A-Za-z0-9_<>.]+)')
BINDS_METHOD_PATTERN = re.compile(r'@Binds\s+(?:@\w+\s+)*(?:abstract\s+)?fun\s+([A-Za-z0-9_]+)\s*\([^:]+:\s*([A-Za-z0-9_<>.]+)\)\s*:\s*([A-Za-z0-9_<>.]+)')
HILT_VIEWMODEL_PATTERN = re.compile(r'@HiltViewModel\s+(?:@\w+\s+)*class\s+([A-Za-z0-9_]+)')
ENTRYPOINT_PATTERN = re.compile(r'@EntryPoint\b|@AndroidEntryPoint\b')


def export_kotlin_di_graph(tree_root):
    """
    Deep Dependency Injection (Hilt / Dagger) graph extractor with Mermaid component visualization.
    """
    hilt_modules = []
    viewmodels = []
    entrypoints = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            rel_p = _get_rel_path(node.path)

            # 1. Hilt Modules
            if MODULE_PATTERN.search(code):
                install_match = INSTALL_IN_PATTERN.search(code)
                component = install_match.group(1) if install_match else "UnspecifiedComponent"
                
                provides = PROVIDES_METHOD_PATTERN.findall(code)
                binds = BINDS_METHOD_PATTERN.findall(code)

                hilt_modules.append({
                    "file": rel_p,
                    "name": node.name.replace(".kt", ""),
                    "component": component,
                    "provides": [(fn, ret.split('<')[0].split('.')[-1]) for fn, ret in provides],
                    "binds": [(impl.split('<')[0].split('.')[-1], iface.split('<')[0].split('.')[-1]) for fn, impl, iface in binds]
                })

            # 2. Hilt ViewModels
            for vm in HILT_VIEWMODEL_PATTERN.findall(code):
                viewmodels.append((vm, rel_p))

            # 3. Android EntryPoints
            if ENTRYPOINT_PATTERN.search(code):
                entrypoints.append(rel_p)

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    if not hilt_modules and not viewmodels:
        return (
            "=" * 60 + "\n"
            "KOTLIN DEPENDENCY INJECTION GRAPH\n"
            "=" * 60 + "\n\n"
            "No Hilt or Dagger DI annotations detected in project."
        )

    lines = []
    lines.append("=" * 70)
    lines.append("💉 KOTLIN DEPENDENCY INJECTION GRAPH (HILT / DAGGER)")
    lines.append("=" * 70)
    lines.append(f"• Hilt Modules: {len(hilt_modules)}")
    lines.append(f"• Injected ViewModels: {len(viewmodels)}")
    lines.append(f"• Android EntryPoints (@AndroidEntryPoint): {len(entrypoints)}")
    lines.append("")

    # 1. Hilt Modules Section
    lines.append("## 1. HILT MODULES & PROVISIONING BINDINGS")
    for mod in sorted(hilt_modules, key=lambda m: m["name"]):
        lines.append(f"### Module: `{mod['name']}` (@InstallIn({mod['component']}::class))")
        lines.append(f"File: `{mod['file']}`")
        if mod["provides"]:
            lines.append("  • **Provided Instances (@Provides):**")
            for fn, ret in mod["provides"]:
                lines.append(f"    - `{fn}()` → `{ret}`")
        if mod["binds"]:
            lines.append("  • **Interface Bindings (@Binds):**")
            for impl, iface in mod["binds"]:
                lines.append(f"    - `{iface}` ⇐ `{impl}`")
        if not mod["provides"] and not mod["binds"]:
            lines.append("  • *(Custom scope or factory configuration)*")
        lines.append("")

    # 2. ViewModels Section
    lines.append("## 2. HILT VIEWMODELS (@HiltViewModel)")
    lines.append("| ViewModel Class | Defined In File |")
    lines.append("| :--- | :--- |")
    for vm, f in sorted(viewmodels):
        lines.append(f"| `{vm}` | `{f}` |")
    lines.append("")

    # 3. Mermaid Diagram
    lines.append("## 3. MERMAID DI COMPONENT DIAGRAM")
    lines.append("```mermaid")
    lines.append("graph TD")
    for mod in hilt_modules[:8]:
        m_name = re.sub(r'[^a-zA-Z0-9_]', '_', mod["name"])
        comp = mod["component"]
        lines.append(f"    Comp_{comp}[{comp}] --> Mod_{m_name}[Module: {mod['name']}]")
        for fn, ret in mod["provides"][:4]:
            clean_ret = re.sub(r'[^a-zA-Z0-9_]', '_', ret)
            lines.append(f"    Mod_{m_name} --> Type_{clean_ret}[{ret}]")
    lines.append("```")

    return "\n".join(lines)