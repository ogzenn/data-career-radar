"""
SQLite database layer. Replaces the old seen_jobs.json approach with
a real database that also enables analytics for the dashboard.
"""

import sqlite3
import os
from datetime import datetime, timezone
from config import DATABASE_PATH
from utils import get_logger, to_iso_string, safe_join

logger = get_logger("database.db")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    logger.info("Database initialized.")


def is_seen(job_id):
    conn = get_connection()
    cur = conn.execute("SELECT 1 FROM jobs WHERE id = ?", (job_id,))
    result = cur.fetchone() is not None
    conn.close()
    return result


def insert_job(job):
    conn = get_connection()
    conn.execute(
        """
        INSERT OR IGNORE INTO jobs
        (id, title, company, description, tags, location, source, url,
         posted_at, collected_at, experience_level, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job["id"],
            safe_join(job["title"]),
            safe_join(job.get("company", "")),
            safe_join(job.get("description", "")),
            safe_join(job.get("tags", "")),
            safe_join(job.get("location", "")),
            safe_join(job.get("source", "")),
            safe_join(job.get("url", "")),
            to_iso_string(job.get("posted_at")),
            datetime.now(timezone.utc).isoformat(),
            safe_join(job.get("experience_level", "Unclear")),
            job.get("score", 0),
        ),
    )
    conn.commit()
    conn.close()


def mark_posted(job_id, channel="discord"):
    column = "posted_to_discord" if channel == "discord" else "posted_to_telegram"
    conn = get_connection()
    conn.execute(f"UPDATE jobs SET {column} = 1 WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) as c FROM jobs").fetchone()["c"]
    by_source = conn.execute(
        "SELECT source, COUNT(*) as c FROM jobs GROUP BY source ORDER BY c DESC"
    ).fetchall()
    by_experience = conn.execute(
        "SELECT experience_level, COUNT(*) as c FROM jobs GROUP BY experience_level ORDER BY c DESC"
    ).fetchall()
    conn.close()
    return {
        "total": total,
        "by_source": [dict(r) for r in by_source],
        "by_experience": [dict(r) for r in by_experience],
    }


def get_recent_jobs(limit=100):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM jobs ORDER BY collected_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
