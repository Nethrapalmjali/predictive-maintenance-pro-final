import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import parse_cors_origins  # noqa: E402


def test_default_is_wildcard():
    assert parse_cors_origins(None) == ["*"]
    assert parse_cors_origins("") == ["*"]
    assert parse_cors_origins(" , ") == ["*"]


def test_strips_whitespace_and_trailing_slash():
    raw = "http://localhost:3000/, https://app.example.com ,"
    assert parse_cors_origins(raw) == [
        "http://localhost:3000",
        "https://app.example.com",
    ]
