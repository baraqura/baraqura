from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
import datetime
import motor.motor_asyncio

app = FastAPI()

# এনভায়রনমেন্ট ভেরিয়েবল
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
            # TLS/SSL এরর এড়াতে কিছু এক্সট্রা প্যারামিটার যোগ করা হয়েছে
            client = motor.motor_asyncio.AsyncIOMotorClient(
                MONGO_URI, 
                serverSelectionTimeoutMS=5000,
                tlsInsecure=True 
            )
            db = client[DB_NAME]
            print("V10 Sentinel: Database logic initialized.")
        except Exception as e:
            print(f"DB Init Error: {e}")

@app.get("/")
async def read_root():
    # লাইভ কানেকশন চেক
    db_status = "Disconnected ❌"
    if client:
        try:
            await client.admin.command('ping')
            db_status = "Connected ✅"
        except:
            db_status = "Auth/Network Failed ⚠️"

    return {
        "project": "BaraQura V10",
        "database": db_status,
        "env_check": {
            "MONGO_URI": "Found" if MONGO_URI else "Missing",
            "SECRET_KEY": "Found" if SECRET_KEY else "Missing"
        },
        "time": str(datetime.datetime.now())
    }

# ডিবগ এন্ডপয়েন্ট
@app.get("/v10/test-connection")
async def test_conn():
    if not MONGO_URI:
        return {"error": "MONGO_URI missing in Vercel!"}
    try:
        temp_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        server_info = await temp_client.server_info()
        return {"status": "Online", "version": server_info.get('version')}
    except Exception as e:
        return {"status": "Offline", "error": str(e)}
