"""WeWorkRemotely collector - parses public RSS feeds, no auth required."""

import feedparser
from utils import parse_date_safe, get_logger

logger = get_logger("collectors.weworkremotely")

FEEDS = [
    "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-data-jobs.rss",
]


def fetch_weworkremotely_jobs():
    jobs = []
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logger.error(f"fetch failed for {feed_url}: {e}")
            continue

        for entry in feed.entries:
            job_id = entry.get("id") or entry.get("link")
            jobs.append({
                "id": f"wwr_{job_id}",
                "title": entry.get("title", "Untitled role"),
                "company": "",  # WWR titles are usually "Company: Role"
                "url": entry.get("link", ""),
                "description": (entry.get("summary") or "")[:800],
                "tags": "",
                "location": "Remote",
                "source": "WeWorkRemotely",
                "posted_at": parse_date_safe(entry.get("published")),
            })
    return jobs
