import sys
import os

try:
    # পথ চিনিয়ে দেওয়া
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from app.core.main import app
    print("V10 App loaded successfully!")
except Exception as e:
    print(f"ERROR LOCATED: {e}")
    # এটি ভুল খুঁজে পেতে সাহায্য করবে
    raise e
