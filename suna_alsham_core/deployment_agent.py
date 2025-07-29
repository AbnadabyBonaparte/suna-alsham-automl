#!/usr/bin/env python3
"""
Módulo do Deployment Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com integração real com GitPython e Docker SDK,
permitindo que o agente execute operações de deploy de forma autônoma.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] Bibliotecas de deploy são importadas de forma segura.
try:
    import git
    import docker
    DEPLOY_LIBS_AVAILABLE = True
except ImportError:
    DEPLOY_LIBS_AVAILABLE = False

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Enums e Dataclasses ---
class DeployStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCESSFUL = "successful"
    FAILED = "failed"

@dataclass
class DeploymentJob:
    """Representa um trabalho de deploy."""
    job_id: str
    target_branch: str
    docker_image_tag: str
    status: DeployStatus = DeployStatus.PENDING
    logs: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# --- Classe Principal do Agente ---
class DeploymentAgent(BaseNetworkAgent):
    """
    Agente especialista em automatizar o processo de CI/CD (Continuous
    Integration/Continuous Deployment) do próprio sistema SUNA-ALSHAM.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DeploymentAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "continuous_deployment",
            "git_operations",
            "docker_build_push",
        ])
        self.repo_path = Path.cwd()
        
        if not DEPLOY_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.critical("Bibliotecas 'gitpython' ou 'docker' não encontradas. O DeploymentAgent operará em modo degradado.")
        else:
            try:
                self.repo = git.Repo(self.repo_path)
                self.docker_client = docker.from_env()
            except Exception as e:
                logger.critical(f"Erro ao inicializar Git/Docker: {e}")
                self.status = "degraded"

        logger.info(f"🚀 {self.agent_id} (Deployment) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de deploy."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "deploy":
            result = self.deploy(message.content)
            await self.publish_response(message, result)

    def deploy(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Orquestra um ciclo de deploy completo.
        NOTA: Esta é uma operação síncrona e bloqueante por simplicidade na Fase 2.
        """
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de deploy indisponível."}

        target_branch = request_data.get("branch", "main")
        
        job = DeploymentJob(
            job_id=f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            target_branch=target_branch,
            docker_image_tag=f"suna-alsham:{target_branch}-latest"
        )
        
        try:
            # 1. Puxar as últimas alterações do Git
            job.logs.append(f"Puxando alterações da branch '{target_branch}'...")
            origin = self.repo.remotes.origin
            origin.pull(target_branch)
            job.logs.append("Git pull concluído com sucesso.")

            # 2. Construir a imagem Docker
            job.status = DeployStatus.BUILDING
            job.logs.append(f"Construindo imagem Docker: {job.docker_image_tag}...")
            image, build_logs = self.docker_client.images.build(
                path=str(self.repo_path),
                tag=job.docker_image_tag,
                rm=True
            )
            job.logs.extend([log.get("stream", "").strip() for log in build_logs])
            job.logs.append(f"Imagem {image.short_id} construída com sucesso.")
            
            # 3. (Opcional) Push para um registry
            # self.docker_client.images.push(job.docker_image_tag)

            job.status = DeployStatus.SUCCESSFUL
            return {"status": "completed", "job_id": job.job_id, "final_image_id": image.short_id}

        except Exception as e:
            logger.error(f"❌ Falha no deploy: {e}", exc_info=True)
            job.status = DeployStatus.FAILED
            job.logs.append(f"ERRO: {e}")
            return {"status": "error", "message": str(e), "job_id": job.job_id}

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
