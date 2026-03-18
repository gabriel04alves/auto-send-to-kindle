# Configuracao do Google Drive (OAuth) para o Projeto

Este guia explica, passo a passo, como configurar o acesso ao Google Drive usado por este projeto.

Use este tutorial para gerar corretamente o `credentials.json` e o `token.json`.

## Visao geral

Voce vai:

1. Criar um projeto no Google Cloud.
2. Ativar a Google Drive API.
3. Configurar a tela de consentimento OAuth.
4. Criar credencial OAuth do tipo Desktop App.
5. Baixar o arquivo `credentials.json`.
6. Rodar o script Python para gerar o `token.json`.

## 1. Criar projeto no Google Cloud

1. Acesse `https://console.cloud.google.com/`.
2. No topo, clique em `Select Project`.
3. Clique em `New Project`.
4. Defina um nome, por exemplo: `Kindle Sync`.
5. Clique em `Create`.

## 2. Ativar a Google Drive API

1. No menu lateral, acesse `APIs & Services > Library`.
2. Busque por `Google Drive API`.
3. Abra a API e clique em `Enable`.

## 3. Configurar OAuth Consent Screen

1. Acesse `APIs & Services > OAuth consent screen`.
2. Escolha `External`.
3. Preencha os campos principais:

- `App name`: Kindle Sync
- `User support email`: seu e-mail
- `Developer contact email`: seu e-mail

4. Continue e salve.

### Scopes (importante)

1. Clique em `Add or Remove Scopes`.
2. Adicione exatamente o escopo abaixo:

```text
https://www.googleapis.com/auth/drive.readonly
```

3. Salve.

### Test users

1. Em `Test users`, clique em `Add Users`.
2. Adicione o seu proprio e-mail da conta Google que sera usada no login.
3. Salve.

## 4. Criar credencial OAuth (Desktop App)

1. Acesse `APIs & Services > Credentials`.
2. Clique em `Create Credentials > OAuth client ID`.
3. Em `Application type`, selecione `Desktop app`.
4. Defina um nome, por exemplo: `Kindle Sync Client`.
5. Clique em `Create`.

## 5. Baixar e posicionar o credentials.json

1. Apos criar a credencial, clique em `Download`.
2. Garanta que o nome do arquivo seja `credentials.json`.
3. Coloque o arquivo na raiz do projeto:

```bash
~/auto-send-to-kindle/credentials.json
```

## Boas praticas de seguranca

Nunca publique estes arquivos em repositorios publicos:

- `credentials.json`
- `token.json`

No seu `.gitignore`, mantenha ambos ignorados.
