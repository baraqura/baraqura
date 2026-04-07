from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import os
import datetime

# ================================
# 🚀 FastAPI Initializing
# ================================
app = FastAPI()

# ================================
# 🧠 AI BRAIN LOGIC (আপনার পুরানো লজিক)
# ================================
def respond(msg):
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
# 🌐 WEB ROUTES (ইন্টারনেটে ব্যবহারের জন্য)
# ================================

class ChatInput(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "BaraQura AI is Live ✅", "time": str(datetime.datetime.now())}

@app.post("/chat")
def chat(data: ChatInput):
    # input() এর বদলে এখানে ডাটা রিসিভ করা হচ্ছে
    response = respond(data.message)
    return {
        "user": data.message,
        "ai_response": response,
        "log": f"Executed at {datetime.datetime.now()}"
    }
