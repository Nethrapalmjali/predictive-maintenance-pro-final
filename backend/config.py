"""Small configuration helpers that do not depend on the rest of the app."""
from typing import List, Optional


def parse_cors_origins(raw: Optional[str]) -> List[str]:
    """Turn a comma-separated CORS_ORIGINS string into a clean list.

    Whitespace around entries and trailing slashes are removed (browsers send
    the Origin header without a trailing slash) and empty entries are dropped.
    An unset or blank value falls back to ``["*"]`` (allow all origins).
    """
    origins = [o.strip().rstrip("/") for o in (raw or "").split(",")]
    origins = [o for o in origins if o]
    return origins or ["*"]


def parse_port(raw: Optional[str], default: int = 8000) -> int:
    """Return a valid TCP port from the PORT env value, or ``default``.

    Blank, non-numeric or out-of-range (not 1-65535) values fall back to the
    default instead of crashing the server at startup.
    """
    try:
        port = int((raw or "").strip())
    except ValueError:
        return default
    return port if 1 <= port <= 65535 else default
