"""Himalayas collector - free public search API, no auth required."""

import requests
from config import REQUEST_HEADERS, MAX_PER_SOURCE
from utils import parse_date_safe, get_logger, strip_html, safe_join

logger = get_logger("collectors.himalayas")

SEARCH_TERMS = [
    "data analyst",
    "data scientist",
    "python developer",
    "sql developer",
]


def fetch_himalayas_jobs():
    jobs = []
    for term in SEARCH_TERMS:
        try:
            resp = requests.get(
                "https://himalayas.app/jobs/api/search",
                params={"q": term},
                headers=REQUEST_HEADERS,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"fetch failed for '{term}': {e}")
            continue

        for item in data.get("jobs", [])[:MAX_PER_SOURCE]:
            guid = item.get("guid") or item.get("id")
            company = item.get("companyName")
            if not company and isinstance(item.get("company"), dict):
                company = item["company"].get("name")
            jobs.append({
                "id": f"himalayas_{guid}",
                "title": item.get("title", "Untitled role"),
                "company": company or "Unknown company",
                "url": item.get("applicationLink") or item.get("url", ""),
                "description": strip_html((item.get("excerpt") or item.get("description") or "")[:800]),
                "tags": safe_join(item.get("categories")),
                "location": safe_join(item.get("locationRestrictions", "Remote")) or "Remote",
                "source": "Himalayas",
                "posted_at": parse_date_safe(item.get("publishedAt") or item.get("pubDate")),
            })
    return jobs
