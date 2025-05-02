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

def get_memory(sender, key):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value FROM memory
            WHERE sender = ? AND key = ?
            ORDER BY created_at DESC LIMIT 1
        """, (sender, key.strip()))
        row = cursor.fetchone()
        return row[0] if row else None

def list_keys(sender):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT key FROM memory
            WHERE sender = ?
            ORDER BY key ASC
        """, (sender,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

def forget_key(sender, key):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM memory WHERE sender = ? AND key = ?
        """, (sender, key.strip()))
        conn.commit()
        return cursor.rowcount  # returns # of deleted rows
