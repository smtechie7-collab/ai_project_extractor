import os
from datetime import datetime


def export_ai_master_index(project_root):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []

    lines.append("############################################")
    lines.append("### AI MASTER INDEX — READ THIS FIRST ###")
    lines.append("############################################\n")

    lines.append(f"Generated At : {now}")
    lines.append(f"Project Root : {project_root}\n")

    # -------------------------------------------------
    lines.append("## 1. PROJECT OVERVIEW")
    lines.append(
        "- This is an Android/Kotlin ERP-style application.\n"
        "- Architecture follows layered / clean principles:\n"
        "  UI → ViewModel → UseCase → Repository → DAO → Database\n"
        "- Multiple business domains exist (Sales, Inventory, Accounting, Service).\n"
        "- Project uses Jetpack Compose for UI.\n"
    )

    # -------------------------------------------------
    lines.append("## 2. HOW TO READ THIS PROJECT (AI INSTRUCTIONS)")
    lines.append(
        "IMPORTANT RULES FOR AI:\n"
        "1. Do NOT assume missing code — rely only on exported files.\n"
        "2. Backend and UI are strictly separated.\n"
        "3. Never mix domain logic into UI reasoning.\n"
        "4. Treat ViewModels as orchestration layers only.\n"
        "5. Repository is the single source of truth for data access.\n"
    )

    # -------------------------------------------------
    lines.append("## 3. FILE READING ORDER (CRITICAL)")
    lines.append(
        "AI MUST READ FILES IN THIS EXACT ORDER:\n\n"
        "STEP 1 → 00_project_structure.txt\n"
        "STEP 2 → A01_app_entry_and_bootstrap.txt\n"
        "STEP 3 → A02_dependency_container_di.txt\n"
        "STEP 4 → A03_global_session_and_state.txt\n"
        "STEP 5 → U01_navigation_core.txt\n"
        "STEP 6 → U02_navigation_routes.txt\n"
        "STEP 7 → U03_dashboard_and_home_flow.txt\n"
        "STEP 8 → B0*_backend_system_map.txt\n"
        "STEP 9 → C01_viewmodel_to_usecase_map.txt\n"
        "STEP 10 → C03_ui_backend_full_contract.txt\n"
        "STEP 11 → R01_fragile_and_god_classes.txt\n"
        "STEP 12 → R02_layer_violation_report.txt\n"
    )

    # -------------------------------------------------
    lines.append("## 4. EXPORT FILE CATALOG")
    lines.append(
        "STRUCTURE:\n"
        "- 00_project_structure.txt → Complete folder/file hierarchy\n\n"
        "APPLICATION CONTEXT:\n"
        "- A01_app_entry_and_bootstrap.txt → App start & lifecycle\n"
        "- A02_dependency_container_di.txt → Dependency wiring\n"
        "- A03_global_session_and_state.txt → Global state/session\n\n"
        "UI FLOW:\n"
        "- U01_navigation_core.txt → NavHost & controllers\n"
        "- U02_navigation_routes.txt → Route definitions\n"
        "- U03_dashboard_and_home_flow.txt → Main & dashboard\n"
        "- U04_screen_to_screen_flow.txt → Screen navigation\n\n"
        "BACKEND DOMAINS:\n"
        "- B01–B05_*_system_map.txt → Domain-wise backend flows\n"
        "- B99_cross_domain_coupling.txt → Cross-module coupling\n\n"
        "UI ↔ BACKEND CONTRACT:\n"
        "- C01_viewmodel_to_usecase_map.txt\n"
        "- C02_usecase_to_repository_map.txt\n"
        "- C03_ui_backend_full_contract.txt\n"
        "- C04_async_flow_and_transactions.txt\n\n"
        "RISK & FRAGILITY:\n"
        "- R01_fragile_and_god_classes.txt\n"
        "- R02_layer_violation_report.txt\n"
        "- R03_missing_or_dangling_references.txt\n"
        "- R04_high_risk_async_and_transaction_zones.txt\n"
    )

    # -------------------------------------------------
    lines.append("## 5. KNOWN RISK ZONES (AI SHOULD BE CAREFUL)")
    lines.append(
        "- Sales ↔ Inventory ↔ Accounting coupling\n"
        "- Async operations touching DB & UI\n"
        "- Large ViewModels or Facades\n"
        "- Global session / profile switching\n"
    )

    # -------------------------------------------------
    lines.append("## 6. NON-GOALS (IMPORTANT)")
    lines.append(
        "- Do NOT rewrite code automatically.\n"
        "- Do NOT assume missing files exist.\n"
        "- Do NOT flatten layers.\n"
        "- Refactoring must be incremental & safe.\n"
    )

    # -------------------------------------------------
    lines.append("## 7. FINAL INSTRUCTION TO AI")
    lines.append(
        "You now have FULL CONTEXT of this project.\n"
        "Proceed with audits, fixes, or refactors ONLY\n"
        "based on these exported files.\n"
    )

    with open("output/00_AI_READ_FIRST_INDEX.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
