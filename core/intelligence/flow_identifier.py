import re
import os
from typing import List, Dict

class FlowIdentifier:
    """
    Business Processes detect karta hai (Sales, Inventory, etc.)
    Trace karta hai: ViewModel -> UseCase -> Repository.
    """
    
    # Business domains ke keywords
    DOMAINS = {
        "SALES_FLOW": ["sale", "invoice", "bill", "customer", "order", "payment"],
        "INVENTORY_FLOW": ["stock", "inventory", "product", "warehouse", "adjustment", "unit"],
        "ACCOUNTING_FLOW": ["ledger", "journal", "voucher", "account", "tax", "gst", "debit", "credit"],
        "AUTH_FLOW": ["login", "token", "session", "user", "auth", "permission", "profile"]
    }

    @staticmethod
    def identify_critical_paths(metrics) -> Dict[str, List[str]]:
        paths = {domain: [] for domain in FlowIdentifier.DOMAINS}
        
        for m in metrics:
            path_lower = m.path.lower()
            filename = os.path.basename(m.path)
            
            for domain, keywords in FlowIdentifier.DOMAINS.items():
                if any(kw in path_lower for kw in keywords):
                    # Sirf main components ko flow mein dikhayenge
                    if m.role in ["VIEWMODEL", "USECASE", "REPOSITORY", "DAO", "SCREEN"]:
                        paths[domain].append(f"{m.role}: {filename}")
        
        # Sirf wahi domains rakho jinke files mili hain
        return {d: p for d, p in paths.items() if p}

    @staticmethod
    def format_report(flow_map: Dict[str, List[str]]) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("🎯 CRITICAL BUSINESS FLOWS (AUTO-DETECTED)")
        lines.append("=" * 60)
        
        if not flow_map:
            lines.append("Koi clear business flows nahi mile. File names check karein.")
            return "\n".join(lines)

        for domain, components in flow_map.items():
            lines.append(f"\n🔹 {domain}")
            lines.append("-" * (len(domain) + 3))
            
            # Logic: VM -> UC -> REPO -> DAO ke order mein sort karna
            order = {"SCREEN": 0, "VIEWMODEL": 1, "USECASE": 2, "REPOSITORY": 3, "DAO": 4, "BACKEND": 5}
            sorted_comp = sorted(components, key=lambda x: order.get(x.split(":")[0], 99))
            
            for i, comp in enumerate(sorted_comp):
                prefix = "   " if i == 0 else "   → "
                lines.append(f"{prefix}{comp}")
        
        lines.append("\n[INSIGHT] AI Prompting Tip: In flow groups ko AI ko batayein behtar logic ke liye.")
        return "\n".join(lines)