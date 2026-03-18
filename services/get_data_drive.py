import os
import io
from variables import *
from db.already_sent import already_sent
from googleapiclient.http import MediaIoBaseDownload


def list_new_files(service, conn):
    query = (
        f"'{FOLDER_ID}' in parents and trashed = false "
        f"and (mimeType = 'application/pdf' or mimeType = 'application/epub+zip')"
    )

    results = (
        service.files()
        .list(q=query, fields="files(id, name, mimeType, modifiedTime)", pageSize=100)
        .execute()
    )

    files = results.get("files", [])
    return [f for f in files if not already_sent(conn, f["id"])]


def download_file(service, file_id, filename):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    path = os.path.join(DOWNLOAD_DIR, filename)

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(path, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    fh.close()
    return path
