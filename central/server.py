from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def hub():
    try:
        return send_from_directory('.', 'index.html')
    except:
        return "ALSHAM QUANTUM v11.0 - Sistema AI Online!", 200

@app.route('/dashboard-metrics/')
def dashboard():
    return send_from_directory('dashboard-metrics', 'index.html')

@app.route('/pwa-mobile/')  
def mobile():
    return send_from_directory('pwa-mobile', 'index.html')

@app.route('/cliente-portal/')
def client():
    return send_from_directory('cliente-portal', 'index.html')

if __name__ == '__main__':
    # Configuração mais flexível da porta
    port = int(os.environ.get('PORT', os.environ.get('port', 5000)))
    debug = os.environ.get('ENVIRONMENT', 'development') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
