"""Jobicy collector - free public API, no auth required."""

import requests
from config import REQUEST_HEADERS
from utils import parse_date_safe, get_logger

logger = get_logger("collectors.jobicy")

QUERIES = [
    "https://jobicy.com/api/v2/remote-jobs?count=50&industry=data-science",
    "https://jobicy.com/api/v2/remote-jobs?count=50&industry=dev",
]


def fetch_jobicy_jobs():
    jobs = []
    for feed_url in QUERIES:
        try:
            resp = requests.get(feed_url, headers=REQUEST_HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"fetch failed for {feed_url}: {e}")
            continue

        for item in data.get("jobs", []):
            jobs.append({
                "id": f"jobicy_{item.get('id')}",
                "title": item.get("jobTitle", "Untitled role"),
                "company": item.get("companyName", "Unknown company"),
                "url": item.get("url", ""),
                "description": (item.get("jobExcerpt") or "")[:800],
                "tags": item.get("jobIndustry", ""),
                "location": item.get("jobGeo", "Remote"),
                "source": "Jobicy",
                "posted_at": parse_date_safe(item.get("pubDate")),
            })
    return jobs
