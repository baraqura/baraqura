# ================================
# 🔐 BaraQura AI - All in One File
# ================================

import json
import os
import datetime
import subprocess
import sys


# ================================
# 🔐 AUTH SYSTEM (Login)
# ================================
def login(user, password):
    if user == "admin" and password == "1234":
        return True
    return False


# ================================
# 🔐 PERMISSION SYSTEM
# ================================
def ask_permission(action):
    choice = input(f"Allow '{action}'? (yes/no): ")
    return choice.lower() == "yes"


# ================================
# 🧾 LOGGING SYSTEM
# ================================
def log(message):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open("logs/system.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")


# ================================
# 🧠 AI BRAIN
# ================================
def respond(msg):
    msg = msg.lower()

    if "price" in msg:
        return "Our price is best for quality."

    elif "buy" in msg:
        return "Great! Let's proceed with your order."

    elif "delivery" in msg:
        return "We provide fast delivery service."

    else:
        return "Tell me more about your need."


# ================================
# 💾 MEMORY SYSTEM
# ================================
MEMORY_FILE = "memory.json"


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


# ================================
# 🚀 MAIN SYSTEM START
# ================================
print("🔐 BaraQura AI Secure System Start")

user = input("Username: ")
password = input("Password: ")

if not login(user, password):
    print("Login Failed ❌")
    log("Failed login attempt")
    exit()

print("Login Successful ✅")
log("User logged in")


# ================================
# 🔁 MAIN LOOP
# ================================
while True:
    action = input("Enter action (or 'exit'): ")

    if action.lower() == "exit":
        print("Goodbye 👋")
        break

    if action.upper() == "STOP":
        print("SYSTEM SHUTDOWN 🚨")
        log("System stopped by admin")
        break

    if not ask_permission(action):
        print("Blocked 🚫")
        log(f"Blocked: {action}")
        continue

    print(f"Executing: {action}")
    log(f"Executed: {action}")

    memory_answer = get_answer(action)

    if memory_answer:
        print("AI (Memory):", memory_answer)
        log(f"Memory used: {action}")
    else:
        response = respond(action)
        print("AI:", response)

        save = input("Save this response to memory? (yes/no): ")

        if save.lower() == "yes":
            add_memory(action, response)
            print("Saved to memory ✅")
            log(f"Saved: {action}")
        else:
            log(f"Not saved: {action}")



