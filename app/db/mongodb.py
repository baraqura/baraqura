import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# ভার্সেল থেকে ডাটাবেস ইনফো নেওয়া হচ্ছে
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "baraqura_db")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    # এখানে কানেকশন মজবুত করার জন্য নতুন লজিক যোগ করা হলো
    db_instance.client = AsyncIOMotorClient(
        MONGO_URI, 
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    db_instance.db = db_instance.client[DB_NAME]
    try:
        # কানেকশন চেক করার পিং
        await db_instance.client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("❌ MongoDB connection closed")

# আপনার পুরনো save_chat ফাংশনটি এখানে রাখা হলো
async def save_chat(user_id: str, message: str, response: str):
    chat_data = {
        "user_id": user_id,
        "message": message,
        "response": response,
        "timestamp": str(datetime.now()) # অটোমেটিক টাইমস্ট্যাম্প
    }
    if db_instance.db is not None:
        await db_instance.db.chats.insert_one(chat_data)
