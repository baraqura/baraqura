import sys
import os

# আপনার মেইন ফোল্ডার পাথ সেট করা
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# এখানে 'main' এর পরে স্পেস হবে, ডট নয়
from app.core.main import app
