from telegram import Update
from telegram.ext import ContextTypes
from config import model
import logging

logger = logging.getLogger(__name__)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles errors globally."""
    logger.error(f"Error occurred: {context.error}")

    # Try to send the error to the user, if possible
    try:
        if update.message:
            await update.message.reply_text("⚠️ An error occurred.")
        elif update.callback_query:
            await update.callback_query.answer("⚠️ An error occurred.", show_alert=True)
        # You can add more handlers here if needed
    except Exception as e:
        logger.error(f"Failed to send error message to user: {e}")
