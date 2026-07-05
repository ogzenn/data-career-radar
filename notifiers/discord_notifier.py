"""Discord notifier - posts job alerts via a Discord webhook."""

import time
import requests
from config import DISCORD_WEBHOOK_URL
from utils import get_logger

logger = get_logger("notifiers.discord")


def post_to_discord(job):
    if not DISCORD_WEBHOOK_URL:
        logger.warning("No DISCORD_WEBHOOK_URL set - skipping Discord post.")
        return False

    embed = {
        "title": job["title"][:256],
        "url": job["url"],
        "description": (job.get("description") or "No description provided.")[:400],
        "color": 5814783,
        "fields": [
            {"name": "Company", "value": job.get("company") or "See listing", "inline": True},
            {"name": "Location", "value": job.get("location") or "Unknown", "inline": True},
            {"name": "Source", "value": job.get("source", "Unknown"), "inline": True},
            {"name": "Level", "value": job.get("experience_level", "Unclear"), "inline": True},
            {"name": "Score", "value": str(job.get("score", 0)), "inline": True},
        ],
        "footer": {"text": "Data Career Radar 🚨"},
    }

    payload = {"embeds": [embed]}

    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
        if resp.status_code >= 300:
            logger.error(f"Discord post failed ({resp.status_code}): {resp.text}")
            return False
        logger.info(f"Posted to Discord: {job['title']}")
        return True
    except Exception as e:
        logger.error(f"Discord post error: {e}")
        return False
    finally:
        time.sleep(1)  # be nice to Discord rate limits
