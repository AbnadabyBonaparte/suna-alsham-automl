import os
import random
import time
from flask import Flask, send_from_directory, jsonify

# --- CONFIGURAÇÃO ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = 'frontend-official'

# Garante que a pasta existe
if not os.path.exists(os.path.join(BASE_DIR, FRONTEND_FOLDER)):
    for f in ['frontend-alsham', 'frontend']:
        if os.path.exists(os.path.join(BASE_DIR, f)):
            FRONTEND_FOLDER = f
            break

app = Flask(__name__, static_folder=FRONTEND_FOLDER)

# --- DADOS REAIS DO SISTEMA (Baseado no RAIO_X) ---
# Estrutura hierárquica dos seus agentes
AGENTS_DB = {
    "core": [
        {"id": "orch_01", "name": "Quantum Orchestrator", "status": "online", "type": "master"},
        {"id": "sec_01", "name": "Security Guardian", "status": "online", "type": "security"},
        {"id": "data_01", "name": "Data Collector", "status": "processing", "type": "worker"},
        {"id": "evo_01", "name": "Real Evolution Engine", "status": "standby", "type": "creator"}
    ],
    "sales": [
        {"id": "sales_orch", "name": "Sales Orchestrator", "status": "online", "type": "manager"},
        {"id": "funnel_01", "name": "Sales Funnel Agent", "status": "online", "type": "worker"},
        {"id": "price_01", "name": "Pricing Optimizer", "status": "processing", "type": "analyst"},
        {"id": "rev_01", "name": "Revenue Optimizator", "status": "online", "type": "analyst"}
    ],
    "social": [
        {"id": "soc_orch", "name": "Social Media Orchestrator", "status": "online", "type": "manager"},
        {"id": "cont_01", "name": "Content Creator", "status": "creating", "type": "creative"},
        {"id": "inf_01", "name": "Influencer Network", "status": "scanning", "type": "networker"},
        {"id": "video_01", "name": "Video Automation", "status": "rendering", "type": "creative"}
    ],
    "support": [
        {"id": "sup_orch", "name": "Support Orchestrator", "status": "online", "type": "manager"},
        {"id": "chat_01", "name": "Chatbot Agent", "status": "active", "type": "worker"},
        {"id": "sat_01", "name": "Satisfaction Analyzer", "status": "online", "type": "analyst"}
    ],
    "analytics": [
        {"id": "ana_orch", "name": "Analytics Orchestrator", "status": "online", "type": "manager"},
        {"id": "pred_01", "name": "Predictive Analysis", "status": "computing", "type": "analyst"}
    ]
}

# --- ROTAS DE API (O Frontend consome isso) ---

@app.route('/api/network/map')
def get_network_map():
    """Retorna os nós e arestas para desenhar a Rede Neural"""
    nodes = []
    edges = []
    
    # Nó Central
    nodes.append({"id": 0, "label": "SUNA CORE", "group": "core", "value": 20})
    
    current_id = 1
    
    for domain, agents in AGENTS_DB.items():
        # Nó de Domínio (Ex: Sales Sector)
        domain_node_id = current_id
        nodes.append({"id": domain_node_id, "label": domain.upper(), "group": "domain", "value": 15})
        edges.append({"from": 0, "to": domain_node_id}) # Liga Core ao Domínio
        current_id += 1
        
        for agent in agents:
            # Nó do Agente
            agent_id = current_id
            status_color = "#10b981" if agent['status'] == 'online' else "#f59e0b"
            if agent['status'] == 'rendering': status_color = "#8b5cf6"
            
            nodes.append({
                "id": agent_id, 
                "label": agent['name'], 
                "group": agent['type'], 
                "title": f"Status: {agent['status']}",
                "value": 10
            })
            edges.append({"from": domain_node_id, "to": agent_id}) # Liga Domínio ao Agente
            
            # Conexões aleatórias entre agentes para simular complexidade neural
            if random.random() > 0.7:
                edges.append({"from": agent_id, "to": random.randint(1, current_id-1)})
                
            current_id += 1
            
    return jsonify({"nodes": nodes, "edges": edges})

@app.route('/api/metrics/realtime')
def get_metrics():
    """Simula dados em tempo real para os gráficos"""
    return jsonify({
        "cpu": random.randint(20, 45),
        "memory": random.randint(40, 65),
        "requests": random.randint(1000, 5000),
        "active_agents": 57,
        "optimization_level": f"{random.uniform(98.5, 99.9):.2f}%"
    })

# --- ROTAS DE FRONTEND ---

@app.route('/')
def home():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/rede-neural')
def neural_page():
    return send_from_directory(FRONTEND_FOLDER, 'rede_neural.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

if __name__ == '__main__':
    app.run(debug=True)
