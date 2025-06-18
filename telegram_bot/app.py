"""Telegram Bot to register users in a Django application via API."""

import logging
from os import getenv

import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

# Load env vars
BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8000/api/telegram/register/"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # noqa: ARG001
    """Handle the /start command and register the user in Django."""
    user = update.effective_user

    payload = {
        "telegram_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(API_URL, json=payload)
    except Exception: # noqa: BLE001
        logger.error("Failed to POST to Django") # noqa: TRY400

    await update.message.reply_text(f"Hi, welcome! {user.username}")

# Main
def main() -> None:
    """Start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
