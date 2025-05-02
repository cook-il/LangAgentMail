import sqlite3
import os

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
                received_at TEXT NOT NULL,
                raw_body TEXT,
                status TEXT DEFAULT 'pending'
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

def store_message(sender, subject, received_at, raw_body):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (sender, subject, received_at, raw_body)
            VALUES (?, ?, ?, ?)
        """, (sender, subject, received_at, raw_body))
        conn.commit()

def get_pending_messages():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, sender, subject, raw_body
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
