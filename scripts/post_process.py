import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.mail_store import get_pending_messages, mark_as_processed
from scripts.command_parser import detect_command, generate_response

def run_post_processing():
    messages = get_pending_messages()
    print("Loaded messages:", messages)
    print(f"Found {len(messages)} pending messages.\n")

    for msg_id, sender, subject, body in messages:
        print(f"🔍 ID {msg_id} | From: {sender} | Subject: {subject[:60]}")
        print(f"Preview: {body[:200]}...\n")

        # Placeholder: Add filters, command parsing, etc.
        mark_as_processed(msg_id)

        command = detect_command(body)
        if command:
            reply_text = generate_response(command)
            print(f"[COMMAND: /{command}] Respond with:\n{reply_text}\n")
        else:
            print(f"[No command detected in ID {msg_id}]")

if __name__ == "__main__":
    run_post_processing()
