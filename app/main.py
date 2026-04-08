import uuid
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings

# ১. সেটিংস লোড করা
settings = get_settings()

# ২. FastAPI অ্যাপ ইনিশিয়ালাইজ করা
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# ৩. CORS সেটআপ (Vercel ও অন্যান্য ফ্রন্টএন্ডের জন্য)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ৪. Unique Request ID Middleware (আপনার ১১.৮% এরর ধরার অস্ত্র)
@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    # প্রতিটা রিকোয়েস্টের জন্য একটা ইউনিক আইডি তৈরি হচ্ছে
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    
    # রিকোয়েস্ট প্রসেস করা
    response = await call_next(request)
    
    # রেসপন্স হেডারে আইডি এবং প্রসেসিং টাইম যোগ করা (ট্র্যাকিংয়ের জন্য)
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# ৫. বেসিক রুট (সিস্টেম চেক করার জন্য)
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "BaraQura V10 AI OS is running",
        "version": "1.0.0"
    }

# ৬. হেলথ চেক এন্ডপয়েন্ট
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}
