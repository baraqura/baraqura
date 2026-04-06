def respond(msg):
    msg = msg.lower()

    if "price" in msg:
        return "Our price is best for quality."
    elif "buy" in msg:
        return "Great! Let's proceed with your order."
    else:
        return "Tell me more."
