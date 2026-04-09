from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
import datetime
# ডাটাবেস কানেকশন ইমপোর্ট (আপনার ফোল্ডার স্ট্রাকচার অনুযায়ী বড় হাতের 'App')
try:
    from App.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance
except ImportError:
    # যদি ফোল্ডার নাম ছোট হাতের হয় তবে তার জন্য ব্যাকআপ
    from app.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance

app = FastAPI()

# ভার্সেল থেকে সিক্রেট কি নেওয়া
SECRET_KEY = os.getenv("SECRET_KEY")

# সার্ভার স্টার্ট হওয়ার সময় ডাটাবেস কানেক্ট হবে
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# সার্ভার বন্ধ হওয়ার সময় কানেকশন কাটবে
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# 🧠 AI BRAIN LOGIC
def respond(msg: str):
    msg = msg.lower()
    if "price" in msg:
        return "Our price is best for quality. (V10 Optimized)"
    elif "buy" in msg:
        return "Great! Let's proceed with your order. (V10 Optimized)"
    elif "delivery" in msg:
        return "We provide fast delivery service. (V10 Optimized)"
    else:
        return "BaraQura V10 is thinking... Tell me more about your need."

# API মডেল
class ChatInput(BaseModel):
    message: str
    master_key: str = None

# ওয়েব রুট (হোম পেজ) - এটিই Vercel প্রথমে চেক করবে
@app.get("/")
def read_root():
    db_status = "Connected ✅" if db_instance.client else "Disconnected ❌"
    return {
        "message": "BaraQura AI V10 is Live!",
        "status": "Online ✅",
        "database": db_status,
        "timestamp": str(datetime.datetime.now())
    }

# চ্যাট এন্ডপয়েন্ট
@app.post("/chat")
async def chat(data: ChatInput):
    # মাস্টার কি ভেরিফিকেশন
    if data.master_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Master Key!")
    
    # রেসপন্স নেওয়া হচ্ছে
    response = respond(data.message)
    
    return {
        "user": data.message,
        "ai_response": response,
        "db_status": "Syncing..." if db_instance.client else "Offline",
        "log": f"V10 Processed at {datetime.datetime.now()}"
    }
