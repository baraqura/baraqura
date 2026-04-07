import httpx
import logging
from config.settings import settings

logger = logging.getLogger("BaraQura-Grok")

class GrokAPI:
    def __init__(self):
        self.api_key = settings.GROK_API_KEY
        self.base_url = "https://api.x.ai/v1/chat/completions" # এক্স-এআই এর স্ট্যান্ডার্ড এন্ডপয়েন্ট

    async def ask_grok(self, prompt: str, system_message: str = "You are a logical business expert."):
        """Grok AI থেকে উত্তর নিয়ে আসা (Primary Backup)"""
        if not self.api_key:
            logger.error("❌ Grok API Key missing!")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "grok-beta", # অথবা লেটেস্ট মডেল নাম
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, headers=headers, json=payload, timeout=30.0)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    logger.warning(f"⚠️ Grok API returned error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Grok Connection Error: {e}")
            return None

# গ্রোক এপিআই অবজেক্ট তৈরি
grok = GrokAPI()
