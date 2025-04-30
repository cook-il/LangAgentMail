# LangChainMail

A lightweight, cron-invoked email agent that reads incoming questions from info@cook-il.us and replies via ai@cook-il.us using YunoHost's SMTP relay.

## Structure

- `config/email_settings.py` - Mail credentials and connection settings.
- `scripts/fetch_and_reply.py` - Main agent that pulls mail and sends replies.
- `scripts/process_email.py` - Placeholder for LangChain-based AI response logic.
- `logs/email.log` - Output log for monitoring.
