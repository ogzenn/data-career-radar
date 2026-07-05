"""Greenhouse collector - free public API per company, no auth required.
Add company board tokens in config.py -> GREENHOUSE_BOARDS to pull their listings.

How to find a token: on a company's careers page hosted at
boards.greenhouse.io/{token}, the token is that last URL segment.
"""

import requests
from config import REQUEST_HEADERS, GREENHOUSE_BOARDS
from utils import parse_date_safe, get_logger

logger = get_logger("collectors.greenhouse")


def fetch_greenhouse_jobs():
    jobs = []
    for token in GREENHOUSE_BOARDS:
        url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
        try:
            resp = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"fetch failed for board '{token}': {e}")
            continue

        for item in data.get("jobs", []):
            jobs.append({
                "id": f"greenhouse_{item.get('id')}",
                "title": item.get("title", "Untitled role"),
                "company": token,
                "url": item.get("absolute_url", ""),
                "description": (item.get("content") or "")[:800],
                "tags": "",
                "location": (item.get("location") or {}).get("name", "Unknown"),
                "source": "Greenhouse",
                "posted_at": parse_date_safe(item.get("updated_at")),
            })
    return jobs
