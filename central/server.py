#!/usr/bin/env python3
# server.py - VERSÃO EMERGENCIAL SUPER SIMPLES
import os
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import logging

# Configurar logging BÁSICO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Rota principal - retorna o HTML
@app.route('/')
def index():
    logger.info("Requisição para index.html")
    try:
        return send_file('index.html')
    except:
        return """
        <h1>ALSHAM QUANTUM v12.0</h1>
        <p>Dashboard em manutenção</p>
        <p>Sistema principal operando em: https://suna-alsham-automl-production.up.railway.app</p>
        """

# APIs básicas apontando para o sistema principal
@app.route('/api/status')
def status():
    return jsonify({
        "status": "operational",
        "message": "Use o sistema principal em https://suna-alsham-automl-production.up.railway.app",
        "agents": 50,
        "version": "12.0"
    })

@app.route('/api/agents')
def agents():
    return jsonify({
        "total": 50,
        "active": 50,
        "message": "Agentes rodando no sistema principal"
    })

@app.route('/api/metrics')
def metrics():
    return jsonify({
        "performance": 95.5,
        "roi": 2.0,
        "value": 2550000
    })

@app.route('/api/logs')
def logs():
    return jsonify({
        "logs": [
            {"level": "info", "message": "Sistema operacional"},
            {"level": "success", "message": "50 agentes ativos"}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Servidor iniciando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
