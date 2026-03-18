from dotenv import load_dotenv

from variables import *
from db.init_db import init_db
from db.mark_sent import mark_sent
from utils.sanitize_filename import sanitize_filename
from services.get_data_drive import list_new_files, download_file
from config.config_google_auth import get_drive_service
from services.send_to_kindle import send_to_kindle

load_dotenv()


def run_once():
    print("Conectando ao banco de dados local...")
    conn = init_db(DB_PATH)
    print("Conectando ao Google Drive...")
    service = get_drive_service()

    new_files = list_new_files(service, conn)

    if not new_files:
        print("Nenhum arquivo novo encontrado. Encerrando execução.")
        conn.close()
        return

    for f in new_files:
        print(f"Processando: {f['name']} ({f['id']})")
        clean_name = sanitize_filename(f["name"])
        local_path = download_file(service, f["id"], clean_name)
        send_to_kindle(local_path, clean_name, f["mimeType"])
        mark_sent(conn, f["id"], f["name"])
        print(f"Enviado e registrado: {f['name']}")

    conn.close()
    return


def main():
    try:
        run_once()
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
