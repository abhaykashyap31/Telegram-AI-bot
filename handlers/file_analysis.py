from telegram import Update
from telegram.ext import ContextTypes
from config import model
from database import files_collection
import fitz
import io
import traceback
from datetime import datetime
import logging
from PIL import Image

logger = logging.getLogger(__name__)

async def analyze_image(image_bytes):
    """Analyzes an image using Gemini API and returns the response."""
    image = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content([image, "Describe the contents of this image."])
    return response.text

async def image_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.message.chat.id
        file = update.message.document or update.message.photo[-1]

        file_path = await context.bot.get_file(file.file_id)
        file_content = await file_path.download_as_bytearray()
        analysis = await analyze_image(file_content)

        await update.message.reply_text(f"File analyzed: {analysis}")
    except Exception as e:
        logger.error(f"Error in image_analysis: {e}")
        await update.message.reply_text("Sorry, I couldn't analyze the file.")
        
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



