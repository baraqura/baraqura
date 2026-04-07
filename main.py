from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import os
import datetime

# ================================
# 🚀 FastAPI Initializing
# ================================
app = FastAPI()

# আপনার অনুরোধ অনুযায়ী অ্যাপ অবজেক্ট রেফারেন্স
app = app 

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
# 📩 API MODELS
# ================================
class ChatInput(BaseModel):
    message: str

# ================================
# 🌐 WEB ROUTES (Merged: Old + New Update)
# ================================

@app.get("/")
def read_root():
    # এটি আপনার নতুন আপডেট করা অংশ
    return {
        "message": "BaraQura AI is Live!",
        "status": "BaraQura AI is Live ✅",
        "time": str(datetime.datetime.now())
    }

@app.get("/status")
def status():
    # এটিও নতুন আপডেট করা অংশ
    return {
        "status": "Running",
        "db": "connected"
    }

@app.post("/chat")
def chat(data: ChatInput):
    # আপনার আগের চ্যাট লজিক এখানে অক্ষুণ্ণ রাখা হয়েছে
    response = respond(data.message)
    return {
        "user": data.message,
        "ai_response": response,
        "log": f"Executed at {datetime.datetime.now()}"
    }
