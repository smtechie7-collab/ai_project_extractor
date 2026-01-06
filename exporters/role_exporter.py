import os
from core.classifier import classify_file


def export_by_role(tree_root, project_root):
    role_buckets = {}

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            role = classify_file(node.path, content)
            role_buckets.setdefault(role, []).append((node.path, content))

        for child in node.children:
            walk(child)

    walk(tree_root)

    os.makedirs("output/roles", exist_ok=True)

    for role, files in role_buckets.items():
        out_path = f"output/roles/{role}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            for path, content in files:
                rel = os.path.relpath(path, project_root)
                f.write(f"\n\n=== FILE: {rel} ===\n")
                f.write(content)

    return role_buckets
