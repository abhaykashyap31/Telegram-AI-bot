from utils.gemini import generate_response
from utils.database import save_chat_history

def handle_text(update, context):
    """
    Handles user text input, generates a response using Gemini API,
    and stores the conversation in MongoDB.

    Args:
        update: Telegram update object.
        context: Telegram context object.
    """
    user = update.message.from_user
    chat_id = user.id
    user_input = update.message.text

    # Generate a response using Gemini API
    bot_response = generate_response(user_input)

    # Send response to the user
    update.message.reply_text(bot_response)

    # Save chat history in MongoDB
    save_chat_history({
        "chat_id": chat_id,
        "user_input": user_input,
        "bot_response": bot_response,
        "timestamp": update.message.date.isoformat(),
    })
