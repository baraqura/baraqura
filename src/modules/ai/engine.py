def get_ai_response(msg: str):
    msg = msg.lower()
    if "price" in msg:
        return "Our price is best for quality. (V10 Modular)"
    elif "buy" in msg:
        return "Great! Let's proceed with your order."
    elif "delivery" in msg:
        return "We provide fast delivery service."
    return "BaraQura V10 is thinking... Tell me more."
