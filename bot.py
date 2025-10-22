from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import init_db, add_reflection, get_week_summary
from notion_integration import add_reflection_to_notion
from scheduler import setup_schedules
from config import BOT_TOKEN

init_db()

WAITING_FOR_MORNING = {}
WAITING_FOR_EVENING = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"🔹 User started bot: {user.id} ({user.first_name})")
    await update.message.reply_text(
        f"🌿 Hello {user.first_name}! I'm your Thrive Companion.\n\n"
        "I'll message you morning & evening to help you reflect.\n"
        "You can also type /summary anytime to view your week’s reflections.\n\n"
        "✨ Stay mindful and consistent!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if WAITING_FOR_MORNING.get(chat_id):
        add_reflection(chat_id, "morning", text)
        add_reflection_to_notion("morning", text)
        WAITING_FOR_MORNING[chat_id] = False
        await update.message.reply_text("🌿 Beautiful. Logged in Notion & saved locally.")
    elif WAITING_FOR_EVENING.get(chat_id):
        add_reflection(chat_id, "evening", text)
        add_reflection_to_notion("evening", text)
        WAITING_FOR_EVENING[chat_id] = False
        await update.message.reply_text("🌾 Reflection added to Notion. Peace flows through you.")
    else:
        await update.message.reply_text("🌱 I'm listening. Is this a morning or evening reflection?")

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    data = get_week_summary(user_id)
    if not data:
        await update.message.reply_text("No reflections yet this week 🌿")
        return

    mornings = [m for t, m in data if t == "morning"]
    evenings = [m for t, m in data if t == "evening"]
    text = (f"📅 *Your Thrive Summary:*\n\n"
            f"🌞 Morning reflections: {len(mornings)}\n"
            f"🌙 Evening reflections: {len(evenings)}\n"
            f"Keep showing up — peace flows through you 💚")
    await update.message.reply_text(text, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    setup_schedules(app)
    app.run_polling()
