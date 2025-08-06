#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
Versão Railway Safe - Healthcheck Imediato
"""
import os
import logging
import asyncio
from contextlib import asynccontextmanager
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
agents = {}
agent_registry = None
network = None
system_status = {
    "bootstrap_completed": False,
    "system_healthy": True,
    "agents_active": 0,
    "total_agents_expected": 56,
    "warnings": 0,
    "errors": 0,
    "agent_loader_available": False,
    "agent_registry_available": False,
    "original_system_loaded": False
}

# Criação do app principal
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA Autônomo - Railway Safe Mode",
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

# Endpoint de healthcheck IMEDIATO (sem depender de nenhuma carga)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Healthcheck imediato - Railway Safe Mode",
        "success_rate": "n/a (modo simplificado)",
        "agents_loaded": "verificando..."
    }

# Rota raiz simples
@app.get("/")
async def root():
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "status": "online",
        "message": "Sistema iniciado em modo seguro. Agentes em carregamento."
    }

# Lifespan separado (NÃO bloqueia o startup do Railway)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global agents, agent_registry, network

    logger.info("🚀 ALSHAM QUANTUM - Modo seguro iniciado")

    try:
        from suna_alsham_core.agent_loader import initialize_all_agents
        from suna_alsham_core.multi_agent_network import MessageBus

        class SafeNetwork:
            def __init__(self):
                self.message_bus = MessageBus()
                self.agents = {}

            async def start(self):
                await self.message_bus.start()

            def register_agent(self, agent):
                name = getattr(agent, 'name', getattr(agent, 'agent_id', f"agent_{len(self.agents)}"))
                self.agents[name] = agent

        network = SafeNetwork()
        await network.start()

        result = await initialize_all_agents(network)
        agents = network.agents

        system_status["agents_active"] = result.get("agents_loaded", 0)
        system_status["warnings"] = result.get("modules_failed", 0)
        system_status["original_system_loaded"] = True
        system_status["agent_loader_available"] = True

        logger.info(f"✅ {system_status['agents_active']} agentes carregados")

    except Exception as e:
        logger.error(f"❌ Erro ao carregar agentes: {e}")
        system_status["errors"] += 1

    yield

    logger.info("🔄 Encerrando sistema")
    try:
        if network and hasattr(network.message_bus, 'stop'):
            await network.message_bus.stop()
    except Exception as e:
        logger.error(f"❌ Falha ao encerrar: {e}")

# Injetar lifespan no app
app.router.lifespan_context = lifespan
