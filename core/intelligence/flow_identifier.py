import os


class FlowIdentifier:
    """
    Detects critical business flows (Sales, Inventory, Auth, Data Processing)
    and sequences them logically: Entry/Route -> Business Logic -> Data/Model.
    """

    # Business domain keywords (checked against path/filename tokens)
    DOMAINS = {
        "SALES_PAYMENT_FLOW": ["sale", "billing", "invoice", "checkout", "cart", "order", "payment", "stripe", "transaction", "pos", "quotation"],
        "PURCHASE_PROCUREMENT_FLOW": ["purchase", "procurement", "supplier", "vendor", "buy"],
        "INVENTORY_CATALOG_FLOW": ["inventory", "stock", "product", "warehouse", "catalog", "item", "adjustment"],
        "ACCOUNTING_FINANCE_FLOW": ["ledger", "journal", "voucher", "account", "tax", "gst", "balance", "financial", "capital", "expense", "daybook", "cash"],
        "AUTH_SECURITY_FLOW": ["auth", "login", "signup", "register", "session", "oauth", "jwt", "password", "credential", "permission", "onboarding", "kyc"],
        "CONTENT_NOTIFICATION_FLOW": ["notification", "email", "message", "alert", "feed", "post", "comment", "whatsapp", "communication"]
    }

    FLOW_ROLES = {
        # Kotlin / Android
        "SCREEN", "VIEWMODEL", "UISTATE", "USECASE", "REPOSITORY", "REPO_IMPL", "DAO", "ENTITY", "WORKER",
        # Python
        "ROUTER", "SERVICE", "MODEL", "TASK", "CLI",
        # JS / TS / Web
        "PAGE_ROUTE", "COMPONENT", "FEATURE_MODULE", "APP_ENTRY", "HOOK", "STORE", "SERVICE_API", "SERVER", "MODEL_TYPE",
        # Java
        "CONTROLLER", "DTO",
        # Universal
        "UI", "DATA_ACCESS"
    }

    ROLE_SORT_ORDER = {
        # Entry / UI / Controllers
        "APP_ENTRY": 0, "SCREEN": 0, "COMPONENT": 0, "FEATURE_MODULE": 0, "PAGE_ROUTE": 0, "ROUTER": 0, "CONTROLLER": 0, "CLI": 0, "UI": 0,
        # Logic / State / Orchestration
        "VIEWMODEL": 1, "HOOK": 1, "STORE": 1, "USECASE": 1, "SERVICE": 1, "UISTATE": 1,
        # Data / Storage
        "REPOSITORY": 2, "REPO_IMPL": 2, "SERVICE_API": 2, "DAO": 2, "ENTITY": 2, "MODEL": 2, "MODEL_TYPE": 2, "DTO": 2, "DATA_ACCESS": 2,
        # Background / Tasks
        "WORKER": 3, "TASK": 3, "SERVER": 3
    }

    @staticmethod
    def identify_critical_paths(metrics) -> dict[str, list[str]]:
        paths = {domain: [] for domain in FlowIdentifier.DOMAINS}

        from state.app_state import AppState

        for m in metrics:
            if m.role not in FlowIdentifier.FLOW_ROLES:
                continue

            filename = os.path.basename(m.path)
            try:
                rel = os.path.relpath(m.path, AppState.project_root) if AppState.project_root else filename
            except Exception:
                rel = filename
            token_string = rel.lower().replace("\\", "/")

            for domain, keywords in FlowIdentifier.DOMAINS.items():
                if any(kw in token_string for kw in keywords):
                    paths[domain].append(f"{m.role}: {filename}")

        # Keep only domains where relevant components exist
        return {d: list(dict.fromkeys(p)) for d, p in paths.items() if p}

    @staticmethod
    def format_report(flow_map: dict[str, list[str]]) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("🎯 CRITICAL BUSINESS FLOWS (AUTO-DETECTED)")
        lines.append("=" * 60)

        if not flow_map:
            lines.append("No explicit business domain flows identified from component naming.")
            return "\n".join(lines)

        for domain, components in flow_map.items():
            lines.append(f"\n🔹 {domain}")
            lines.append("-" * (len(domain) + 3))

            # Sort by architectural sequence: Entry -> Logic -> Data
            sorted_comp = sorted(components, key=lambda x: FlowIdentifier.ROLE_SORT_ORDER.get(x.split(":")[0], 99))

            for i, comp in enumerate(sorted_comp):
                prefix = "   " if i == 0 else "   → "
                lines.append(f"{prefix}{comp}")

        lines.append("\n[AI GUIDANCE] Feed these sequence flows into LLMs for domain-accurate feature additions and refactoring.")
        return "\n".join(lines)