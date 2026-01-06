import os


ENTRY_KEYWORDS = {
    "APPLICATION": ["Application", "extends Application", ": Application"],
    "MAIN_ACTIVITY": ["MainActivity"],
    "SPLASH": ["Splash"],
    "NAV_HOST": ["NavHost", "AppNavHost"],
}


def detect_entry_files(tree_root):
    result = {
        "APPLICATION": [],
        "MAIN_ACTIVITY": [],
        "SPLASH": [],
        "NAV_HOST": [],
    }

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for key, keywords in ENTRY_KEYWORDS.items():
                for kw in keywords:
                    if kw in content:
                        result[key].append((node.path, content))
                        break

        for child in node.children:
            walk(child)

    walk(tree_root)
    return result
