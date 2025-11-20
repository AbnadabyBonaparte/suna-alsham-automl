import os
from flask import Flask, send_from_directory, jsonify

# Descobre onde este arquivo está rodando
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tenta achar a pasta do frontend automaticamente
possible_folders = ['frontend-official', 'frontend-alsham', 'frontend']
FRONTEND_FOLDER = None

for folder in possible_folders:
    path_to_check = os.path.join(BASE_DIR, folder)
    if os.path.exists(path_to_check):
        FRONTEND_FOLDER = folder
        break

# Fallback se não achar nada
if not FRONTEND_FOLDER:
    FRONTEND_FOLDER = '.'

app = Flask(__name__, static_folder=FRONTEND_FOLDER)

@app.route('/')
def home():
    try:
        return send_from_directory(FRONTEND_FOLDER, 'index.html')
    except Exception as e:
        return jsonify({
            "error": "Erro ao carregar index.html",
            "message": str(e),
            "folder_detected": FRONTEND_FOLDER,
            "files_in_folder": os.listdir(FRONTEND_FOLDER) if os.path.exists(FRONTEND_FOLDER) else "Pasta nao existe"
        })

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

@app.route('/debug')
def debug():
    return jsonify({
        "status": "online",
        "frontend_folder": FRONTEND_FOLDER
    })

if __name__ == '__main__':
    app.run(debug=True)
