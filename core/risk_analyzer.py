import os

SIZE_THRESHOLD_LINES = 500
ROLE_KEYWORDS = [
    "ViewModel",
    "UseCase",
    "Repository",
    "Dao",
    "Entity",
    "@Composable",
    "NavHost",
]


def detect_fragile_classes(tree_root):
    risky = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except Exception:
                return

            line_count = len(lines)
            content = "".join(lines)

            matched_roles = [k for k in ROLE_KEYWORDS if k in content]

            if line_count > SIZE_THRESHOLD_LINES or len(matched_roles) >= 3:
                risky.append({
                    "path": node.path,
                    "lines": line_count,
                    "roles": matched_roles,
                    "content": content,
                })

        for child in node.children:
            walk(child)

    walk(tree_root)
    return risky
