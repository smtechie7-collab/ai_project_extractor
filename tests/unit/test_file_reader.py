"""
tests/unit/test_file_reader.py
==============================
Unit tests for safe file reading and caching.
"""

from __future__ import annotations

from pathlib import Path

from core.utils.file_reader import (
    clear_cache,
    is_binary_file,
    read_text_file,
)


def test_read_text_file_basic(tmp_path: Path):
    sample = tmp_path / "hello.txt"
    sample.write_text("Hello, World!\nSecond line", encoding="utf-8")

    content = read_text_file(str(sample))
    assert "Hello, World!" in content
    assert "Second line" in content


def test_read_text_file_caching(tmp_path: Path):
    clear_cache()
    sample = tmp_path / "cached.txt"
    sample.write_text("Original content", encoding="utf-8")

    first_read = read_text_file(str(sample))
    assert first_read == "Original content"

    # Modify file without changing mtime/stat or inspect cache
    cached_read = read_text_file(str(sample))
    assert cached_read == "Original content"


def test_read_text_file_size_limit(tmp_path: Path):
    big_file = tmp_path / "large.txt"
    # Write 600 KB of text
    big_file.write_text("A" * (600 * 1024), encoding="utf-8")

    result = read_text_file(str(big_file), max_size_kb=500)
    assert "[FILE TOO LARGE:" in result


def test_is_binary_file(tmp_path: Path):
    text_file = tmp_path / "clean.txt"
    text_file.write_text("Clean text without null bytes", encoding="utf-8")
    assert not is_binary_file(str(text_file))

    bin_file = tmp_path / "binary.dat"
    bin_file.write_bytes(b"hello\x00world")
    assert is_binary_file(str(bin_file))


def test_nonexistent_file():
    result = read_text_file("nonexistent_path_that_does_not_exist.txt")
    assert result == "[FILE NOT FOUND]"
