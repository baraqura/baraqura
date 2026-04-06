
from security.auth import login
from security.access_control import ask_permission
from security.logger import log

print("🔐 BaraQura AI Secure System Start")

user = input("Username: ")
password = input("Password: ")

if login(user, password):
    print("Login Successful ✅")
    log("User logged in")

    while True:
        action = input("Enter action (or 'exit'): ")

        if action == "exit":
            break

        if ask_permission(action):
            print(f"Executing: {action}")
            log(f"Executed: {action}")
        else:
            print("Blocked 🚫")
            log(f"Blocked: {action}")

else:
    print("Login Failed ❌")
    log("Failed login attempt")

if action == "STOP":
    print("SYSTEM SHUTDOWN 🚨")
    log("System stopped by admin")
    break

from ai.brain import respond

# inside loop
response = respond(action)
print("AI:", response)
