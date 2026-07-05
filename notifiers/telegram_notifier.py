"""
Telegram notifier - posts job alerts to a Telegram chat/group via the Bot API.

Setup:
1. Message @BotFather on Telegram, run /newbot, follow prompts - you get a bot token
2. Add your bot to your group/channel
3. Get your chat ID (easiest way: send a message in the group, then visit
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates and look for "chat":{"id": ...}
4. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as GitHub Secrets
"""

import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils import get_logger

logger = get_logger("notifiers.telegram")


def post_to_telegram(job):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured - skipping Telegram post.")
        return False

    text = (
        f"*{job['title']}*\n"
        f"🏢 {job.get('company', 'Unknown')}\n"
        f"📍 {job.get('location', 'Unknown')}\n"
        f"📊 Level: {job.get('experience_level', 'Unclear')} | Score: {job.get('score', 0)}\n"
        f"🔗 {job['url']}\n"
        f"_Source: {job.get('source', 'Unknown')}_"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }

    try:
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code >= 300:
            logger.error(f"Telegram post failed ({resp.status_code}): {resp.text}")
            return False
        logger.info(f"Posted to Telegram: {job['title']}")
        return True
    except Exception as e:
        logger.error(f"Telegram post error: {e}")
        return False
    finally:
        time.sleep(1)
