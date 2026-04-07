from fastapi import FastAPI
from pydantic import BaseModel
import os
import datetime

# ================================
# 🚀 FastAPI Initializing
# ================================
app = FastAPI()

# আপনার অনুরোধ অনুযায়ী অ্যাপ অবজেক্ট রেফারেন্স
app = app 

# ================================
# 🧠 AI BRAIN LOGIC
# ================================
def get_ai_response(msg: str):
    msg = msg.lower()
    if "price" in msg:
        return "Our price is best for quality."
    elif "buy" in msg:
        return "Great! Let's proceed with your order."
    elif "delivery" in msg:
        return "We provide fast delivery service."
    else:
        return "Tell me more about your need."

# ================================
# 📩 API MODELS
# ================================
class ChatRequest(BaseModel):
    message: str

# ================================
# 🌐 API ROUTES (ইন্টারনেটে ব্যবহারের জন্য)
# ================================

@app.get("/")
def home():
    return {"status": "BaraQura AI is Live 🚀", "time": str(datetime.datetime.now())}

@app.post("/chat")
def chat(request: ChatRequest):
    response = get_ai_response(request.message)
    return {
        "user_message": request.message,
        "ai_response": response
    }

# ================================
# 🔐 AUTH & LOGGING (Simplified for API)
# ================================
# নোট: API-তে input() কাজ করে না, তাই এগুলোকে ফাংশন হিসেবে রাখা হয়েছে
