import os
import re
import ast
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from collections import defaultdict

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
    counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    total_lines: int = 0
    language: str = "general"

class RoleAuditor:
    """
    Production-grade Architectural Role Auditor.
    Provides first-class role analysis for Python, JavaScript/TypeScript, Kotlin, Java, and Universal projects.
    """
    GOD_CLASS_THRESHOLD = 500
    DEPENDENCY_THRESHOLD = 10

    JS_IMPORT_RE = re.compile(r"""(?:import\s+.*?from\s+['"]([^'"]+)['"]|import\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\))""")
    KOTLIN_JAVA_IMPORT_RE = re.compile(r"""import\s+(?:static\s+)?([\w.]+)""")
    CPP_INCLUDE_RE = re.compile(r"""#include\s*[<"]([^>"]+)[>"]""")

    @staticmethod
    def audit_project(tree_root, language: str) -> Tuple[List[RoleMetric], ProjectStats]:
        metrics = []
        lang = (language or "kotlin").lower()
        stats = ProjectStats(language=lang)

        # Initialize default categories based on ecosystem
        default_keys = RoleAuditor._get_default_roles_for_lang(lang)
        for k in default_keys:
            stats.counts[k] = 0

        def walk(node):
            if not node.is_dir:
                metric = RoleAuditor.audit_file(node.path, lang)
                metrics.append(metric)
                stats.counts[metric.role] += 1
                stats.total_lines += metric.line_count

            for child in node.children:
                walk(child)

        walk(tree_root)
        return metrics, stats

    @staticmethod
    def _get_default_roles_for_lang(lang: str) -> List[str]:
        if "python" in lang:
            return ["ROUTER", "SERVICE", "MODEL", "TASK", "CONFIG", "UTIL", "TEST", "CLI", "OTHER"]
        elif "javascript" in lang or "js" in lang:
            return ["COMPONENT", "PAGE_ROUTE", "HOOK", "STORE", "SERVICE_API", "SERVER", "MODEL_TYPE", "CONFIG", "UTIL", "TEST", "OTHER"]
        elif "kotlin" in lang:
            return ["SCREEN", "VIEWMODEL", "UISTATE", "USECASE", "REPOSITORY", "REPO_IMPL", "DAO", "ENTITY", "WORKER", "DI_MODULE", "OTHER"]
        elif "java" in lang:
            return ["CONTROLLER", "SERVICE", "REPOSITORY", "ENTITY", "CONFIG", "DTO", "TEST", "OTHER"]
        else:
            return ["UI", "CONTROLLER", "SERVICE", "DATA_ACCESS", "MODEL", "CONFIG", "UTIL", "TEST", "OTHER"]

    @staticmethod
    def extract_dependencies(path: str, content: str, lang: str) -> set:
        """Extracts unique dependencies cleanly using language-appropriate methods."""
        deps = set()
        if not content:
            return deps

        if "python" in lang or path.endswith(".py"):
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            deps.add(n.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            deps.add(node.module.split('.')[0])
            except SyntaxError:
                # Fallback to regex on syntax errors
                for m in re.finditer(r"^(?:import|from)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE):
                    deps.add(m.group(1))
            return deps

        if "javascript" in lang or path.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")):
            for match in RoleAuditor.JS_IMPORT_RE.finditer(content):
                imp = match.group(1) or match.group(2) or match.group(3)
                if imp:
                    deps.add(imp)
            return deps

        if "kotlin" in lang or "java" in lang or path.endswith((".kt", ".kts", ".java")):
            for match in RoleAuditor.KOTLIN_JAVA_IMPORT_RE.finditer(content):
                deps.add(match.group(1))
            return deps

        if "cpp" in lang or path.endswith((".c", ".cpp", ".h", ".hpp", ".cc", ".cxx")):
            for match in RoleAuditor.CPP_INCLUDE_RE.finditer(content):
                deps.add(match.group(1))
            return deps

        return deps

    @staticmethod
    def audit_file(path: str, lang: str) -> RoleMetric:
        from core.utils.file_reader import read_text_file

        content = read_text_file(path)
        lines = content.splitlines()
        line_count = len(lines)

        deps = RoleAuditor.extract_dependencies(path, content, lang)
        dep_count = len(deps)

        role = RoleAuditor.classify_role(path, content, lang)

        # Risk scoring
        is_god = line_count > RoleAuditor.GOD_CLASS_THRESHOLD
        score = 0
        if line_count > 300: score += 15
        if line_count > 600: score += 25
        if dep_count > 8: score += 15
        if dep_count > 15: score += 20

        # Language-specific risks
        if "kotlin" in lang and "!!" in content:
            score += 15
        elif "python" in lang and ("eval(" in content or "exec(" in content):
            score += 15
        elif ("javascript" in lang or "js" in lang) and ("eval(" in content or "dangerouslySetInnerHTML" in content):
            score += 15

        return RoleMetric(
            path=path,
            role=role,
            line_count=line_count,
            dependency_count=dep_count,
            is_god_class=is_god,
            risk_score=min(score, 100)
        )

    @staticmethod
    def classify_role(path: str, content: str, lang: str) -> str:
        name = os.path.basename(path).lower()
        lower_path = path.replace("\\", "/").lower()
        content_lower = content.lower()

        # ── 1. PYTHON CLASSIFICATION ──
        if "python" in lang or path.endswith(".py"):
            if "test" in name or "/test" in lower_path or "/tests" in lower_path:
                return "TEST"
            if name in ["main.py", "cli.py", "run.py", "app.py", "__main__.py"]:
                return "CLI"
            if any(k in name or f"/{k}" in lower_path for k in ["route", "router", "endpoint", "api", "view", "controller"]) or "apirouter" in content_lower or "blueprint" in content_lower:
                return "ROUTER"
            if any(k in name or f"/{k}" in lower_path for k in ["service", "manager", "logic", "usecase", "handler"]):
                return "SERVICE"
            if any(k in name or f"/{k}" in lower_path for k in ["model", "schema", "entity", "dto"]) or "basemodel" in content_lower or "declarative_base" in content_lower or "db.model" in content_lower:
                return "MODEL"
            if any(k in name or f"/{k}" in lower_path for k in ["worker", "task", "job", "celery", "cron", "consumer"]):
                return "TASK"
            if any(k in name or f"/{k}" in lower_path for k in ["config", "setting", "env", "constant"]):
                return "CONFIG"
            if any(k in name or f"/{k}" in lower_path for k in ["util", "helper", "tool", "common"]):
                return "UTIL"
            return "OTHER"

        # ── 2. JAVASCRIPT / TYPESCRIPT CLASSIFICATION ──
        if "javascript" in lang or "js" in lang or path.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")):
            if ".test." in name or ".spec." in name or "/test" in lower_path or "/__tests__" in lower_path:
                return "TEST"
            if name.startswith("use") and not name.startswith("user"):
                return "HOOK"
            if any(k in name or f"/{k}" in lower_path for k in ["store", "slice", "reducer", "atom", "state"]) or "zustand" in content_lower or "createSlice" in content:
                return "STORE"
            if "/pages/" in lower_path or "/app/" in lower_path and ("page." in name or "route." in name) or "route" in name:
                return "PAGE_ROUTE"
            if any(k in name or f"/{k}" in lower_path for k in ["service", "api", "client", "fetcher", "query"]):
                return "SERVICE_API"
            if name in ["server.js", "server.ts", "app.js", "app.ts"] or "express" in content_lower or "fastify" in content_lower:
                return "SERVER"
            if any(k in name or f"/{k}" in lower_path for k in ["model", "type", "interface", "schema", "dto"]):
                return "MODEL_TYPE"
            if path.endswith((".jsx", ".tsx")) or "/components/" in lower_path or name[0].isupper():
                return "COMPONENT"
            if any(k in name for k in ["config", "rc", "webpack", "vite", "package.json"]):
                return "CONFIG"
            if any(k in name or f"/{k}" in lower_path for k in ["util", "helper", "lib", "common"]):
                return "UTIL"
            return "OTHER"

        # ── 3. KOTLIN / ANDROID CLASSIFICATION ──
        if "kotlin" in lang or path.endswith((".kt", ".kts")):
            if "viewmodel" in name: return "VIEWMODEL"
            if "uistate" in name or "state.kt" in name: return "UISTATE"
            if "repositoryimpl" in name or "repoimpl" in name: return "REPO_IMPL"
            if "repository" in name: return "REPOSITORY"
            if "worker" in name or "workermanager" in content_lower: return "WORKER"
            if "usecase" in name or "interactor" in name: return "USECASE"
            if "screen" in name or "@composable" in content: return "SCREEN"
            if "dao" in name or "@dao" in content_lower: return "DAO"
            if "entity" in name or "@entity" in content_lower: return "ENTITY"
            if "module" in name or "container" in name or "@module" in content_lower: return "DI_MODULE"
            return "OTHER"

        # ── 4. JAVA CLASSIFICATION ──
        if "java" in lang or path.endswith(".java"):
            if "test" in name or "Test" in name: return "TEST"
            if "controller" in name or "@restcontroller" in content_lower or "@controller" in content_lower: return "CONTROLLER"
            if "service" in name or "@service" in content_lower: return "SERVICE"
            if "repository" in name or "dao" in name or "@repository" in content_lower: return "REPOSITORY"
            if "entity" in name or "@entity" in content_lower: return "ENTITY"
            if "dto" in name or "request" in name or "response" in name: return "DTO"
            if "config" in name or "@configuration" in content_lower: return "CONFIG"
            return "OTHER"

        # ── 5. UNIVERSAL / C++ / GENERAL ──
        if "test" in name or "test" in lower_path: return "TEST"
        if "main" in name: return "CLI"
        if path.endswith((".h", ".hpp", ".hh", ".hxx")): return "HEADER"
        if any(k in name or f"/{k}" in lower_path for k in ["controller", "api", "route"]): return "CONTROLLER"
        if any(k in name or f"/{k}" in lower_path for k in ["service", "logic", "manager"]): return "SERVICE"
        if any(k in name or f"/{k}" in lower_path for k in ["model", "entity", "schema"]): return "MODEL"
        if any(k in name or f"/{k}" in lower_path for k in ["dao", "repo", "db", "database"]): return "DATA_ACCESS"
        if any(k in name or f"/{k}" in lower_path for k in ["util", "helper", "common"]): return "UTIL"
        return "OTHER"

    @staticmethod
    def detect_violations(metrics: List[RoleMetric]) -> List[str]:
        violations = []
        for m in metrics:
            fname = os.path.basename(m.path)
            if m.role in ["SCREEN", "COMPONENT", "UI"] and m.dependency_count > 12:
                violations.append(f"🚩 UI Overload: {fname} has {m.dependency_count} dependencies (tightly coupled UI).")
            elif m.role in ["REPO_IMPL", "SERVICE", "CONTROLLER", "ROUTER"] and m.line_count > 400:
                violations.append(f"🔥 Fat Component: {fname} ({m.role}) has {m.line_count} lines (high complexity).")
            elif m.is_god_class:
                violations.append(f"💀 God Object: {fname} exceeds {RoleAuditor.GOD_CLASS_THRESHOLD} lines.")
            elif m.dependency_count > 15:
                violations.append(f"⚠️ Dependency Explosion: {fname} imports {m.dependency_count} dependencies.")
        return violations
