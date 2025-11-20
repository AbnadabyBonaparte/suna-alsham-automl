#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Registry Central de Agentes
Registry profissional e padronizado para gerenciamento de todos os agentes do sistema.
Inclui integração com agent_loader via factory create_agents.
Versão corrigida e otimizada.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Tipos de agentes no sistema ALSHAM QUANTUM."""
    SPECIALIZED = "specialized"
    SYSTEM = "system"
    SERVICE = "service"
    META_COGNITIVE = "meta_cognitive"
    DOMAIN = "domain"
    CORE = "core"
    AI_POWERED = "ai_powered"

class AgentStatus(Enum):
    """Status possíveis de um agente no sistema."""
    INACTIVE = "inactive"
    INITIALIZING = "initializing" 
    ACTIVE = "active"
    ERROR = "error"
    MAINTENANCE = "maintenance"

@dataclass
class AgentInfo:
    """Estrutura de dados para armazenar informações e instância de um agente."""
    id: str
    name: str
    type: AgentType
    description: str
    status: AgentStatus = AgentStatus.INACTIVE
    instance: Optional[Any] = None
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

class BaseAgent(ABC):
    """Classe base abstrata para todos os agentes do sistema."""
    
    def __init__(self, agent_id: str, name: str, agent_type: AgentType = AgentType.SYSTEM) -> None:
        self.agent_id: str = agent_id
        self.name: str = name
        self.agent_type: AgentType = agent_type
        self.status: AgentStatus = AgentStatus.INACTIVE
        self.capabilities: List[str] = []
        self.logger = logging.getLogger(f"agent.{agent_id}")

    @abstractmethod
    async def initialize(self) -> bool:
        """Inicializa o agente. Deve ser implementado pelas subclasses."""
        pass

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma tarefa. Deve ser implementado pelas subclasses."""
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """Desliga o agente. Deve ser implementado pelas subclasses."""
        pass

