import sys
import os

# পাথ সেট করা
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# এখানে ডট হবে না, স্পেস হবে
from app.core.main import app
