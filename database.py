import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("thrive.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_reflection(user_id, rtype, message):
    conn = sqlite3.connect("thrive.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reflections (user_id, type, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, rtype, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_week_summary(user_id):
    conn = sqlite3.connect("thrive.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, message FROM reflections
        WHERE user_id = ? 
        AND timestamp >= datetime('now', '-7 days')
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data
