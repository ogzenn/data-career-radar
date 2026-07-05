"""
Shared helper functions - mainly date parsing, used by collectors and filters.
"""

import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# ---------- LOGGING ----------

def get_logger(name):
    """Standard logger config used across all modules."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# ---------- DATE PARSING ----------

def parse_date_safe(value):
    """Try several common date formats. Returns a timezone-aware datetime or None."""
    if not value:
        return None
    if isinstance(value, (int, float)):
        try:
            # Handle both seconds and milliseconds epoch timestamps
            if value > 10_000_000_000:  # looks like milliseconds
                value = value / 1000
            return datetime.fromtimestamp(value, tz=timezone.utc)
        except Exception:
            return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            pass
        try:
            return parsedate_to_datetime(value)
        except Exception:
            pass
    return None


def to_iso_string(dt):
    """Convert a datetime to an ISO string for DB storage. Returns None if dt is None."""
    if dt is None:
        return None
    return dt.isoformat()
