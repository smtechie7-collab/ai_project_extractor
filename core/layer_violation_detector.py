LAYER_RULES = [
    ("ui", "Dao"),
    ("ui", "Entity"),
    ("ui", "Database"),
    ("domain", "@Composable"),
]


def detect_layer_violations(tree_root):
    violations = []

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            path_lower = node.path.lower()

            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for layer, forbidden in LAYER_RULES:
                if f"/{layer}/" in path_lower and forbidden in content:
                    violations.append({
                        "path": node.path,
                        "violation": f"{layer.upper()} layer contains forbidden reference: {forbidden}",
                        "content": content,
                    })

        for child in node.children:
            walk(child)

    walk(tree_root)
    return violations
