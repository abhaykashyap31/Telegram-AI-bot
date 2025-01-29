import os
import asyncio
from typing import Final
import logging
import traceback
from PIL import Image
import io
import requests
import fitz
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from pymongo import MongoClient
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# Bot Configuration

load_dotenv()

TOKEN: Final = os.getenv("BOT_API_KEY")
BOT_USERNAME: Final = os.getenv("BOT_NAME")
MONGO_URI: Final = os.getenv("MONGO_URL")
GEMINI_API_KEY: Final = os.getenv("GEMINI_API_KEY")

client = MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_collection = db["users"]
chat_history_collection = db["chat_history"]
files_collection = db["file_metadata"]


# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

abort_controller = {}

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


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
        logger.debug(traceback.format_exc())
        await update.message.reply_text("An error occurred. Please try again.")

### 2️⃣ Handle Phone Contact ###
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.message.chat.id
        phone = update.message.contact.phone_number

        users_collection.update_one({"chat_id": chat_id}, {"$set": {"phone": phone}})

        await update.message.reply_text("✅ Thank you! You are now fully registered.")
    except Exception as e:
        logger.error(f"Error in handle_contact: {e}")
        await update.message.reply_text("⚠️ An error occurred while processing your contact.")

### 3️⃣ Gemini Chat - Button to Prevent Auto-Requests ###
async def gemini_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a button asking if the user wants an AI response."""
    chat_id = update.message.chat.id
    text = update.message.text

    keyboard = [[InlineKeyboardButton("🤖 Get AI Response", callback_data=f"ai_response|{text}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Click below to get a response:", reply_markup=reply_markup)

### 4️⃣ Handle Button Click - Triggers AI Response ###
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
        # Store the async task in AbortController
        abort_controller[chat_id] = asyncio.create_task(fetch_response())
        bot_reply = await abort_controller[chat_id]
    except asyncio.CancelledError:
        bot_reply = "⚠️ Previous request canceled."
    except asyncio.TimeoutError:
        bot_reply = "⚠️ AI response took too long."
    except Exception as e:
        logger.error(f"Error in AI response: {e}")
        bot_reply = "⚠️ Error generating response."

    await query.message.reply_text(bot_reply)

### 5️⃣ Image Analysis ###
async def analyze_image(image_bytes):
    """Analyzes an image using Gemini API and returns the response."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    image = Image.open(io.BytesIO(image_bytes))

    # Ensure the API call is awaited
    response = model.generate_content([image, "Describe the contents of this image."])

    return response.text


async def image_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.message.chat.id

        if update.message.document:
            file = update.message.document
        elif update.message.photo:
            file = update.message.photo[-1]
        else:
            await update.message.reply_text("Please send a valid image or file.")
            return

        file_id = file.file_id
        file_path = await context.bot.get_file(file_id)
        file_content = await file_path.download_as_bytearray()

        # Analyze the image using Gemini API (await is added here)
        analysis = await analyze_image(file_content)

        # Save file metadata to DB
        files_collection.insert_one(
            {
                "chat_id": chat_id,
                "file_name": file.file_name if hasattr(file, "file_name") else "image.jpg",
                "description": analysis,
                "timestamp": datetime.utcnow(),
            }
        )

        await update.message.reply_text(f"File analyzed: {analysis}")
    except Exception as e:
        logger.error(f"Error in image_analysis: {e}")
        logger.debug(traceback.format_exc())
        await update.message.reply_text("Sorry, I couldn't analyze the file.")
        
        
# PDF analyzer
import fitz  # PyMuPDF
import io

async def analyze_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.message.chat.id
        
        # Check if the user uploaded a document
        if update.message.document:
            file = update.message.document
            if not file.mime_type.startswith("application/pdf"):
                await update.message.reply_text("Please send a valid PDF file.")
                return
        else:
            await update.message.reply_text("Please send a valid document.")
            return

        # Download the PDF file
        file_id = file.file_id
        file_path = await context.bot.get_file(file_id)
        pdf_bytes = await file_path.download_as_bytearray()

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_bytes)

        if not pdf_text.strip():
            await update.message.reply_text("The PDF seems to have no extractable text.")
            return

        # Send extracted text to Gemini for summarization
        response = model.generate_content(f"Summarize this document: {pdf_text[:3000]}")
        summary = response.text

        # Save file metadata to DB
        files_collection.insert_one(
            {
                "chat_id": chat_id,
                "file_name": file.file_name,
                "description": summary,
                "timestamp": datetime.utcnow(),
            }
        )

        await update.message.reply_text(f"PDF Analysis:\n{summary}")

    except Exception as e:
        logger.error(f"Error in analyze_pdf: {e}")
        logger.debug(traceback.format_exc())
        await update.message.reply_text("Sorry, I couldn't analyze the PDF.")

def extract_text_from_pdf(pdf_bytes):
    """Extracts text from a PDF file."""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    extracted_text = ""

    for page in pdf_document:
        extracted_text += page.get_text("text") + "\n"

    return extracted_text



### 6️⃣ Web Search using AI ###
async def web_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Performs AI-powered web search."""
    try:
        user_query = " ".join(context.args)
        if not user_query:
            await update.message.reply_text("🔍 Please provide a search query.")
            return

        response = model.generate_content(f"Summarize top results for: {user_query}")
        summary = response.text

        await update.message.reply_text(f"📜 Search Results:\n{summary}")
    except Exception as e:
        logger.error(f"Error in web_search: {e}")
        await update.message.reply_text("⚠️ Couldn't perform the web search.")

### 7️⃣ Error Handler ###
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles errors globally."""
    logger.error(f"Error occurred: {context.error}")
    await update.message.reply_text("⚠️ An error occurred.")

### 8️⃣ Main Function ###
if __name__ == "__main__":
    logger.info("🚀 Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("websearch", web_search))

    # Message Handlers
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gemini_chat))
    app.add_handler(
    MessageHandler(
        (filters.Document.MimeType("image/jpeg") | 
         filters.Document.MimeType("image/png") | 
         filters.Document.MimeType("image/jpeg") |
         filters.PHOTO),
        image_analysis
    )
)

    app.add_handler(MessageHandler(filters.Document.PDF, analyze_pdf))


    # Button Handler
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # Error Handler
    app.add_error_handler(error)

    logger.info("📡 Polling...")
    app.run_polling(poll_interval=3)