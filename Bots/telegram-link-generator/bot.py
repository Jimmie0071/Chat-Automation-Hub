import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Send me phone numbers (single or multiple)\n"
        "I’ll convert them into Telegram t.me links.\n\n"
        "Example:\n+919876543210\n447700900123"
    )

def clean_number(text: str) -> str:
    return re.sub(r"\D", "", text)

async def generate_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = update.message.text.splitlines()
    links = []

    for line in lines:
        number = clean_number(line)
        if len(number) >= 7:
            links.append(f"https://t.me/+{number}")

    if not links:
        await update.message.reply_text("❌ No valid phone numbers found.")
        return

    await update.message.reply_text(
        "✅ Telegram Links:\n\n" + "\n".join(links)
    )

def main():
    app = ApplicationBuilder().token("8565690230:AAFwFG44pyCKSOED5l5mS_rqAUEXUYNvmOI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_links))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
