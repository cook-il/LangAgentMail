import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import imaplib
import email
from email.message import EmailMessage
from datetime import datetime

from config.email_settings import *
from scripts.mail_store import init_db, store_message
from scripts.process_email import extract_clean_text

def process_inbox():
    init_db()
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')
    if status != "OK":
        print("No unread messages.")
        return

    for num in messages[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        sender = msg["From"]
        subject = msg["Subject"] or "(no subject)"
        clean_subject = subject.replace('\n', ' ').replace('\r', ' ').strip()
        from datetime import datetime, timezone
        timestamp = datetime.now(timezone.utc).isoformat()


        body = extract_clean_text(msg)

        store_message(sender, clean_subject, timestamp, body)

        # Mark message as seen
        mail.store(num, '+FLAGS', '\\Seen')

    mail.logout()

if __name__ == "__main__":
    process_inbox()
