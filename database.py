"""SQLite event logging for local analytics."""
import csv
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("data/hand_tracking.db")

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            gesture TEXT,
            finger_count INTEGER,
            fps REAL,
            details TEXT
        )""")
        db.commit()

def log_event(event_type, gesture="", finger_count=0, fps=0.0, details=""):
    init_db()
    with connect() as db:
        db.execute("INSERT INTO events(timestamp,event_type,gesture,finger_count,fps,details) VALUES(?,?,?,?,?,?)",
                   (datetime.now(timezone.utc).isoformat(), event_type, gesture, int(finger_count), float(fps), str(details)))
        db.commit()

def recent_events(limit=100):
    init_db()
    with connect() as db:
        rows = db.execute("SELECT id,timestamp,event_type,gesture,finger_count,fps,details FROM events ORDER BY id DESC LIMIT ?",
                          (max(1, min(int(limit), 1000)),)).fetchall()
    return [dict(zip(("id","timestamp","event_type","gesture","finger_count","fps","details"), row)) for row in rows]

def export_csv(path="data/analytics_export.csv"):
    rows = recent_events(1000)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id","timestamp","event_type","gesture","finger_count","fps","details"])
        writer.writeheader()
        writer.writerows(reversed(rows))
    return path
