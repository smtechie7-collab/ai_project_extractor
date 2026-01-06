import os
import re
from core.utils.file_reader import read_text_file

# --- Dagger/Hilt Patterns ---
MODULE_PATTERN = re.compile(r"@Module|@InstallIn")
PROVIDES_PATTERN = re.compile(r"@Provides|@Binds")

# --- Manual DI Patterns (AppContainer) ---
# Looks for class names ending in "Container" or "Factory"
CONTAINER_PATTERN = re.compile(r'class\s+(\w*AppContainer|\w*Container|\w*Factory)')
# Looks for "val repository =" or "val useCase =" lines inside containers
MANUAL_PROP_PATTERN = re.compile(r'(val|var)\s+(\w+)\s*[:=]\s*')

def export_kotlin_di_graph(tree_root):
    findings = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                code = read_text_file(node.path)
            except:
                return

            # 1. Check Dagger/Hilt
            if MODULE_PATTERN.search(code):
                provides_count = len(PROVIDES_PATTERN.findall(code))
                findings.append({
                    "type": "Hilt/Dagger Module",
                    "file": node.name,
                    "details": f"Contains {provides_count} provisioning methods"
                })
            
            # 2. Check Manual DI (AppContainer)
            # Sirf tab check karein agar ye Dagger module nahi hai
            else:
                container_match = CONTAINER_PATTERN.search(code)
                if container_match:
                    container_name = container_match.group(1)
                    # Count properties that might be dependencies
                    deps_count = len(MANUAL_PROP_PATTERN.findall(code))
                    
                    findings.append({
                        "type": "Manual DI Container",
                        "file": container_name,
                        "details": f"Manages approx {deps_count} dependencies (Manual DI)"
                    })

        for c in node.children:
            walk(c)

    walk(tree_root)

    if not findings:
        return "No DI modules detected (Checked for Hilt, Dagger, and AppContainer)."

    lines = []
    lines.append("=" * 50)
    lines.append("KOTLIN DEPENDENCY INJECTION GRAPH")
    lines.append("=" * 50)
    lines.append("")

    for item in findings:
        lines.append(f"[{item['type']}]")
        lines.append(f"FILE : {item['file']}")
        lines.append(f"INFO : {item['details']}")
        lines.append("-" * 40)
        lines.append("")

    return "\n".join(lines)