from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import model
import asyncio
import logging

logger = logging.getLogger(__name__)

abort_controller = {}

async def gemini_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a button asking if the user wants an AI response."""
    chat_id = update.message.chat.id
    text = update.message.text

    keyboard = [[InlineKeyboardButton("🤖 Get AI Response", callback_data=f"ai_response|{text}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Click below to get a response:", reply_markup=reply_markup)

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button clicks and triggers AI response."""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    user_text = query.data.split("|")[1]

    # Abort previous request if exists
    if chat_id in abort_controller and not abort_controller[chat_id].done():
        abort_controller[chat_id].cancel()

    async def fetch_response():
        response = model.generate_content(user_text)
        return response.text

    try:
        abort_controller[chat_id] = asyncio.create_task(fetch_response())
        bot_reply = await abort_controller[chat_id]
    except asyncio.CancelledError:
        bot_reply = "⚠️ Previous request canceled."
    except Exception as e:
        logger.error(f"Error in AI response: {e}")
        bot_reply = "⚠️ Error generating response."

    await query.message.reply_text(bot_reply)
