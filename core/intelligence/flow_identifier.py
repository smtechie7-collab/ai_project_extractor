import re
import os
from typing import List, Dict

class FlowIdentifier:
    """
    Detects critical business flows (Sales, Inventory, Auth, Data Processing)
    and sequences them logically: Entry/Route -> Business Logic -> Data/Model.
    """
    
    # Business domain keywords (checked against path/filename tokens)
    DOMAINS = {
        "SALES_PAYMENT_FLOW": ["sale", "billing", "invoice", "checkout", "cart", "order", "payment", "stripe", "transaction"],
        "INVENTORY_CATALOG_FLOW": ["inventory", "stock", "product", "warehouse", "catalog", "item", "adjustment"],
        "ACCOUNTING_FINANCE_FLOW": ["ledger", "journal", "voucher", "account", "tax", "gst", "invoice", "balance", "financial"],
        "AUTH_SECURITY_FLOW": ["auth", "login", "signup", "register", "session", "oauth", "jwt", "password", "credential", "permission", "user"],
        "CONTENT_NOTIFICATION_FLOW": ["notification", "email", "message", "alert", "feed", "post", "comment", "media", "upload"]
    }

    FLOW_ROLES = {
        # Kotlin / Android
        "SCREEN", "VIEWMODEL", "UISTATE", "USECASE", "REPOSITORY", "REPO_IMPL", "DAO", "ENTITY", "WORKER",
        # Python
        "ROUTER", "SERVICE", "MODEL", "TASK", "CLI",
        # JS / TS
        "PAGE_ROUTE", "COMPONENT", "HOOK", "STORE", "SERVICE_API", "SERVER", "MODEL_TYPE",
        # Java
        "CONTROLLER", "SERVICE", "REPOSITORY", "ENTITY", "DTO",
        # Universal
        "UI", "DATA_ACCESS"
    }

    ROLE_SORT_ORDER = {
        # Entry / UI / Controllers
        "SCREEN": 0, "COMPONENT": 0, "PAGE_ROUTE": 0, "ROUTER": 0, "CONTROLLER": 0, "CLI": 0, "UI": 0,
        # Logic / State / Orchestration
        "VIEWMODEL": 1, "HOOK": 1, "STORE": 1, "USECASE": 1, "SERVICE": 1, "UISTATE": 1,
        # Data / Storage
        "REPOSITORY": 2, "REPO_IMPL": 2, "SERVICE_API": 2, "DAO": 2, "ENTITY": 2, "MODEL": 2, "MODEL_TYPE": 2, "DTO": 2, "DATA_ACCESS": 2,
        # Background / Tasks
        "WORKER": 3, "TASK": 3, "SERVER": 3
    }

    @staticmethod
    def identify_critical_paths(metrics) -> Dict[str, List[str]]:
        paths = {domain: [] for domain in FlowIdentifier.DOMAINS}
        
        for m in metrics:
            if m.role not in FlowIdentifier.FLOW_ROLES:
                continue

            path_lower = m.path.lower()
            filename = os.path.basename(m.path)
            
            for domain, keywords in FlowIdentifier.DOMAINS.items():
                # Avoid trivial matches on generic words like "role" or single letters
                if any(kw in path_lower for kw in keywords):
                    paths[domain].append(f"{m.role}: {filename}")
        
        # Keep only domains where relevant components exist
        return {d: list(dict.fromkeys(p)) for d, p in paths.items() if p}

    @staticmethod
    def format_report(flow_map: Dict[str, List[str]]) -> str:
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