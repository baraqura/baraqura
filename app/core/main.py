from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
import datetime
import logging

# লগিং সেটআপ যাতে এরর বোঝা যায়
logger = logging.getLogger("v10_debug")

try:
    from app.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance
except ImportError:
    from App.db.mongodb import connect_to_mongo, close_mongo_connection, db_instance

app = FastAPI()

# ভার্সেল থেকে ভেরিয়েবল রিড করা
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI") # নিশ্চিত করো ভার্সেলে এই নামেই আছে

@app.on_event("startup")
async def startup_event():
    # মঙ্গোডিবি কানেকশন ট্রাই করা
    try:
        await connect_to_mongo()
        print("V10: Database Connection Attempted")
    except Exception as e:
        logger.error(f"DB Connection Error: {e}")

@app.get("/")
def read_root():
    # কানেকশন স্ট্যাটাস চেক করার সহজ উপায়
    db_alive = False
    try:
        if db_instance.client:
            db_alive = True
    except:
        pass
        
    return {
        "message": "BaraQura AI V10",
        "database_connected": db_alive,
        "env_key_found": SECRET_KEY is not None,
        "mongo_uri_found": MONGO_URI is not None,
        "timestamp": str(datetime.datetime.now())
    }

# --- স্পেশাল ডিবগ লিঙ্ক (এটা চেক করলেই বুঝবো সমস্যা কোথায়) ---
@app.get("/v10/fix-db")
async def fix_db():
    import motor.motor_asyncio
    try:
        if not MONGO_URI:
            return {"error": "MONGO_URI missing in Vercel settings!"}
        
        # সরাসরি টেস্ট কানেকশন
        test_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        info = await test_client.server_info() # এটা কানেকশন চেক করে
        
        return {
            "status": "Success ✅",
            "server_info": "Connected to MongoDB Atlas",
            "db_version": info.get('version')
        }
    except Exception as e:
        return {
            "status": "Failed ❌",
            "error_message": str(e),
            "advice": "Check if IP 0.0.0.0/0 is allowed in MongoDB Atlas Network Access"
        }

# তোমার পুরনো চ্যাট এন্ডপয়েন্ট আগের মতোই থাকবে
class ChatInput(BaseModel):
    message: str
    master_key: str = None

@app.post("/chat")
async def chat(data: ChatInput):
    if data.master_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Key")
    return {"ai_response": "Engine is stabilizing. Check /v10/fix-db first."}
