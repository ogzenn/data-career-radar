"""
Shared helper functions - date parsing, logging, and text cleanup,
used by collectors, filters, and notifiers.
"""

import re
import html
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


# ---------- TEXT CLEANUP ----------

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def strip_html(text):
    """Removes HTML tags and decodes entities (e.g. &amp; -> &).
    Job description fields from several APIs come pre-formatted as HTML,
    which looks messy when posted as plain text in Discord/Telegram/email."""
    if not text:
        return ""
    text = html.unescape(text)
    text = _TAG_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def safe_join(value, separator=" "):
    """Some APIs return a field as a list (e.g. tags, industries) and others
    return it as a plain string. This normalizes either case to a single
    string so it can be safely stored in the database."""
    if value is None:
        return ""
    if isinstance(value, list):
        return separator.join(str(v) for v in value)
    return str(value)


# ---------- DATE PARSING ----------

def parse_date_safe(value):
    """Try several common date formats. Returns a timezone-aware datetime or None."""
    if not value:
        return None
    if isinstance(value, (int, float)):
        try:
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
