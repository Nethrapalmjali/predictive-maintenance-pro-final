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


def test_parse_port():
    from config import parse_port

    assert parse_port("9000") == 9000
    assert parse_port(" 8080 ") == 8080
    assert parse_port(None) == 8000
    assert parse_port("abc") == 8000
    assert parse_port("0") == 8000
    assert parse_port("70000") == 8000
    assert parse_port("abc", default=5000) == 5000
