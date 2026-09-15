import os

from core.language_registry import LANGUAGE_PROFILES
from state.app_state import AppState


from models.tree_node import Node, TreeNode

def is_supported_file(path: str) -> bool:
    profile = LANGUAGE_PROFILES.get(AppState.selected_language)
    if not profile:
        return False

    extensions = profile["extensions"]
    if not extensions:
        return True # All files mode

    return any(path.endswith(ext) for ext in extensions)

IGNORED_DIRS = {
    "__pycache__", "build", "dist", "node_modules", "venv", ".venv",
    ".git", ".idea", ".vs", "target", ".gradle", ".pytest_cache"
}
ALLOWED_HIDDEN = {".github", ".gitignore"}


def scan_directory(root_path: str, whitelist_files: set = None) -> Node:
    """
    Scans directory iteratively using os.walk (no recursion).
    If 'whitelist_files' is provided, ONLY includes files present in that set.
    Empty directories containing no supported files are automatically pruned.
    """
    root_norm = os.path.normpath(root_path)
    root_node = Node(root_path, True)
    dir_nodes: dict[str, Node] = {root_norm: root_node}

    # Normalize whitelist if provided
    normalized_whitelist = None
    if whitelist_files is not None:
        normalized_whitelist = {os.path.normpath(f) for f in whitelist_files}

    try:
        walker = os.walk(root_path, topdown=True)
    except (PermissionError, FileNotFoundError):
        return root_node

    for dirpath, dirnames, filenames in walker:
        # Prune ignored and hidden directories in-place before os.walk descends
        dirnames[:] = [
            d for d in dirnames
            if d not in IGNORED_DIRS and (not d.startswith(".") or d in ALLOWED_HIDDEN)
        ]

        # Filter and collect accepted files in current dirpath
        for item in sorted(filenames):
            if item.startswith(".") and item not in ALLOWED_HIDDEN:
                continue

            full_path = os.path.join(dirpath, item)
            if not is_supported_file(full_path):
                continue

            norm_file = os.path.normpath(full_path)
            if normalized_whitelist is not None and norm_file not in normalized_whitelist:
                continue

            # Ensure parent chain exists in dir_nodes
            parent_dir = os.path.normpath(dirpath)
            if parent_dir not in dir_nodes:
                # Build directory chain up to root
                chain = []
                curr = parent_dir
                while curr and curr != root_norm and curr not in dir_nodes:
                    chain.append(curr)
                    next_curr = os.path.normpath(os.path.dirname(curr))
                    if next_curr == curr:
                        break
                    curr = next_curr

                # Attach downwards from the nearest ancestor
                for d in reversed(chain):
                    ancestor = os.path.normpath(os.path.dirname(d))
                    ancestor_node = dir_nodes.get(ancestor, root_node)
                    d_node = Node(d, True)
                    ancestor_node.children.append(d_node)
                    dir_nodes[d] = d_node

            # Attach file node
            dir_nodes[parent_dir].children.append(Node(full_path, False))

    return root_node
