from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import users_collection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        chat_id = update.message.chat.id

        if not users_collection.find_one({"chat_id": chat_id}):
            users_collection.insert_one(
                {
                    "chat_id": chat_id,
                    "first_name": user.first_name,
                    "username": user.username,
                    "phone": None,
                    "registered_at": datetime.now(),
                }
            )

        phone_button = KeyboardButton(text="📞 Share phone number", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[phone_button]], resize_keyboard=True)

        await update.message.reply_text(
            "Welcome! Please share your phone number to complete registration.", reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("An error occurred. Please try again.")

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.message.chat.id
        phone = update.message.contact.phone_number

        users_collection.update_one({"chat_id": chat_id}, {"$set": {"phone": phone}})
        await update.message.reply_text("✅ Thank you! You are now fully registered.")
    except Exception as e:
        logger.error(f"Error in handle_contact: {e}")
        await update.message.reply_text("⚠️ An error occurred while processing your contact.")

