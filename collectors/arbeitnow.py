"""Arbeitnow collector - aggregates jobs from Greenhouse, SmartRecruiters and others.
Free public API, no auth required. EU/remote heavy."""

import requests
from config import REQUEST_HEADERS, MAX_PER_SOURCE
from utils import parse_date_safe, get_logger, strip_html

logger = get_logger("collectors.arbeitnow")

API_URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_arbeitnow_jobs():
    try:
        resp = requests.get(API_URL, headers=REQUEST_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"fetch failed: {e}")
        return []

    jobs = []
    for item in data.get("data", []):
        slug = item.get("slug", "")
        jobs.append({
            "id": f"arbeitnow_{slug}",
            "title": item.get("title", "Untitled role"),
            "company": item.get("company_name", "Unknown company"),
            "url": item.get("url", ""),
            "description": strip_html((item.get("description") or "")[:800]),
            "tags": " ".join(item.get("tags", [])),
            "location": item.get("location", "Remote"),
            "source": "Arbeitnow",
            "posted_at": parse_date_safe(item.get("created_at")),
        })
    return jobs[:MAX_PER_SOURCE * 5]
