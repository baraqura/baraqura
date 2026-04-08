import sys
import os

# পাইথনকে আপনার বর্তমান ফোল্ডার পাথ চিনিয়ে দেওয়া
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# এবার ভেতরের মেইন অ্যাপ ইমপোর্ট করা
from app.core.main import app
