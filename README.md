# Datalogger Backend com Dash e Simulador

Este projeto recebe e visualiza dados de um datalogger (simulado ou real) com Flask + Dash.

## Estrutura:
- `/datalog`: recebe POST com dados JSON
- `/dashboard/`: painel web com gráficos e mapa

## Execução local:
```bash
pip install -r requirements.txt
python app.py
```

## Deploy no Render:
1. Suba os arquivos para um repositório GitHub
2. Crie um Web Service no Render
3. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:server`
4. Defina a variável de ambiente: `PORT=5000`
5. Acesse `https://<seu-app>.onrender.com/dashboard/`
