from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import datetime
import motor.motor_asyncio

# অ্যাপ ইনিশিয়ালাইজেশন
app = FastAPI()

# এনভায়রনমেন্ট ভেরিয়েবল (ভার্সেল থেকে আসবে)
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "baraqura_db")

# গ্লোবাল ডাটাবেজ ক্লায়েন্ট
client = None
db = None

@app.on_event("startup")
async def startup_event():
    global client, db
    if MONGO_URI:
        try:
            # TLS/SSL এবং DNS ইস্যু এড়াতে সেটিংস
            client = motor.motor_asyncio.AsyncIOMotorClient(
                MONGO_URI, 
                serverSelectionTimeoutMS=5000,
                tlsInsecure=True 
            )
            db = client[DB_NAME]
            print("V10 Sentinel: Database logic initialized.")
        except Exception as e:
            print(f"DB Init Error: {e}")

# 🧠 তোমার আগের AI ব্রেইন লজিক (যা আমি এখানে রেখে দিয়েছি)
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

# হোম রুট (সাদা স্ক্রিন এড়ানোর জন্য JSONResponse ব্যবহার করা হয়েছে)
@app.get("/")
async def read_root():
    db_status = "Disconnected ❌"
    if client:
        try:
            await client.admin.command('ping')
            db_status = "Connected ✅"
        except:
            db_status = "Auth/Network Failed ⚠️"

    return JSONResponse(content={
        "project": "BaraQura V10",
        "status": "Live 🚀",
        "database": db_status,
        "env_check": {
            "MONGO_URI_FOUND": MONGO_URI is not None,
            "SECRET_KEY_FOUND": SECRET_KEY is not None
        },
        "time": str(datetime.datetime.now())
    })

# তোমার আগের চ্যাট এন্ডপয়েন্ট (এখন IP ট্র্যাকিং সহ)
@app.post("/chat")
async def chat(data: ChatInput, request: Request):
    client_ip = request.client.host
    
    # মাস্টার কি ভেরিফিকেশন
    if data.master_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Master Key!")
    
    # রেসপন্স জেনারেট করা
    response = respond(data.message)
    
    return {
        "user_ip": client_ip,
        "ai_response": response,
        "status": "SECURED_BY_V10"
    }

# ডিবগ এন্ডপয়েন্ট (কানেকশন টেস্ট করার জন্য)
@app.get("/v10/test-connection")
async def test_conn():
    if not MONGO_URI:
        return JSONResponse(content={"error": "MONGO_URI missing in Vercel!"})
    try:
        temp_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        server_info = await temp_client.server_info()
        return JSONResponse(content={"status": "Online", "version": server_info.get('version')})
    except Exception as e:
        return JSONResponse(content={"status": "Offline", "error": str(e)})

# --- VERCEL DEPLOYMENT HANDLER ---
# এই লাইনটিই ভেরসেলকে অ্যাপটি রান করতে সাহায্য করবে
app = app

# আগের ইমপোর্টগুলো থাকবে...

app = FastAPI()

# মঙ্গোডিবি ক্লায়েন্টকে গ্লোবাল না রেখে ফাংশনের ভেতর চেক করবো
async def get_db():
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    client = motor.motor_asyncio.AsyncIOMotorClient(
        uri, 
        serverSelectionTimeoutMS=2000 # ২ সেকেন্ডের বেশি ওয়েট করবে না
    )
    return client

@app.get("/")
async def read_root():
    return {
        "project": "BaraQura V10",
        "status": "Online 🚀",
        "time": str(datetime.datetime.now())
    }

# একদম শেষে এই ৩টি লাইন নিশ্চিত করো
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

app = app # ভেরসেলের জন্য
