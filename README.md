# Auto Send To Kindle

Automatiza o envio de arquivos novos de uma pasta do Google Drive para o Kindle, por e-mail, com controle local para evitar reenvio do mesmo arquivo.

## Como funciona

O fluxo executado em `app.py` é:

1. Inicializa um banco SQLite local (`sent_files`) para registrar arquivos já enviados.
2. Autentica no Google Drive usando OAuth2 (`credentials.json` + `token.json`).
3. Lista arquivos novos da pasta configurada (`FOLDER_ID`) com MIME suportado:
   - `application/pdf`
   - `application/epub+zip`
4. Faz download para `~/kindle-sync/downloads`.
5. Envia por SMTP (Gmail) para o e-mail `@kindle.com`.
6. Marca o arquivo como enviado no SQLite para não repetir.

## Pré-requisitos

- Linux (ou ambiente com Python 3 e `systemd --user` para automação por timer)
- Python 3.10+
- Conta Google com API do Drive habilitada e OAuth Client configurado
- Conta de e-mail com senha de app (ex.: Gmail com 2FA)
- Endereço Send to Kindle ativo

## Configuração

Antes de seguir, veja o guia detalhado de configuração da conta Google e OAuth:

- [`docs/google-drive-setup.md`](docs/google-drive-setup.md) (explicação completa da config do Google para este projeto)

### 1. Clone e instale dependências

```bash
git clone https://github.com/gabriel04alves/auto-send-to-kindle
cd auto-send-to-kindle

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure variáveis de ambiente

Crie o arquivo `.env` com base em `.env.example`:

```bash
cp .env.example .env
```

Valores esperados:

- `KINDLE_EMAIL`: e-mail `@kindle.com` de destino
- `SMTP_USER`: seu e-mail remetente (ex.: Gmail)
- `SMTP_PASS`: senha de app do e-mail remetente (veja a seção `Como obter a SMTP_PASS (senha de app Google)`)
- `FOLDER_ID`: ID da pasta do Google Drive a ser monitorada

Exemplo:

```bash
export KINDLE_EMAIL="seu_endereco_send_to_kindle@kindle.com"
export SMTP_USER="seuemail@gmail.com"
export SMTP_PASS="sua_senha_de_app"
export FOLDER_ID="id_da_pasta"
```

### Como obter a SMTP_PASS (senha de app Google)

Use esta seção para preencher o valor de `SMTP_PASS` no `.env`.

1. Acesse `https://myaccount.google.com/` com a conta usada em `SMTP_USER`.
2. Entre em `Segurança`.
3. Ative `Verificacao em duas etapas` (obrigatorio para senha de app).
4. Volte para `Segurança` e abra `Senhas de app`.
5. Em tipo de app, selecione `E-mail`.
6. Em dispositivo, escolha um nome como `Auto Send To Kindle (Desktop)`.
7. Clique em `Gerar` e copie a senha exibida (16 caracteres).
8. Cole no `.env` em `SMTP_PASS`.

Exemplo:

```bash
export SMTP_PASS="abcd efgh ijkl mnop"
```

Notas:

- Nao use sua senha normal da conta Google.
- Se sua conta for Google Workspace, o admin pode bloquear senha de app.
- Trate `SMTP_PASS` como segredo e nunca publique em repositório.

### 3. Configure credenciais do Google Drive

Coloque o arquivo OAuth client em `credentials.json`.

Na primeira execução, o projeto abrirá o fluxo OAuth local para gerar/atualizar `token.json`.

Se quiser o passo a passo completo no Google Cloud Console, use:

- [`docs/google-drive-setup.md`](docs/google-drive-setup.md)

## Execução manual

Com ambiente virtual ativo:

```bash
python app.py
```

Primeira execução (gera `token.json`):

- Execute localmente no terminal (nao via `systemd`).
- O navegador abrira para login Google e permissao OAuth.
- Se aparecer `app not verified`, use `Advanced` e depois `Continue`.
- Ao concluir, o projeto cria automaticamente `token.json`.

Esse token permite que as proximas execucoes acessem o Drive sem novo login interativo.

Saídas esperadas:

- conexão com banco local
- conexão com Google Drive
- listagem e processamento de arquivos novos
- confirmação de envio e registro

## Automação diária com systemd user timer

O script `setup_timer.sh` cria automaticamente:

- `~/.config/systemd/user/kindle-sync.service`
- `~/.config/systemd/user/kindle-sync.timer`

### Uso rápido

```bash
chmod +x setup_timer.sh
./setup_timer.sh
```

Por padrão, roda diariamente às `17:54:50`.

### Variáveis opcionais do script

- `PROJECT_DIR` (default: diretório atual)
- `SERVICE_NAME` (default: `kindle-sync`)
- `VENV_DIR` (default: `$PROJECT_DIR/venv`)
- `PYTHON_BIN` (default: `$VENV_DIR/bin/python`)
- `RUN_TIME` (default: `17:54:50`)
- `SYSTEM_PYTHON` (default: `python3`)

Exemplo com horário customizado:

```bash
RUN_TIME="08:00:00" ./setup_timer.sh
```

### Comandos úteis

```bash
systemctl --user list-timers
systemctl --user start kindle-sync.service
journalctl --user -u kindle-sync.service -n 50 --no-pager
```

## Estrutura do projeto

```text
.
├── app.py                      # Orquestra o fluxo principal
├── variables.py                # Variáveis de ambiente, caminhos e constantes
├── config/
│   └── config_google_auth.py   # OAuth2 e cliente Google Drive
├── services/
│   ├── get_data_drive.py       # Listagem de arquivos novos e download
│   └── send_to_kindle.py       # Envio SMTP com anexo
├── db/
│   ├── init_db.py              # Criação de tabela sent_files
│   ├── already_sent.py         # Verifica se arquivo já foi enviado
│   └── mark_sent.py            # Registra envio com timestamp UTC
├── utils/
│   └── sanitize_filename.py    # Sanitiza nome de arquivo
├── setup_timer.sh              # Configura service/timer no systemd user
└── requirements.txt
```

## Banco local

Arquivo SQLite padrão:

- `~/auto-send-to-kindle/data/state.db`

Tabela criada automaticamente:

- `sent_files(file_id PRIMARY KEY, file_name, sent_at)`

## Segurança

- Nunca versionar `.env`, `credentials.json` e `token.json` em repositórios públicos.
- Use senha de app no SMTP (não use senha principal da conta).
- Se qualquer segredo já foi exposto no histórico Git, revogue e gere novos imediatamente.

## Troubleshooting

- `Defina KINDLE_EMAIL, SMTP_USER e SMTP_PASS no ambiente.`
  - Verifique se o `.env` está correto e carregado no shell/processo.

- `Erro: python3 nao encontrado no PATH` durante `setup_timer.sh`
  - Instale Python 3 ou ajuste `SYSTEM_PYTHON`.

- Serviço `systemd --user` falha ao iniciar
  - Consulte logs com `journalctl --user -u kindle-sync.service -n 50 --no-pager`.
  - Confirme que `ExecStart` aponta para o Python do `venv` correto.

- Arquivo não aparece para envio
  - Confirme `FOLDER_ID`.
  - Verifique se o MIME é PDF/EPUB.
  - Cheque se o arquivo já está registrado em `sent_files`.
