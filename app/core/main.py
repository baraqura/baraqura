from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
import datetime

# আপনার ডাটাবেস ইমপোর্ট লজিক
try:
    from app.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance
except ImportError:
    # ব্যাকআপ হিসেবে যদি কোনো কারণে পাথ না পায়
    from App.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance

# অ্যাপ ইনিশিয়ালাইজেশন
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

# 🧠 AI ব্রেইন লজিক (ভবিষ্যতে এখানে Gemini/Grok ইনটিগ্রেট হবে)
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

# চ্যাট এন্ডপয়েন্ট (এটিতে Zero-Trust এর প্রথম ধাপ IP Tracking যোগ করা হয়েছে)
@app.post("/chat")
async def chat(data: ChatInput, request: Request):
    # ইউজার আইপি রিড করা (Zero-Trust Logic)
    client_ip = request.client.host
    
    # মাস্টার কি ভেরিফিকেশন
    if data.master_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Master Key!")
    
    # রেসপন্স জেনারেট করা
    response = respond(data.message)
    
    return {
        "user_ip": client_ip,
        "user_message": data.message,
        "ai_response": response,
        "status": "SECURED_BY_V10",
        "timestamp": str(datetime.datetime.now())
    }

# --- V10 DEBUG SYSTEM (Day 01) ---
# এই অংশটুকু আমাদের ডাটাবেজ এবং এনভায়রনমেন্ট চেক করতে সাহায্য করবে

@app.get("/v10/debug/db")
async def debug_db():
    try:
        # db_instance.client.list_database_names() ব্যবহার করে চেক
        if db_instance.client:
            collections = await db_instance.db.list_collection_names()
            return {
                "status": "connected",
                "database_name": db_instance.db.name,
                "collections": collections,
                "message": "V10 Sentinel: Database logic synced!"
            }
        else:
            return {"status": "error", "message": "Database client not initialized"}
    except Exception as e:
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e)
        }

@app.get("/v10/debug/env")
async def debug_env():
    import os
    master_key_check = os.getenv("SECRET_KEY")
    return {
        "Vercel_Env_Active": master_key_check is not None,
        "Key_Length": len(master_key_check) if master_key_check else 0,
        "System": "V10 Sentinel Identity Guard"
    }
