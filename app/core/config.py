import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# .env ফাইল লোড করা
load_dotenv()

class Settings(BaseSettings):
    # প্রোজেক্ট ডিটেইলস
    APP_NAME: str = "BaraQura V10"
    DEBUG: bool = True
    
    # সিকিউরিটি (আপনার এডমিন আইডি ও সিক্রেট)
    ADMIN_TELEGRAM_ID: str = os.getenv("ADMIN_TELEGRAM_ID", "your_id_here")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    
    # ডাটাবেস (Supabase Connection String)
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # এআই ইঞ্জিন কী (OpenAI & Gemini)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    # টেলিগ্রাম বট টোকেন
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

    class Config:
        case_sensitive = True

# লজিক যাতে বারবার লোড হয়ে সিস্টেম স্লো না করে (Caching)
@lru_cache()
def get_settings():
    return Settings()
