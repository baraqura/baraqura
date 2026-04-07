import logging
import google.generativeai as genai
from config.settings import settings
from ai.intent_detector import detector
from ai.persona_engine import persona_engine
from ai.uncertainty_engine import ue_engine

logger = logging.getLogger("BaraQura-Brain-Tuned")

genai.configure(api_key=settings.GEMINI_API_KEY)

class BaraQuraBrain:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def process_message(self, user_input: str, context: str = "") -> str:
        try:
            # ১. ইনটেন্ট ও ইমোশন ডিটেকশন
            intent_data = await detector.analyze(user_input)
            
            # ২. আনসার্টেনিটি চেক
            if not ue_engine.evaluate_intent(intent_data):
                return ue_engine.get_clarification_prompt()

            # ৩. পারসোনা ও সেলস লজিক ট্রিগার
            persona = persona_engine.select_persona(intent_data)
            emotion = intent_data.get("emotion", "neutral")
            
            # ৪. সেলস হায়ারার্কি ইনজেকশন (আপনার দেওয়া ৫টি পিলার)
            sales_priority = """
            1. Urgency: If closing is near, emphasize limited time.
            2. Fear of Loss: Highlight what they miss by not choosing us.
            3. Risk Reversal: Offer guarantees or safety.
            4. ROI: Show logical profit/benefit.
            5. Social Proof: Mention success and trust.
            """

            # ৫. অ্যাডাপ্টিভ বিহেভিয়ার গাইডলাইন
            behavior_guide = {
                "skeptical": "Focus on Proof + Data (Analyst Mode).",
                "excited": "Move fast to close (Urgency + Driver Mode).",
                "fearful": "Focus on Risk Reversal & Assurance.",
                "confused": "Simplify the solution, don't push hard."
            }.get(emotion.lower(), "Be helpful and build trust.")

            # ৬. ফাইনাল সিস্টেম প্রম্পট (The Sales Weapon)
            system_instruction = f"""
            ROLE: BaraQura Master Sales AI
            CURRENT PERSONA: {persona}
            CUSTOMER EMOTION: {emotion}
            SALES HIERARCHY: {sales_priority}
            BEHAVIOR GUIDE: {behavior_guide}
            CONTEXT: {context}
            
            INSTRUCTION: Use the Sales Hierarchy to guide the customer through a psychological journey. 
            Do not just 'sell'; make them feel it is their best 'decision'. 
            If they move back in the funnel, reactivate trust triggers.
            """

            response = self.model.generate_content([system_instruction, user_input])
            return response.text

        except Exception as e:
            logger.error(f"Brain Tuning Error: {e}")
            return "⚠️ সিস্টেমে সাময়িক সমস্যা। আমি আপনার রিকোয়েস্টটি প্রসেস করতে পারছি না।"

brain = BaraQuraBrain()
