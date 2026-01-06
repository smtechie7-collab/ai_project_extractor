import os
from core.navigation_extractor import extract_navigation_files
from core.ui_flow_extractor import extract_routes_and_flows


def export_navigation_context(tree_root, project_root):
    os.makedirs("output", exist_ok=True)

    nav_files = extract_navigation_files(tree_root)
    routes, flows = extract_routes_and_flows(nav_files)

    # ---------------- NAV CORE ----------------
    with open(
        "output/U01_navigation_core.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### NAVIGATION CORE FILES ###\n")
        for path, content in nav_files:
            rel = os.path.relpath(path, project_root)
            f.write(f"\n--- FILE: {rel} ---\n")
            f.write(content)

    # ---------------- ROUTES ----------------
    with open(
        "output/U02_navigation_routes.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### ALL DETECTED ROUTES ###\n\n")
        for r in routes:
            f.write(f"- {r}\n")

    # ---------------- DASHBOARD / HOME ----------------
    with open(
        "output/U03_dashboard_and_home_flow.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### DASHBOARD & HOME FLOW ###\n")
        for path, content in nav_files:
            if "Dashboard" in content or "MainScreen" in content:
                rel = os.path.relpath(path, project_root)
                f.write(f"\n--- FILE: {rel} ---\n")
                f.write(content)

    # ---------------- SCREEN TO SCREEN FLOW ----------------
    with open(
        "output/U04_screen_to_screen_flow.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("### SCREEN TO SCREEN NAVIGATION CALLS ###\n")
        for path, content in flows:
            rel = os.path.relpath(path, project_root)
            f.write(f"\n--- FILE: {rel} ---\n")
            f.write(content)
