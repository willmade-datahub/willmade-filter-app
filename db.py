import sqlite3
import pandas as pd
import os

DB_PATH = "./data/storage.db"

def init_db():
    if not os.path.exists("./data"):
        os.makedirs("./data")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matched_list (
            아이디 TEXT PRIMARY KEY,
            전화번호 TEXT,
            메모 TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_matched(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("matched_list", conn, if_exists="replace", index=False)
    conn.close()


def load_matched():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM matched_list", conn)
    conn.close()
    return df


def clear_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM matched_list")
    conn.commit()
    conn.close()
