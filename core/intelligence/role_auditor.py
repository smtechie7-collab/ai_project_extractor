import os
import re
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class RoleMetric:
    path: str
    role: str
    line_count: int
    dependency_count: int
    is_god_class: bool
    risk_score: int  # 0 to 100

class RoleAuditor:
    """
    Analyzes files based on their architectural roles.
    Answers: 'Is this ViewModel too heavy?', 'Is UI touching DAO?'
    """
    
    GOD_CLASS_THRESHOLD = 500  # Lines
    DEPENDENCY_THRESHOLD = 7
    
    # Patterns for different languages
    IMPORT_PATTERN = {
        "kotlin": re.compile(r"import\s+([\w.]+)"),
        "python": re.compile(r"import\s+(\w+)|from\s+(\w+)\s+import"),
        "js": re.compile(r"import\s+.*from\s+['\"](.*)['\"]")
    }

    @staticmethod
    def audit_project(tree_root, language: str) -> List[RoleMetric]:
        metrics = []
        
        def walk(node):
            if not node.is_dir:
                metrics.append(RoleAuditor.audit_file(node.path, language))
            for child in node.children:
                walk(child)
        
        walk(tree_root)
        return metrics

    @staticmethod
    def audit_file(path: str, lang: str) -> RoleMetric:
        from core.utils.file_reader import read_text_file
        from core.classifier import classify_file
        
        content = read_text_file(path)
        lines = content.splitlines()
        line_count = len(lines)
        
        # Calculate Dependencies
        pattern = RoleAuditor.IMPORT_PATTERN.get(lang, RoleAuditor.IMPORT_PATTERN["kotlin"])
        deps = set(pattern.findall(content))
        dep_count = len(deps)
        
        role = classify_file(path, content)
        
        # God Class Logic
        is_god = line_count > RoleAuditor.GOD_CLASS_THRESHOLD or dep_count > RoleAuditor.DEPENDENCY_THRESHOLD
        
        # Risk Scoring
        score = 0
        if line_count > 300: score += 30
        if line_count > 600: score += 40
        if dep_count > 5: score += 15
        if dep_count > 10: score += 15
        
        return RoleMetric(
            path=path,
            role=role,
            line_count=line_count,
            dependency_count=dep_count,
            is_god_class=is_god,
            risk_score=min(score, 100)
        )

    @staticmethod
    def detect_violations(metrics: List[RoleMetric]) -> List[str]:
        violations = []
        for m in metrics:
            # Rule: UI should not have too many dependencies
            if m.role == "SCREEN" and m.dependency_count > 10:
                violations.append(f"🚩 UI Logic Heavy: {os.path.basename(m.path)} manages too many imports.")
            
            # Rule: ViewModel size
            if m.role == "VIEWMODEL" and m.is_god_class:
                violations.append(f"🔥 God ViewModel: {os.path.basename(m.path)} is becoming hard to maintain.")
        
        return violations