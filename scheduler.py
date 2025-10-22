from apscheduler.schedulers.background import BackgroundScheduler
from datetime import time
from telegram.ext import Application
import asyncio
from config import USER_ID

async def send_message(app: Application, chat_id: int, text: str):
    try:
        await app.bot.send_message(chat_id, text)
    except Exception as e:
        print(f"❌ Failed to send scheduled message: {e}")

def setup_schedules(app: Application):
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    if USER_ID == 0:
        print("⚠️ USER_ID not set. Run /start once to get your chat ID, then update config.py or Render env.")
        return

    # Morning message (8:00 AM)
    scheduler.add_job(
        lambda: asyncio.run(send_message(app, USER_ID, "🌞 Good morning! What’s one focus for today?")),
        trigger='cron', hour=8, minute=0
    )

    # Evening message (9:00 PM)
    scheduler.add_job(
        lambda: asyncio.run(send_message(app, USER_ID, "🌙 Evening reflection time! What went well today?")),
        trigger='cron', hour=21, minute=0
    )

    scheduler.start()
    print("✅ Daily schedules set (8 AM & 9 PM, Asia/Kolkata)")
