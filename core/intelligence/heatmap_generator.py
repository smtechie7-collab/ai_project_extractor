import os

class RiskHeatmap:
    """
    Generates a visual 'Heatmap' of the project architecture.
    """
    
    @staticmethod
    def generate(metrics) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("🔥 ARCHITECTURE RISK HEATMAP")
        lines.append("=" * 60)
        lines.append(f"{'RISK':<10} | {'ROLE':<15} | {'FILE'}")
        lines.append("-" * 60)
        
        # Sort by risk score
        sorted_metrics = sorted(metrics, key=lambda x: x.risk_score, reverse=True)
        
        for m in sorted_metrics:
            filename = os.path.basename(m.path)
            
            if m.risk_score >= 70:
                indicator = "🔴 CRITICAL"
            elif m.risk_score >= 40:
                indicator = "🟡 WARNING "
            else:
                indicator = "🟢 SAFE    "
                
            lines.append(f"{indicator} | {m.role:<15} | {filename}")
            
        lines.append("\n[HEATMAP SUMMARY]")
        critical_count = len([x for x in metrics if x.risk_score >= 70])
        lines.append(f"• Critical Assets (Red): {critical_count}")
        lines.append(f"• Refactor Priority: {'HIGH' if critical_count > 2 else 'MODERATE'}")
        
        return "\n".join(lines)