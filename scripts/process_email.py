# scripts/process_email.py

import re
from bs4 import BeautifulSoup
from email.message import EmailMessage

# Regex pattern to strip full URLs starting with common protocols
URL_PATTERN = re.compile(r'<https://[^>]+>')

def extract_clean_text(msg: EmailMessage) -> str:
    """
    Extract and normalize text from an email message.
    Strips HTML, removes script/style blocks, and strips all URLs.
    """
    def strip_urls(text):
        return URL_PATTERN.sub('[URL removed]', text)

    def extract_from_html(html):
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        return strip_urls(text.strip())

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True).decode(errors="replace")
                return strip_urls(payload.strip())
            elif content_type == "text/html":
                html = part.get_payload(decode=True).decode(errors="replace")
                return extract_from_html(html)
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True).decode(errors="replace")
        if content_type == "text/plain":
            return strip_urls(payload.strip())
        elif content_type == "text/html":
            return extract_from_html(payload)

    return "[No readable content found]"

