import uuid, time, os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.config.db import connect_to_mongo, db_instance
from src.modules.ai.engine import get_ai_response

app = FastAPI(title="V10 Sentinel")

# CORS Setup
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Middleware: Request ID & Tracker
@app.middleware("http")
async def sentinel_tracker(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.get("/")
async def status():
    return {"status": "Online", "module": "V10 Sentinel Core", "db": db_instance.db is not None}

@app.post("/chat")
async def chat(data: dict):
    user_msg = data.get("message", "")
    reply = get_ai_response(user_msg)
    return {"ai_response": reply, "status": "SECURED"}

# Vercel Handler
app = app
