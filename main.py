# ================================
# 🔐 BaraQura AI - All in One File
# ================================

# 🔹 json → memory save/load করার জন্য
import json

# 🔹 os → file আছে কিনা check করার জন্য
import os

# 🔹 datetime → log এ সময় save করার জন্য
import datetime


# ================================
# 🔐 AUTH SYSTEM (Login)
# ================================
def login(user, password):
    # 👉 simple login check (future এ database হবে)
    if user == "admin" and password == "1234":
        return True
    return False


# ================================
# 🔐 PERMISSION SYSTEM
# ================================
def ask_permission(action):
    # 👉 action execute করার আগে user কে জিজ্ঞাসা করবে
    choice = input(f"Allow '{action}'? (yes/no): ")
    return choice.lower() == "yes"


# ================================
# 🧾 LOGGING SYSTEM
# ================================
def log(message):
    # 👉 logs folder না থাকলে create করবে
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 👉 log file এ message লিখবে
    with open("logs/system.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")


# ================================
# 🧠 AI BRAIN (Basic)
# ================================
def respond(msg):
    msg = msg.lower()

    # 👉 simple keyword-based response
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

# 👉 memory file path
MEMORY_FILE = "memory.json"


# 🔹 memory load
def load_memory():
    # 👉 file না থাকলে empty memory
    if not os.path.exists(MEMORY_FILE):
        return {}
    
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


# 🔹 memory save
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


# 🔹 memory থেকে answer খোঁজা
def get_answer(question):
    memory = load_memory()
    return memory.get(question.lower())


# 🔹 memory add করা
def add_memory(question, answer):
    memory = load_memory()
    memory[question.lower()] = answer
    save_memory(memory)


# ================================
# 🚀 MAIN SYSTEM START
# ================================

print("🔐 BaraQura AI Secure System Start")

# 🔐 login input
user = input("Username: ")
password = input("Password: ")

# ❌ login fail হলে exit
if not login(user, password):
    print("Login Failed ❌")
    log("Failed login attempt")
    exit()

# ✅ login success
print("Login Successful ✅")
log("User logged in")


# ================================
# 🔁 MAIN LOOP (AI run)
# ================================
while True:
    action = input("Enter action (or 'exit'): ")

    # ❌ exit
    if action.lower() == "exit":
        print("Goodbye 👋")
        break

    # 🔴 kill switch
    if action.upper() == "STOP":
        print("SYSTEM SHUTDOWN 🚨")
        log("System stopped by admin")
        break

    # 🔐 permission check
    if not ask_permission(action):
        print("Blocked 🚫")
        log(f"Blocked: {action}")
        continue

    # ✅ execute allowed
    print(f"Executing: {action}")
    log(f"Executed: {action}")

    # 🧠 Step 1: memory check
    memory_answer = get_answer(action)

    if memory_answer:
        # 👉 memory থেকে answer
        print("AI (Memory):", memory_answer)
        log(f"Memory used: {action}")

    else:
        # 🤖 AI brain response
        response = respond(action)
        print("AI:", response)

        # 💾 save করার permission
        save = input("Save this response to memory? (yes/no): ")

        if save.lower() == "yes":
            add_memory(action, response)
            print("Saved to memory ✅")
            log(f"Saved: {action}")
        else:
            log(f"Not saved: {action}")
