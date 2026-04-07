import openai
import logging
from config.settings import settings

logger = logging.getLogger("BaraQura-OpenAI-Fallback")

class OpenAIFallbackAPI:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
        else:
            logger.error("❌ OpenAI API Key missing in Settings!")

    async def ask_openai(self, prompt: str, system_instruction: str = "You are a helpful office assistant."):
        """OpenAI (GPT-4o/3.5) থেকে উত্তর নিয়ে আসা (Final Backup Layer)"""
        if not self.api_key:
            return None

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini", # কস্ট-ইফেক্টিভ এবং ফাস্ট ব্যাকআপ হিসেবে সেরা
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            if response.choices[0].message.content:
                return response.choices[0].message.content
            return None
                
        except Exception as e:
            logger.error(f"OpenAI Fallback Error: {e}")
            return None

# ওপেনএআই ব্যাকআপ অবজেক্ট তৈরি
openai_fallback = OpenAIFallbackAPI()
