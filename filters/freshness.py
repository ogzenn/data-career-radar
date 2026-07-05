"""Freshness filter - rejects jobs older than MAX_AGE_DAYS when a posted date is known."""

from datetime import datetime, timezone, timedelta
from config import MAX_AGE_DAYS


def is_recent_enough(job):
    """If we can't determine the date, we keep the job (better to show than hide).
    If we CAN determine it, it must be within MAX_AGE_DAYS."""
    posted = job.get("posted_at")
    if posted is None:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    if posted.tzinfo is None:
        posted = posted.replace(tzinfo=timezone.utc)
    return posted >= cutoff
