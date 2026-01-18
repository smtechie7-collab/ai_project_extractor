import os

class ExecutiveSummaryV2:
    """
    High-level project maturity score and health audit.
    Includes embedded support and contact info.
    """
    
    @staticmethod
    def build(project_name: str, metrics, violations) -> str:
        avg_risk = sum(m.risk_score for m in metrics) / len(metrics) if metrics else 0
        maturity_score = max(0, 100 - avg_risk)
        
        lines = []
        lines.append("🚀 AI CONTEXT ARCHITECTURAL AUDIT v2.0")
        lines.append("=" * 60)
        lines.append(f"PROJECT NAME    : {project_name.upper()}")
        lines.append(f"MATURITY SCORE  : {maturity_score:.1f}/100")
        
        status = "HEALTHY" if maturity_score > 75 else "NEEDS ATTENTION" if maturity_score > 50 else "AT RISK"
        lines.append(f"SYSTEM STATUS   : {status}")
        lines.append("-" * 60)
        
        lines.append("\n📊 MODULE DISTRIBUTION")
        roles = {}
        for m in metrics:
            roles[m.role] = roles.get(m.role, 0) + 1
            
        for role, count in sorted(roles.items()):
            lines.append(f"• {role:<12}: {count} assets detected")
            
        lines.append("\n🚩 CRITICAL ARCHITECTURAL RISKS")
        if not violations:
            lines.append("• Clean Architecture: No major violations found.")
        else:
            for v in violations[:10]:
                lines.append(f"• {v}")
                
        lines.append("\n💡 STRATEGIC RECOMMENDATIONS")
        if maturity_score < 65:
            lines.append("- Critical: Refactor high-risk modules to prevent technical debt.")
        lines.append("- Optimize: Use the 'Flow Identifier' output to map complex business logic.")

        # --- Developer Support ---
        lines.append("\n" + "=" * 60)
        lines.append("📬 SUPPORT THE DEVELOPER")
        lines.append("=" * 60)
        lines.append("If this tool helps your workflow, consider supporting development.")
        lines.append("Support ensures regular updates and enterprise feature additions.")
        lines.append("")
        lines.append("Developer : Hasnain Raza Memon")
        lines.append("Email     : hasnainrazamemon9@gmail.com")
        lines.append("UPI       : 9925811505")
        lines.append("PayPal    : https://paypal.me/raza489991")
        lines.append("-" * 60)
        lines.append("Scan the QR code in the application header for quick support. ☕")
            
        return "\n".join(lines)