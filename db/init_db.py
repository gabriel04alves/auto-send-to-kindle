import sqlite3
from dotenv import load_dotenv

load_dotenv()


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sent_files (
            file_id TEXT PRIMARY KEY,
            file_name TEXT NOT NULL,
            sent_at TEXT NOT NULL
        )
    """
    )
    conn.commit()
    return conn
