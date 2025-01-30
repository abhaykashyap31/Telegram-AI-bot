from telegram import Update
from telegram.ext import ContextTypes
from config import model
import logging

logger = logging.getLogger(__name__)

async def web_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Performs AI-powered web search."""
    try:
        user_query = " ".join(context.args)
        response = model.generate_content(f"Summarize top results for: {user_query}")
        await update.message.reply_text(f"📜 Search Results:\n{response.text}")
    except Exception as e:
        logger.error(f"Error in web_search: {e}")
        await update.message.reply_text("⚠️ Couldn't perform the web search.")
