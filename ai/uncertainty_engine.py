import logging
from typing import Dict

logger = logging.getLogger("BaraQura-UE")

class UncertaintyEngine:
    def __init__(self, confidence_threshold: float = 0.6):
        # এই থ্রেশহোল্ডের নিচে গেলেই এআই ইউজারকে প্রশ্ন করবে
        self.threshold = confidence_threshold

    def evaluate_intent(self, intent_data: Dict) -> bool:
        """ইনটেন্টের কনফিডেন্স লেভেল চেক করা"""
        
        confidence = intent_data.get("confidence", 0.0)
        
        if confidence < self.threshold:
            logger.warning(f"⚠️ Low confidence detected: {confidence}. Triggering clarification.")
            return False  # অনিশ্চিত
        
        return True  # নিশ্চিত

    def get_clarification_prompt(self) -> str:
        """অনিশ্চিত অবস্থায় ইউজারকে জিজ্ঞাসা করার ইনস্ট্রাকশন"""
        
        return """
        I am not 100% sure what you meant. 
        Could you please clarify so I can assist you better? 
        I want to make sure I provide the most accurate solution for your office task.
        """

# আনসার্টেনিটি ইঞ্জিন অবজেক্ট তৈরি
ue_engine = UncertaintyEngine()
