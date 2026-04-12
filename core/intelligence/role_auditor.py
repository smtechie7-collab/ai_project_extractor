import os
import re
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class RoleMetric:
    path: str
    role: str
    line_count: int
    dependency_count: int
    is_god_class: bool
    risk_score: int  # 0 to 100

@dataclass
class ProjectStats:
    counts: Dict[str, int] = field(default_factory=lambda: {
        "VIEWMODEL": 0,
        "UISTATE": 0,
        "REPOSITORY": 0,
        "REPO_IMPL": 0,
        "SCREEN": 0,
        "WORKER": 0,
        "USECASE": 0,
        "DAO": 0,
        "OTHER": 0
    })
    total_lines: int = 0

class RoleAuditor:
    """
    Analyzes files based on their architectural roles.
    Now tracks exact counts for ViewModels, States, Repos, and Workers.
    """
    
    GOD_CLASS_THRESHOLD = 500
    DEPENDENCY_THRESHOLD = 8
    
    IMPORT_PATTERN = {
        "kotlin": re.compile(r"import\s+([\w.]+)"),
        "python": re.compile(r"import\s+(\w+)|from\s+(\w+)\s+import"),
        "js": re.compile(r"import\s+.*from\s+['\"](.*)['\"]")
    }

    @staticmethod
    def audit_project(tree_root, language: str):
        metrics = []
        stats = ProjectStats()
        
        def walk(node):
            if not node.is_dir:
                metric = RoleAuditor.audit_file(node.path, language)
                metrics.append(metric)
                
                # Update Stats
                role = metric.role
                if role in stats.counts:
                    stats.counts[role] += 1
                else:
                    stats.counts["OTHER"] += 1
                stats.total_lines += metric.line_count
                
            for child in node.children:
                walk(child)
        
        walk(tree_root)
        return metrics, stats

    @staticmethod
    def audit_file(path: str, lang: str) -> RoleMetric:
        from core.utils.file_reader import read_text_file
        
        content = read_text_file(path)
        lines = content.splitlines()
        line_count = len(lines)
        
        # Dependency Detection
        pattern = RoleAuditor.IMPORT_PATTERN.get(lang.lower(), RoleAuditor.IMPORT_PATTERN["kotlin"])
        deps = set(pattern.findall(content))
        dep_count = len(deps)
        
        # Refined Classification Logic
        role = RoleAuditor.classify_refined(path, content)
        
        # God Class & Risk Logic
        is_god = line_count > RoleAuditor.GOD_CLASS_THRESHOLD
        score = 0
        if line_count > 300: score += 20
        if line_count > 600: score += 40
        if dep_count > 8: score += 20
        if "!!" in content: score += 10 # Kotlin specific risk
        
        return RoleMetric(
            path=path,
            role=role,
            line_count=line_count,
            dependency_count=dep_count,
            is_god_class=is_god,
            risk_score=min(score, 100)
        )

    @staticmethod
    def classify_refined(path: str, content: str) -> str:
        name = os.path.basename(path).lower()
        
        # Priority Order for Classification
        if "viewmodel" in name: return "VIEWMODEL"
        if "uistate" in name or "state.kt" in name: return "UISTATE"
        if "repositoryimpl" in name or "repoimpl" in name: return "REPO_IMPL"
        if "repository" in name: return "REPOSITORY"
        if "worker" in name: return "WORKER"
        if "usecase" in name: return "USECASE"
        if "screen" in name or "@composable" in content: return "SCREEN"
        if "dao" in name or "@dao" in content.lower(): return "DAO"
        if "entity" in name or "@entity" in content.lower(): return "ENTITY"
        
        return "OTHER"

    @staticmethod
    def detect_violations(metrics: List[RoleMetric]) -> List[str]:
        violations = []
        for m in metrics:
            if m.role == "SCREEN" and m.dependency_count > 12:
                violations.append(f"🚩 UI Overload: {os.path.basename(m.path)} has too many dependencies.")
            if m.role == "REPO_IMPL" and m.line_count > 400:
                violations.append(f"🔥 Fat Repository: {os.path.basename(m.path)} logic is too complex.")
            if m.is_god_class:
                violations.append(f"💀 God Object: {os.path.basename(m.path)} exceeds maintenance limits.")
        return violations
