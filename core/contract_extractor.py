import os
import re

VIEWMODEL_PATTERN = re.compile(r'class\s+(\w+ViewModel)')
USECASE_PATTERN = re.compile(r'(\w+UseCase)')
REPOSITORY_PATTERN = re.compile(r'(\w+Repository)')

def extract_ui_backend_contract(tree_root):
    contracts = []

    def walk(node):
        if not node.is_dir and node.path.endswith("ViewModel.kt"):
            try:
                with open(node.path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return

            vm_match = VIEWMODEL_PATTERN.search(content)
            viewmodel = vm_match.group(1) if vm_match else os.path.basename(node.path)

            usecases = sorted(set(USECASE_PATTERN.findall(content)))
            repositories = sorted(set(REPOSITORY_PATTERN.findall(content)))

            contracts.append({
                "viewmodel": viewmodel,
                "path": node.path,
                "usecases": usecases,
                "repositories": repositories,
                "content": content,
            })

        for child in node.children:
            walk(child)

    walk(tree_root)
    return contracts
