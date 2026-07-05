"""Lever collector - free public API per company, no auth required.
Add company slugs in config.py -> LEVER_COMPANIES to pull their listings.

How to find a slug: on a company's careers page hosted at
jobs.lever.co/{slug}, the slug is that last URL segment.
"""

import requests
from config import REQUEST_HEADERS, LEVER_COMPANIES
from utils import parse_date_safe, get_logger

logger = get_logger("collectors.lever")


def fetch_lever_jobs():
    jobs = []
    for slug in LEVER_COMPANIES:
        url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
        try:
            resp = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"fetch failed for company '{slug}': {e}")
            continue

        for item in data:
            categories = item.get("categories", {}) or {}
            jobs.append({
                "id": f"lever_{item.get('id')}",
                "title": item.get("text", "Untitled role"),
                "company": slug,
                "url": item.get("hostedUrl") or item.get("applyUrl", ""),
                "description": (item.get("descriptionPlain") or item.get("description") or "")[:800],
                "tags": categories.get("team", ""),
                "location": categories.get("location", "Unknown"),
                "source": "Lever",
                "posted_at": parse_date_safe(item.get("createdAt")),
            })
    return jobs
