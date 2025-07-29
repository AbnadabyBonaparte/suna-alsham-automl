#!/usr/bin/env python3
"""
Ponto de Entrada Único e Oficial do Sistema SUNA-ALSHAM.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# --- CORREÇÃO DEFINITIVA DO PATH ---
# Adiciona a pasta raiz do projeto ao "mapa" do Python.
# Isso permite que qualquer arquivo, em qualquer lugar, importe outros
# usando o caminho completo (ex: from suna_alsham_core...).
sys.path.append(str(Path(__file__).parent.resolve()))
# ------------------------------------

# Agora que o path está configurado, podemos importar nossos módulos.
from suna_alsham_core.system import SUNAAlshamSystemV2

# --- Configuração de Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SUNA_ALSHAM_START")

# --- Instância Global do Sistema ---
system: SUNAAlshamSystemV2 = None

# --- Ciclo de Vida da Aplicação (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    """
    global system
    logger.info("🚀 INICIANDO SEQUÊNCIA DE STARTUP DO SUNA-ALSHAM...")
    
    try:
        logger.info("🤖 Instanciando a classe principal do sistema...")
        system = SUNAAlshamSystemV2()
        
        success = await system.initialize_complete_system()
        
        if success:
            logger.info(f"✅ SISTEMA INICIALIZADO COM SUCESSO! Status: {system.system_status.upper()}")
        else:
            logger.critical("❌ FALHA CRÍTICA NA INICIALIZAÇÃO DO SISTEMA DE AGENTES.")
            
    except Exception as e:
        logger.critical(f"FATAL: Um erro inesperado ocorreu durante a inicialização: {e}", exc_info=True)
        if not system:
             system = SUNAAlshamSystemV2()
        system.system_status = "error"

    yield

    # --- Lógica de Shutdown ---
    logger.info("🛑 INICIANDO SEQUÊNCIA DE SHUTDOWN...")
    if system and hasattr(system, 'network') and hasattr(system.network, 'message_bus') and hasattr(system.network.message_bus, 'stop'):
        await system.network.message_bus.stop()
    logger.info("✅ Sistema finalizado.")

# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="SUNA-ALSHAM: Sistema Multi-Agente Auto-Evolutivo",
    description="API para o Núcleo do Sistema SUNA-ALSHAM.",
    version="2.1.0",
    lifespan=lifespan
)

# --- Middlewares ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints da API ---
@app.get("/", tags=["Status"])
async def root():
    if not system:
        return {"message": "SUNA-ALSHAM Sistema Multi-Agente em Inicialização..."}
    return system.get_system_status()

@app.get("/health", tags=["Status"])
async def health_check():
    if system and system.system_status in ["active", "degraded"]:
        return JSONResponse(status_code=200, content={"status": "healthy"})
    else:
        return JSONResponse(status_code=503, content={"status": "unhealthy"})

# --- Execução do Servidor ---
def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🌐 Servidor Uvicorn será iniciado em http://{host}:{port}")
    uvicorn.run("start:app", host=host, port=port, log_level="info", reload=False)

if __name__ == "__main__":
    main()
