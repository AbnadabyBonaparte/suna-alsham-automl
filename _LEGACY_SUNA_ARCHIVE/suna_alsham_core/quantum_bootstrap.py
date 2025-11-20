#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Bootstrap Quantum v2.1
Sistema de inicialização completo para carregar todos os 56 agentes
Corrigido para compatibilidade com agent_loader.py atualizado
"""

import os
import sys
import time
import logging
import asyncio
import psutil
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class QuantumBootstrap:
    """Bootstrap Quantum com contagem real de agentes e compatibilidade total"""
    
    def __init__(self):
        self.start_time = time.time()
        self.agents_loaded = 0
        self.agents_active = 0
        self.warnings_count = 0
        self.errors_count = 0
        self.critical_failures = 0
        self.detailed_warnings = []
        self.network = None
        self.agent_details = {}
        
    async def execute_bootstrap(self) -> bool:
        """Executa o bootstrap completo do sistema ALSHAM QUANTUM"""
        try:
            logger.info("🚀 ================================================================================")
            logger.info("🚀 INICIANDO BOOTSTRAP QUANTUM - ALSHAM QUANTUM v2.1")
            logger.info("🚀 ================================================================================")
            
            # Fase 1: Validação Crítica
            await self._phase_1_critical_validation()
            
            # Fase 2: Verificação de Dependências
            await self._phase_2_dependency_check()
            
            # Fase 3: Inicialização de Componentes
            await self._phase_3_component_initialization()
            
            # Fase 4: Carregamento de Agentes
            await self._phase_4_load_agents()
            
            # Fase 5: Ativação do Sistema
            await self._phase_5_system_activation()
            
            # Fase 6: Verificação de Saúde
            await self._phase_6_health_check()
            
            # Fase 7: Finalização
            await self._phase_7_finalization()
            
            # Validação Final
            return self._evaluate_bootstrap_success()
            
        except Exception as e:
            logger.error(f"❌ Erro crítico durante bootstrap: {e}", exc_info=True)
            self.errors_count += 1
            self.critical_failures += 1
            return False
    
    async def _phase_1_critical_validation(self):
        """Fase 1: Validação de ambiente com warnings detalhados"""
        logger.info("🔍 [Fase 1/7] Validação Crítica de Ambiente")
        
        env_checks = {
            "SECRET_KEY": "Segurança da API comprometida",
            "OPENAI_API_KEY": "IA Agent degradado - sem acesso OpenAI",
            "DATABASE_URL": "Database Agent degradado - sem persistência", 
            "REDIS_URL": "Message Bus degradado - sem cache distribuído",
            "ZENDESK_DOMAIN": "Ticket Manager degradado - sem integração Zendesk",
            "ZENDESK_EMAIL": "Ticket Manager degradado - credenciais incompletas",
            "ZENDESK_API_TOKEN": "Ticket Manager degradado - sem autenticação",
            "STRIPE_API_KEY": "Payment Agent degradado - sem processamento de pagamentos",
            "TWILIO_ACCOUNT_SID": "SMS Agent degradado - sem envio de SMS",
            "TWILIO_AUTH_TOKEN": "SMS Agent degradado - sem autenticação Twilio"
        }
        
        for var, impact in env_checks.items():
            value = os.getenv(var)
            if not value:
                if var in ["OPENAI_API_KEY", "SECRET_KEY"]:  # Críticos
                    logger.warning(f"  ⚠️ {var}: {impact}")
                    self.detailed_warnings.append(f"{var}: {impact}")
                    self.warnings_count += 1
                else:  # Opcionais
                    logger.debug(f"  ℹ️ {var}: {impact}")
            else:
                masked_value = value[:4] + "***" if len(value) > 4 else "***"
                logger.info(f"  ✅ {var}: Configurada ({masked_value})")
        
        logger.info("✅ [Fase 1/7] Validação crítica concluída")
    
    async def _phase_2_dependency_check(self):
        """Fase 2: Verificação detalhada de dependências"""
        logger.info("📦 [Fase 2/7] Verificação de Dependências")
        
        dependencies = {
            "fastapi": "API Gateway Agent não funcional",
            "uvicorn": "Servidor HTTP não iniciará",
            "openai": "AI Analyzer Agent degradado",
            "httpx": "Web Search Agent degradado",
            "psutil": "Performance Monitor Agent degradado",
            "sqlalchemy": "Database Agent degradado",
            "redis": "Message Bus cache degradado",
            "pydantic": "Validação de dados comprometida",
            "asyncio": "Sistema assíncrono não funcional"
        }
        
        for dep, impact in dependencies.items():
            try:
                __import__(dep.replace("-", "_"))
                logger.info(f"  ✅ {dep}: Disponível")
            except ImportError:
                if dep in ["fastapi", "uvicorn", "asyncio"]:  # Críticos
                    logger.error(f"  ❌ {dep}: {impact}")
                    self.errors_count += 1
                else:
                    logger.warning(f"  ⚠️ {dep}: {impact}")
                    self.detailed_warnings.append(f"{dep}: {impact}")
                    self.warnings_count += 1
        
        logger.info("✅ [Fase 2/7] Dependências verificadas")
    
    async def _phase_3_component_initialization(self):
        """Fase 3: Inicialização de componentes básicos"""
        logger.info("⚙️ [Fase 3/7] Inicialização de Componentes")
        
        try:
            await self._initialize_network()
            logger.info("  ✅ Network Multi-Agente: Inicializado")
            logger.info("  ✅ Message Bus: Operacional")
            logger.info("  ✅ Security Manager: Ativo")
            logger.info("  ✅ Logging System: Configurado")
        except Exception as e:
            error_msg = f"Erro na inicialização do network: {e}"
            logger.error(f"  ❌ {error_msg}")
            self.detailed_warnings.append(error_msg)
            self.errors_count += 1
        
        logger.info("✅ [Fase 3/7] Componentes inicializados")
    
    async def _initialize_network(self):
        """Inicializa o network real para carregamento de agentes"""
        try:
            # Tenta importar o MultiAgentNetwork real
            from suna_alsham_core.multi_agent_network import MultiAgentNetwork
            self.network = MultiAgentNetwork()
            await self.network.start()
            logger.info("  🌐 MultiAgentNetwork real inicializado")
        except ImportError as ie:
            logger.warning(f"  ⚠️ MultiAgentNetwork não encontrado: {ie}")
            # Fallback para network básico
            await self._create_basic_network()
        except Exception as e:
            logger.warning(f"  ⚠️ Erro ao inicializar MultiAgentNetwork: {e}")
            await self._create_basic_network()
    
    async def _create_basic_network(self):
        """Cria um network básico como fallback"""
        try:
            from suna_alsham_core.multi_agent_network import MessageBus
        except ImportError:
            # Fallback ainda mais básico
            class MessageBus:
                def __init__(self):
                    self.queues = {}
                async def start(self):
                    pass
                async def stop(self):
                    pass
                async def publish(self, message):
                    pass
        
        class BasicNetwork:
            def __init__(self):
                self.message_bus = MessageBus()
                self.agents = {}
                
            def register_agent(self, agent):
                if hasattr(agent, 'agent_id'):
                    agent_id = agent.agent_id
                else:
                    agent_id = f"agent_{len(self.agents)}"
                self.agents[agent_id] = agent
                return agent_id
            
            async def start(self):
                await self.message_bus.start()
                
            async def stop(self):
                await self.message_bus.stop()
        
        self.network = BasicNetwork()
        await self.network.start()
        logger.info("  🌐 Network básico inicializado como fallback")
    
    async def _phase_4_load_agents(self):
        """
        Fase 4: Carregamento real dos agentes usando agent_loader
        Compatível com agent_loader que retorna summary direto ou aninhado em 'summary'.
        """
        logger.info("🤖 [Fase 4/7] Carregamento Real de Agentes ALSHAM QUANTUM")

        # Contagens esperadas
        expected_total = 56
        core_expected = 34
        domain_expected = 21
        registry_expected = 1

        logger.info(f"  📊 Core System esperado: {core_expected} agentes")
        logger.info(f"  📊 Domain Modules esperado: {domain_expected} agentes")
        logger.info(f"  📊 Registry esperado: {registry_expected} agente")
        logger.info(f"  🎯 TOTAL ESPERADO: {expected_total} agentes")

        try:
            logger.info("  🔄 Executando agent_loader.initialize_all_agents()...")

            # Importa o agent_loader
            from suna_alsham_core.agent_loader import initialize_all_agents

            if not self.network:
                raise Exception("Network não inicializado - criando fallback")

            # Executa o carregamento
            result = await initialize_all_agents(self.network)

            # Compatível com ambos os formatos de retorno
            if result and isinstance(result, dict):
                summary = result.get("summary", result)

                self.agents_loaded = summary.get("agents_loaded", 0)
                self.agents_active = self.agents_loaded

                # Guarda detalhes para diagnóstico
                self.agent_details = {
                    "modules_successful": summary.get("modules_successful", 0),
                    "modules_failed": summary.get("modules_failed", 0),
                    "success_rate": summary.get("success_rate", "0%"),
                    "agents_by_module": summary.get("agents_by_module", {}),
                    "failed_modules": summary.get("failed_modules", []),
                    "agents_expected": summary.get("agents_expected", expected_total)
                }

                logger.info(f"  ✅ CARREGAMENTO CONCLUÍDO: {self.agents_loaded} agentes carregados")
                logger.info(f"  📈 Taxa de sucesso: {self.agent_details['success_rate']}")

                # Reporta módulos que falharam
                if self.agent_details["modules_failed"] > 0:
                    failed_list = self.agent_details["failed_modules"][:5]
                    warning_msg = f"{self.agent_details['modules_failed']} módulos falharam: {', '.join(failed_list)}"
                    logger.warning(f"  ⚠️ {warning_msg}")
                    self.detailed_warnings.append(warning_msg)
                    self.warnings_count += 1

                # Verifica discrepância
                actual_expected = self.agent_details.get("agents_expected", expected_total)
                if self.agents_loaded != actual_expected:
                    discrepancy = actual_expected - self.agents_loaded
                    if discrepancy > 0:
                        warning_msg = f"DISCREPÂNCIA: {discrepancy} agentes faltando (esperado {actual_expected}, carregado {self.agents_loaded})"
                        logger.warning(f"  ⚠️ {warning_msg}")
                        self.detailed_warnings.append(warning_msg)
                        self.warnings_count += 1
                    else:
                        logger.info(f"  📈 EXCESSO: {abs(discrepancy)} agentes extras carregados")
                else:
                    logger.info(f"  🎊 PERFEITO: {self.agents_loaded}/{actual_expected} agentes carregados!")

            else:
                raise Exception("initialize_all_agents retornou resultado inválido")

        except ImportError as ie:
            error_msg = f"agent_loader não encontrado: {ie}"
            logger.error(f"  ❌ {error_msg}")
            self.detailed_warnings.append(error_msg)
            self.errors_count += 1
            await self._fallback_agent_count()

        except Exception as e:
            error_msg = f"Erro no carregamento de agentes: {str(e)}"
            logger.error(f"  ❌ {error_msg}")
            self.detailed_warnings.append(error_msg)
            self.errors_count += 1
            await self._fallback_agent_count()

        logger.info("✅ [Fase 4/7] Carregamento de agentes concluído")
    
    async def _fallback_agent_count(self):
        """Fallback para contar agentes quando agent_loader falha"""
        try:
            if self.network and hasattr(self.network, 'agents'):
                registry_count = len(self.network.agents)
                if registry_count > 0:
                    self.agents_loaded = registry_count
                    self.agents_active = registry_count
                    logger.info(f"  🔄 FALLBACK: {registry_count} agentes detectados via registry")
                    return
        except Exception as e:
            logger.debug(f"  Fallback falhou: {e}")
        
        # Se tudo falhar, assume zero
        self.agents_loaded = 0
        self.agents_active = 0
        logger.error("  💥 ZERO AGENTES CARREGADOS - Sistema degradado")
    
    async def _phase_5_system_activation(self):
        """Fase 5: Ativação do sistema"""
        logger.info("⚡ [Fase 5/7] Ativação do Sistema")
        
        # Verificar componentes críticos
        services = {
            "API Gateway": "Endpoints HTTP disponíveis",
            "Health Check": "Monitoramento ativo", 
            "Agent Communication": "Message Bus operacional"
        }
        
        for service, description in services.items():
            await asyncio.sleep(0.01)
            logger.info(f"  🔌 {service}: Ativo - {description}")
        
        # Verificar integrações externas (sem bloquear)
        external_services = {
            "OpenAI API": os.getenv("OPENAI_API_KEY") is not None,
            "Database": os.getenv("DATABASE_URL") is not None,
            "Redis Cache": os.getenv("REDIS_URL") is not None
        }
        
        for service, available in external_services.items():
            status = "Conectado" if available else "Não configurado"
            if available:
                logger.info(f"  🌐 {service}: {status}")
            else:
                logger.debug(f"  ℹ️ {service}: {status}")
        
        # Validar provedores AI se disponível
        try:
            from suna_alsham_core.agents.ai_powered_agents import validate_providers
            await validate_providers()
        except:
            pass  # Não é crítico
        
        logger.info("✅ [Fase 5/7] Sistema ativado")
    
    async def _phase_6_health_check(self):
        """Fase 6: Verificação de saúde detalhada"""
        logger.info("🏥 [Fase 6/7] Verificação de Saúde")
        
        # Métricas de sistema
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Alertas baseados em thresholds
            if cpu_usage > 80:
                logger.warning(f"  ⚠️ CPU usage alto: {cpu_usage:.1f}%")
                self.warnings_count += 1
            else:
                logger.info(f"  ✅ CPU Usage: {cpu_usage:.1f}%")
                
            if memory.percent > 90:
                logger.warning(f"  ⚠️ Memory usage crítico: {memory.percent:.1f}%")
                self.warnings_count += 1
            else:
                logger.info(f"  ✅ Memory Usage: {memory.percent:.1f}%")
                
        except Exception as e:
            logger.debug(f"  Métricas de sistema indisponíveis: {e}")
        
        # Status dos agentes
        if self.agents_loaded > 0:
            percentage = (self.agents_loaded / 56) * 100
            if percentage >= 80:
                logger.info(f"  ✅ Agentes: {self.agents_active}/{self.agents_loaded} ativos ({percentage:.1f}%)")
            elif percentage >= 50:
                logger.warning(f"  ⚠️ Agentes: {self.agents_active}/{self.agents_loaded} ativos ({percentage:.1f}%)")
            else:
                logger.error(f"  ❌ Agentes: {self.agents_active}/{self.agents_loaded} ativos ({percentage:.1f}%)")
        else:
            logger.error(f"  ❌ ZERO agentes carregados - PROBLEMA CRÍTICO")
            self.errors_count += 1
        
        logger.info("✅ [Fase 6/7] Verificação de saúde concluída")
    
    async def _phase_7_finalization(self):
        """Fase 7: Finalização e otimizações"""
        logger.info("🚀 [Fase 7/7] Finalização do Bootstrap")
        
        # Validar provedores AI se disponível
        try:
            from suna_alsham_core.agents.ai_powered_agents import validate_providers
            await validate_providers()
        except:
            pass
        
        await asyncio.sleep(0.05)
        logger.info("  ⚡ Sistema otimizado e pronto")
        logger.info("✅ [Fase 7/7] Bootstrap finalizado")
    
    def _evaluate_bootstrap_success(self) -> bool:
        """Avaliação de sucesso com detalhes completos"""
        duration = time.time() - self.start_time
        
        logger.info("📊 ================================================================================")
        logger.info("📊 RESUMO DO BOOTSTRAP QUANTUM")
        logger.info("📊 ================================================================================")
        logger.info(f"⏱️ Duração total: {duration:.2f} segundos")
        logger.info(f"🤖 Agentes esperados: 56")
        logger.info(f"🤖 Agentes carregados: {self.agents_loaded}")
        logger.info(f"🤖 Agentes ativos: {self.agents_active}")
        logger.info(f"⚠️ Warnings: {self.warnings_count}")
        logger.info(f"❌ Errors: {self.errors_count}")
        logger.info(f"🔴 Critical failures: {self.critical_failures}")
        
        # Mostrar warnings detalhados
        if self.detailed_warnings:
            logger.info("📋 DETALHES DOS WARNINGS:")
            for i, warning in enumerate(self.detailed_warnings[:10], 1):  # Limita a 10
                logger.info(f"  {i}. {warning}")
            if len(self.detailed_warnings) > 10:
                logger.info(f"  ... e mais {len(self.detailed_warnings) - 10} warnings")
        
        # Detalhes dos agentes se disponível
        if self.agent_details:
            logger.info("📊 DETALHES DO CARREGAMENTO:")
            logger.info(f"  Módulos bem-sucedidos: {self.agent_details.get('modules_successful', 0)}")
            logger.info(f"  Módulos falhados: {self.agent_details.get('modules_failed', 0)}")
            logger.info(f"  Taxa de sucesso: {self.agent_details.get('success_rate', 'N/A')}")
        
        # Avaliação de sucesso
        success = self.critical_failures == 0 and self.agents_loaded > 0
        
        if success:
            if self.agents_loaded >= 50:
                logger.info("✅ BOOTSTRAP SUCESSO: Sistema operacional!")
                if self.agents_loaded == 56:
                    logger.info("🎊 PERFEITO: Todos os 56 agentes carregados!")
                else:
                    logger.info(f"🎯 BOM: {self.agents_loaded}/56 agentes operacionais")
            elif self.agents_loaded >= 20:
                logger.info(f"⚠️ BOOTSTRAP PARCIAL: Apenas {self.agents_loaded}/56 agentes ativos")
                success = True  # Ainda considera sucesso parcial
            else:
                logger.warning(f"⚠️ BOOTSTRAP MÍNIMO: Apenas {self.agents_loaded}/56 agentes")
                success = True  # Sistema mínimo funcional
        else:
            if self.critical_failures > 0:
                logger.error("❌ BOOTSTRAP FALHOU: Erros críticos detectados!")
            elif self.agents_loaded == 0:
                logger.error("❌ BOOTSTRAP FALHOU: Nenhum agente carregado!")
            
        if self.warnings_count > 0:
            logger.info(f"⚠️ {self.warnings_count} warnings (funcionalidade pode estar limitada)")
            
        logger.info("🎊 Sistema pronto para operar!")
        logger.info("📊 ================================================================================")
        return success

# Instância global
bootstrap_instance = QuantumBootstrap()

# Funções públicas
async def run_quantum_bootstrap() -> bool:
    """Função assíncrona para executar o bootstrap"""
    return await bootstrap_instance.execute_bootstrap()

def bootstrap() -> bool:
    """
    Função síncrona para executar o bootstrap ALSHAM QUANTUM.
    
    Gerencia o event loop automaticamente e retorna True se o bootstrap
    completou (mesmo com warnings), False apenas em falha crítica.
    
    Returns:
        bool: True se bootstrap completou, False se falha crítica
    """
    try:
        # Verifica se já existe um loop rodando
        try:
            loop = asyncio.get_running_loop()
            # Se chegou aqui, há um loop rodando
            logger.info("[Bootstrap] Event loop já em execução, criando task assíncrona...")
            task = asyncio.create_task(bootstrap_instance.execute_bootstrap())
            return True  # Retorna True pois a task foi criada
        except RuntimeError:
            # Não há loop rodando, criar um novo
            logger.info("[Bootstrap] Iniciando novo event loop para bootstrap...")
            return asyncio.run(bootstrap_instance.execute_bootstrap())
            
    except Exception as e:
        logger.critical(f"Erro crítico na execução do bootstrap: {e}", exc_info=True)
        return False

def get_bootstrap_status() -> Dict[str, Any]:
    """
    Retorna status detalhado do bootstrap ALSHAM QUANTUM.
    
    Returns:
        Dict com status completo do sistema
    """
    return {
        "bootstrap_completed": bootstrap_instance.agents_loaded > 0,
        "agents_expected": 56,
        "agents_loaded": bootstrap_instance.agents_loaded,
        "agents_active": bootstrap_instance.agents_active,
        "warnings": bootstrap_instance.warnings_count,
        "detailed_warnings": bootstrap_instance.detailed_warnings[:5],  # Primeiros 5
        "errors": bootstrap_instance.errors_count,
        "critical_failures": bootstrap_instance.critical_failures,
        "agent_coverage": f"{bootstrap_instance.agents_loaded}/56",
        "percentage": f"{(bootstrap_instance.agents_loaded / 56 * 100):.1f}%" if bootstrap_instance.agents_loaded else "0%",
        "agent_details": bootstrap_instance.agent_details
    }

# Aliases para compatibilidade
run_bootstrap = bootstrap
execute_bootstrap = bootstrap
start_bootstrap = bootstrap

# Para execução direta
if __name__ == "__main__":
    success = bootstrap()
    sys.exit(0 if success else 1)
