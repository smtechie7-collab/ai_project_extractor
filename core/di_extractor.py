import os


DI_KEYWORDS = [
    "AppContainer",
    "Container",
    "provide",
    "Repository",
    "Database",
    "Session",
]


def detect_di_files(tree_root):
    di_files = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for kw in DI_KEYWORDS:
                if kw in content:
                    di_files.append((node.path, content))
                    break

        for child in node.children:
            walk(child)

    walk(tree_root)
    return di_files
