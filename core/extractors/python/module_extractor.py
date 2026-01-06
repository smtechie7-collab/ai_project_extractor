def extract_modules(tree_root):
    modules = []

    def walk(node):
        if node.name.endswith(".py"):
            modules.append(node.path)
        for child in node.children:
            walk(child)

    walk(tree_root)
    return modules
