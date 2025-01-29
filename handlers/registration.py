from telegram import ReplyKeyboardMarkup
from utils.database import save_user

def start(update, context):
    user = update.message.from_user
    save_user({
        "first_name": user.first_name,
        "username": user.username,
        "chat_id": user.id
    })
    contact_button = ReplyKeyboardMarkup([[{"text": "Share Contact", "request_contact": True}]], one_time_keyboard=True)
    update.message.reply_text("Welcome! Please share your contact information.", reply_markup=contact_button)

def save_contact(update, context):
    contact = update.message.contact
    user_data = {
        "chat_id": contact.user_id,
        "phone_number": contact.phone_number
    }
    save_user(user_data)
    update.message.reply_text("Thank you! You're now registered.")
