import re
from config.email_settings import ALLOWED_DOMAINS

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

def is_allowed_sender(sender):
    match = re.search(r'<([^>]+)>', sender)
    email = match.group(1) if match else sender

    if "@" not in email:
        return False

    domain = email.split("@")[-1].lower()
    return any(domain.endswith(allowed) for allowed in ALLOWED_DOMAINS)