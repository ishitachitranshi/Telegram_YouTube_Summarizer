import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from src.core.assistant import YouTubeResearchAssistant, detect_requested_lang

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

assistant = YouTubeResearchAssistant()


def looks_like_youtube_url(text: str) -> bool:
    return "youtube.com" in text or "youtu.be" in text


async def send_long_message(update: Update, text: str, chunk_size: int = 3500):
    if not text:
        return
    for i in range(0, len(text), chunk_size):
        await update.message.reply_text(text[i:i + chunk_size])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send a YouTube link.\n"
        "I will fetch transcript + summary.\n"
        "Then you can ask questions."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return

    lang = detect_requested_lang(text)

    if looks_like_youtube_url(text):
        await update.message.reply_text("Processing video...")
        result = assistant.handle_youtube_link(update.effective_chat.id, text, lang)
    else:
        result = assistant.answer_question(update.effective_chat.id, text, lang)

    await send_long_message(update, result)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN missing in .env")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
