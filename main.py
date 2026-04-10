import sys
import os

# আপনার কোডের পাথ চিনিয়ে দেওয়া
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.core.main import app

# ভেরসেলের জন্য অ্যাপ এক্সপোর্ট
app = app
