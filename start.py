#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
Modo compatível com Railway (Healthcheck imediato e inicialização paralela)
"""
import os
import logging
import asyncio
import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Setup de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Estado do sistema
system_status = {
    "agents_loaded": False,
    "errors": 0,
    "warnings": 0,
    "success_rate": "0%"
}

# Criação do app principal
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA Autônomo - Railway Safe Startup",
    version="2.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de healthcheck IMEDIATO
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Healthcheck imediato - Railway Safe Mode",
        "agents_ready": system_status["agents_loaded"],
        "success_rate": system_status["success_rate"]
    }

# Rota raiz
@app.get("/")
async def root():
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "status": "online",
        "message": "Sistema iniciado. Agentes carregando em segundo plano."
    }

# Inicializador de agentes assíncrono em background
async def initialize_agents_background():
    try:
        from suna_alsham_core.agent_loader import initialize_all_agents
        from suna_alsham_core.multi_agent_network import MessageBus

        class Network:
            def __init__(self):
                self.message_bus = MessageBus()
                self.agents = {}

            async def start(self):
                await self.message_bus.start()

            def register_agent(self, agent):
                name = getattr(agent, 'name', getattr(agent, 'agent_id', f"agent_{len(self.agents)}"))
                self.agents[name] = agent

        network = Network()
        await network.start()
        result = await initialize_all_agents(network)

        system_status["agents_loaded"] = True
        success = result.get("agents_loaded", 0)
        fail = result.get("modules_failed", 0)
        total = success + fail if (success + fail) > 0 else 1
        system_status["success_rate"] = f"{(success / total * 100):.1f}%"
        system_status["warnings"] = fail

        logger.info(f"✅ Agentes carregados: {success} | Falhas: {fail}")

    except Exception as e:
        logger.error(f"❌ Erro na inicialização dos agentes: {e}")
        system_status["errors"] += 1

# Função para iniciar em thread paralela
@app.on_event("startup")
def start_background_tasks():
    def runner():
        asyncio.run(initialize_agents_background())
    thread = threading.Thread(target=runner)
    thread.start()
