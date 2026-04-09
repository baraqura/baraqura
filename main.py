import sys
import os

# পাইথনকে পাথ চিনিয়ে দেওয়া
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ভেতরের অ্যাপ ইমপোর্ট করা
try:
    from app.core.main import app
except ImportError as e:
    print(f"Import Error: {e}")
    raise e
