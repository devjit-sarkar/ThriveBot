import os
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from notion_integration import add_reflection_to_notion

BOT_TOKEN = os.getenv("BOT_TOKEN")

WAITING_FOR_MORNING = {}
WAITING_FOR_EVENING = {}
REFLECTIONS = {}

# Simple in-memory log (you can persist to a file if you want)
def add_reflection(chat_id, ref_type, text):
    if chat_id not in REFLECTIONS:
        REFLECTIONS[chat_id] = []
    REFLECTIONS[chat_id].append({
        "type": ref_type,
        "text": text,
        "timestamp": datetime.now().isoformat()
    })

# --- Web server for Render ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("🌿 Thrive Bot is alive.".encode("utf-8"))
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"✅ Web server running on port {port}")
    httpd.serve_forever()

# --- Telegram commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌞 Welcome to Thrive Companion!\nUse /morning or /evening to log reflections.")

async def morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    WAITING_FOR_MORNING[chat_id] = True
    await update.message.reply_text("☀️ Morning reflection — what’s your intention today?")

async def evening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    WAITING_FOR_EVENING[chat_id] = True
    await update.message.reply_text("🌙 Evening reflection — how did today go?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    if WAITING_FOR_MORNING.get(chat_id):
        add_reflection(chat_id, "morning", text)
        add_reflection_to_notion("morning", text)
        WAITING_FOR_MORNING[chat_id] = False
        await update.message.reply_text("🌿 Logged in Notion. Have a great day ahead!")
    elif WAITING_FOR_EVENING.get(chat_id):
        add_reflection(chat_id, "evening", text)
        add_reflection_to_notion("evening", text)
        WAITING_FOR_EVENING[chat_id] = False
        await update.message.reply_text("🌾 Reflection saved to Notion. Rest easy tonight.")
    else:
        await update.message.reply_text("Use /morning or /evening to begin your reflection 🌱")

def main():
    threading.Thread(target=run_server).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("morning", morning))
    app.add_handler(CommandHandler("evening", evening))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Thrive Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
