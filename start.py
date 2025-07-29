#!/usr/bin/env python3
"""
Ponto de Entrada Único e Oficial do Sistema SUNA-ALSHAM.

[Fase 2] - Fortalecido e totalmente integrado com a nova arquitetura.
Este script é responsável por:
1. Configurar o logging.
2. Inicializar a aplicação web FastAPI.
3. Instanciar e inicializar o sistema SUNAAlshamSystemV2 completo na startup.
4. Expor os endpoints essenciais da API (health, status).
5. Iniciar o servidor web Uvicorn, pronto para produção.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Adicionar o diretório do núcleo ao path para garantir que os imports funcionem
# de forma consistente, não importa de onde o script seja chamado.
sys.path.append(str(Path(__file__).parent / "suna_alsham_core"))

# Agora que o path está configurado, podemos importar nossos módulos do núcleo.
from system import SUNAAlshamSystemV2

# --- Configuração de Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SUNA_ALSHAM_START")

# --- Instância Global do Sistema ---
# Esta variável irá conter a instância principal do nosso sistema de agentes.
system: SUNAAlshamSystemV2 = None

# --- Ciclo de Vida da Aplicação (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação. A lógica de startup é executada
    antes de a aplicação começar a aceitar requisições.
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
            # Em um sistema real, poderíamos notificar um serviço de monitoramento aqui.
            
    except Exception as e:
        logger.critical(f"FATAL: Um erro inesperado ocorreu durante a inicialização: {e}", exc_info=True)
        # Em um ambiente de produção, o orquestrador (como Kubernetes) reiniciaria o container.
        # Para evitar um loop de falhas, não saímos do processo, mas o sistema ficará em estado de erro.
        if not system:
             system = SUNAAlshamSystemV2() # Garante que 'system' existe
        system.system_status = "error"

    yield  # A aplicação roda aqui

    # --- Lógica de Shutdown (executa ao parar o servidor) ---
    logger.info("🛑 INICIANDO SEQUÊNCIA DE SHUTDOWN...")
    if system and hasattr(system.network.message_bus, 'stop'):
        await system.network.message_bus.stop()
    logger.info("✅ Sistema finalizado.")


# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="SUNA-ALSHAM: Sistema Multi-Agente Auto-Evolutivo",
    description="API para o Núcleo do Sistema SUNA-ALSHAM.",
    version="2.0.0-fortified",
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
    """Endpoint raiz que fornece um status geral e boas-vindas."""
    if not system:
        return {"message": "SUNA-ALSHAM Sistema Multi-Agente em Inicialização..."}

    return {
        "message": "SUNA-ALSHAM Sistema Multi-Agente Online",
        "status": system.system_status,
        "total_agents": system.total_agents,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health", tags=["Status"])
async def health_check():
    """
    Health Check. Essencial para sistemas de orquestração (como Kubernetes ou Railway)
    saberem se a aplicação está viva e saudável.
    """
    if system and system.system_status in ["active", "degraded"]:
        return JSONResponse(status_code=200, content={"status": "healthy"})
    else:
        return JSONResponse(status_code=503, content={"status": "unhealthy"})


@app.get("/status", tags=["Status"])
async def get_system_status():
    """Retorna o status detalhado de todos os componentes do sistema."""
    if not system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado.")
    
    return system.get_system_status()


# --- Execução do Servidor ---

def main():
    """Função principal que inicia o servidor web Uvicorn."""
    host = os.environ.get("HOST", "0.0.0.0")
    # Railway define a porta através de uma variável de ambiente.
    # Usamos 8080 como padrão para desenvolvimento local.
    port = int(os.environ.get("PORT", 8080))

    logger.info(f"🌐 Servidor Uvicorn será iniciado em http://{host}:{port}")

    uvicorn.run(
        "start:app",
        host=host,
        port=port,
        log_level="info",
        reload=False # 'reload=True' é ótimo para dev, mas deve ser False em produção.
    )


if __name__ == "__main__":
    main()
