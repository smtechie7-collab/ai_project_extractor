"""
tests/unit/test_sanitizer.py
============================
Unit tests for security sanitizer secret redaction.
"""

from __future__ import annotations

from core.security.sanitizer.SecuritySanitizer import SecuritySanitizer


def test_sanitize_aws_key():
    raw = 'aws_key = "AKIA1234567890ABCDEF"'
    sanitized = SecuritySanitizer.sanitize(raw)
    assert "AKIA1234567890ABCDEF" not in sanitized
    assert "[AWS_KEY_REDACTED]" in sanitized


def test_sanitize_google_key():
    key = "AIzaSyDa-1234567890abcdefghijklmnopqrst"
    raw = f'gcp_key = "{key}"'
    sanitized = SecuritySanitizer.sanitize(raw)
    assert key not in sanitized
    assert "[GOOGLE_KEY_REDACTED]" in sanitized


def test_sanitize_generic_secret():
    raw = 'password = "supersecretpassword123"'
    sanitized = SecuritySanitizer.sanitize(raw)
    assert "supersecretpassword123" not in sanitized
    assert "[SECRET_REDACTED]" in sanitized


def test_sanitize_email():
    raw = "contact me at developer@company.com please"
    sanitized = SecuritySanitizer.sanitize(raw)
    assert "developer@company.com" not in sanitized
    assert "[EMAIL_REDACTED]" in sanitized


def test_sanitize_preserves_clean_code():
    code = 'def calculate_sum(a, b):\n    return a + b\n'
    sanitized = SecuritySanitizer.sanitize(code)
    assert sanitized == code
