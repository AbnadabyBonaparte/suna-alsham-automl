# Correção para o problema de WebSocket 404
#!/usr/bin/env python3
from flask import Flask, jsonify, send_file, Blueprint
from flask_cors import CORS
from flask_socketio import SocketIO
import logging
import requests
from datetime import datetime
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação do app Flask
app = Flask(__name__)
CORS(app)

# IMPORTANTE: Inicialização do Socket.IO com configurações específicas
socketio = SocketIO(app, 
                   cors_allowed_origins="*", 
                   async_mode='threading',  # Usar threading para compatibilidade
                   logger=True,            # Habilitar logs do socketio
                   engineio_logger=True)   # Habilitar logs do engineio

# O restante do seu código permanece o mesmo...

# Eventos SocketIO
@socketio.on('connect')
def handle_connect():
    logger.info('Cliente conectado via WebSocket')
    # Emitir um evento de teste para confirmar conexão
    socketio.emit('server_response', {'data': 'Conexão estabelecida!'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Cliente WebSocket desconectado')

# No final do arquivo, a parte mais importante:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Servidor iniciando na porta {port}")
    logger.info(f"Sistema configurado para 6 ciclos por hora")
    
    # ESTA É A LINHA CRUCIAL: usar socketio.run() com as opções corretas
    socketio.run(app, 
                host='0.0.0.0', 
                port=port, 
                debug=False,
                allow_unsafe_werkzeug=True)  # Esta opção é importante para o Railway
