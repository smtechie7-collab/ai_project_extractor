import os
from core.entry_extractor import detect_entry_files
from core.di_extractor import detect_di_files


def export_app_context(tree_root, project_root):
    os.makedirs("output", exist_ok=True)

    # ---------------- ENTRY & BOOTSTRAP ----------------
    entry_data = detect_entry_files(tree_root)

    with open(
        "output/A01_app_entry_and_bootstrap.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### APPLICATION ENTRY & BOOTSTRAP CONTEXT ###\n")

        for role, files in entry_data.items():
            f.write(f"\n\n## {role}\n")
            for path, content in files:
                rel = os.path.relpath(path, project_root)
                f.write(f"\n--- FILE: {rel} ---\n")
                f.write(content)

    # ---------------- DEPENDENCY / DI ----------------
    di_files = detect_di_files(tree_root)

    with open(
        "output/A02_dependency_container_di.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### DEPENDENCY & APP CONTAINER CONTEXT ###\n")

        for path, content in di_files:
            rel = os.path.relpath(path, project_root)
            f.write(f"\n--- FILE: {rel} ---\n")
            f.write(content)

    # ---------------- GLOBAL SESSION ----------------
    with open(
        "output/A03_global_session_and_state.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### GLOBAL SESSION / STATE FILES ###\n")

        for path, content in di_files:
            if "Session" in content or "Profile" in content:
                rel = os.path.relpath(path, project_root)
                f.write(f"\n--- FILE: {rel} ---\n")
                f.write(content)
