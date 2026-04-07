import logging
from typing import Dict

logger = logging.getLogger("BaraQura-Persona")

class PersonaEngine:
    def __init__(self):
        # ডিফল্ট পারসোনা: Amiable (বন্ধুসুলভ)
        self.current_persona = "Amiable"

    def select_persona(self, intent_data: Dict) -> str:
        """ইনটেন্ট এবং ইমোশন অনুযায়ী সঠিক ব্যক্তিত্ব নির্বাচন করা"""
        
        intent = intent_data.get("intent", "general_info").lower()
        emotion = intent_data.get("emotion", "neutral").lower()
        urgency = intent_data.get("urgency", "low").lower()

        # 🧠 লজিক ১: The Analyst (যদি তথ্য বা ROI নিয়ে কথা হয়)
        if "pricing" in intent or "info" in intent or emotion == "skeptical":
            self.current_persona = "Analyst"
        
        # 🚀 লজিক ২: The Driver (যদি কাজ খুব জরুরি হয় বা সরাসরি ক্লোজিং চায়)
        elif urgency == "high" or intent == "closing":
            self.current_persona = "Driver"
        
        # 😍 লজিক ৩: The Expressive (যদি কাস্টমার খুব এক্সাইটেড থাকে)
        elif emotion == "excited":
            self.current_persona = "Expressive"
        
        # 🤝 লজিক ৪: The Amiable (অন্য সব সাধারণ ক্ষেত্রে)
        else:
            self.current_persona = "Amiable"

        logger.info(f"🎭 Persona Selected: {self.current_persona}")
        return self.current_persona

    def get_style_instruction(self, persona: str) -> str:
        """এলএলএম-এর জন্য পারসোনা ভিত্তিক গাইডলাইন"""
        
        styles = {
            "Analyst": "Be data-driven, use facts, comparisons, and ROI. Stay logical and precise.",
            "Driver": "Be fast-paced, result-oriented, and decisive. Create urgency and focus on closing.",
            "Expressive": "Be energetic, visionary, and focus on the overall experience and success story.",
            "Amiable": "Be supportive, friendly, and empathetic. Focus on building trust and long-term relationship."
        }
        return styles.get(persona, styles["Amiable"])

# পারসোনা ইঞ্জিন অবজেক্ট তৈরি
persona_engine = PersonaEngine()
