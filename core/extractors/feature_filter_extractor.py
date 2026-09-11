"""
feature_filter_extractor.py
============================
Kisi bhi feature/module ka naam do (jaise "billing", "repair", "purchase")
aur yeh module sirf usse RELATED files extract karke deta hai.

Scoring System:
  +10  → Path mein keyword match
  +8   → File name mein keyword match
  +5   → Import statement mein related class/file ka naam
  +3   → Content mein keyword (class/function level)
  +2   → Content mein keyword (general mention)
"""

import os
import re
from collections import defaultdict
from core.utils.file_reader import read_text_file


# ─────────────────────────────────────────────
# RELATED TERMS MAP
# Jab user "billing" likhe to related terms bhi search karo
# ─────────────────────────────────────────────
RELATED_TERMS_MAP = {
    "billing":      ["billing", "invoice", "checkout", "cart", "sale", "payment"],
    "purchase":     ["purchase", "supplier", "procure", "buy", "vendor"],
    "sales":        ["sale", "billing", "invoice", "revenue"],
    "repair":       ["repair", "job", "technician", "diagnosis", "warranty"],
    "inventory":    ["inventory", "stock", "product", "warehouse", "batch"],
    "accounting":   ["accounting", "ledger", "voucher", "gst", "tax", "journal"],
    "customer":     ["customer", "client", "ledger", "kyc"],
    "supplier":     ["supplier", "vendor", "purchase", "ledger"],
    "dashboard":    ["dashboard", "home", "summary", "health", "overview"],
    "service":      ["service", "contract", "amc", "call", "followup"],
    "report":       ["report", "analytics", "gst", "export", "pdf"],
    "settings":     ["settings", "config", "profile", "preferences"],
    "auth":         ["auth", "login", "session", "user", "permission"],
    "migration":    ["migration", "import", "export", "csv", "mapper"],
    "restaurant":   ["restaurant", "kot", "table", "kitchen", "shift"],
    "manufacture":  ["manufacture", "bom", "production", "order"],
    "expense":      ["expense", "budget", "recurring"],
    "warranty":     ["warranty", "expiry", "claim"],
    "staff":        ["staff", "employee", "attendance", "commission"],
    "payment":      ["payment", "emi", "collection", "receipt"],
    "backup":       ["backup", "restore", "drive", "storage"],
    "navigation":   ["navigation", "nav", "route", "screen", "deeplink"],
    "di":           ["di", "module", "hilt", "inject", "provide", "container"],
    "database":     ["database", "room", "dao", "entity", "migration"],
    "notification": ["notification", "reminder", "alert", "worker"],
    "kyc":          ["kyc", "document", "verification", "identity"],
}

# Architecture roles jinhe HAMESHA include karo agar relevant ho
ARCH_ROLES = ["ViewModel", "UseCase", "Repository", "Dao", "Entity", "Screen", "State"]


