# scheduler.py
import os
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Application
import asyncio
from dotenv import load_dotenv

load_dotenv()
USER_ID = os.getenv("USER_ID")
# --- Messages ---
MORNING_MESSAGE = "🌞 Good morning! Remember: Peace flows through me, for I know I gave today."
EVENING_MESSAGE = "🌙 Good evening! Reflect on your progress — peace, purpose, and patience."

# --- Helper function to send message ---
async def send_message(app: Application, chat_id: int, text: str):
    try:
        await app.bot.send_message(chat_id=chat_id, text=text)
        print(f"✅ Sent scheduled message to {chat_id}: {text[:40]}...")
    except Exception as e:
        print(f"❌ Failed to send scheduled message: {e}")

# --- Main scheduler setup ---
def setup_schedules(app: Application):
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    if not USER_ID:
        print("⚠️ USER_ID not set. Run /start once to get your chat ID, then update config.py or Render env.")
        return

    # Morning update (8 AM)
    scheduler.add_job(
        lambda: asyncio.run(send_message(app, USER_ID, MORNING_MESSAGE)),
        trigger='cron', hour=8, minute=0
    )

    # Evening update (7 PM)
    scheduler.add_job(
        lambda: asyncio.run(send_message(app, USER_ID, EVENING_MESSAGE)),
        trigger='cron', hour=19, minute=0
    )

    scheduler.start()
    print("✅ Daily schedules set (8 AM & 7 PM, Asia/Kolkata)")
