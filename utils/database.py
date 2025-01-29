from pymongo import MongoClient
from config import MONGO_URI

def setup_database():
    client = MongoClient(MONGO_URI)
    db = client['telegram_ai_bot']
    return db

db = setup_database()

def save_user(data):
    users = db['users']
    users.update_one({'chat_id': data['chat_id']}, {'$set': data}, upsert=True)

def save_chat_history(chat):
    history = db['chat_history']
    history.insert_one(chat)
