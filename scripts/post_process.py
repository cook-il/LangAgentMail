import sys
import os
from datetime import datetime, timezone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.langchain_agent.agent_core import generate_langchain_response
from scripts.mail_store import get_message_history
from scripts.memory_store import store_memory, get_memory, list_keys


from scripts.mail_store import (
    get_pending_messages,
    mark_as_processed,
    queue_reply,
    archive_all_from_sender,
    get_message_history,
    archive_message,
)

from scripts.command_parser import detect_commands, generate_response, is_allowed_sender

def run_post_processing():
    messages = get_pending_messages()
    print(f"Found {len(messages)} pending messages.\n")

    for msg_id, sender, subject, body in messages:
        print(f" ID {msg_id} | From: {sender} | Subject: {subject[:60]}")
        print(f"Preview: {body[:200]}...\n")

        if not is_allowed_sender(sender):
            print(f"[BLOCKED] Sender '{sender}' is not allowed to issue commands.\n")
            mark_as_processed(msg_id)
            continue

        commands = detect_commands(body)
        if commands:
            for command in commands:
                if command == "mine":
                    archived_count = archive_all_from_sender(sender)
                    reply_text = f"🗃 Archived {archived_count} messages from {sender}"

                elif command.startswith("tag:"):
                    tag_label = command.split(":", 1)[1]
                    archive_message(msg_id, tag=tag_label)
                    reply_text = f"🏷️ Message tagged as '{tag_label}' and archived."

                elif command in ["ask", "ai"]:
                    history = get_message_history(sender)
                    reply_text = generate_langchain_response(sender, body, history, subject=subject)

                elif command.startswith("remember "):
                    parts = command.split(" ", 1)[1].split(":", 1)
                    if len(parts) == 2:
                        key, value = parts
                        store_memory(sender, key, value)
                        reply_text = f"📝 Remembered '{key.strip()}' = \"{value.strip()}\""
                    else:
                        reply_text = "⚠️ Invalid format. Use /remember key: value"

                elif command.startswith("query "):
                    query_key = command.split(" ", 1)[1].strip()
                    value = get_memory(sender, query_key)
                    if value:
                        reply_text = f"📌 {query_key}: {value}"
                    else:
                       reply_text = f"🤔 No memory found for '{query_key}'."

                elif command == "recall":
                    keys = list_keys(sender)
                    if keys:
                        reply_text = "🧾 Stored keys:\n- " + "\n- ".join(keys)
                    else:
                        reply_text = "📭 You haven’t stored any memory yet."

                else:
                    reply_text = generate_response(command)

                print(f"[COMMAND: /{command}] Respond with:\n{reply_text}\n")

                queue_reply(
                    message_id=msg_id,
                    recipient=sender,
                    subject=f"Re: {subject.strip()}",
                    reply_body=reply_text,
                    created_at=datetime.now(timezone.utc).isoformat()
                )
        else:
            print(f"[No command detected in ID {msg_id}]")

        mark_as_processed(msg_id)

if __name__ == "__main__":
    run_post_processing()
