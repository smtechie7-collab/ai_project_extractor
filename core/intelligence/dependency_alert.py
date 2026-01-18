import os

class DependencyAlert:
    """
    'Dependency Explosion' detect karta hai (Jab ek file bahut zyada complex ho jaye).
    """
    
    # Thresholds: Isse zyada imports matlab "Danger"
    LIMITS = {
        "VIEWMODEL": 7,
        "SCREEN": 10,
        "REPOSITORY": 6,
        "USECASE": 4
    }

    @staticmethod
    def analyze(metrics) -> str:
        alerts = []
        
        for m in metrics:
            limit = DependencyAlert.LIMITS.get(m.role)
            if limit and m.dependency_count > limit:
                alerts.append({
                    "file": os.path.basename(m.path),
                    "role": m.role,
                    "count": m.dependency_count,
                    "limit": limit,
                    "severity": "CRITICAL" if m.dependency_count > (limit * 1.6) else "WARNING"
                })

        if not alerts:
            return ""

        lines = ["\n⚠️ DEPENDENCY EXPLOSION ALERTS (Fragile Code Detection)", "-" * 55]
        for a in alerts:
            icon = "🔥" if a["severity"] == "CRITICAL" else "🟡"
            lines.append(f"{icon} {a['file']} ({a['role']})")
            lines.append(f"   Complexity: {a['count']} dependencies (Safe limit: {a['limit']})")
            if a["severity"] == "CRITICAL":
                lines.append("   Action: Is file ko multiple smaller files mein break karein.")
        
        return "\n".join(lines)