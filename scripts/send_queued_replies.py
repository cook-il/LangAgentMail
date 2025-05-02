import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import smtplib
from email.message import EmailMessage
from config.email_settings import *
from scripts.mail_store import get_queued_replies, mark_reply_sent

def send_all_queued():
    replies = get_queued_replies()
    print(f"Found {len(replies)} queued replies.")

    for reply_id, recipient, subject, body in replies:
        msg = EmailMessage()
        msg["From"] = FROM_ADDRESS
        msg["To"] = recipient
        msg["Subject"] = subject
        msg["Reply-To"] = REPLY_TO
        msg.set_content(body)

        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                if SMTP_USE_TLS:
                    server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f"✅ Sent reply to {recipient}")
                mark_reply_sent(reply_id)
        except Exception as e:
            print(f"❌ Failed to send reply to {recipient}: {e}")

if __name__ == "__main__":
    send_all_queued()
