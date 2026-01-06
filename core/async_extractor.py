ASYNC_KEYWORDS = [
    "suspend ",
    "Flow<",
    "StateFlow<",
    "MutableStateFlow",
    "withContext",
    "launch(",
    "async(",
    "transaction",
    "runInTransaction",
]

def extract_async_context(tree_root):
    async_files = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for kw in ASYNC_KEYWORDS:
                if kw in content:
                    async_files.append((node.path, content))
                    break

        for child in node.children:
            walk(child)

    walk(tree_root)
    return async_files
