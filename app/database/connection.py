from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
import logging

# সেটিংস লোড করা
settings = get_settings()

# লগিং সেটআপ (যাতে এরর হলে আমরা সাথে সাথে বুঝতে পারি)
logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_instance = MongoDB()

async def connect_to_mongo():
    """ডাটাবেস কানেকশন তৈরি করা"""
    try:
        db_instance.client = AsyncIOMotorClient(settings.DATABASE_URL)
        # ডাটাবেস নাম আপনার .env থেকে নিবে অথবা ডিফল্ট 'baraqura_db'
        db_instance.db = db_instance.client.get_database("baraqura_db")
        
        # কানেকশন টেস্ট করা
        await db_instance.client.admin.command('ping')
        print("✅ MongoDB Connection Successful! V10 is now online.")
    except Exception as e:
        logger.error(f"❌ Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """সার্ভার বন্ধ করার সময় কানেকশন ক্লোজ করা"""
    if db_instance.client:
        db_instance.client.close()
        print("🔌 MongoDB Connection Closed.")

def get_database():
    """কোডের অন্যান্য জায়গায় ডাটাবেস এক্সেস করার জন্য এটি ব্যবহার হবে"""
    return db_instance.db
