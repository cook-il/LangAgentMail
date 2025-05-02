import sqlite3
import os
from datetime import datetime, timezone

# Database location: ../data/mailstore.db
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "mailstore.db"))

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                subject TEXT,
                body TEXT,
                status TEXT DEFAULT 'pending',
                tag TEXT,
                archived_at TEXT,
                received_at TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                recipient TEXT NOT NULL,
                subject TEXT,
                reply_body TEXT NOT NULL,
                status TEXT DEFAULT 'queued',
                created_at TEXT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES messages(id)
            );
        """)

        conn.commit()

def store_message(sender, subject, received_at, body):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (sender, subject, received_at, body)
            VALUES (?, ?, ?, ?)
        """, (sender, subject, received_at, body))
        conn.commit()

def get_pending_messages():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, sender, subject, body
            FROM messages
            WHERE status = 'pending'
        """)
        return cursor.fetchall()

def mark_as_processed(message_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages
            SET status = 'processed'
            WHERE id = ?
        """, (message_id,))
        conn.commit()

def queue_reply(message_id, recipient, subject, reply_body, created_at):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO replies (message_id, recipient, subject, reply_body, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (message_id, recipient, subject, reply_body, created_at))
        conn.commit()

def get_queued_replies():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, recipient, subject, reply_body
            FROM replies
            WHERE status = 'queued'
        """)
        return cursor.fetchall()

def mark_reply_sent(reply_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE replies
            SET status = 'sent'
            WHERE id = ?
        """, (reply_id,))
        conn.commit()

def tag_message(msg_id, tag):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages
            SET tag = ?
            WHERE id = ?
        """, (tag, msg_id))
        conn.commit()

def archive_message(msg_id, tag=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages
            SET status = 'archived',
                archived_at = ?,
                tag = COALESCE(?, tag)
            WHERE id = ?
        """, (datetime.now(timezone.utc).isoformat(), tag, msg_id))
        conn.commit()

def archive_all_from_sender(sender_email):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        tag = f"mine-{sender_email.split('@')[0]}"
        now = datetime.now(timezone.utc).isoformat()

        cursor.execute("""
            UPDATE messages
            SET status = 'archived',
                archived_at = ?,
                tag = COALESCE(?, tag)
            WHERE sender LIKE ?
              AND status != 'archived'
        """, (now, tag, f"%{sender_email}%"))

        conn.commit()
        return cursor.rowcount  # number of rows archived

def get_message_history(sender, limit=5):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT body FROM messages
            WHERE sender LIKE ?
              AND status = 'archived'
              AND body IS NOT NULL
            ORDER BY received_at DESC
            LIMIT ?
        """, (f"%{sender}%", limit))
        rows = cursor.fetchall()
        return [r[0] for r in rows]
