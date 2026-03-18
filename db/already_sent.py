def already_sent(conn, file_id):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM sent_files WHERE file_id = ?", (file_id,))
    return cur.fetchone() is not None
