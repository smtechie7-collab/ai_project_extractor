import os


NAV_KEYWORDS = [
    "NavHost",
    "NavController",
    "AppNavHost",
    "composable(",
    "navController.navigate",
    "startDestination",
    "Routes.",
]


def extract_navigation_files(tree_root):
    results = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for kw in NAV_KEYWORDS:
                if kw in content:
                    results.append((node.path, content))
                    break

        for child in node.children:
            walk(child)

    walk(tree_root)
    return results
