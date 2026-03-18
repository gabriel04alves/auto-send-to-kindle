from datetime import datetime, timezone


def mark_sent(conn, file_id, file_name):
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO sent_files (file_id, file_name, sent_at) VALUES (?, ?, ?)",
        (file_id, file_name, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
