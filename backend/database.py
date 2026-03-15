import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "reader.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS voices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voice_id Text NOT NULL UNIQUE,
            voice_name Text NOT NULL)""")
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS page_ranges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename Text NOT NULL UNIQUE,
                total_pages INTEGER NOT NULL,
                start_page INTEGER NOT NULL DEFAULT 1,
                end_page INTEGER NOT NULL)""")
    conn.commit()
    conn.close()

def save_voices(voice_list):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voices")
    cursor.executemany("INSERT INTO voices (voice_id, voice_name )VALUES (?,?)",
       [(v["id"], v["name"]) for v in voice_list])
    conn.commit()
    conn.close()

def get_voices():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT voice_id, voice_name FROM voices")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows