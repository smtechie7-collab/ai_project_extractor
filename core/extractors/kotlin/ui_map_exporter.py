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


COMPOSABLE_SCREEN_PATTERN = re.compile(r'@Composable\s+fun\s+([A-Za-z0-9_]*Screen)\s*\(')
ALL_COMPOSABLE_PATTERN = re.compile(r'@Composable\s+fun\s+([A-Za-z0-9_]+)\s*\(')
FEATURE_GATE_PATTERN = re.compile(r'\b(FeatureGate|RoleGate|RoleRestrictedScreen)\b')


def export_kotlin_ui_map(tree_root):
    """
    Extracts Jetpack Compose UI architecture, feature modules, and FeatureGate compliance.
    """
    feature_screens = defaultdict(list)
    xml_layouts = []
    ungated_screens = []

    def walk(node):
        if not node.is_dir and node.name.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            rel_p = _get_rel_path(node.path)

            screens = COMPOSABLE_SCREEN_PATTERN.findall(code)
            if not screens and "Screen" in node.name:
                screens = ALL_COMPOSABLE_PATTERN.findall(code)

            if screens:
                has_gate = bool(FEATURE_GATE_PATTERN.search(code))
                
                # Determine feature grouping
                parts = rel_p.replace("\\", "/").split("/")
                feature_name = "Core UI"
                if "feature" in parts:
                    f_idx = parts.index("feature")
                    if f_idx + 1 < len(parts):
                        feature_name = f"feature/{parts[f_idx+1]}"
                elif "ui" in parts:
                    feature_name = "ui/shared"

                for sc in screens:
                    feature_screens[feature_name].append({
                        "screen": sc,
                        "file": rel_p,
                        "gated": has_gate
                    })
                    if not has_gate and "Screen" in sc:
                        ungated_screens.append((sc, rel_p))

        elif not node.is_dir and node.name.endswith(".xml"):
            if "layout" in node.path.lower():
                xml_layouts.append(_get_rel_path(node.path))

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    lines = []
    lines.append("=" * 70)
    lines.append("📱 KOTLIN JETPACK COMPOSE UI MAP & FEATURE-GATE AUDIT")
    lines.append("=" * 70)
    total_screens = sum(len(v) for v in feature_screens.values())
    lines.append(f"• Total Composable Screen Components: {total_screens}")
    lines.append(f"• Feature Modules Detected: {len(feature_screens)}")
    if xml_layouts:
        lines.append(f"• Legacy XML Layouts: {len(xml_layouts)}")
    lines.append("")

    lines.append("## 1. FEATURE SCREENS & SECURITY GATING")
    for feat, scr_list in sorted(feature_screens.items()):
        lines.append(f"### Feature: `{feat}` ({len(scr_list)} screens)")
        lines.append("| Screen Composable | File | Protected by Gate? |")
        lines.append("| :--- | :--- | :--- |")
        for item in sorted(scr_list, key=lambda x: x["screen"]):
            gate_badge = "🛡️ FeatureGate / RoleGate" if item["gated"] else "⚪ Direct Access"
            lines.append(f"| `{item['screen']}` | `{item['file']}` | {gate_badge} |")
        lines.append("")

    lines.append("## 2. CONSTITUTION RULE 99: FEATURE GATING COMPLIANCE")
    if ungated_screens:
        lines.append(f"⚠ **{len(ungated_screens)} Screen(s) Without Explicit In-File Gate:**")
        lines.append("(Note: Verify if gated at NavHost destination level)")
        for sc, f in ungated_screens[:10]:
            lines.append(f"  • `{sc}` in `{f}`")
    else:
        lines.append("✅ All screens include explicit FeatureGate/RoleGate checks!")
    lines.append("")

    return "\n".join(lines)
