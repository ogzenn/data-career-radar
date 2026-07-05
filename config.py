"""
Central configuration for Data Career Radar.
Change keywords, thresholds, and source settings here - nothing else
should need to change when you tweak filtering behavior.
"""

import os

# ---------- SECRETS (set these as GitHub Secrets / environment variables) ----------

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.environ.get("SENDER_APP_PASSWORD")  # Gmail App Password, not your real password
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

# ---------- KEYWORDS ----------

POSITIVE_KEYWORDS = {
    "data analyst": 3,
    "data analytics": 3,
    "data scientist": 3,
    "data science": 3,
    "business analyst": 2,
    "analytics engineer": 2,
    "bi analyst": 2,
    "power bi": 2,
    "tableau": 2,
    "sql analyst": 2,
    "reporting analyst": 2,
    "python": 1,
    "sql": 1,
    "excel": 1,
    "internship": 2,
    "intern": 1,
    "graduate": 1,
    "entry level": 2,
    "junior": 2,
    "fresher": 2,
}

NEGATIVE_KEYWORDS = {
    "senior": -5,
    "sr.": -5,
    "principal": -6,
    "staff ": -5,
    "lead ": -4,
    "manager": -5,
    "director": -6,
    "head of": -6,
    "vp ": -6,
    "vice president": -6,
    "architect": -4,
    "5+ years": -4,
    "6+ years": -5,
    "7+ years": -5,
    "8+ years": -6,
    "9+ years": -6,
    "10+ years": -6,
    "5-10 years": -4,
    "minimum 5 years": -4,
    "at least 5 years": -4,
}

# Jobs need at least this total score to be posted.
MIN_SCORE_TO_POST = 3

# ---------- FRESHNESS ----------

MAX_AGE_DAYS = 7  # jobs older than this are ignored, even if they match keywords

# ---------- SOURCE LIMITS ----------

MAX_PER_SOURCE = 10  # cap per individual source/query to avoid one source dominating

# ---------- GREENHOUSE / LEVER BOARDS ----------
# Add company board tokens here to pull their listings.
# Greenhouse: find the token in the company's careers URL, e.g.
#   boards.greenhouse.io/{token}  ->  add "{token}" below
# Lever: careers URL is jobs.lever.co/{token}  ->  add "{token}" below
# NOTE: JPMorgan, Barclays, HSBC, and Amex use Workday, not Greenhouse/Lever,
# so they can't be added this way - see README for why.

GREENHOUSE_BOARDS = [
    # "example-company-token",
]

LEVER_COMPANIES = [
    # "example-company-token",
]

# ---------- DATABASE ----------

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "jobs.db")

# ---------- REQUEST HEADERS ----------

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataCareerRadar/1.0; +https://github.com/)"
}