class RegistryAgent(BaseAgent):
    """
    Agente especializado para gerenciamento do registry central.
    Integra perfeitamente com o sistema de message_bus do ALSHAM QUANTUM.
    """
    
    def __init__(self, message_bus=None):
        super().__init__(
            agent_id="registry_central_001", 
            name="Registry Central", 
            agent_type=AgentType.SYSTEM
        )
        self.message_bus = message_bus
        self.registry = AgentRegistry()
        self.capabilities = [
            "agent_management",
            "registry_operations", 
            "system_monitoring",
            "agent_lookup",
            "status_tracking"
        ]

    async def initialize(self) -> bool:
        """Inicializa o registry agent e todos os agentes mock."""
        try:
            self.status = AgentStatus.INITIALIZING
            
            # Inicializa todos os agentes mock do registry
            counters = await self.registry.initialize_all_agents()
            
            self.status = AgentStatus.ACTIVE
            
            total_active = sum(counters.values())
            self.logger.info(f"✅ Registry Central inicializado: {total_active} agentes mock ativos")
            self.logger.info(f"📊 Breakdown: {dict(counters)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na inicialização do Registry: {e}", exc_info=True)
            self.status = AgentStatus.ERROR
            return False

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Executa operações do registry baseadas no tipo de task."""
        try:
            task_type = task.get("type", "status")
            
            if task_type == "status":
                return self.registry.get_system_status()
            elif task_type == "lookup":
                agent_id = task.get("agent_id")
                return self.registry.lookup_agent(agent_id)
            elif task_type == "list":
                return {"agents": list(self.registry.agents.keys())}
            elif task_type == "health_check":
                return await self._health_check()
            else:
                return {"error": f"Tipo de task desconhecido: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"Erro na execução da task: {e}", exc_info=True)
            return {"error": str(e)}

    async def _health_check(self) -> Dict[str, Any]:
        """Verifica a saúde de todos os agentes registrados."""
        status = self.registry.get_system_status()
        health_score = (status["active_agents"] / status["total_agents"]) * 100 if status["total_agents"] > 0 else 0
        
        return {
            "registry_status": "healthy" if health_score >= 80 else "degraded",
            "health_score": f"{health_score:.1f}%",
            "total_agents": status["total_agents"],
            "active_agents": status["active_agents"],
            "details": status
        }

    async def shutdown(self) -> bool:
        """Desliga o registry agent e todos os agentes registrados."""
        try:
            await self.registry.shutdown_all_agents()
            self.status = AgentStatus.INACTIVE
            self.logger.info("🔻 Registry Central desligado com sucesso")
            return True
        except Exception as e:
            self.logger.error(f"Erro no shutdown do Registry: {e}", exc_info=True)
            return False

class MockAgent(BaseAgent):
    """Agente mock para testes e fallback do registry."""
    
    def __init__(self, agent_id: str, name: str, agent_type: AgentType = AgentType.SYSTEM):
        super().__init__(agent_id, name, agent_type)

    async def initialize(self) -> bool:
        self.status = AgentStatus.ACTIVE
        return True

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "completed", 
            "agent": self.agent_id,
            "mock": True,
            "task_type": task.get("type", "unknown")
        }

    async def shutdown(self) -> bool:
        self.status = AgentStatus.INACTIVE
        return True

class AgentRegistry:
    """
    Registry central de agentes do ALSHAM QUANTUM.
    Gerencia instâncias, status e operações de todos os agentes do sistema.
    """
    
    def __init__(self) -> None:
        self.agents: Dict[str, AgentInfo] = {}
        self._initialize_comprehensive_mock_agents()

    def _initialize_comprehensive_mock_agents(self) -> None:
        """
        Inicializa um conjunto abrangente de 40 agentes mock cobrindo todos os domínios.
        Garante que o registry nunca fique vazio e facilita testes/integração.
        """
        mock_agents_config = [
            # SPECIALIZED (8 agents)
            ("data_analysis_001", "Data Analysis Agent", AgentType.SPECIALIZED, ["data_processing", "analytics"]),
            ("document_processor_001", "Document Processor", AgentType.SPECIALIZED, ["pdf_processing", "text_extraction"]),
            ("image_processor_001", "Image Processor", AgentType.SPECIALIZED, ["image_analysis", "computer_vision"]),
            ("web_scraping_001", "Web Scraping Agent", AgentType.SPECIALIZED, ["web_crawling", "data_extraction"]),
            ("code_generator_001", "Code Generator", AgentType.SPECIALIZED, ["code_generation", "programming"]),
            ("api_integration_001", "API Integration", AgentType.SPECIALIZED, ["api_calls", "integration"]),
            ("file_manager_001", "File Manager", AgentType.SPECIALIZED, ["file_operations", "storage"]),
            ("notification_sender_001", "Notification Sender", AgentType.SPECIALIZED, ["notifications", "alerts"]),
            
            # SYSTEM (8 agents)
            ("logging_001", "Logging System", AgentType.SYSTEM, ["logging", "monitoring"]),
            ("security_001", "Security Manager", AgentType.SYSTEM, ["security", "authentication"]),
            ("monitoring_001", "System Monitor", AgentType.SYSTEM, ["monitoring", "health_check"]),
            ("backup_001", "Backup Manager", AgentType.SYSTEM, ["backup", "recovery"]),
            ("configuration_001", "Config Manager", AgentType.SYSTEM, ["configuration", "settings"]),
            ("scheduler_001", "Task Scheduler", AgentType.SYSTEM, ["scheduling", "cron"]),
            ("error_handler_001", "Error Handler", AgentType.SYSTEM, ["error_handling", "debugging"]),
            ("performance_001", "Performance Monitor", AgentType.SYSTEM, ["performance", "optimization"]),
            
            # SERVICE (8 agents)  
            ("database_001", "Database Service", AgentType.SERVICE, ["database", "persistence"]),
            ("cache_001", "Cache Service", AgentType.SERVICE, ["caching", "redis"]),
            ("file_storage_001", "File Storage", AgentType.SERVICE, ["storage", "files"]),
            ("network_001", "Network Service", AgentType.SERVICE, ["networking", "http"]),
            ("queue_001", "Queue Service", AgentType.SERVICE, ["queuing", "messaging"]),
            ("email_001", "Email Service", AgentType.SERVICE, ["email", "smtp"]),
            ("sms_001", "SMS Service", AgentType.SERVICE, ["sms", "twilio"]),
            ("payment_001", "Payment Service", AgentType.SERVICE, ["payments", "stripe"]),
            
            # META_COGNITIVE (8 agents)
            ("planning_001", "Planning Agent", AgentType.META_COGNITIVE, ["planning", "strategy"]),
            ("reasoning_001", "Reasoning Engine", AgentType.META_COGNITIVE, ["reasoning", "logic"]),
            ("learning_001", "Learning System", AgentType.META_COGNITIVE, ["learning", "adaptation"]),
            ("memory_001", "Memory Manager", AgentType.META_COGNITIVE, ["memory", "knowledge"]),
            ("attention_001", "Attention Manager", AgentType.META_COGNITIVE, ["attention", "focus"]),
            ("decision_001", "Decision Maker", AgentType.META_COGNITIVE, ["decision", "choice"]),
            ("reflection_001", "Reflection Agent", AgentType.META_COGNITIVE, ["reflection", "analysis"]),
            ("creativity_001", "Creativity Engine", AgentType.META_COGNITIVE, ["creativity", "innovation"]),
            
            # DOMAIN (8 agents)
            ("analytics_001", "Analytics Domain", AgentType.DOMAIN, ["business_analytics", "reporting"]),
            ("sales_001", "Sales Domain", AgentType.DOMAIN, ["sales", "crm"]),
            ("social_media_001", "Social Media Domain", AgentType.DOMAIN, ["social_media", "content"]),
            ("support_001", "Support Domain", AgentType.DOMAIN, ["customer_support", "tickets"]),
            ("marketing_001", "Marketing Domain", AgentType.DOMAIN, ["marketing", "campaigns"]),
            ("content_001", "Content Domain", AgentType.DOMAIN, ["content_creation", "writing"]),
            ("research_001", "Research Domain", AgentType.DOMAIN, ["research", "analysis"]),
            ("automation_001", "Automation Domain", AgentType.DOMAIN, ["automation", "workflows"])
        ]
        
        for agent_id, name, agent_type, capabilities in mock_agents_config:
            mock_instance = MockAgent(agent_id, name, agent_type)
            mock_instance.capabilities = capabilities
            
            self.agents[agent_id] = AgentInfo(
                id=agent_id,
                name=name,
                type=agent_type,
                description=f"Mock agent for {name.lower()}",
                instance=mock_instance,
                capabilities=capabilities
            )

    def register_real_agent(self, agent: BaseAgent) -> bool:
        """
        Registra um agente real no registry, substituindo mock se existir.
        """
        try:
            agent_info = AgentInfo(
                id=agent.agent_id,
                name=agent.name,
                type=agent.agent_type,
                description=f"Real agent: {agent.name}",
                instance=agent,
                capabilities=getattr(agent, 'capabilities', [])
            )
            
            self.agents[agent.agent_id] = agent_info
            logger.info(f"✅ Agente real registrado: {agent.agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao registrar agente {agent.agent_id}: {e}")
            return False

    def lookup_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Busca informações de um agente específico."""
        if agent_id in self.agents:
            agent_info = self.agents[agent_id]
            return {
                "id": agent_info.id,
                "name": agent_info.name,
                "type": agent_info.type.value,
                "status": agent_info.status.value,
                "capabilities": agent_info.capabilities,
                "is_mock": isinstance(agent_info.instance, MockAgent)
            }
        return None

    async def initialize_all_agents(self) -> Dict[str, int]:
        """Inicializa todos os agentes registrados."""
        counters: Dict[str, int] = {agent_type.value: 0 for agent_type in AgentType}
        
        for agent_info in self.agents.values():
            try:
                agent_info.status = AgentStatus.INITIALIZING
                success = await agent_info.instance.initialize()
                
                if success:
                    agent_info.status = AgentStatus.ACTIVE
                    counters[agent_info.type.value] += 1
                else:
                    agent_info.status = AgentStatus.ERROR
                    
            except Exception as e:
                agent_info.status = AgentStatus.ERROR
                logger.error(f"Erro na inicialização do agente {agent_info.name}: {e}")
                
        return counters

    async def shutdown_all_agents(self) -> None:
        """Desliga todos os agentes ativos registrados."""
        for agent_info in self.agents.values():
            if agent_info.instance and agent_info.status == AgentStatus.ACTIVE:
                try:
                    await agent_info.instance.shutdown()
                    agent_info.status = AgentStatus.INACTIVE
                except Exception as e:
                    logger.error(f"Erro ao desligar agente {agent_info.name}: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna o status geral do sistema."""
        status_counts: Dict[str, int] = {status.value: 0 for status in AgentStatus}
        type_counts: Dict[str, int] = {agent_type.value: 0 for agent_type in AgentType}
        
        mock_count = 0
        real_count = 0
        
        for agent_info in self.agents.values():
            status_counts[agent_info.status.value] += 1
            type_counts[agent_info.type.value] += 1
            
            if isinstance(agent_info.instance, MockAgent):
                mock_count += 1
            else:
                real_count += 1
        
        return {
            "total_agents": len(self.agents),
            "by_status": status_counts,
            "by_type": type_counts,
            "active_agents": status_counts.get("active", 0),
            "mock_agents": mock_count,
            "real_agents": real_count,
            "registry_health": "operational" if status_counts.get("active", 0) > 0 else "degraded"
        }

# Instância global do registry
global_agent_registry = AgentRegistry()

def create_agents(message_bus) -> List[BaseAgent]:
    """
    Factory function for agent_loader integration.
    Cria e retorna o RegistryAgent que gerencia todo o registry.
    
    Args:
        message_bus: MessageBus do sistema multi-agente
        
    Returns:
        List[BaseAgent]: Lista contendo o RegistryAgent
    """
    try:
        registry_agent = RegistryAgent(message_bus)
        logger.info("✅ RegistryAgent criado para agent_loader")
        return [registry_agent]
    except Exception as e:
        logger.error(f"❌ Erro ao criar RegistryAgent: {e}")
        return []

# Para compatibilidade e acesso direto
def get_registry() -> AgentRegistry:
    """Retorna a instância global do registry."""
    return global_agent_registry

# Alias para facilitar importação
agent_registry = global_agent_registry
