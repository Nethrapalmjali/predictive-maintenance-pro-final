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
