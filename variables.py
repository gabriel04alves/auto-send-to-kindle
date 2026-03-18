import os
from dotenv import load_dotenv

load_dotenv()

FOLDER_ID = os.getenv("FOLDER_ID", "")
DOWNLOAD_DIR = os.path.expanduser("~/kindle-sync/downloads")
DB_PATH = os.path.expanduser("~/auto-send-to-kindle/data/state.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

KINDLE_EMAIL = os.getenv("KINDLE_EMAIL", "")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/epub+zip",
}
