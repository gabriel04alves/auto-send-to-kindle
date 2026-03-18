#!/usr/bin/env bash

set -e

PROJECT_DIR="${PROJECT_DIR:-$PWD}"
SERVICE_NAME="${SERVICE_NAME:-kindle-sync}"
VENV_DIR="${VENV_DIR:-$PROJECT_DIR/venv}"
PYTHON_BIN="${PYTHON_BIN:-$VENV_DIR/bin/python}"
RUN_TIME="${RUN_TIME:-17:54:50}"
SYSTEM_PYTHON="${SYSTEM_PYTHON:-python3}"

if [[ ! -x "$PYTHON_BIN" ]]; then
	echo "Venv nao encontrada em $VENV_DIR. Criando..."
	if ! command -v "$SYSTEM_PYTHON" >/dev/null 2>&1; then
		echo "Erro: $SYSTEM_PYTHON nao encontrado no PATH."
		exit 1
	fi
	"$SYSTEM_PYTHON" -m venv "$VENV_DIR"
	if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then
		echo "Instalando dependencias..."
		"$PYTHON_BIN" -m pip install --upgrade pip
		"$PYTHON_BIN" -m pip install -r "$PROJECT_DIR/requirements.txt"
	fi
fi

echo "Criando diretório do systemd (user)..."
mkdir -p ~/.config/systemd/user

echo "Criando service..."
cat <<EOF > ~/.config/systemd/user/${SERVICE_NAME}.service
[Unit]
Description=Auto send to Kindle

[Service]
Type=oneshot
WorkingDirectory=${PROJECT_DIR}
ExecStart=${PYTHON_BIN} ${PROJECT_DIR}/app.py
EOF

echo "Criando timer..."
cat <<EOF > ~/.config/systemd/user/${SERVICE_NAME}.timer
[Unit]
Description=Run Kindle sync daily

[Timer]
OnCalendar=*-*-* ${RUN_TIME}
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "Recarregando systemd..."
systemctl --user daemon-reload

echo "Ativando timer..."
systemctl --user enable --now ${SERVICE_NAME}.timer

echo ""
echo "Automação configurada!"
echo ""
echo "Ver timers:"
echo "systemctl --user list-timers"
echo ""
echo "Testar manualmente:"
echo "systemctl --user start ${SERVICE_NAME}.service"
echo ""
echo "Ver logs:"
echo "journalctl --user -u ${SERVICE_NAME}.service -n 50 --no-pager"