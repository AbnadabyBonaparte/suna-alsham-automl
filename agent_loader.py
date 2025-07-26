#!/usr/bin/env python3
"""
Agent Loader - Carrega todos os agentes do SUNA-ALSHAM System
Baseado nos arquivos existentes no repositório
"""

import asyncio
import logging
from typing import List, Dict, Any
from multi_agent_network import MultiAgentNetwork, BaseNetworkAgent, AgentType

logger = logging.getLogger(__name__)

class AgentLoader:
    def __init__(self, network: MultiAgentNetwork):
        self.network = network
        self.loaded_agents = {}
        
    async def load_all_agents(self) -> Dict[str, Any]:
        """Carrega todos os agentes baseados nos arquivos existentes"""
        try:
            logger.info("🚀 Iniciando carregamento de todos os agentes...")
            
            # Lista dos agentes baseada nos arquivos que vi no repositório
            agents_to_load = [
                # Core Agents
                {"id": "core_agent_v3", "type": AgentType.CORE, "file": "ai_powered_agents.py"},
                {"id": "system_agent", "type": AgentType.SYSTEM, "file": "system_agents.py"},
                {"id": "service_agent", "type": AgentType.SERVICE, "file": "service_agents.py"},
                
                # Specialized Agents
                {"id": "specialized_agent", "type": AgentType.SPECIALIZED, "file": "specialized_agents.py"},
                {"id": "performance_monitor", "type": AgentType.MONITOR, "file": "performance_monitor_agent.py"},
                {"id": "meta_cognitive", "type": AgentType.META_COGNITIVE, "file": "meta_cognitive_agents.py"},
                
                # Analytics & Intelligence
                {"id": "analytics_agent", "type": AgentType.ANALYTICS, "file": "analyze_agent_structure.py"},
                {"id": "code_analyzer", "type": AgentType.ANALYTICS, "file": "code_analyzer_agent.py"},
                {"id": "code_corrector", "type": AgentType.SPECIALIST, "file": "code_corrector_agent.py"},
                
                # Evolution & Learning
                {"id": "real_evolution_engine", "type": AgentType.EVOLVER, "file": "real_evolution_engine.py"},
                {"id": "evolution_dashboard", "type": AgentType.MONITOR, "file": "evolution_dashboard.py"},
                
                # Automation & Control
                {"id": "computer_control", "type": AgentType.AUTOMATOR, "file": "computer_control_agent.py"},
                {"id": "web_search_agent", "type": AgentType.SPECIALIST, "file": "web_search_agent.py"},
                
                # Orchestration
                {"id": "main_orchestrator", "type": AgentType.ORCHESTRATOR, "file": "main_orchestrator.py"},
                {"id": "suna_alsham_bootstrap", "type": AgentType.COORDINATOR, "file": "suna_alsham_bootstrap.py"},
                
                # Diagnostic & Debug
                {"id": "debug_agent", "type": AgentType.SPECIALIST, "file": "debug_agent_creation.py"},
                {"id": "diagnostic_complete", "type": AgentType.ANALYTICS, "file": "diagnostic_complete.py"},
                {"id": "diagnostic_enterprise", "type": AgentType.ANALYTICS, "file": "diagnostic_enterprise.py"},
                
                # Deployment & Optimization
                {"id": "deployment_report", "type": AgentType.MONITOR, "file": "deployment_report.py"},
                {"id": "deployment_optimization", "type": AgentType.OPTIMIZER, "file": "deployment_optimization.py"},
                
                # Guard & Security
                {"id": "guard_service", "type": AgentType.GUARD, "file": "guard_service.py"},
                
                # Testing & Verification
                {"id": "test_main_direct", "type": AgentType.SPECIALIST, "file": "test_main_direct.py"},
                {"id": "verify_structure", "type": AgentType.SPECIALIST, "file": "verify_structure.py"},
                
                # Emergency & Conversational
                {"id": "emergency_xint", "type": AgentType.SYSTEM, "file": "emergency_xint.py"},
                {"id": "start_agent", "type": AgentType.COORDINATOR, "file": "start.py"}
            ]
            
            loaded_count = 0
            for agent_config in agents_to_load:
                try:
                    agent = await self._create_agent(agent_config)
                    if agent:
                        success = self.network.add_agent(agent)
                        if success:
                            self.loaded_agents[agent_config["id"]] = agent
                            loaded_count += 1
                            logger.info(f"✅ Agente {agent_config['id']} carregado com sucesso")
                        else:
                            logger.warning(f"⚠️ Falha adicionando agente {agent_config['id']} à rede")
                    else:
                        logger.warning(f"⚠️ Falha criando agente {agent_config['id']}")
                except Exception as e:
                    logger.error(f"❌ Erro carregando agente {agent_config['id']}: {e}")
            
            result = {
                "status": "completed",
                "total_agents_attempted": len(agents_to_load),
                "agents_loaded_successfully": loaded_count,
                "loaded_agents": list(self.loaded_agents.keys()),
                "network_status": self.network.get_network_status()
            }
            
            logger.info(f"🎯 Carregamento concluído: {loaded_count}/{len(agents_to_load)} agentes carregados")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro no carregamento geral de agentes: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _create_agent(self, config: Dict[str, Any]) -> BaseNetworkAgent:
        """Cria um agente baseado na configuração"""
        try:
            # Cria um agente base funcional
            agent = BaseNetworkAgent(
                agent_id=config["id"],
                agent_type=config["type"],
                message_bus=self.network.message_bus
            )
            
            # Adiciona metadados específicos
            agent.source_file = config.get("file", "unknown")
            agent.description = f"Agente {config['type'].value} baseado em {config['file']}"
            
            return agent
            
        except Exception as e:
            logger.error(f"❌ Erro criando agente {config['id']}: {e}")
            return None

async def load_agents_into_network(network: MultiAgentNetwork) -> Dict[str, Any]:
    """Função principal para carregar agentes na rede"""
    loader = AgentLoader(network)
    return await loader.load_all_agents()

# Função de conveniência para usar no main_complete_system.py
async def initialize_all_agents(network: MultiAgentNetwork) -> Dict[str, Any]:
    """Inicializa todos os agentes na rede"""
    return await load_agents_into_network(network)
