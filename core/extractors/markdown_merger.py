# -*- coding: utf-8 -*-
"""
core/extractors/markdown_merger.py
===================================
Merges multiple Markdown (.md / .markdown) files into a unified, AI-ready
"Full Source" document.

Features:
- Scans directories or AST trees for markdown files.
- Prioritizes root-level documentation (README, AGENTS, ARCHITECTURE, etc.).
- Computes comprehensive metadata: total lines, token estimates, file sizes.
- Generates a Table of Contents (TOC) with file stats.
- Encapsulates each file with clear, unambiguous delimiters so LLMs (ChatGPT,
  Claude, Gemini) can parse boundaries accurately.
"""

import os
import re
from datetime import datetime
from core.utils.file_reader import read_text_file

SKIP_DIRS = {
    ".git", ".github", ".idea", ".vscode", "node_modules", "venv", ".venv",
    "env", "__pycache__", "build", "dist", ".gradle", "bin", "obj", ".vs"
}

PRIORITY_ROOT_DOCS = [
    "readme.md", "readme.markdown",
    "agents.md", "agents.markdown",
    "architecture.md", "constitution.md",
    "summary.md", "overview.md",
    "requirements.md", "specs.md", "specification.md",
    "contributing.md", "license.md", "changelog.md"
]


def scan_markdown_files(folder_path: str, recursive: bool = True) -> list[str]:
    """
    Scans a folder and returns absolute paths of all .md and .markdown files.
    """
    md_files = []
    if not folder_path or not os.path.isdir(folder_path):
        return md_files

    if not recursive:
        try:
            for item in os.listdir(folder_path):
                fp = os.path.join(folder_path, item)
                if os.path.isfile(fp) and item.lower().endswith((".md", ".markdown")):
                    md_files.append(os.path.abspath(fp))
        except Exception as e:
            print(f"[MarkdownMerger] Error listing folder: {e}")
        return md_files

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for file in files:
            if file.lower().endswith((".md", ".markdown")):
                md_files.append(os.path.abspath(os.path.join(root, file)))

    return md_files


def collect_markdown_from_tree(tree_root) -> list[str]:
    """
    Extracts all markdown file paths from a project scan AST Node tree.
    """
    md_files = []

    def walk(node):
        if not node:
            return
        if not node.is_dir and node.name.lower().endswith((".md", ".markdown")):
            md_files.append(os.path.abspath(node.path))
        if hasattr(node, "children"):
            for child in node.children:
                walk(child)

    walk(tree_root)
    return md_files


def _sort_markdown_files(file_paths: list[str], base_root: str = None) -> list[str]:
    """
    Sorts markdown files logically:
    1. Root priority files (README, AGENTS, ARCHITECTURE, etc.)
    2. Other root-level markdown files
    3. Nested files ordered by relative directory and name
    """
    def sort_key(path):
        rel = os.path.relpath(path, start=base_root) if base_root else os.path.basename(path)
        norm_rel = rel.replace("\\", "/").lower()
        parts = norm_rel.split("/")
        filename = parts[-1]
        depth = len(parts) - 1

        priority = 100
        if depth == 0:
            if filename in PRIORITY_ROOT_DOCS:
                priority = PRIORITY_ROOT_DOCS.index(filename)
            else:
                priority = 50
        else:
            priority = 100 + depth

        return (priority, norm_rel)

    return sorted(file_paths, key=sort_key)


def merge_markdown_files(file_paths: list[str], base_root: str = None) -> str:
    """
    Merges multiple markdown files into a single, AI-ready Full Source document.

    Args:
        file_paths: List of absolute or relative file paths to markdown files.
        base_root: Optional root directory used to generate clean relative paths.

    Returns:
        Consolidated markdown text formatted for AI copy-pasting.
    """
    if not file_paths:
        return "# No Markdown Files Selected\n\nPlease select one or more .md files to merge."

    # Remove duplicates while preserving absolute paths
    clean_paths = []
    seen = set()
    for p in file_paths:
        abs_p = os.path.abspath(p)
        if abs_p not in seen and os.path.exists(abs_p):
            seen.add(abs_p)
            clean_paths.append(abs_p)

    if not clean_paths:
        return "# Error: None of the specified markdown files exist on disk."

    # Determine base root if not provided
    if not base_root:
        try:
            base_root = os.path.commonpath(clean_paths)
            if os.path.isfile(base_root):
                base_root = os.path.dirname(base_root)
        except Exception:
            base_root = os.path.dirname(clean_paths[0])

    # Sort files
    sorted_paths = _sort_markdown_files(clean_paths, base_root)

    # Read and inspect files
    file_records = []
    total_lines = 0
    total_chars = 0

    for path in sorted_paths:
        content = read_text_file(path, max_size_kb=2048)
        lines_count = content.count("\n") + (1 if content else 0)
        chars_count = len(content)
        size_kb = os.path.getsize(path) / 1024 if os.path.exists(path) else 0.0

        rel_path = os.path.relpath(path, start=base_root).replace("\\", "/")
        file_records.append({
            "abs_path": path,
            "rel_path": rel_path,
            "content": content,
            "lines": lines_count,
            "chars": chars_count,
            "size_kb": size_kb
        })

        total_lines += lines_count
        total_chars += chars_count

    estimated_tokens = int(total_chars / 3.8)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_count = len(file_records)

    # Build Output
    out = []
    out.append("=" * 80)
    out.append("📚 CONSOLIDATED MARKDOWN FULL SOURCE (AI CONTEXT READY)")
    out.append("=" * 80)
    out.append(f"Generated At   : {now_str}")
    out.append(f"Total Files    : {file_count}")
    out.append(f"Total Lines    : {total_lines:,}")
    out.append(f"Approx Tokens  : ~{estimated_tokens:,}")
    if base_root:
        out.append(f"Base Directory : {base_root}")
    out.append("=" * 80)
    out.append("")

    out.append("### 🤖 AI INSTRUCTIONS")
    out.append(
        "- The following document compiles multiple project Markdown (.md) files into a single source.\n"
        "- Each file is delimited by explicit '--- START OF FILE ---' and '--- END OF FILE ---' headers.\n"
        "- Use the Table of Contents below to navigate between different specifications and documents.\n"
        "- Do not alter original documentation meanings when referencing or generating code."
    )
    out.append("")

    out.append("## 📑 TABLE OF CONTENTS / FILE INDEX")
    out.append("| # | File Path | Lines | Size |")
    out.append("|---|-----------|-------|------|")
    for idx, rec in enumerate(file_records, 1):
        out.append(f"| {idx} | `{rec['rel_path']}` | {rec['lines']:,} | {rec['size_kb']:.1f} KB |")
    out.append("")
    out.append("---")
    out.append("")

    # Append each file content
    for idx, rec in enumerate(file_records, 1):
        out.append("=" * 80)
        out.append(f"📄 [{idx}/{file_count}] FILE: {rec['rel_path']}")
        out.append(f"Lines: {rec['lines']:,} | Size: {rec['size_kb']:.1f} KB | Full Path: {rec['abs_path']}")
        out.append("=" * 80)
        out.append(f"--- START OF FILE: `{rec['rel_path']}` ---")
        out.append("")
        out.append(rec["content"].rstrip())
        out.append("")
        out.append(f"--- END OF FILE: `{rec['rel_path']}` ---")
        out.append("\n")

    return "\n".join(out)
