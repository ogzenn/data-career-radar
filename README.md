# 📊 Data Career Radar

A job intelligence platform that automatically discovers, scores, and alerts on
fresh Data Analyst / Data Science / Business Analyst friendly job postings —
filtering out senior/experienced roles and stale listings, so you only see
what's actually relevant and recent.

Built entirely on free tools: no paid APIs, no paid hosting.

## Features

- ✅ **Multi-source collection**: RemoteOK, WeWorkRemotely, Arbeitnow, Jobicy, Himalayas, Greenhouse, Lever
- ✅ **Freshness filtering**: ignores listings older than 7 days
- ✅ **Experience-level scoring**: weighted keyword scoring favors fresher/entry-level roles, penalizes senior/lead/manager postings
- ✅ **Cross-source deduplication**: same job posted on 2+ boards is only shown once
- ✅ **SQLite database**: full history of every job seen, enabling analytics
- ✅ **Discord alerts**: rich embeds with company, location, score, experience level
- ✅ **Telegram alerts**: same info, sent to a Telegram group/channel
- ✅ **Daily email digest**: summary of the last 24 hours, sent automatically
- ✅ **Analytics dashboard**: Streamlit app with charts, search, and filtering
- ✅ **Fully automated**: runs every 30 minutes via GitHub Actions, completely free

## Architecture

```
data-career-radar/
├── collectors/          # One file per job source, all return the same job format
│   ├── remoteok.py
│   ├── weworkremotely.py
│   ├── arbeitnow.py
│   ├── jobicy.py
│   ├── himalayas.py
│   ├── greenhouse.py    # configurable by company board token
│   └── lever.py         # configurable by company slug
├── filters/
│   ├── freshness.py      # rejects stale listings
│   ├── scoring.py        # weighted keyword scoring + experience classification
│   └── duplicate.py      # cross-source dedup
├── database/
│   ├── schema.sql
│   └── db.py             # SQLite access layer
├── notifiers/
│   ├── discord_notifier.py
│   └── telegram_notifier.py
├── digest/
│   └── email_digest.py   # daily summary email
├── dashboard/
│   └── app.py             # Streamlit analytics dashboard
├── .github/workflows/
│   ├── job-alert.yml      # runs main.py every 30 min
│   └── daily-digest.yml   # runs the email digest once a day
├── config.py               # all settings live here
├── utils.py                # shared helpers (date parsing, logging)
├── main.py                 # orchestrates the full pipeline
└── requirements.txt
```

Adding a new job source means creating one new file in `collectors/` that
returns the same job format, then adding it to the `COLLECTORS` list in
`main.py` — nothing else needs to change.

## How the pipeline works

1. **Collect**: each collector fetches jobs from its source
2. **Dedupe**: identical jobs across sources are collapsed into one
3. **Freshness check**: jobs older than `MAX_AGE_DAYS` (config.py) are dropped
4. **Scoring**: each job gets a numeric score from weighted keywords
   (e.g. "data analyst" +3, "senior" -5) — this is rule-based scoring,
   not machine learning, kept simple and easy to explain
5. **Threshold check**: only jobs scoring above `MIN_SCORE_TO_POST` continue
6. **Store**: the job is saved to the SQLite database (`jobs.db`)
7. **Notify**: Discord and Telegram alerts are sent for the new job

## Setup

### 1. Discord webhook
Server → channel → gear icon → Integrations → Webhooks → New Webhook → copy the URL.

### 2. Telegram bot (optional)
Message `@BotFather` on Telegram → `/newbot` → follow prompts → copy the bot token.
Add the bot to your group, then get the chat ID by visiting
`https://api.telegram.org/bot<TOKEN>/getUpdates` after sending a message in the group.

### 3. Gmail app password for the digest (optional)
Enable 2-Step Verification on your Google account → generate an App Password at
myaccount.google.com/apppasswords.

### 4. Add GitHub Secrets
In your repo: Settings → Secrets and variables → Actions → New repository secret.
Add whichever of these you're using:
- `DISCORD_WEBHOOK_URL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `SENDER_EMAIL`, `SENDER_APP_PASSWORD`, `RECEIVER_EMAIL`

### 5. Test it
Actions tab → Job Alert Bot → Run workflow. Check the logs and your Discord/Telegram.

### 6. Deploy the dashboard (optional, separate step)
GitHub Actions can't host a live webpage — it only runs scheduled scripts.
For the dashboard:
1. Go to share.streamlit.io, sign in with GitHub
2. Point it at this repo, main file path: `dashboard/app.py`
3. Deploy — it's free, and auto-redeploys whenever the bot commits new data

## Adding company-specific sources (Greenhouse/Lever)

Open `config.py`, add company tokens:
```python
GREENHOUSE_BOARDS = ["companyname"]
LEVER_COMPANIES = ["companyname"]
```
Find the token in the company's careers URL (`boards.greenhouse.io/{token}` or
`jobs.lever.co/{token}`).

**Note on JPMorgan, Barclays, HSBC, American Express**: these use Workday,
which doesn't expose a simple public API like Greenhouse/Lever do. They're
intentionally not included here to keep the project stable — Workday's
endpoints are per-tenant and less predictable.

## Roadmap (not yet built)

These are documented as future direction, not implemented yet:
- AI/LLM-based ranking (current scoring is rule-based keyword weighting, not ML)
- Full web dashboard beyond Streamlit (custom frontend)
- Historical trend analysis over months of data
- Multi-user support (currently single-user/single-Discord-server)

## Tech stack

Python, SQLite, GitHub Actions (scheduling), Streamlit (dashboard),
Discord Webhooks, Telegram Bot API, Gmail SMTP.
