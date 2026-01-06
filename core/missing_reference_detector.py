import re
import os

CLASS_REF_PATTERN = re.compile(r'\b([A-Z][A-Za-z0-9_]+)\b')


def detect_missing_references(tree_root):
    declared = set()
    referenced = set()

    def walk(node):
        if not node.is_dir and node.path.endswith(".kt"):
            name = os.path.splitext(os.path.basename(node.path))[0]
            declared.add(name)

            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            for ref in CLASS_REF_PATTERN.findall(content):
                referenced.add(ref)

        for child in node.children:
            walk(child)

    walk(tree_root)

    missing = sorted(ref for ref in referenced if ref not in declared)
    return missing
