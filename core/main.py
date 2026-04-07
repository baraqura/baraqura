from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.controller import controller
from database.db import db
import uvicorn

# FastAPI অ্যাপ তৈরি
app = FastAPI(title="BaraQura V10 AI", version="10.0.0")

# ডাটা মডেল (ইউজার কী পাঠাবে)
class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.on_event("startup")
async def startup_db_client():
    # অ্যাপ শুরু হওয়ার সময় ডেটাবেস কানেক্ট করা
    await db.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    # অ্যাপ বন্ধ হওয়ার সময় কানেকশন অফ করা
    await db.close_mongo_connection()

@app.get("/")
async def root():
    return {"status": "online", "message": "BaraQura V10 Brain is Active!"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """এআই-এর সাথে কথা বলার মেইন এন্ডপয়েন্ট"""
    try:
        response = await controller.get_ai_response(request.user_id, request.message)
        return {"user_id": request.user_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# সরাসরি রান করার জন্য
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
