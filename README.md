# Datalogger Backend + Dash com Simulador ESP32

Este projeto recebe e visualiza dados de um datalogger (real ou simulado):
- Localização em mapa (GPS)
- Temperatura e pressão
- Mensagens CAN

### Executar localmente:
```bash
pip install -r requirements.txt
python app.py
```

### Deploy em Render.com:
1. Suba os arquivos em um repositório GitHub
2. Crie um Web Service no Render com Python 3
3. Configure o build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Acesse: `https://<seu-app>.onrender.com/dashboard/`
