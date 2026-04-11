# ai/engine.py

class SentinelEngine:
    def __init__(self):
        self.threat_logs = []
        self.clone_memory = []

    def scan_security_feed(self, incoming_data):
        # হ্যাকার চেক করার লজিক
        if "attack" in incoming_data:
            self.threat_logs.append(incoming_data)
            return "THREAT_BLOCKED"
        return "SAFE"

    def recall_clone_memory(self):
        # ক্লোন এর মেমরি রি-কল
        return self.clone_memory

# ইঞ্জিন স্টার্ট
engine = SentinelEngine()
