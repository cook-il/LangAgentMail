import sqlite3
import os

# Database location: ../data/mailstore.db
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mailstore.db")

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
        conn.commit()

def store_message(sender, subject, received_at, raw_body):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (sender, subject, received_at, raw_body)
            VALUES (?, ?, ?, ?)
        """, (sender, subject, received_at, raw_body))
        conn.commit()
