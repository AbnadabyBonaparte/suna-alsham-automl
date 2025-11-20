import os
from flask import Flask, send_from_directory, jsonify

# Configuração Automática de Pasta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = 'frontend-official'

# Verificação de segurança da pasta
if not os.path.exists(os.path.join(BASE_DIR, FRONTEND_FOLDER)):
    for f in ['frontend-alsham', 'frontend']:
        if os.path.exists(os.path.join(BASE_DIR, f)):
            FRONTEND_FOLDER = f
            break

app = Flask(__name__, static_folder=FRONTEND_FOLDER)

@app.route('/')
def home():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/agentes')
def agentes():
    return send_from_directory(FRONTEND_FOLDER, 'agentes.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(FRONTEND_FOLDER, 'manifest.json', mimetype='application/json')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

if __name__ == '__main__':
    app.run(debug=True)
