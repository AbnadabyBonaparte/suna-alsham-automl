from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def hub():
    return send_from_directory('.', 'index.html')

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
