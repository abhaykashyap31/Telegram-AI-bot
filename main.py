import logging
import traceback
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers.registration import start_command, handle_contact
from handlers.chat import gemini_chat, handle_button_click
from handlers.file_analysis import image_analysis, analyze_pdf
from handlers.web_search import web_search
from handlers.error_handler import error
from config import TOKEN
from fastapi import FastAPI

# Initialize logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("websearch", web_search))

    # Message Handlers
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gemini_chat))
    app.add_handler(MessageHandler(filters.Document.PDF, analyze_pdf))
    app.add_handler(
        MessageHandler(
            (filters.Document.MimeType("image/jpeg") | 
             filters.Document.MimeType("image/png") | 
             filters.Document.MimeType("image/jpeg") |
             filters.PHOTO),
            image_analysis
        )
    )

    # Button Handler
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # Error Handler
    app.add_error_handler(error)

    logger.info("📡 Polling...")
    app.run_polling(poll_interval=3)

app_fastapi = FastAPI()

@app_fastapi.get("/healthz")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    main()