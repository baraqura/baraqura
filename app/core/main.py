from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
import datetime

# আপনার ডাটাবেস ইমপোর্ট লজিক
try:
    from app.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance
except ImportError:
    # ব্যাকআপ হিসেবে যদি কোনো কারণে পাথ না পায়
    from App.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance

# অ্যাপ ইনিশিয়ালাইজেশন
app = FastAPI()

# ভার্সেল এনভায়রনমেন্ট থেকে সিক্রেট কি
SECRET_KEY = os.getenv("SECRET_KEY")

# ডাটাবেস কানেকশন ইভেন্টস
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# 🧠 AI ব্রেইন লজিক
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

# ডাটা মডেল
class ChatInput(BaseModel):
    message: str
    master_key: str = None

# হোম রুট
@app.get("/")
def read_root():
    # ডাটাবেস কানেকশন চেক
    try:
        db_status = "Connected ✅" if db_instance.client else "Disconnected ❌"
    except:
        db_status = "Status Unknown ⚠️"
        
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
    
    # রেসপন্স জেনারেট করা
    response = respond(data.message)
    
    return {
        "user": data.message,
        "ai_response": response,
        "log": f"V10 Processed at {datetime.datetime.now()}"
    }
