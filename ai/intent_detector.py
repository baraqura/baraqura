import google.generativeai as genai
import json
import re
import logging
from config.settings import settings

logger = logging.getLogger("BaraQura-Intent")

# Gemini API কনফিগারেশন
genai.configure(api_key=settings.GEMINI_API_KEY)

class IntentDetector:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    async def analyze(self, user_input: str) -> dict:
        """ইউজারের ইনপুট থেকে ইনটেন্ট, কনফিডেন্স এবং ইমোশন বের করা"""
        
        prompt = f"""
        Analyze this user message: "{user_input}"
        Identify:
        1. intent: (e.g., sales_query, general_info, complain, pricing, closing)
        2. confidence: (0.0 to 1.0)
        3. emotion: (e.g., excited, skeptical, angry, neutral)
        4. urgency: (high, medium, low)

        Return ONLY a clean JSON object like this:
        {{"intent": "string", "confidence": float, "emotion": "string", "urgency": "string"}}
        """

        try:
            # AI রেসপন্স জেনারেট করা
            response = self.model.generate_content(prompt)
            
            # JSON এক্সট্রাক্ট করা (রেগুলার এক্সপ্রেশন দিয়ে নিরাপদ রাখা)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {
                "intent": "unknown", 
                "confidence": 0.0, 
                "emotion": "neutral", 
                "urgency": "low"
            }
            
        except Exception as e:
            logger.error(f"Intent Detection Error: {e}")
            return {"error": "Failed to detect intent"}

# ইনটেন্ট ডিটেক্টর অবজেক্ট তৈরি
detector = IntentDetector()
