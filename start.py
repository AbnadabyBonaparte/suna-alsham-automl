#!/usr/bin/env python3
"""
Ponto de Entrada Único e Oficial do Sistema SUNA-ALSHAM.
"""

# --- PASSO 1: Configuração de Ambiente ANTES de tudo ---
import matplotlib
matplotlib.use('Agg')

# --- PASSO 2: Logging Básico ---
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SUNA_ALSHAM_START")

# --- PASSO 3: Adiciona o path do projeto no sys.path ---
sys.path.append(str(Path(__file__).parent.resolve()))

# --- PASSO 4: Imports da Aplicação ---
import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from suna_alsham_core.system import SUNAAlshamSystemV2
    from suna_alsham_core.multi_agent_network import AgentMessage, MessageType
    logger.info("✅ Importações do sistema realizadas com sucesso.")
except Exception as e:
    logger.critical(f"❌ ERRO CRÍTICO NA IMPORTAÇÃO DO SISTEMA: {e}", exc_info=True)
    sys.exit(1)

# --- Instância Global do Sistema ---
system: SUNAAlshamSystemV2 = None

# --- Ciclo de Vida da Aplicação ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global system
    logger.info("🚀 Iniciando o sistema SUNA-ALSHAM...")
    try:
        system = SUNAAlshamSystemV2()
        success = await system.initialize_complete_system()
        if success:
            logger.info("✅ Sistema inicializado com sucesso.")
        else:
            logger.critical("❌ Falha crítica ao inicializar o sistema.")
    except Exception as e:
        logger.critical(f"Erro durante inicialização: {e}", exc_info=True)
        system = SUNAAlshamSystemV2()
        system.system_status = "error"
    yield
    logger.info("🛑 Encerrando sistema...")
    if system and hasattr(system.network.message_bus, "stop"):
        await system.network.message_bus.stop()
    logger.info("✅ Sistema desligado.")

# --- Inicializa FastAPI ---
app = FastAPI(
    title="SUNA-ALSHAM: Sistema Multi-Agente Auto-Evolutivo",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# --- Endpoints ---

@app.get("/", tags=["Status"])
async def root():
    if not system or not system.initialized:
        raise HTTPException(status_code=503, detail="Sistema não está pronto.")
    return system.get_system_status()

@app.post("/submit_task", tags=["Tarefas"])
async def submit_task(request: Dict[str, Any]):
    if not system or not system.initialized:
        raise HTTPException(status_code=503, detail="Sistema não está inicializado.")

    recipient = request.get("recipient_id")
    task_content = request.get("content")

    if not recipient or not task_content:
        raise HTTPException(status_code=400, detail="Campos 'recipient_id' e 'content' são obrigatórios.")

    # --- LINHA DA CORREÇÃO AQUI ---
    # Garantimos que o 'content' da mensagem seja sempre um dicionário,
    # alinhando a API com o formato que a rede de agentes espera.
    formatted_content = {"content": task_content}

    message = AgentMessage(
        sender_id="api_gateway",
        recipient_id=recipient,
        message_type=MessageType.REQUEST,
        content=formatted_content, # Usamos o conteúdo formatado
    )

    await system.network.message_bus.publish(message)
    logger.info(f"Tarefa enviada ao agente {recipient}")
    return {"status": "accepted", "message": "Tarefa recebida e encaminhada."}

# --- Execução Local ---
if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("start:app", host=host, port=port, log_level="info", reload=False)
