"""
core/logging_setup.py
=====================
Centralized logging configuration for AI Context Extractor.
Configures console (stderr) output and rotating log file.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_INITIALIZED = False
_LOG_DIR = Path.home() / ".aice" / "logs"
_LOG_FILE = _LOG_DIR / "aice.log"


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | str | None = None,
) -> None:
    """Configures root logger with stderr stream and rotating file handler."""
    global _INITIALIZED
    if _INITIALIZED:
        return

    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler (stderr)
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(formatter)
    console.setLevel(level)
    root.addHandler(console)

    # File Handler
    target_file = Path(log_file) if log_file else _LOG_FILE
    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            target_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root.addHandler(file_handler)
    except Exception as exc:  # noqa: BLE001 - File logging fallback must not crash app
        console.warning(f"Could not initialize file logger at {target_file}: {exc}")

    _INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance with the given name."""
    if not _INITIALIZED:
        setup_logging()
    return logging.getLogger(name)
