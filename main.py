from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import os
import datetime

# ================================
# 🚀 FastAPI Initializing
# ================================
app = FastAPI()
app = app # আপনার অনুরোধ অনুযায়ী রেফারেন্স

# ================================
# 💾 MEMORY SYSTEM (Old Logic)
# ================================
MEMORY_FILE = "/tmp/memory.json" # Vercel-এ ফাইলের জন্য /tmp ব্যবহার করতে হয়

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def get_answer(question):
    memory = load_memory()
    return memory.get(question.lower())

def add_memory(question, answer):
    memory = load_memory()
    memory[question.lower()] = answer
    save_memory(memory)

# ================================
# 🧠 AI BRAIN (Old Logic)
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
# 🌐 WEB ROUTES (New FastAPI Integration)
# ================================

class ChatInput(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "status": "BaraQura AI is Live ✅",
        "system": "Hybrid Memory + FastAPI",
        "time": str(datetime.datetime.now())
    }

@app.post("/chat")
def chat(data: ChatInput):
    user_msg = data.message
    
    # প্রথমে মেমরি চেক (Old Logic)
    memory_answer = get_answer(user_msg)
    
    if memory_answer:
        final_response = f"(From Memory) {memory_answer}"
    else:
        # মেমরিতে না থাকলে ব্রেইন থেকে উত্তর (Old Logic)
        final_response = respond(user_msg)
        # অটোমেটিক মেমরিতে সেভ করে রাখা (পুরানো সিস্টেমে যেটা input দিয়ে করতেন)
        add_memory(user_msg, final_response)

    return {
        "user": user_msg,
        "ai": final_response,
        "timestamp": str(datetime.datetime.now())
    }

# নোট: Vercel-এ input() কাজ করে না বলে login/permission পার্টগুলো 
# সরাসরি API ইন্টারফেসে ইন্টিগ্রেট করা হয়েছে।
