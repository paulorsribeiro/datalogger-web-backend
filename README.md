# Datalogger Backend com Dash e Simulador

Este projeto roda um painel web com Dash + Flask e simula um datalogger ESP32.

## Instruções para Deploy no Render:

1. Suba os arquivos em um repositório GitHub.
2. Configure como Web Service em https://render.com
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:server`
5. Adicione variável de ambiente: `PORT=5000`
6. Acesse via `https://<seu-app>.onrender.com/dashboard/`

## Execução Local:
```bash
pip install -r requirements.txt
python app.py
```
