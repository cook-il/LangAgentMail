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
        return (
        "🆘 Available commands:\n"
        "  /status - Check system status\n"
        "  /help   - List available commands\n"
        "\n"
        "Email info@cook-il.us with questions or suggestions."
    )

    return "❓ Unknown command."
