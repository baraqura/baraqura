import os
from motor.motor_asyncio import AsyncIOMotorClient

# ভার্সেল থেকে ডাটাবেস ইনফো নেওয়া হচ্ছে
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "baraqura_db")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    db_instance.client = AsyncIOMotorClient(MONGO_URI)
    db_instance.db = db_instance.client[DB_NAME]
    print(f"✅ Connected to MongoDB: {DB_NAME}")

async def close_mongo_connection():
    db_instance.client.close()
    print("❌ MongoDB connection closed")

# ডাটাবেসে ইউজার ডাটা বা চ্যাট সেভ করার একটা ছোট্ট ফাংশন
async def save_chat(user_id: str, message: str, response: str):
    chat_data = {
        "user_id": user_id,
        "message": message,
        "response": response,
        "timestamp": os.getenv("TIMESTAMP") # বা টাইপস্ট্যাম্প জেনারেটর
    }
    await db_instance.db.chats.insert_one(chat_data)
