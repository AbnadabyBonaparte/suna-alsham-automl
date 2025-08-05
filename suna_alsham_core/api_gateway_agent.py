#!/usr/bin/env python3
"""
API Gateway – Entrada Universal do SUNA-ALSHAM com FastAPI completo.
Aceita JSON estruturado e texto livre via endpoints HTTP.
"""

import logging
import asyncio
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json

from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

# Modelos Pydantic para validação
class TaskSubmission(BaseModel):
    task_type: str
    content: Dict[str, Any]
    priority: Optional[str] = "normal"
    requester_id: Optional[str] = "api_user"

class TaskResponse(BaseModel):
    status: str
    task_id: str
    message: str

class HealthResponse(BaseModel):
    status: str
    uptime: float
    agents_active: int

class APIGatewayAgent(BaseNetworkAgent):
    """
    Agente API Gateway com servidor FastAPI integrado
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.app = FastAPI(
            title="ALSHAM QUANTUM API Gateway",
            description="Gateway universal para o sistema multi-agente ALSHAM QUANTUM",
            version="2.1.0"
        )
        self.setup_middleware()
        self.setup_routes()
        self.task_counter = 0
        self.start_time = asyncio.get_event_loop().time()
        logger.info(f"🚪 {self.agent_id} inicializado com FastAPI completo.")

    def setup_middleware(self):
        """Configura middleware do FastAPI"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_routes(self):
        """Configura todas as rotas do API Gateway"""
        
        @self.app.get("/", response_model=Dict[str, str])
        async def root():
            """Endpoint raiz"""
            return {
                "service": "ALSHAM QUANTUM API Gateway",
                "version": "2.1.0",
                "status": "operational",
                "documentation": "/docs"
            }

        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Endpoint de verificação de saúde"""
            uptime = asyncio.get_event_loop().time() - self.start_time
            
            # Contar agentes ativos no message bus
            agents_active = len(self.message_bus.queues) if hasattr(self.message_bus, 'queues') else 0
            
            return HealthResponse(
                status="healthy",
                uptime=uptime,
                agents_active=agents_active
            )

        @self.app.post("/submit_task", response_model=TaskResponse)
        async def submit_task(task: TaskSubmission):
            """
            ENDPOINT CRÍTICO: Submissão de tarefas para o sistema ALSHAM QUANTUM
            """
            try:
                # Incrementar contador de tarefas
                self.task_counter += 1
                task_id = f"task_{self.task_counter:06d}"
                
                logger.info(f"📝 Nova tarefa recebida [{task_id}]: {task.task_type}")
                
                # Criar mensagem para o orquestrador
                message_content = {
                    "task_id": task_id,
                    "task_type": task.task_type,
                    "content": task.content,
                    "priority": task.priority,
                    "requester_id": task.requester_id,
                    "source": "api_gateway"
                }
                
                # Enviar para o orquestrador
                await self.handle_incoming(message_content)
                
                logger.info(f"✅ Tarefa [{task_id}] enviada para processamento")
                
                return TaskResponse(
                    status="accepted",
                    task_id=task_id,
                    message=f"Tarefa {task.task_type} aceita e enviada para processamento"
                )
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar tarefa: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro interno: {str(e)}"
                )

        @self.app.post("/submit_text")
        async def submit_text(request: Request):
            """Endpoint para submissão de texto livre"""
            try:
                body = await request.body()
                text_content = body.decode('utf-8')
                
                # Converter texto livre em tarefa estruturada
                task_data = TaskSubmission(
                    task_type="text_processing",
                    content={"text": text_content},
                    priority="normal"
                )
                
                return await submit_task(task_data)
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar texto: {e}")
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.get("/agents/status")
        async def agents_status():
            """Status dos agentes conectados"""
            try:
                agents_list = list(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else []
                return {
                    "total_agents": len(agents_list),
                    "agents": agents_list,
                    "timestamp": asyncio.get_event_loop().time()
                }
            except Exception as e:
                return {"error": str(e), "total_agents": 0, "agents": []}

        @self.app.get("/system/info")
        async def system_info():
            """Informações do sistema"""
            return {
                "system": "ALSHAM QUANTUM",
                "version": "2.1.0",
                "api_gateway_id": self.agent_id,
                "capabilities": self.capabilities,
                "uptime": asyncio.get_event_loop().time() - self.start_time,
                "tasks_processed": self.task_counter
            }

    async def handle_incoming(self, payload: Dict[str, Any]):
        """
        Processa payload recebido e encaminha para o orquestrador
        """
        try:
            msg = self.create_message(
                recipient_id="orchestrator_001",
                message_type=MessageType.REQUEST,
                content=payload
            )
            await self.message_bus.publish(msg)
            logger.debug(f"📤 Mensagem enviada para orchestrator_001: {payload.get('task_id', 'unknown')}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem: {e}")
            raise

    async def start_server(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Inicia o servidor FastAPI
        """
        try:
            logger.info(f"🚀 Iniciando servidor FastAPI em {host}:{port}")
            config = uvicorn.Config(
                app=self.app,
                host=host,
                port=port,
                log_level="info",
                access_log=True
            )
            server = uvicorn.Server(config)
            await server.serve()
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar servidor: {e}")
            raise

    def get_app(self):
        """Retorna a instância FastAPI para uso externo"""
        return self.app

def create_api_gateway_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente API Gateway"""
    return [APIGatewayAgent("api_gateway_001", message_bus)]
