"""
ALSHAM QUANTUM - Registry Central de Agentes (SINTAXE CORRIGIDA)
Gerenciamento completo dos 34 agentes do registry
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Tipos de agentes no sistema"""
    SPECIALIZED = "specialized"
    SYSTEM = "system" 
    SERVICE = "service"
    META_COGNITIVE = "meta_cognitive"
    DOMAIN = "domain"

class AgentStatus(Enum):
    """Status dos agentes"""
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ERROR = "error"
    MAINTENANCE = "maintenance"

@dataclass
class AgentInfo:
    """Informações de um agente"""
    id: str
    name: str
    type: AgentType
    description: str
    status: AgentStatus = AgentStatus.INACTIVE
    instance: Optional[Any] = None

class BaseAgent(ABC):
    """Classe base para todos os agentes"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.status = AgentStatus.INACTIVE
        self.logger = logging.getLogger(f"agent.{agent_id}")
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Inicializar o agente"""
        pass
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executar uma tarefa"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Desligar o agente"""
        pass

# ===== AGENTES SIMPLIFICADOS =====

class MockAgent(BaseAgent):
    """Agente mock para registry"""
    
    async def initialize(self) -> bool:
        self.status = AgentStatus.ACTIVE
        return True
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "completed", "agent": self.agent_id}
    
    async def shutdown(self) -> bool:
        self.status = AgentStatus.INACTIVE
        return True

# ===== REGISTRY PRINCIPAL =====


class AgentRegistry:
    """
    Registry central de agentes do ALSHAM QUANTUM.
    Gerencia instâncias, status e operações de todos os agentes do sistema.
    Implementa singleton global para acesso centralizado.
    """

    def __init__(self) -> None:
        self.agents: Dict[str, AgentInfo] = {}
        self._initialize_mock_agents()

    def _initialize_mock_agents(self) -> None:
        """
        Inicializa 34 agentes mock, um para cada tipo e domínio, para garantir que o registry nunca fique vazio.
        Facilita testes, integração e evita erros de lookup.
        """
        agent_names = [
            # Specialized (5)
            "data_analysis", "document_processor", "image_processor", "web_scraping", "code_generator",
            # System (5)
            "logging", "security", "monitoring", "backup", "configuration",
            # Service (5)
            "database", "cache", "file_storage", "network", "queue",
            # Meta-Cognitive (5)
            "planning", "reasoning", "learning", "memory", "attention",
            # Domain (14)
            "analytics", "sales", "social_media", "support", "marketing", "content",
            "research", "automation", "optimization", "integration", "translation",
            "voice", "video", "workflow"
        ]
        for i, agent_name in enumerate(agent_names):
            if i < 5:
                agent_type = AgentType.SPECIALIZED
            elif i < 10:
                agent_type = AgentType.SYSTEM
            elif i < 15:
                agent_type = AgentType.SERVICE
            elif i < 20:
                agent_type = AgentType.META_COGNITIVE
            else:
                agent_type = AgentType.DOMAIN
            self.agents[agent_name] = AgentInfo(
                id=agent_name,
                name=f"{agent_name.replace('_', ' ').title()} Agent",
                type=agent_type,
                description=f"Mock agent for {agent_name}",
                instance=MockAgent(agent_name, f"{agent_name}_agent")
            )

    async def initialize_all_agents(self) -> Dict[str, int]:
        """
        Inicializa todos os agentes registrados, atualizando status e contando por tipo.
        :return: Dicionário com contagem de agentes ativos por tipo.
        """
        counters = {agent_type.value: 0 for agent_type in AgentType}
        for agent_info in self.agents.values():
            try:
                agent_info.status = AgentStatus.INITIALIZING
                success = await agent_info.instance.initialize()
                if success:
                    agent_info.status = AgentStatus.ACTIVE
                    counters[agent_info.type.value] += 1
                    logger.info(f"✅ {agent_info.name} inicializado com sucesso.")
                else:
                    agent_info.status = AgentStatus.ERROR
                    logger.warning(f"⚠️ {agent_info.name} falhou ao inicializar.")
            except Exception as e:
                agent_info.status = AgentStatus.ERROR
                logger.error(f"Erro na inicialização do agente {agent_info.name}: {e}", exc_info=True)
        return counters

    async def shutdown_all_agents(self) -> None:
        """
        Desliga todos os agentes ativos registrados, atualizando status.
        """
        for agent_info in self.agents.values():
            if agent_info.instance and agent_info.status == AgentStatus.ACTIVE:
                try:
                    await agent_info.instance.shutdown()
                    agent_info.status = AgentStatus.INACTIVE
                    logger.info(f"🔻 {agent_info.name} desligado com sucesso.")
                except Exception as e:
                    logger.error(f"Erro ao desligar agente {agent_info.name}: {e}", exc_info=True)

    def get_system_status(self) -> Dict[str, Any]:
        """
        Retorna o status geral do sistema, incluindo totais por status e tipo.
        :return: Dicionário com totais e breakdown dos agentes.
        """
        status_counts = {status.value: 0 for status in AgentStatus}
        type_counts = {agent_type.value: 0 for agent_type in AgentType}
        for agent_info in self.agents.values():
            status_counts[agent_info.status.value] += 1
            type_counts[agent_info.type.value] += 1
        return {
            "total_agents": len(self.agents),
            "by_status": status_counts,
            "by_type": type_counts,
            "active_agents": status_counts.get("active", 0)
        }

# Instância global
agent_registry = AgentRegistry()
