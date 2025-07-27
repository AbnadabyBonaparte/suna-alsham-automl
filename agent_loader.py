#!/usr/bin/env python3
"""
Agent Loader REAL - Chama as funções create_*_agents() dos arquivos
Sistema completo com 39 agentes poderosos
"""

import asyncio
import logging
from typing import List, Dict, Any
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class RealAgentLoader:
    def __init__(self, network: MultiAgentNetwork):
        self.network = network
        self.loaded_agents = {}
        self.total_agents = 0
        
    async def load_all_agents(self) -> Dict[str, Any]:
        """Carrega TODOS os agentes chamando as funções create_*_agents() reais"""
        try:
            logger.info("🚀 Iniciando carregamento REAL de TODOS os agentes...")
            
            results = {
                "status": "in_progress",
                "loaded_by_module": {},
                "total_agents": 0,
                "failed_modules": []
            }
            
            # 1. CORE AGENTS V3 (5 agentes)
            try:
                from core_agents_v3 import create_core_agents_v3
                core_agents = create_core_agents_v3(self.network.message_bus)
                await self._add_agents_to_network(core_agents, "core_agents_v3")
                results["loaded_by_module"]["core_agents_v3"] = len(core_agents)
                logger.info(f"✅ core_agents_v3: {len(core_agents)} agentes carregados")
            except Exception as e:
                logger.error(f"❌ Erro carregando core_agents_v3: {e}")
                results["failed_modules"].append(f"core_agents_v3: {e}")
            
            # 2. SPECIALIZED AGENTS (5 agentes)
            try:
                from specialized_agents import create_specialized_agents
                specialized_agents = create_specialized_agents(self.network.message_bus)
                await self._add_agents_to_network(specialized_agents, "specialized_agents")
                results["loaded_by_module"]["specialized_agents"] = len(specialized_agents)
                logger.info(f"✅ specialized_agents: {len(specialized_agents)} agentes carregados")
            except Exception as e:
                logger.error(f"❌ Erro carregando specialized_agents: {e}")
                results["failed_modules"].append(f"specialized_agents: {e}")
            
            # 3. AI POWERED AGENTS (3 agentes)
            try:
                from ai_powered_agents import create_ai_agents
                ai_agents = create_ai_agents(self.network.message_bus)
                await self._add_agents_to_network(ai_agents, "ai_powered_agents")
                results["loaded_by_module"]["ai_powered_agents"] = len(ai_agents)
                logger.info(f"✅ ai_powered_agents: {len(ai_agents)} agentes carregados")
            except Exception as e:
                logger.error(f"❌ Erro carregando ai_powered_agents: {e}")
                results["failed_modules"].append(f"ai_powered_agents: {e}")
            
            # 4. SYSTEM AGENTS
            try:
                from system_agents import create_system_agents
                system_agents = create_system_agents(self.network.message_bus)
                await self._add_agents_to_network(system_agents, "system_agents")
                results["loaded_by_module"]["system_agents"] = len(system_agents)
                logger.info(f"✅ system_agents: {len(system_agents)} agentes carregados")
            except Exception as e:
                logger.error(f"❌ Erro carregando system_agents: {e}")
                results["failed_modules"].append(f"system_agents: {e}")
            
            # 5. SERVICE AGENTS
            try:
                from service_agents import create_service_agents
                service_agents = create_service_agents(self.network.message_bus)
                await self._add_agents_to_network(service_agents, "service_agents")
                results["loaded_by_module"]["service_agents"] = len(service_agents)
                logger.info(f"✅ service_agents: {len(service_agents)} agentes carregados")
            except Exception as e:
                logger.error(f"❌ Erro carregando service_agents: {e}")
                results["failed_modules"].append(f"service_agents: {e}")
            
            # 6. META COGNITIVE AGENTS
            try:
                from meta_cognitive_agents import create_meta_cognitive_agents
                meta_agents = create_meta_cognitive_agents(self.network.message_bus)
                await self._add_agents_to_network(meta_agents, "meta_cognitive_agents")
                results["loaded_by_module"]["meta_cognitive_agents"] = len(meta_agents)
                logger.info(f"✅ meta_cognitive_agents: {len(meta_agents)} agentes carregados")
            except Exception as e:
                logger.error(f"❌ Erro carregando meta_cognitive_agents: {e}")
                results["failed_modules"].append(f"meta_cognitive_agents: {e}")
            
            # 7. AGENTES INDIVIDUAIS (AGORA COM TODOS OS 16 NOVOS!)
            individual_agents = [
                # Agentes existentes
                ("code_analyzer_agent", "create_code_analyzer_agent"),
                ("analyze_agent_structure", "create_structure_analyzer_agent"),
                ("performance_monitor_agent", "create_performance_monitor"),
                ("computer_control_agent", "create_computer_control_agent"),
                ("web_search_agent", "create_web_search_agent"),
                ("code_corrector_agent", "create_code_corrector_agent"),
                ("debug_agent_creation", "create_debug_master_agent"),
                
                # NOVOS AGENTES DE SEGURANÇA (PRIORIDADE ALTA)
                ("security_guardian_agent", "create_security_guardian_agent"),
                ("validation_sentinel_agent", "create_validation_sentinel_agent"),
                ("disaster_recovery_agent", "create_disaster_recovery_agent"),
                
                # NOVOS AGENTES DE INFRAESTRUTURA
                ("backup_agent", "create_backup_agent"),
                ("database_agent", "create_database_agent"),
                ("logging_agent", "create_logging_agent"),
                
                # NOVOS AGENTES DE SERVIÇO
                ("api_gateway_agent", "create_api_gateway_agent"),
                ("notification_agent", "create_notification_agent"),
                ("deployment_agent", "create_deployment_agent"),
                
                # NOVOS AGENTES DE QUALIDADE
                ("testing_agent", "create_testing_agent"),
                ("visualization_agent", "create_visualization_agent")
            ]
            
            for module_name, function_name in individual_agents:
                try:
                    module = __import__(module_name)
                    create_function = getattr(module, function_name)
                    agents = create_function(self.network.message_bus)
                    
                    # Normalizar para lista se retornar agente único
                    if not isinstance(agents, list):
                        agents = [agents] if agents else []
                    
                    await self._add_agents_to_network(agents, module_name)
                    results["loaded_by_module"][module_name] = len(agents)
                    logger.info(f"✅ {module_name}: {len(agents)} agentes carregados")
                except Exception as e:
                    logger.error(f"❌ Erro carregando {module_name}: {e}")
                    results["failed_modules"].append(f"{module_name}: {e}")
            
            # RESULTADO FINAL
            results["total_agents"] = self.total_agents
            results["status"] = "completed"
            results["network_status"] = self.network.get_network_status()
            results["summary"] = {
                "modules_attempted": len(results["loaded_by_module"]) + len(results["failed_modules"]),
                "modules_successful": len(results["loaded_by_module"]),
                "modules_failed": len(results["failed_modules"]),
                "agents_loaded": self.total_agents
            }
            
            logger.info(f"🎯 CARREGAMENTO CONCLUÍDO!")
            logger.info(f"📊 Total de agentes: {self.total_agents}")
            logger.info(f"✅ Módulos bem-sucedidos: {len(results['loaded_by_module'])}")
            logger.info(f"❌ Módulos com falha: {len(results['failed_modules'])}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro crítico no carregamento: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _add_agents_to_network(self, agents: List, module_name: str):
        """Adiciona lista de agentes à rede"""
        if not agents:
            logger.warning(f"⚠️ Nenhum agente retornado de {module_name}")
            return
        
        for agent in agents:
            try:
                success = self.network.add_agent(agent)
                if success:
                    self.loaded_agents[agent.agent_id] = agent
                    self.total_agents += 1
                    logger.info(f"   ✅ {agent.agent_id} adicionado à rede")
                else:
                    logger.warning(f"   ⚠️ Falha adicionando {agent.agent_id} à rede")
            except Exception as e:
                logger.error(f"   ❌ Erro adicionando agente de {module_name}: {e}")

async def load_agents_into_network(network: MultiAgentNetwork) -> Dict[str, Any]:
    """Função principal para carregar TODOS os agentes reais"""
    loader = RealAgentLoader(network)
    return await loader.load_all_agents()

async def initialize_all_agents(network: MultiAgentNetwork) -> Dict[str, Any]:
    """Inicializa TODOS os agentes reais na rede"""
    return await load_agents_into_network(network)
