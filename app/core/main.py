from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
import os
import datetime

app = FastAPI()

# ভার্সেল থেকে সিক্রেট কি নেওয়ার লজিক
SECRET_KEY = os.getenv("SECRET_KEY")

# ================================
# 🧠 AI BRAIN LOGIC (আপনার পুরনো লজিক ফিরিয়ে আনা হলো)
# ================================
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

# ================================
# 📩 API MODELS
# ================================
class ChatInput(BaseModel):
    message: str
    master_key: str = None

# ================================
# 🌐 WEB ROUTES
# ================================

@app.get("/")
def read_root():
    return {
        "message": "BaraQura AI V10 is Live!",
        "status": "Online ✅",
        "timestamp": str(datetime.datetime.now())
    }

@app.post("/chat")
async def chat(data: ChatInput):
    # আপনার সেই মাস্টার কি ভেরিফিকেশন লজিক
    if data.master_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Master Key!")
        
    response = respond(data.message)
    return {
        "user": data.message,
        "ai_response": response,
        "log": f"V10 Processed at {datetime.datetime.now()}"
    }
