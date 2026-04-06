import json
import os

MEMORY_FILE = "ai/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def get_answer(question):
    memory = load_memory()
    return memory.get(question.lower())

def add_memory(question, answer):
    memory = load_memory()
    memory[question.lower()] = answer
    save_memory(memory)
