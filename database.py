from pymongo import MongoClient

from config import MONGO_URI

# Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_collection = db["users"]
chat_history_collection = db["chat_history"]
files_collection = db["file_metadata"]
