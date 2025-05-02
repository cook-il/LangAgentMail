import re
from config.email_settings import ALLOWED_DOMAINS

def detect_commands(text):
    lines = text.lower().splitlines()
    commands = []
    for line in lines:
        line = line.strip()
        if line.startswith("/"):
            if "&&" in line or "||" in line:
                chain = [cmd.strip() for cmd in re.split(r"&&|\|\|", line)]
            else:
                chain = [line]

            for cmd in chain:
                cmd = cmd.strip().lstrip("/")
                if cmd.startswith("tag "):  # Normalize /tag <label> to tag:<label>
                    parts = cmd.split(" ", 1)
                    if len(parts) > 1:
                        commands.append(f"tag:{parts[1]}")
                else:
                    commands.append(cmd)
            break
    return commands


def generate_response(command):
    if command == "status":
        return "✅ LangAgentMail is online and responding to approved queries."
    elif command == "mine":
        return "🗃 Archiving all your messages. Please wait..."
    elif command == "help":
        return (
            "🆘 Available commands:\n"
            "  /status - Check system status\n"
            "  /help   - List available commands\n"
            "  /mine   - Archive all your previously sent messages\n"
            "  /ask    - Query AI with context-aware response\n"
            "  /tag <label> - Assign a tag to this message and archive it\n"
            "\n"
            "LangAgentMail v0.1.4 — Archiving and Tagging in progress.\n"
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