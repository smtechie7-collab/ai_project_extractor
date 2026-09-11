import os

class DependencyAlert:
    """
    Detects 'Dependency Explosion' and excessive coupling across components.
    """
    
    # Safe limits for imported dependencies per architectural role
    LIMITS = {
        # Kotlin / Android
        "VIEWMODEL": 8,
        "SCREEN": 10,
        "REPOSITORY": 6,
        "USECASE": 5,
        "DAO": 6,
        # Python
        "ROUTER": 8,
        "SERVICE": 8,
        "MODEL": 6,
        "TASK": 7,
        # JS / TS
        "COMPONENT": 10,
        "PAGE_ROUTE": 8,
        "HOOK": 6,
        "STORE": 6,
        "SERVICE_API": 7,
        # Java
        "CONTROLLER": 8,
        # Universal
        "UI": 10
    }

    @staticmethod
    def analyze(metrics) -> str:
        alerts = []
        
        for m in metrics:
            limit = DependencyAlert.LIMITS.get(m.role, 12)
            if m.dependency_count > limit:
                alerts.append({
                    "file": os.path.basename(m.path),
                    "role": m.role,
                    "count": m.dependency_count,
                    "limit": limit,
                    "severity": "CRITICAL" if m.dependency_count > (limit * 1.5) else "WARNING"
                })

        if not alerts:
            return "No dependency explosion detected. Component coupling levels are within healthy boundaries."

        lines = ["\n⚠️ DEPENDENCY EXPLOSION ALERTS (High Coupling Risk)", "-" * 55]
        for a in alerts:
            icon = "🔥" if a["severity"] == "CRITICAL" else "🟡"
            lines.append(f"{icon} {a['file']} ({a['role']})")
            lines.append(f"   Coupling: {a['count']} dependencies (Threshold: {a['limit']})")
            if a["severity"] == "CRITICAL":
                lines.append("   Recommendation: High fan-out detected. Consider splitting this into smaller focused units.")
        
        return "\n".join(lines)