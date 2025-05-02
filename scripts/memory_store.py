import sqlite3
from datetime import datetime, timezone
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'mailstore.db')

def init_memory_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                key TEXT,
                value TEXT,
                created_at TEXT
            )
        """)
        conn.commit()

def store_memory(sender, key, value):
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO memory (sender, key, value, created_at)
            VALUES (?, ?, ?, ?)
        """, (sender, key.strip(), value.strip(), datetime.now(timezone.utc).isoformat()))
        conn.commit()
