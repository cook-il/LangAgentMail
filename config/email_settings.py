import os

from dotenv import load_dotenv
import os

load_dotenv()  # Automatically load .env file

EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

IMAP_HOST = "cook-il.us"
IMAP_PORT = 993

SMTP_HOST = "cook-il.us"
SMTP_PORT = 587
SMTP_USE_TLS = True

FROM_ADDRESS = "aiagent@cook-il.us"
REPLY_TO = "info@cook-il.us"
