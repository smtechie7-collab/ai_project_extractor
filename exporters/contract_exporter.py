import os
from core.contract_extractor import extract_ui_backend_contract
from core.async_extractor import extract_async_context


def export_ui_backend_contracts(tree_root, project_root):
    os.makedirs("output", exist_ok=True)

    contracts = extract_ui_backend_contract(tree_root)

    # -------- ViewModel → UseCase --------
    with open("output/C01_viewmodel_to_usecase_map.txt", "w", encoding="utf-8") as f:
        f.write("### VIEWMODEL → USECASE MAP ###\n\n")
        for c in contracts:
            rel = os.path.relpath(c["path"], project_root)
            f.write(f"{c['viewmodel']}  ({rel})\n")
            for uc in c["usecases"]:
                f.write(f"  └── uses → {uc}\n")
            f.write("\n")

    # -------- UseCase → Repository --------
    with open("output/C02_usecase_to_repository_map.txt", "w", encoding="utf-8") as f:
        f.write("### USECASE → REPOSITORY MAP ###\n\n")
        for c in contracts:
            for uc in c["usecases"]:
                f.write(f"{uc}\n")
                for repo in c["repositories"]:
                    f.write(f"  └── accesses → {repo}\n")
                f.write("\n")

    # -------- Full Contract --------
    with open("output/C03_ui_backend_full_contract.txt", "w", encoding="utf-8") as f:
        f.write("### FULL UI ↔ BACKEND CONTRACT ###\n\n")
        for c in contracts:
            rel = os.path.relpath(c["path"], project_root)
            f.write(f"VIEWMODEL: {c['viewmodel']}\n")
            f.write(f"PATH: {rel}\n")
            for uc in c["usecases"]:
                f.write(f"  CALLS → {uc}\n")
            for repo in c["repositories"]:
                f.write(f"  USES → {repo}\n")
            f.write("\n")

    # -------- Async / Flow --------
    async_files = extract_async_context(tree_root)
    with open("output/C04_async_flow_and_transactions.txt", "w", encoding="utf-8") as f:
        f.write("### ASYNC / FLOW / TRANSACTION CONTEXT ###\n")
        for path, content in async_files:
            rel = os.path.relpath(path, project_root)
            f.write(f"\n--- FILE: {rel} ---\n")
            f.write(content)
