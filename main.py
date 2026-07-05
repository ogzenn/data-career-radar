"""
Data Career Radar - Main orchestrator.

Pipeline: collect -> dedupe -> score -> filter (freshness + score threshold)
-> store in database -> notify (Discord + Telegram for anything new).

Run this every 30 minutes via GitHub Actions (see .github/workflows/job-alert.yml).
"""

from collectors.remoteok import fetch_remoteok_jobs
from collectors.weworkremotely import fetch_weworkremotely_jobs
from collectors.arbeitnow import fetch_arbeitnow_jobs
from collectors.jobicy import fetch_jobicy_jobs
from collectors.himalayas import fetch_himalayas_jobs
from collectors.greenhouse import fetch_greenhouse_jobs
from collectors.lever import fetch_lever_jobs

from filters.duplicate import dedupe_across_sources
from filters.freshness import is_recent_enough
from filters.scoring import score_job, passes_score_threshold, classify_experience_level

from database.db import init_db, is_seen, insert_job, mark_posted
from notifiers.discord_notifier import post_to_discord
from notifiers.telegram_notifier import post_to_telegram

from utils import get_logger

logger = get_logger("main")

COLLECTORS = [
    fetch_remoteok_jobs,
    fetch_weworkremotely_jobs,
    fetch_arbeitnow_jobs,
    fetch_jobicy_jobs,
    fetch_himalayas_jobs,
    fetch_greenhouse_jobs,
    fetch_lever_jobs,
]


def collect_all_jobs():
    all_jobs = []
    for collector in COLLECTORS:
        try:
            jobs = collector()
            logger.info(f"{collector.__module__}: fetched {len(jobs)} jobs")
            all_jobs.extend(jobs)
        except Exception as e:
            logger.error(f"{collector.__module__} failed entirely: {e}")
    return all_jobs


def main():
    init_db()

    raw_jobs = collect_all_jobs()
    logger.info(f"Fetched {len(raw_jobs)} total jobs from all sources.")

    deduped = dedupe_across_sources(raw_jobs)
    logger.info(f"{len(deduped)} jobs after cross-source dedup.")

    new_jobs = 0
    posted_jobs = 0
    rejected_stale = 0
    rejected_score = 0
    rejected_duplicate_db = 0

    for job in deduped:
        if is_seen(job["id"]):
            rejected_duplicate_db += 1
            continue

        if not is_recent_enough(job):
            rejected_stale += 1
            continue

        job["score"] = score_job(job)
        job["experience_level"] = classify_experience_level(job)

        if not passes_score_threshold(job):
            rejected_score += 1
            continue

        # Store every job that passes filters, whether or not the alert send succeeds -
        # this keeps the database complete for the dashboard/analytics.
        insert_job(job)
        new_jobs += 1

        discord_ok = post_to_discord(job)
        if discord_ok:
            mark_posted(job["id"], "discord")

        telegram_ok = post_to_telegram(job)
        if telegram_ok:
            mark_posted(job["id"], "telegram")

        if discord_ok or telegram_ok:
            posted_jobs += 1

    logger.info(
        f"Summary: {new_jobs} new jobs stored, {posted_jobs} alerts sent | "
        f"rejected: {rejected_stale} stale, {rejected_score} low-score, "
        f"{rejected_duplicate_db} already-seen"
    )


if __name__ == "__main__":
    main()
