"""
Daily email digest - summarizes the day's collected jobs and emails them.
Uses Gmail SMTP with an App Password (not your real Gmail password).

Setup:
1. Enable 2-Step Verification on your Google account
2. Go to myaccount.google.com/apppasswords, generate an app password
3. Set SENDER_EMAIL, SENDER_APP_PASSWORD, RECEIVER_EMAIL as GitHub Secrets
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta

from config import SENDER_EMAIL, SENDER_APP_PASSWORD, RECEIVER_EMAIL
from database.db import get_connection
from utils import get_logger

logger = get_logger("digest.email")


def get_last_24h_jobs():
    conn = get_connection()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    rows = conn.execute(
        "SELECT * FROM jobs WHERE collected_at >= ? ORDER BY score DESC", (cutoff,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_email_html(jobs):
    if not jobs:
        return "<p>No new matching jobs were found in the last 24 hours.</p>"

    rows_html = ""
    for job in jobs:
        rows_html += f"""
        <tr>
            <td><a href="{job['url']}">{job['title']}</a></td>
            <td>{job.get('company', '')}</td>
            <td>{job.get('source', '')}</td>
            <td>{job.get('experience_level', '')}</td>
            <td>{job.get('score', 0)}</td>
        </tr>
        """

    return f"""
    <h2>Data Career Radar - Daily Digest</h2>
    <p>{len(jobs)} new matching jobs found in the last 24 hours:</p>
    <table border="1" cellpadding="6" cellspacing="0">
        <tr><th>Title</th><th>Company</th><th>Source</th><th>Level</th><th>Score</th></tr>
        {rows_html}
    </table>
    """


def send_daily_digest():
    if not (SENDER_EMAIL and SENDER_APP_PASSWORD and RECEIVER_EMAIL):
        logger.warning("Email not configured - skipping digest.")
        return False

    jobs = get_last_24h_jobs()
    html = build_email_html(jobs)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Data Career Radar Digest - {len(jobs)} new jobs"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        logger.info(f"Digest email sent with {len(jobs)} jobs.")
        return True
    except Exception as e:
        logger.error(f"Failed to send digest email: {e}")
        return False


if __name__ == "__main__":
    send_daily_digest()
