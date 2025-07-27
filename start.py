#!/usr/bin/env python3
"""
Ponto de Entrada Único e Oficial do Sistema SUNA-ALSHAM.

Este script é responsável por:
1. Configurar o logging.
2. Inicializar a aplicação web FastAPI.
3. Instanciar e inicializar o sistema SUNAAlshamSystemV2 completo na startup.
4. Expor os endpoints essenciais da API (health, status, metrics).
5. Iniciar o servidor web Uvicorn, detectando a porta do ambiente (Railway).
"""

import os
import sys
import asyncio
import uvicorn
import logging
from typing import Optional
from pathlib import Path

# Adicionar o diretório raiz ao path para garantir que os imports funcionem
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# --- Configuração de Logging ---
# Configura um logger claro e informativo para a saída do console.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SUNA_ALSHAM_MAIN")

# --- Variável Global do Sistema ---
# Esta variável irá conter a instância principal do nosso sistema de agentes.
system = None

# --- Inicialização da Aplicação FastAPI ---
# O 'app' é o núcleo da nossa API web.
app = FastAPI(
    title="SUNA-ALSHAM: Sistema Multi-Agente Auto-Evolutivo",
    description="API para o Núcleo do Sistema SUNA-ALSHAM, orquestrando todos os agentes e serviços.",
    version="2.0.0-refactored"
)

# --- Middlewares ---
# Configura CORS para permitir que aplicações web de qualquer origem se comuniquem com nossa API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Eventos de Startup e Shutdown ---

@app.on_event("startup")
async def startup_sequence():
    """
    Executa na inicialização do servidor. É aqui que a "mágica" acontece:
    o sistema completo de agentes é carregado e iniciado.
    """
    global system
    logger.info("🚀 INICIANDO SEQUÊNCIA DE STARTUP DO SUNA-ALSHAM...")
    
    try:
        # Importamos a classe principal do sistema aqui para evitar imports circulares.
        from main_complete_system_v2 import SUNAAlshamSystemV2
        
        logger.info("🤖 Instanciando o sistema de agentes...")
        system = SUNAAlshamSystemV2()
        
        success = await system.initialize_complete_system()
        
        if success:
            logger.info(f"✅ SISTEMA INICIALIZADO COM SUCESSO! {system.total_agents} agentes ativos.")
        else:
            logger.error("❌ FALHA CRÍTICA NA INICIALIZAÇÃO DO SISTEMA DE AGENTES.")
            # Em um sistema de produção real, poderíamos decidir parar o serviço aqui.
            
    except ImportError as e:
        logger.critical(f"FATAL: Não foi possível importar 'SUNAAlshamSystemV2'. Verifique o arquivo 'main_complete_system_v2.py'. Erro: {e}")
        # Parar a aplicação se o componente principal não puder ser importado.
        sys.exit(1)
    except Exception as e:
        logger.critical(f"FATAL: Um erro inesperado ocorreu durante a inicialização: {e}", exc_info=True)
        sys.exit(1)

@app.on_event("shutdown")
async def shutdown_sequence():
    """Executa quando o servidor está sendo desligado para uma finalização limpa."""
    logger.info("🛑 INICIANDO SEQUÊNCIA DE SHUTDOWN...")
    if system:
        # Futuramente, podemos adicionar uma lógica de shutdown gracioso para os agentes aqui.
        logger.info("✅ Sistema finalizado.")

# --- Endpoints da API ---

@app.get("/", tags=["Status"])
async def root():
    """Endpoint raiz que fornece um status geral e boas-vindas."""
    return {
        "message": "SUNA-ALSHAM Sistema Multi-Agente Online",
        "status": system.system_status if system else "initializing",
        "total_agents": system.total_agents if system else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Status"])
async def health_check():
    """
    Health Check. Essencial para sistemas de orquestração (como Kubernetes ou Railway)
    saberem se a aplicação está viva e saudável.
    """
    if system and system.system_status == 'active':
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "agents_count": system.total_agents,
                "uptime_seconds": system.get_uptime()
            }
        )
    else:
        return JSONResponse(
            status_code=503, # Service Unavailable
            content={
                "status": "unhealthy",
                "message": "Sistema em inicialização ou em estado de erro."
            }
        )

@app.get("/status", tags=["Status"])
async def get_system_status():
    """Retorna o status detalhado de todos os componentes do sistema."""
    if not system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado.")
    
    try:
        # Este método deve ser implementado na classe SUNAAlshamSystemV2
        # para retornar um dicionário com o status de cada agente principal.
        return system.get_system_status()
    except Exception as e:
        logger.error(f"Erro ao obter status detalhado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar status do sistema.")

# --- Execução do Servidor ---

def main():
    """Função principal que inicia o servidor web."""
    host = "0.0.0.0"
    # Railway define a porta através de uma variável de ambiente.
    # Usamos 8080 como padrão para desenvolvimento local.
    port = int(os.environ.get("PORT", 8080))

    logger.info(f"🌐 Servidor Uvicorn será iniciado em http://{host}:{port}")

    uvicorn.run(
        "start:app",  # Aponta para a variável 'app' neste arquivo 'start.py'
        host=host,
        port=port,
        log_level="info",
        reload=False # 'reload=True' é ótimo para dev, mas deve ser False em produção.
    )

if __name__ == "__main__":
    main()
