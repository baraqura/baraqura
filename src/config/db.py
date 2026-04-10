import os
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "baraqura_db")
    
    if MONGO_URI:
        try:
            db_instance.client = AsyncIOMotorClient(
                MONGO_URI, 
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000
            )
            db_instance.db = db_instance.client[DB_NAME]
            print(f"✅ DB Connected: {DB_NAME}")
        except Exception as e:
            print(f"❌ DB Error: {e}")
