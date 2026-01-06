import os
from state.app_state import AppState
from core.language_registry import LANGUAGE_PROFILES


class Node:
    def __init__(self, path: str, is_dir: bool):
        self.path = path
        self.name = os.path.basename(path)   # ✅ MANDATORY
        self.is_dir = is_dir
        self.children = []


def is_supported_file(path: str) -> bool:
    profile = LANGUAGE_PROFILES.get(AppState.selected_language)

    if not profile:
        return False

    extensions = profile["extensions"]

    # All languages mode
    if not extensions:
        return True

    return any(path.endswith(ext) for ext in extensions)


def scan_directory(root_path: str) -> Node:
    root = Node(root_path, True)

    try:
        items = os.listdir(root_path)
    except PermissionError:
        return root

    for item in items:
        full_path = os.path.join(root_path, item)

        # Skip junk / heavy dirs
        if item.startswith(".") or item in {
            "__pycache__", "build", "dist", "node_modules", ".git"
        }:
            continue

        if os.path.isdir(full_path):
            child = scan_directory(full_path)
            root.children.append(child)
        else:
            if is_supported_file(full_path):
                root.children.append(Node(full_path, False))

    return root
