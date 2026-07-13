import sqlite3
from contextlib import contextmanager as cm
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'databse.db'

@cm
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS bookings (
                booking_id TEXT PRIMARY KEY,
                room_id TEXT NOT NULL,
                date_start TEXT NOT NULL,
                date_end TEXT NOT NULL,
                username TEXT NOT NULL,
                status TEXT NOT NULL
            )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS rooms (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                capacity INTEGER NOT NULL,
                equipment TEXT NOT NULL
            )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                hashed_pass TEXT NOT NULL,
                role TEXT NOT NULL
            )""")
        conn.commit()