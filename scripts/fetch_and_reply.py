import sys
import os
import imaplib
import smtplib
import email
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from email.message import EmailMessage
from config.email_settings import *
from scripts.process_email import generate_response

def connect_imap():
    M = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    return M


def connect_smtp():
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    if SMTP_USE_TLS:
        server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    return server


def process_inbox():
    imap = connect_imap()
    imap.select("INBOX")
    typ, data = imap.search(None, 'UNSEEN')
    for num in data[0].split():
        typ, msg_data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        from_address = email.utils.parseaddr(msg['From'])[1]
        subject = msg.get("Subject", "(No Subject)")

        # Safer multipart/plain text parsing
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    break
            else:
                body = "[No plain text body found]"
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

        response = generate_response(subject, body)

        reply = EmailMessage()
        reply["Subject"] = f"Re: {subject}"
        reply["From"] = FROM_ADDRESS
        reply["To"] = from_address
        reply["Reply-To"] = REPLY_TO
        reply.set_content(response)

        smtp = connect_smtp()
        smtp.send_message(reply)
        smtp.quit()

        # Mark message as seen
        imap.store(num, '+FLAGS', '\\Seen')

    imap.logout()


if __name__ == "__main__":
    process_inbox()
import imaplib
import smtplib
import email
from email.message import EmailMessage
from config.email_settings import *
from scripts.process_email import generate_response


def connect_imap():
    M = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    return M


def connect_smtp():
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    if SMTP_USE_TLS:
        server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    return server


def process_inbox():
    imap = connect_imap()
    imap.select("INBOX")
    typ, data = imap.search(None, 'UNSEEN')
    for num in data[0].split():
        typ, msg_data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        from_address = email.utils.parseaddr(msg['From'])[1]
        subject = msg.get("Subject", "(No Subject)")

        # Safer multipart/plain text parsing
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    break
            else:
                body = "[No plain text body found]"
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

        response = generate_response(subject, body)

        reply = EmailMessage()
        reply["Subject"] = f"Re: {subject}"
        reply["From"] = FROM_ADDRESS
        reply["To"] = from_address
        reply["Reply-To"] = REPLY_TO
        reply.set_content(response)

        smtp = connect_smtp()
        smtp.send_message(reply)
        smtp.quit()

        # Mark message as seen
        imap.store(num, '+FLAGS', '\\Seen')

    imap.logout()


if __name__ == "__main__":
    process_inbox()

