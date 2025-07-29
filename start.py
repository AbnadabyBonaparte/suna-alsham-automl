#!/usr/bin/env python3
"""
Ponto de Entrada Único e Oficial do Sistema SUNA-ALSHAM.
[Versão Final de Produção]
"""

# --- PASSO 1: Configuração de Ambiente ANTES de tudo ---
# Configura o backend do Matplotlib para ser não-interativo, essencial para servidores.
import matplotlib
matplotlib.use('Agg')

# --- PASSO 2: Configuração de Logging IMEDIATAMENTE ---
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SUNA_ALSHAM_START")

logger.info("--- Log de Nível Básico Configurado ---")

# --- PASSO 3: Imports do Restante do Sistema ---
import asyncio
import os
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Adiciona a pasta raiz do projeto ao "mapa" do Python.
sys.path.append(str(Path(__file__).parent.resolve()))

# Agora, com o logging já configurado, importamos nosso sistema.
# Se houver um erro aqui, ele será logado.
try:
    from suna_alsham_core.system import SUNAAlshamSystemV2
    logger.info("Importação do sistema principal bem-sucedida.")
except Exception as e:
    logger.critical(f"FALHA CRÍTICA AO IMPORTAR O SISTEMA PRINCIPAL: {e}", exc_info=True)
    # Sai se o sistema principal não puder ser importado.
    sys.exit(1)


# --- Instância Global do Sistema ---
system: SUNAAlshamSystemV2 = None

# --- Ciclo de Vida da Aplicação (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
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

    logger.info("🛑 INICIANDO SEQUÊNCIA DE SHUTDOWN...")
    if system and hasattr(system, 'network') and hasattr(system.network.message_bus, 'stop'):
        await system.network.message_bus.stop()
    logger.info("✅ Sistema finalizado.")

# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="SUNA-ALSHAM: Sistema Multi-Agente Auto-Evolutivo",
    version="3.0.0-release",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/", tags=["Status"])
async def root():
    if not system or not system.initialized:
        raise HTTPException(status_code=503, detail="Sistema em inicialização. Tente novamente em alguns segundos.")
    return system.get_system_status()

@app.get("/health", tags=["Status"])
async def health_check():
    if system and system.system_status in ["active", "degraded"]:
        return JSONResponse(status_code=200, content={"status": "healthy"})
    return JSONResponse(status_code=503, content={"status": "unhealthy"})

# --- Execução do Servidor ---
if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🌐 Servidor Uvicorn será iniciado em http://{host}:{port}")
    uvicorn.run("start:app", host=host, port=port, log_level="info", reload=False)
