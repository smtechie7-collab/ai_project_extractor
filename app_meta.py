"""
app_meta.py
===========
Central application metadata, versioning and support configuration.

Single source of truth for anything shown in the UI (titles, version,
sponsor/support links, asset paths). Do NOT hardcode contact details or
asset blobs elsewhere in the codebase.
"""

from __future__ import annotations

import os
from pathlib import Path

# ── Identity ──
APP_NAME = "AI Context Extractor"
APP_TITLE = "AI Context Extractor Pro"
APP_VERSION = "2.4.0"
APP_TAGLINE = "Production Grade • Multi-Language Enterprise Suite"
APP_DESCRIPTION = "Bridge the gap between your local codebase and AI coding assistants."

# ── Support / sponsor configuration ──
# Overridable at runtime via environment variables so no personal data needs to
# be baked into the source tree for a public/open release.
SUPPORT_EMAIL = os.environ.get("AICE_SUPPORT_EMAIL", "")
SPONSOR_URL = os.environ.get(
    "AICE_SPONSOR_URL",
    "https://github.com/smtechie7-collab/ai_project_extractor",
)
# Personal phone number intentionally NOT shipped in the codebase or UI.

# ── Filesystem helpers ──
APP_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = APP_ROOT / "assets"
SPONSOR_QR = ASSETS_DIR / "sponsor_qr.png"


def assets_dir() -> Path:
    """Absolute path to the bundled assets directory."""
    return ASSETS_DIR


def sponsor_qr_path() -> Path:
    """Absolute path to the sponsor QR image (may not exist)."""
    return SPONSOR_QR
