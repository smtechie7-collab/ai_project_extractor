import re
import os
from collections import defaultdict
from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(p: str) -> str:
    try:
        if AppState.project_root:
            return os.path.relpath(p, AppState.project_root).replace("\\", "/")
        return os.path.basename(p)
    except Exception:
        return os.path.basename(p)


def extract_constitution_digest(tree_root):
    """
    Extracts Project Constitution, Supreme Laws, Invariants, and Architecture Documentation
    for Kotlin / Android enterprise codebases (such as VERISTOCK PRO).
    """
    agents_md = None
    doc_files = []

    def walk(node):
        nonlocal agents_md
        if not node.is_dir:
            name_lower = node.name.lower()
            if name_lower == "agents.md":
                agents_md = node.path
            elif name_lower.endswith(".md") and any(sub in node.path.replace("\\", "/").lower() for sub in ["docs/", "constitution/", "standards/", "architecture/", "sync_hardening/"]):
                if not any(sub in name_lower for sub in ["output", "license", "changelog"]):
                    doc_files.append(node.path)

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    lines = []
    lines.append("=" * 70)
    lines.append("🏛️ KOTLIN ARCHITECTURAL CONSTITUTION & INVARIANTS DIGEST")
    lines.append("=" * 70)
    lines.append("")

    # 1. Parse AGENTS.md
    if agents_md:
        try:
            content = read_text_file(agents_md, max_size_kb=200)
            lines.append(f"## 1. ROOT CONSTITUTION: `{_get_rel_path(agents_md)}`")
            
            # Extract Project Overview
            proj_match = re.search(r'## 🚀 PROJECT OVERVIEW([\s\S]*?)(?=##|\Z)', content)
            if proj_match:
                lines.append("### Project Overview & Domain")
                lines.append(proj_match.group(1).strip())
                lines.append("")

            # Extract Tech Stack
            tech_match = re.search(r'## 🛠 TECH STACK([\s\S]*?)(?=##|\Z)', content)
            if tech_match:
                lines.append("### Tech Stack Specifications")
                lines.append(tech_match.group(1).strip())
                lines.append("")

            # Extract Precedence Order
            prec_match = re.search(r'## 📂 DOCUMENT PRECEDENCE ORDER([\s\S]*?)(?=##|\Z)', content)
            if prec_match:
                lines.append("### Document Precedence Hierarchy")
                # Show top 8 precedence rules
                prec_lines = [l for l in prec_match.group(1).strip().splitlines() if l.strip()][:10]
                lines.append("\n".join(prec_lines))
                lines.append("")

            # Extract Supreme Backend Constitution Rules
            const_match = re.search(r'## ⚖️ THE BACKEND CONSTITUTION([\s\S]*?)(?=##|\Z)', content)
            if const_match:
                lines.append("### ⚖️ Supreme Laws & Code Generation Invariants")
                lines.append(const_match.group(1).strip())
                lines.append("")

        except Exception as e:
            lines.append(f"Error reading AGENTS.md: {e}")
    else:
        lines.append("Note: No root AGENTS.md found in project tree.")

    # 2. Key Architecture & Constitution Documentation Index
    if doc_files:
        lines.append("")
        lines.append(f"## 2. PROJECT ARCHITECTURAL DOCUMENTATION REGISTRY ({len(doc_files)} docs)")
        lines.append("| Category | Spec File | Key Subject |")
        lines.append("| :--- | :--- | :--- |")

        for d_path in sorted(doc_files):
            rel_p = _get_rel_path(d_path)
            cat = "General Spec"
            lower_p = rel_p.lower()
            if "constitution" in lower_p: cat = "⚖️ Constitution"
            elif "sync" in lower_p: cat = "🔄 Cloud Sync"
            elif "standard" in lower_p: cat = "📏 Standards"
            elif "architecture" in lower_p: cat = "🏗️ Architecture"
            elif "hardware" in lower_p: cat = "🖨️ Hardware"
            elif "industry" in lower_p: cat = "🏢 Industry Ecosystem"

            # Quick inspect top title
            title = os.path.basename(d_path)
            try:
                snippet = read_text_file(d_path, max_size_kb=20)
                t_match = re.search(r'^#\s+(.+)$', snippet, re.MULTILINE)
                if t_match:
                    title = t_match.group(1).strip()[:50]
            except Exception:
                pass

            lines.append(f"| {cat} | `{rel_p}` | {title} |")

    lines.append("")
    lines.append("=" * 70)
    lines.append("MANDATORY INSTRUCTIONS FOR AI AUDITOR & DEVELOPERS:")
    lines.append("1. Zero 100x Inflation Rule: Always verify if monetary values in DB are in paise (Long)")
    lines.append("   vs rupees (BigDecimal). Never perform ad-hoc /100 or *100 operations.")
    lines.append("2. Multi-Tenant SQL Law (Article 4.4): NEVER use bind parameter tautology in SQLite queries")
    lines.append("   (e.g., 'OR :frontId = \"default_shop\"'). Ensure column-bound fallbacks.")
    lines.append("3. Single Sync Engine (Article 42): NEVER write directly to Firestore from UI or ViewModels.")
    lines.append("   All remote writes MUST route exclusively via SyncOutboxEntity and FirestoreSyncWorker.")
    lines.append("4. Feature Gating: Every feature screen must be guarded by FeatureGate / RoleGate.")
    lines.append("=" * 70)

    return "\n".join(lines)
