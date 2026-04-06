def ask_permission(action):
    choice = input(f"Allow '{action}'? (yes/no): ")
    return choice.lower() == "yes"
