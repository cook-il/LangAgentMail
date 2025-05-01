def detect_command(text):
    """Return the normalized command if found, else None."""
    lines = text.lower().splitlines()
    for line in lines:
        if line.strip().startswith("/status"):
            return "status"
        elif line.strip().startswith("/help"):
            return "help"
    return None

def generate_response(command):
    if command == "status":
        return "✅ LangAgentMail is online and responding to approved queries."
    elif command == "help":
        return "🆘 Available commands: /status, /help\nSend email to info@cook-il.us"
    return "❓ Unknown command."
