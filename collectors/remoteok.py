"""RemoteOK collector - free public API, no auth required."""

import requests
from config import REQUEST_HEADERS, MAX_PER_SOURCE
from utils import parse_date_safe, get_logger, strip_html

logger = get_logger("collectors.remoteok")

API_URL = "https://remoteok.com/api"


def fetch_remoteok_jobs():
    try:
        resp = requests.get(API_URL, headers=REQUEST_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"fetch failed: {e}")
        return []

    jobs = []
    for item in data:
        if not isinstance(item, dict) or "id" not in item:
            continue
        jobs.append({
            "id": f"remoteok_{item.get('id')}",
            "title": item.get("position", "Untitled role"),
            "company": item.get("company", "Unknown company"),
            "url": item.get("url") or f"https://remoteok.com/remote-jobs/{item.get('id')}",
            "description": strip_html((item.get("description") or "")[:800]),
            "tags": " ".join(item.get("tags", [])),
            "location": item.get("location", "Remote"),
            "source": "RemoteOK",
            "posted_at": parse_date_safe(item.get("date")),
        })
    return jobs[:MAX_PER_SOURCE * 5]
