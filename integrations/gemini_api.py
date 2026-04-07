import google.generativeai as genai
import logging
from config.settings import settings

logger = logging.getLogger("BaraQura-Gemini-Pro")

class GeminiProAPI:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # আমরা এখানে নির্দিষ্টভাবে 1.5 pro মডেলটি কল করছি
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            logger.error("❌ Gemini API Key missing in Settings!")

    async def ask_gemini_pro(self, prompt: str, system_instruction: str = None):
        """Gemini 1.5 Pro থেকে উত্তর নিয়ে আসা (Secondary Backup)"""
        if not self.api_key:
            return None

        try:
            # যদি সিস্টেম ইনস্ট্রাকশন থাকে তবে সেটা সহ পাঠানো
            full_prompt = f"{system_instruction}\n\nUser Question: {prompt}" if system_instruction else prompt
            
            response = await self.model.generate_content_async(full_prompt)
            
            if response and response.text:
                return response.text
            else:
                logger.warning("⚠️ Gemini 1.5 Pro returned an empty response.")
                return None
                
        except Exception as e:
            logger.error(f"Gemini 1.5 Pro Error: {e}")
            return None

# জেমিনি প্রো এপিআই অবজেক্ট তৈরি
gemini_pro = GeminiProAPI()
