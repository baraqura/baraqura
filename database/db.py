
import motor.motor_asyncio
import logging
from config.settings import settings

# লগিং সেটআপ (কানেকশন স্ট্যাটাস দেখার জন্য)
logger = logging.getLogger("BaraQura-DB")

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    db = None

    async def connect_to_mongo(self):
        """মোঙ্গোডিবি-র সাথে কানেকশন তৈরি করা"""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.DB_NAME]
            logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")
        except Exception as e:
            logger.error(f"❌ Could not connect to MongoDB: {e}")
            raise

    async def close_mongo_connection(self):
        """কানেকশন বন্ধ করা"""
        if self.client:
            self.client.close()
            logger.info("🔌 MongoDB connection closed.")

# ডেটাবেস অবজেক্ট তৈরি
db = Database()

# সহজে কালেকশন পাওয়ার ফাংশন
def get_collection(collection_name: str):
    return db.db[collection_name]
