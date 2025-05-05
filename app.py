# Backend em Python para recebimento e visualização dos dados do datalogger
# Tecnologias: Flask + SQLite + Dash + Simulador ESP32 embutido (opcional)

from flask import Flask, request, jsonify
import sqlite3
import datetime
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import time
import random
from datetime import datetime as dt

server = Flask(__name__)
DATABASE = 'datalogger.db'

# Inicializa o banco de dados SQLite

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                lat REAL,
                lon REAL,
                can_id TEXT,
                can_data TEXT,
                temp_v REAL,
                press_v REAL
            )
        ''')

# Endpoint para receber dados do ESP32
@server.route('/datalog', methods=['POST'])
def receber_dados():
    data = request.get_json()
    if data:
        try:
            with sqlite3.connect(DATABASE) as conn:
                conn.execute('''
                    INSERT INTO dados (timestamp, lat, lon, can_id, can_data, temp_v, press_v)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('timestamp'),
                    data.get('lat'),
                    data.get('lon'),
                    data.get('can_id'),
                    data.get('can_data'),
                    data.get('temp_v'),
                    data.get('press_v')
                ))
            return jsonify({'status': 'sucesso'}), 200
        except Exception as e:
            return jsonify({'status': 'erro', 'mensagem': str(e)}), 500
    return jsonify({'status': 'erro', 'mensagem': 'JSON inválido'}), 400

# Inicializa DB em thread separada
threading.Thread(target=init_db).start()

# App Dash para visualização
dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Layout do painel
dash_app.layout = html.Div([
    html.H2("Painel de Telemetria - Datalogger"),
    dcc.Interval(id='intervalo', interval=10000, n_intervals=0),
    dcc.Graph(id='grafico_mapa'),
    dcc.Graph(id='grafico_temp'),
    dcc.Graph(id='grafico_pressao'),
    dcc.Graph(id='grafico_can')
])

# Callback para atualizar gráficos
@dash_app.callback(
    [
        Output('grafico_mapa', 'figure'),
        Output('grafico_temp', 'figure'),
        Output('grafico_pressao', 'figure'),
        Output('grafico_can', 'figure')
    ],
    [Input('intervalo', 'n_intervals')]
)
def atualizar_graficos(n):
    with sqlite3.connect(DATABASE) as conn:
        df = pd.read_sql_query("SELECT * FROM dados ORDER BY id DESC LIMIT 100", conn)

    fig_mapa = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        hover_name="timestamp",
        zoom=10,
        height=300
    )
    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig_temp = px.line(df[::-1], x="timestamp", y="temp_v", title="Temperatura (V)")
    fig_press = px.line(df[::-1], x="timestamp", y="press_v", title="Pressão (V)")
    fig_can = px.histogram(df, x="can_id", title="Frequência de IDs CAN")

    return fig_mapa, fig_temp, fig_press, fig_can

# Simulador de ESP32 online (opcional)
def simulador_esp():
    while True:
        dado = {
            "timestamp": dt.utcnow().isoformat(),
            "lat": -23.55 + random.uniform(-0.01, 0.01),
            "lon": -46.63 + random.uniform(-0.01, 0.01),
            "can_id": hex(random.randint(0x100, 0x1FF)),
            "can_data": " ".join([hex(random.randint(0, 255)) for _ in range(8)]),
            "temp_v": round(random.uniform(1.0, 3.0), 2),
            "press_v": round(random.uniform(1.0, 3.0), 2)
        }
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                INSERT INTO dados (timestamp, lat, lon, can_id, can_data, temp_v, press_v)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                dado['timestamp'], dado['lat'], dado['lon'], dado['can_id'], dado['can_data'], dado['temp_v'], dado['press_v']
            ))
        time.sleep(10)

# Ativa simulador automaticamente (remova esta linha se for usar ESP real)
threading.Thread(target=simulador_esp, daemon=True).start()

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    server.run(host='0.0.0.0', port=port)
