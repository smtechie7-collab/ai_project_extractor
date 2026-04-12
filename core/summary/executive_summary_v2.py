import os

class ExecutiveSummaryV2:
    """
    High-level project maturity score and health audit.
    Updated to show exact component counts.
    """
    
    @staticmethod
    def build(project_name: str, metrics, violations, stats=None) -> str:
        avg_risk = sum(m.risk_score for m in metrics) / len(metrics) if metrics else 0
        maturity_score = max(0, 100 - avg_risk)
        
        lines = []
        lines.append("🚀 AI CONTEXT ARCHITECTURAL AUDIT v2.1")
        lines.append("=" * 60)
        lines.append(f"PROJECT        : {project_name.upper()}")
        lines.append(f"MATURITY SCORE : {maturity_score:.1f}/100")
        
        status = "HEALTHY" if maturity_score > 80 else "NEEDS REFACTOR" if maturity_score > 60 else "CRITICAL"
        lines.append(f"SYSTEM STATUS  : {status}")
        lines.append("-" * 60)
        
        if stats:
            lines.append("\n🏗️ PROJECT BLUEPRINT (COMPONENTS)")
            lines.append(f"{'TYPE':<15} | {'COUNT':<6} | {'STATUS'}")
            lines.append("-" * 40)
            for role, count in stats.counts.items():
                if count > 0 or role != "OTHER":
                    indicator = "✅" if count > 0 else "❌"
                    lines.append(f"{role:<15} | {count:<6} | {indicator}")
            
            lines.append(f"\nTotal Source Lines: {stats.total_lines}")

        lines.append("\n🚩 CRITICAL ARCHITECTURAL RISKS")
        if not violations:
            lines.append("• Structure: Architecture appears clean and modular.")
        else:
            for v in violations[:8]:
                lines.append(f"• {v}")
                
        lines.append("\n💡 AI OPTIMIZATION TIP")
        if stats and stats.counts.get("UISTATE", 0) == 0:
            lines.append("- Warning: No UIState files found. AI might struggle with state flow.")
        lines.append("- Action: Share REPO_IMPL files with AI to check for threading leaks.")

        # --- Support Footer ---
        lines.append("\n" + "=" * 60)
        lines.append("📬 DEVELOPER SUPPORT")
        lines.append("Developed by: Hasnain Raza Memon")
        lines.append("Support: hasnainrazamemon9@gmail.com | UPI: 9925811505")
        lines.append("=" * 60)
            
        return "\n".join(lines)
