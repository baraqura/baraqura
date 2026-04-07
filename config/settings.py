import os
from dotenv import load_dotenv

# .env ফাইল থেকে ডেটা লোড করা
load_dotenv()

class Settings:
    # 🧠 PROJECT INFO
    PROJECT_NAME: str = "BaraQura V10 AI"
    VERSION: str = "10.0.0"

    # 🔑 API KEYS
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")

    # 🗄️ DATABASE CONFIG
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "baraqura_db")

    # 🔐 SECURITY & AUTH
    SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_REVENUE_CLOSER")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # 🚦 OPERATIONAL LIMITS
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", 10))

# প্রজেক্টের অন্য জায়গায় ব্যবহারের জন্য একটি ইনস্ট্যান্স তৈরি
settings = Settings()
