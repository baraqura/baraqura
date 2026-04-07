import logging
from config.settings import settings
from ai.intent_detector import detector
from ai.persona_engine import persona_engine
from ai.uncertainty_engine import ue_engine
import google.generativeai as genai

logger = logging.getLogger("BaraQura-Brain")

# Gemini কনফিগারেশন
genai.configure(api_key=settings.GEMINI_API_KEY)

class BaraQuraBrain:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    async def process_message(self, user_input: str, context: dict = None) -> str:
        """ইউজারের মেসেজ প্রসেস করে ফাইনাল আউটপুট জেনারেট করা"""
        
        try:
            # ১. ইনটেন্ট এবং ইমোশন ডিটেকশন
            intent_data = await detector.analyze(user_input)
            
            # ২. কনফিডেন্স চেক (Uncertainty Engine)
            is_confident = ue_engine.evaluate_intent(intent_data)
            
            if not is_confident:
                return ue_engine.get_clarification_prompt()

            # ৩. পারসোনা নির্বাচন
            selected_persona = persona_engine.select_persona(intent_data)
            style_instruction = persona_engine.get_style_instruction(selected_persona)

            # ৪. ফাইনাল প্রম্পট তৈরি (Cognitive Layer)
            system_instruction = f"""
            ROLE: BaraQura Office Intelligence
            PERSONA: {selected_persona}
            STYLE: {style_instruction}
            CONTEXT: {context if context else 'No previous context'}
            USER INTENT: {intent_data.get('intent')}
            USER EMOTION: {intent_data.get('emotion')}
            
            INSTRUCTION: Respond to the user naturally based on their intent and emotion. 
            If it's a sales query, use persuasive language. 
            If it's technical, be precise.
            """

            # ৫. এলএলএম দিয়ে রেসপন্স জেনারেট করা
            response = self.model.generate_content([system_instruction, user_input])
            
            logger.info(f"✅ Brain processed message with persona: {selected_persona}")
            return response.text

        except Exception as e:
            logger.error(f"Brain Execution Error: {e}")
            return "⚠️ দুঃখিত, সিস্টেমে একটি ছোট সমস্যা হয়েছে। আমি আপনার বার্তাটি ঠিকমতো প্রসেস করতে পারছি না।"

# মেইন ব্রেইন অবজেক্ট তৈরি
brain = BaraQuraBrain()
