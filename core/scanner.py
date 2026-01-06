import os
from state.app_state import AppState
from core.language_registry import LANGUAGE_PROFILES

class Node:
    def __init__(self, path: str, is_dir: bool):
        self.path = path
        self.name = os.path.basename(path)
        self.is_dir = is_dir
        self.children = []

def is_supported_file(path: str) -> bool:
    profile = LANGUAGE_PROFILES.get(AppState.selected_language)
    if not profile:
        return False
    
    extensions = profile["extensions"]
    if not extensions:
        return True # All files mode

    return any(path.endswith(ext) for ext in extensions)

def scan_directory(root_path: str, whitelist_files: set = None) -> Node:
    """
    Scans directory recursively.
    If 'whitelist_files' is provided, ONLY includes files present in that set.
    """
    root = Node(root_path, True)

    try:
        items = os.listdir(root_path)
    except PermissionError:
        return root

    has_relevant_children = False

    for item in items:
        full_path = os.path.join(root_path, item)

        # Skip Junk
        if item.startswith(".") and item != ".gitignore": # Keep gitignore sometimes useful
             if item not in [".github"]: # Maybe keep github actions?
                 continue
        if item in {"__pycache__", "build", "dist", "node_modules", "venv", ".git", ".idea"}:
            continue

        if os.path.isdir(full_path):
            # Recurse
            child_node = scan_directory(full_path, whitelist_files)
            # Only add directory if it has content (or if we are not filtering)
            if child_node.children:
                root.children.append(child_node)
                has_relevant_children = True
        else:
            # File Handling
            is_relevant = is_supported_file(full_path)
            
            # 🔥 Git Filter Check
            if whitelist_files is not None:
                if full_path not in whitelist_files:
                    is_relevant = False

            if is_relevant:
                root.children.append(Node(full_path, False))
                has_relevant_children = True

    return root