class FeatureFilterExtractor:

    def __init__(self, query: str, max_files: int = 100):
        self.raw_query = query.strip()
        self.max_files = max_files
        self.keywords = self._resolve_keywords(query)

    # ─────────────────────────────────────────────
    # PUBLIC METHOD
    # ─────────────────────────────────────────────
    def extract(self, tree_root) -> str:
        """
        Main entry point.
        tree_root: Node object from scanner.py
        Returns: Formatted string with all relevant file contents
        """
        scored_files = self._score_all_files(tree_root)

        if not scored_files:
            return (
                f"[RESULT] '{self.raw_query}' ke liye koi relevant file nahi mili.\n"
                f"Try: {', '.join(self.keywords[:5])}"
            )

        # Sort by score descending, limit to max_files (updated to 100)
        top_files = sorted(scored_files, key=lambda x: x[1], reverse=True)[:self.max_files]

        return self._format_output(top_files)

    # ─────────────────────────────────────────────
    # KEYWORD RESOLUTION
    # ─────────────────────────────────────────────
    def _resolve_keywords(self, query: str):
        """
        User ke query se related keywords nikalta hai.
        Example: "billing" → ["billing", "invoice", "checkout", "cart", ...]
        """
        q = query.lower().strip()
        keywords = set(q.split())  # user ke words

        # Map se extra related terms add karo
        for key, terms in RELATED_TERMS_MAP.items():
            if q in key or key in q:
                keywords.update(terms)
                break
        else:
            # Partial match try karo
            for key, terms in RELATED_TERMS_MAP.items():
                if any(word in key for word in q.split()):
                    keywords.update(terms)

        return list(keywords)

    # ─────────────────────────────────────────────
    # SCORING ENGINE
    # ─────────────────────────────────────────────
    def _score_file(self, path: str, content: str) -> int:
        """
        Ek file ko score deta hai (0 = irrelevant, higher = more relevant)
        """
        score = 0
        path_lower = path.lower()
        filename = os.path.basename(path).lower()
        content_lower = content.lower()

        for kw in self.keywords:
            kw_lower = kw.lower()

            # Path mein keyword
            if kw_lower in path_lower:
                score += 10

            # File name mein keyword
            if kw_lower in filename:
                score += 8

            # Import statements mein (strongly indicates dependency)
            if re.search(rf'import\s+.*{re.escape(kw_lower)}', content_lower):
                score += 5

            # Class/function definition level match
            if re.search(
                rf'(class|fun|def|interface|object)\s+\w*{re.escape(kw_lower)}\w*',
                content_lower
            ):
                score += 3

            # General content mention
            if kw_lower in content_lower:
                score += 2

        # Architecture role bonus: ViewModel/UseCase related files ko extra weight
        for role in ARCH_ROLES:
            if role.lower() in filename:
                score += 1  # Tie-breaking bonus for arch files

        return score

    def _score_all_files(self, tree_root):
        """
        Poore tree ko walk karke har file ka score nikalta hai.
        Returns: list of (path, score, content)
        """
        results = []

        def walk(node):
            if node.is_dir:
                for child in node.children:
                    walk(child)
                return

            # Sirf source files process karo
            if not self._is_source_file(node.path):
                return

            try:
                content = read_text_file(node.path)
            except Exception:
                return

            if content.startswith("["):  # Binary/error markers
                return

            score = self._score_file(node.path, content)

            if score > 0:
                results.append((node.path, score, content))

        walk(tree_root)
        return results

    def _is_source_file(self, path: str) -> bool:
        SUPPORTED = (
            ".kt", ".java", ".py", ".js", ".ts",
            ".jsx", ".tsx", ".xml", ".gradle"
        )
        return any(path.endswith(ext) for ext in SUPPORTED)

    # ─────────────────────────────────────────────
    # OUTPUT FORMATTER
    # ─────────────────────────────────────────────
    def _format_output(self, top_files: list) -> str:
        lines = []

        # ── HEADER ──
        lines.append("=" * 70)
        lines.append(f"🎯 FEATURE FILTER: '{self.raw_query.upper()}'")
        lines.append("=" * 70)
        lines.append(f"Keywords used   : {', '.join(self.keywords)}")
        lines.append(f"Files matched   : {len(top_files)}")
        lines.append("")
        lines.append("AI INSTRUCTIONS:")
        lines.append(
            f"  The following files are directly related to the '{self.raw_query}' feature.\n"
            "  Focus your architectural analysis, code modifications, or bug fixes on these files.\n"
            "  Files are grouped by relevance score and architectural layer."
        )
        lines.append("=" * 70)
        lines.append("")

        # ── FILE INDEX (Quick overview) ──
        lines.append("📋 FILE INDEX (Relevance Order)")
        lines.append("-" * 50)
        for i, (path, score, _) in enumerate(top_files, 1):
            rel = self._rel_path(path)
            role = self._detect_role(path)
            lines.append(f"  {i:>2}. [{score:>3}pts] [{role:<15}] {rel}")
        lines.append("")

        # ── GROUPED BY ARCHITECTURE ROLE ──
        groups = defaultdict(list)
        for path, score, content in top_files:
            role = self._detect_role(path)
            groups[role].append((path, score, content))

        for role, files in sorted(groups.items(), key=lambda x: len(x[1]), reverse=True):
            lines.append("#" * 70)
            lines.append(f"LAYER: {role} ({len(files)} files)")
            lines.append("#" * 70)
            lines.append("")

            for path, score, content in sorted(files, key=lambda x: x[1], reverse=True):
                rel = self._rel_path(path)
                lines.append("=" * 70)
                lines.append(f"FILE : {rel}")
                lines.append(f"SCORE: {score} pts")
                lines.append("=" * 70)
                lines.append(content)
                lines.append("")

        # ── FOOTER ──
        lines.append("=" * 70)
        lines.append(f"END OF FEATURE EXTRACT: '{self.raw_query}'")
        lines.append("=" * 70)

        return "\n".join(lines)

    def _detect_role(self, path: str) -> str:
        try:
            from core.intelligence.role_auditor import RoleAuditor
            from state.app_state import AppState
            return RoleAuditor.classify_role(path, "", AppState.selected_language or "general")
        except Exception:
            return "MODULE"

    def _rel_path(self, path: str) -> str:
        """Safe relative path starting from project root"""
        try:
            from state.app_state import AppState
            base = AppState.project_root or os.getcwd()
            return os.path.relpath(path, start=base)
        except Exception:
            return os.path.basename(path)

