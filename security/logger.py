import datetime

def log(message):
    with open("logs/system.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")
