
"""db_store.py
Handles persistence of anomalies into SQLite database for further analysis.
"""
import sqlite3
import json


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            event TEXT,
            time TEXT,
            details TEXT,
            extra TEXT
        )
    """)
    conn.commit()
    return conn


def save_anomalies(db_path, anomalies):
    conn = init_db(db_path)
    cur = conn.cursor()
    for a in anomalies:
        type_ = a.get("type")
        event = a.get("event")
        # prefer single 'time', else start/time_range
        time_val = a.get("time") or a.get("start") or a.get("time_range")
        details = a.get("details") or a.get("description")
        extra = json.dumps(a, default=str)
        cur.execute(
            "INSERT INTO anomalies (type, event, time, details, extra) VALUES (?, ?, ?, ?, ?)",
            (type_, event, str(time_val), details, extra)
        )
    conn.commit()
    conn.close()
    return db_path
