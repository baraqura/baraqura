import logging
from datetime import datetime
from database.db import get_collection

logger = logging.getLogger("BaraQura-Memory")

class MemoryManager:
    def __init__(self):
        # 'chat_history' নামে একটি কালেকশন ব্যবহার করবে
        self.collection = get_collection("chat_history")

    async def save_interaction(self, user_id: str, user_message: str, ai_response: str, metadata: dict = None):
        """কথোপকথন ডাটাবেসে সেভ করা"""
        document = {
            "user_id": user_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow()
        }
        try:
            await self.collection.insert_one(document)
            logger.info(f"💾 Memory saved for user: {user_id}")
        except Exception as e:
            logger.error(f"Memory Save Error: {e}")

    async def get_recent_history(self, user_id: str, limit: int = 5):
        """ইউজারের শেষ কয়েকটি মেসেজ খুঁজে বের করা (Context-এর জন্য)"""
        try:
            cursor = self.collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
            history = await cursor.to_list(length=limit)
            # মেসেজগুলোকে সাজিয়ে টেক্সট আকারে রিটার্ন করা
            context = ""
            for chat in reversed(history):
                context += f"User: {chat['user_message']}\nAI: {chat['ai_response']}\n"
            return context
        except Exception as e:
            logger.error(f"Memory Retrieval Error: {e}")
            return ""

# মেমোরি ম্যানেজার অবজেক্ট তৈরি
memory = MemoryManager()
