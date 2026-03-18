from variables import *
import smtplib
from email.message import EmailMessage


def send_to_kindle(local_path, filename, mime_type):
    if not KINDLE_EMAIL or not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("Defina KINDLE_EMAIL, SMTP_USER e SMTP_PASS no ambiente.")

    msg = EmailMessage()
    msg["Subject"] = filename
    msg["From"] = SMTP_USER
    msg["To"] = KINDLE_EMAIL
    msg.set_content("Envio automático para Kindle.")

    with open(local_path, "rb") as f:
        data = f.read()

    if mime_type == "application/pdf":
        maintype, subtype = "application", "pdf"
    elif mime_type == "application/epub+zip":
        maintype, subtype = "application", "epub+zip"
    else:
        maintype, subtype = "application", "octet-stream"

    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
