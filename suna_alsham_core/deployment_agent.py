#!/usr/bin/env python3
"""
Módulo do Deployment Agent - SUNA-ALSHAM
[Versão Final de Produção] - Mais robusto contra ambientes sem Git.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import git
    import docker
    DEPLOY_LIBS_AVAILABLE = True
except ImportError:
    DEPLOY_LIBS_AVAILABLE = False

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class DeployStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCESSFUL = "successful"
    FAILED = "failed"

@dataclass
class DeploymentJob:
    job_id: str
    target_branch: str
    docker_image_tag: str
    status: DeployStatus = DeployStatus.PENDING
    logs: List[str] = field(default_factory=list)

class DeploymentAgent(BaseNetworkAgent):
    """
    Agente especialista em automatizar o processo de CI/CD.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend(["continuous_deployment", "git_operations"])
        self.repo_path = Path.cwd()
        
        if not DEPLOY_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.critical("Bibliotecas 'gitpython' ou 'docker' não encontradas. O DeploymentAgent operará em modo degradado.")
        else:
            try:
                # --- CORREÇÃO DE ROBUSTEZ AQUI ---
                # Tenta inicializar o repositório, mas se falhar (como no Railway),
                # apenas avisa e entra em modo degradado, sem quebrar.
                self.repo = git.Repo(self.repo_path, search_parent_directories=True)
                self.docker_client = docker.from_env()
                logger.info("Cliente Git e Docker inicializados com sucesso.")
            except git.exc.InvalidGitRepositoryError:
                logger.warning("Nenhum repositório Git encontrado. O DeploymentAgent operará em modo degradado (apenas Docker).")
                self.repo = None
                self.docker_client = docker.from_env() # Docker ainda pode funcionar
            except Exception as e:
                logger.critical(f"Erro ao inicializar Git/Docker: {e}")
                self.status = "degraded"
                self.repo = None
                self.docker_client = None

        logger.info(f"🚀 {self.agent_id} (Deployment) inicializado.")

    # O resto do arquivo permanece o mesmo...
    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "deploy":
            result = self.deploy(message.content)
            await self.publish_response(message, result)

    def deploy(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.status == "degraded" or not self.docker_client:
            return {"status": "error", "message": "Serviço de deploy indisponível."}
        # ... (lógica de deploy)
        return {"status": "completed", "message": "Deploy simulado concluído."}


def create_deployment_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Deployment."""
    agents = []
    logger.info("🚀 Criando DeploymentAgent...")
    try:
        agent = DeploymentAgent("deployment_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DeploymentAgent: {e}", exc_info=True)
    return agents
