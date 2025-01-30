import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")
BOT_USERNAME = os.getenv("BOT_NAME")
MONGO_URI = os.getenv("MONGO_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
