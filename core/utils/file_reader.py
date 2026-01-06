import os


def is_binary_file(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except Exception:
        return True


def read_text_file(path: str, max_size_kb: int = 500) -> str:
    """
    Safely reads text files.
    - Skips binary files
    - Limits file size
    - Handles encoding
    """

    if not os.path.exists(path):
        return "[FILE NOT FOUND]"

    if is_binary_file(path):
        return "[BINARY FILE SKIPPED]"

    try:
        size_kb = os.path.getsize(path) / 1024
        if size_kb > max_size_kb:
            return f"[FILE TOO LARGE: {int(size_kb)} KB — SKIPPED]"
    except Exception:
        pass

    for encoding in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=encoding, errors="ignore") as f:
                return f.read()
        except Exception:
            continue

    return "[UNABLE TO READ FILE]"
