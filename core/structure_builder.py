def build_tree_text(node, indent="", is_last=True):
    """
    Returns a LIST of tree lines.
    Caller must join using '\\n'.
    """

    lines = []

    prefix = "└── " if is_last else "├── "
    lines.append(f"{indent}{prefix}{node.name}")

    next_indent = indent + ("    " if is_last else "│   ")

    for idx, child in enumerate(node.children):
        last = idx == len(node.children) - 1
        lines.extend(
            build_tree_text(
                child,
                indent=next_indent,
                is_last=last
            )
        )

    return lines
