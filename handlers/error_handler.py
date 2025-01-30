from telegram import Update
from telegram.ext import ContextTypes
from config import model
import logging

logger = logging.getLogger(__name__)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles errors globally."""
    logger.error(f"Error occurred: {context.error}")
    await update.message.reply_text("⚠️ An error occurred.")