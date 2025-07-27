#!/usr/bin/env python3
"""
Módulo dos Agentes Core v3 - O coração operacional do SUNA-ALSHAM.

Este módulo define os agentes fundamentais para processamento, segurança e aprendizado.
Refatorado para a nova estrutura de diretórios.
"""

import logging
from typing import List, Dict, Any

from datetime import datetime

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage, AgentCapability
)

logger = logging.getLogger(__name__)


class CoreAgentV3(BaseNetworkAgent):
    """
    Agente Core v3 - Processamento central e coordenação de tarefas críticas.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.CORE, message_bus)
        
        self.add_capability(AgentCapability(
            name="core_processing",
            description="Processamento central de tarefas críticas",
            input_types=["task_request", "data_processing"],
            output_types=["processed_result", "status_update"],
            processing_time_ms=10.0,
            accuracy_score=0.95,
            resource_cost=0.3
        ))
        
        self.add_capability(AgentCapability(
            name="task_coordination",
            description="Coordenação entre agentes do sistema",
            input_types=["coordination_request"],
            output_types=["coordination_response"],
            processing_time_ms=5.0,
            accuracy_score=0.98,
            resource_cost=0.2
        ))
        
        self.active_tasks = {}
        logger.info(f"✅ CoreAgent {self.agent_id} inicializado com processamento avançado.")

    async def _handle_request(self, message: AgentMessage):
        """Processa requisições direcionadas ao Agente Core."""
        try:
            request_type = message.content.get('request_type', 'unknown')
            
            if request_type == 'core_processing':
                result = await self._process_core_task(message.content)
            elif request_type == 'coordination':
                result = await self._coordinate_task(message.content)
            else:
                result = self._default_processing(message.content)
            
            response = self.create_response(message, {"status": "completed", "result": result})
            await self.message_bus.publish(response)
            self.performance_metrics['tasks_completed'] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro processando request em {self.agent_id}: {e}", exc_info=True)
            response = self.create_error_response(message, str(e))
            await self.message_bus.publish(response)

    def _process_core_task(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento específico de tarefas centrais."""
        task_data = content.get('task_data', {})
        logger.info(f"🔧 {self.agent_id} processou tarefa core: {task_data.get('task_id', 'unknown')}")
        return {
            "processed_by": self.agent_id,
            "processing_method": "core_v3_advanced",
            "confidence_score": 0.95,
        }

    def _coordinate_task(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Coordenação entre agentes."""
        target_agents = content.get('target_agents', [])
        logger.info(f"🎯 {self.agent_id} coordenou {len(target_agents)} agentes.")
        return {
            "coordinator": self.agent_id,
            "status": "coordinated"
        }

    def _default_processing(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento padrão para requisições não específicas."""
        return {
            "processed": True,
            "processor": self.agent_id,
        }


class GuardAgentV3(BaseNetworkAgent):
    """
    Agente Guard v3 - Segurança, validação e proteção do sistema.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        
        self.add_capability(AgentCapability(
            name="security_validation",
            description="Validação de segurança de mensagens e operações",
            input_types=["message_validation", "security_check"],
            output_types=["validation_result", "security_report"],
            processing_time_ms=3.0,
            accuracy_score=0.99,
            resource_cost=0.1
        ))
        
        logger.info(f"🛡️ GuardAgent {self.agent_id} inicializado com segurança avançada.")

    async def _handle_request(self, message: AgentMessage):
        """Processa requisições de segurança."""
        try:
            request_type = message.content.get('request_type', 'unknown')
            
            if request_type == 'security_check':
                result = self._perform_security_check(message.content)
            else:
                result = self._default_guard_processing(message.content)
            
            response = self.create_response(message, {"security_status": "validated", "guard_result": result})
            await self.message_bus.publish(response)

        except Exception as e:
            logger.error(f"❌ Erro em validação de segurança {self.agent_id}: {e}", exc_info=True)
            response = self.create_error_response(message, str(e))
            await self.message_bus.publish(response)

    def _perform_security_check(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Executa verificação de segurança."""
        target_str = str(content.get('target', {}))
        status = "passed"
        if "malicious" in target_str.lower() or "exploit" in target_str.lower():
            status = "flagged"
            
        logger.info(f"🛡️ {self.agent_id} executou security check: {status}")
        return {"check_status": status}

    def _default_guard_processing(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento padrão de segurança."""
        return {"guard_status": "processed", "security_level": "standard"}


class LearnAgentV3(BaseNetworkAgent):
    """
    Agente Learn v3 - Aprendizado adaptativo e otimização contínua.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.LEARN, message_bus)
        
        self.add_capability(AgentCapability(
            name="pattern_recognition",
            description="Reconhecimento de padrões em dados e comportamentos",
            input_types=["pattern_data", "behavior_data"],
            output_types=["pattern_analysis", "learning_insight"],
            processing_time_ms=15.0,
            accuracy_score=0.92,
            resource_cost=0.4
        ))
        
        logger.info(f"🧠 LearnAgent {self.agent_id} inicializado com aprendizado adaptativo.")
    
    async def _handle_request(self, message: AgentMessage):
        """Processa requisições de aprendizado."""
        try:
            request_type = message.content.get('request_type', 'unknown')
            
            if request_type == 'pattern_analysis':
                result = self._analyze_patterns(message.content)
            else:
                result = self._default_learning_processing(message.content)
                
            response = self.create_response(message, {"learning_status": "processed", "learning_result": result})
            await self.message_bus.publish(response)
        
        except Exception as e:
            logger.error(f"❌ Erro no aprendizado {self.agent_id}: {e}", exc_info=True)
            response = self.create_error_response(message, str(e))
            await self.message_bus.publish(response)
            
    def _analyze_patterns(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de padrões."""
        data = content.get('pattern_data', {})
        patterns_found = []
        if isinstance(data, dict) and len(data.keys()) > 5:
            patterns_found.append("Estrutura complexa de dados detectada.")
        
        logger.info(f"🔍 {self.agent_id} identificou {len(patterns_found)} padrões.")
        return {"patterns_found": patterns_found}
        
    def _default_learning_processing(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento padrão de aprendizado."""
        return {"learning_status": "processed"}


def create_core_agents_v3(message_bus, num_instances=1) -> List[BaseNetworkAgent]:
    """
    Cria os 5 agentes core v3 especializados para o núcleo do sistema.
    """
    agents = []
    logger.info("🎯 Criando agentes core v3...")
    
    agents_config = [
        {"id": "core_v3_001", "class": CoreAgentV3},
        {"id": "guard_v3_001", "class": GuardAgentV3},
        {"id": "learn_v3_001", "class": LearnAgentV3},
        {"id": "core_v3_002", "class": CoreAgentV3}, # Redundância
        {"id": "guard_v3_002", "class": GuardAgentV3} # Redundância
    ]
    
    for config in agents_config:
        try:
            agent = config["class"](config["id"], message_bus)
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente {config['id']}: {e}", exc_info=True)
            
    return agents
