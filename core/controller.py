import logging
from ai.memory import memory
from integrations.grok_api import grok
from integrations.gemini_api import gemini_pro
from integrations.openai_api import openai_fallback

logger = logging.getLogger("BaraQura-Controller")

class BusinessController:
    async def get_ai_response(self, user_id: str, prompt: str):
        """Tiered Intelligence Hierarchy Logic (Memory -> Grok -> Gemini -> OpenAI)"""
        
        # --- 1st Level: Local Memory (BaraQura DB) ---
        context = await memory.get_recent_history(user_id)
        # Note: এখানে আমরা মেমোরি থেকে কনটেক্সট নিচ্ছি উত্তরের জন্য।
        
        # --- 2nd Level: Grok AI (Primary) ---
        logger.info(f"🚀 Trying Grok for user: {user_id}")
        response = await grok.ask_grok(prompt, system_message=f"Context: {context}\nRole: Sales Manager")
        
        if response:
            await memory.save_interaction(user_id, prompt, response)
            return response

        # --- 3rd Level: Gemini 1.5 Pro (Secondary) ---
        logger.warning(f"⚠️ Grok failed. Trying Gemini 1.5 Pro for: {user_id}")
        response = await gemini_pro.ask_gemini_pro(prompt, system_instruction=f"Context: {context}")
        
        if response:
            await memory.save_interaction(user_id, prompt, response)
            return response

        # --- 4th Level: OpenAI (Tertiary/Final Backup) ---
        logger.error(f"❌ Gemini failed. Triggering Final OpenAI Fallback for: {user_id}")
        response = await openai_fallback.ask_openai(prompt)
        
        if response:
            await memory.save_interaction(user_id, prompt, response)
            return response

        # --- Final Fallback (If everything fails) ---
        return "⚠️ আমি বর্তমানে তথ্যটি খুঁজে পাচ্ছি না। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।"

# কন্ট্রোলার অবজেক্ট তৈরি
controller = BusinessController()
