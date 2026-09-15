from __future__ import annotations

import os

_CONTENT_CACHE: dict[tuple[str, float, int], str] = {}
_MAX_CACHE_ENTRIES = 2048


def clear_cache() -> None:
    """Clears the in-memory file content cache."""
    _CONTENT_CACHE.clear()


def is_binary_file(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except OSError:
        return True


def read_text_file(path: str, max_size_kb: int = 500) -> str:
    """
    Safely reads text files with mtime+size caching:
    - Skips binary files
    - Limits file size
    - Handles multiple encodings (utf-8-sig, utf-8, latin-1)
    - Returns cached string if mtime and size match
    """
    if not os.path.exists(path):
        return "[FILE NOT FOUND]"

    if is_binary_file(path):
        return "[BINARY FILE SKIPPED]"

    try:
        stat = os.stat(path)
        size_kb = stat.st_size / 1024
        if size_kb > max_size_kb:
            return f"[FILE TOO LARGE: {int(size_kb)} KB — SKIPPED]"

        cache_key = (os.path.normpath(path), stat.st_mtime, stat.st_size)
        if cache_key in _CONTENT_CACHE:
            return _CONTENT_CACHE[cache_key]
    except OSError:
        return "[UNABLE TO READ FILE]"

    content: str | None = None
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, encoding=encoding, errors="ignore") as f:
                content = f.read()
                break
        except OSError:
            continue

    if content is None:
        return "[UNABLE TO READ FILE]"

    if len(_CONTENT_CACHE) >= _MAX_CACHE_ENTRIES:
        try:
            _CONTENT_CACHE.pop(next(iter(_CONTENT_CACHE)))
        except KeyError:
            pass

    _CONTENT_CACHE[cache_key] = content
    return content
