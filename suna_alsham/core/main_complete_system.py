"""
🚀 SUNA-ALSHAM Complete Multi-Agent System
Sistema completo com todos os agentes especializados e melhorias dos colaboradores

MELHORIAS IMPLEMENTADAS:
✅ Todos os agentes especializados ativos
✅ Logs detalhados e estruturados
✅ Tratamento robusto de erros
✅ Métricas em tempo real
✅ Sistema de monitoramento avançado
✅ Performance otimizada
"""

import asyncio
import json
import time
import logging
import signal
import sys
import os
from datetime import datetime
from typing import Dict, Any, List
import threading
from concurrent.futures import ThreadPoolExecutor

# Configurar logging avançado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('suna_alsham.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)

# Importar componentes do sistema
try:
    from multi_agent_network import MultiAgentNetwork, AnalyticsAgent
    from specialized_agents import (
        OptimizationAgent, SecurityAgent, LearningAgent, 
        DataAgent, MonitoringAgent
    )
    from ai_powered_agents import SelfEvolvingAgent, AIOptimizationAgent
    logger.info("✅ Todos os módulos importados com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro na importação: {e}")
    sys.exit(1)


class SystemMetricsCollector:
    """Coletor de métricas do sistema em tempo real"""
    
    def __init__(self):
        self.metrics = {
            "system_start_time": datetime.now(),
            "total_agents": 0,
            "active_agents": 0,
            "messages_processed": 0,
            "errors_count": 0,
            "performance_score": 0.0,
            "uptime_seconds": 0
        }
        self.running = False
        self.collector_thread = None
    
    def start_collection(self, network):
        """Inicia coleta de métricas"""
        self.network = network
        self.running = True
        self.collector_thread = threading.Thread(target=self._collect_loop)
        self.collector_thread.daemon = True
        self.collector_thread.start()
        logger.info("📊 Coletor de métricas iniciado")
    
    def stop_collection(self):
        """Para coleta de métricas"""
        self.running = False
        if self.collector_thread:
            self.collector_thread.join()
        logger.info("📊 Coletor de métricas parado")
    
    def _collect_loop(self):
        """Loop de coleta de métricas"""
        while self.running:
            try:
                # Atualizar métricas básicas
                self.metrics["uptime_seconds"] = (datetime.now() - self.metrics["system_start_time"]).total_seconds()
                
                # Obter status da rede
                network_status = self.network.get_network_status()
                self.metrics["total_agents"] = network_status.get("network_metrics", {}).get("total_agents", 0)
                self.metrics["active_agents"] = network_status.get("network_metrics", {}).get("active_agents", 0)
                
                # Calcular score de performance
                if self.metrics["total_agents"] > 0:
                    self.metrics["performance_score"] = (
                        self.metrics["active_agents"] / self.metrics["total_agents"]
                    ) * 100
                
                # Log métricas a cada 30 segundos
                if int(self.metrics["uptime_seconds"]) % 30 == 0:
                    logger.info(f"📈 Métricas: {self.metrics['active_agents']}/{self.metrics['total_agents']} agentes ativos, "
                              f"Performance: {self.metrics['performance_score']:.1f}%, "
                              f"Uptime: {self.metrics['uptime_seconds']:.0f}s")
                
            except Exception as e:
                logger.error(f"❌ Erro coletando métricas: {e}")
                self.metrics["errors_count"] += 1
            
            time.sleep(1)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas atuais"""
        return self.metrics.copy()


class EnhancedSystemManager:
    """Gerenciador do sistema com melhorias dos colaboradores"""
    
    def __init__(self):
        self.network = None
        self.agents = {}
        self.metrics_collector = SystemMetricsCollector()
        self.shutdown_requested = False
        
        # Configurar handlers de sinal
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de shutdown"""
        logger.info(f"🛑 Sinal {signum} recebido, iniciando shutdown graceful...")
        self.shutdown_requested = True
    
    def initialize_system(self):
        """Inicializa o sistema completo"""
        logger.info("🌐 Inicializando sistema SUNA-ALSHAM completo...")
        
        try:
            # Criar rede principal
            self.network = MultiAgentNetwork()
            logger.info("✅ Rede multi-agente criada")
            
            # Criar todos os agentes especializados
            self._create_all_agents()
            
            # Iniciar rede
            self.network.start()
            logger.info("🚀 Rede multi-agente iniciada")
            
            # Iniciar coleta de métricas
            self.metrics_collector.start_collection(self.network)
            
            # Log de inicialização completa
            logger.info(f"🎉 Sistema SUNA-ALSHAM inicializado com {len(self.agents)} agentes especializados!")
            self._log_system_status()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na inicialização do sistema: {e}")
            return False
    
    def _create_all_agents(self):
        """Cria todos os agentes especializados"""
        logger.info("🤖 Criando agentes especializados...")
        
        # Lista de agentes para criar
        agents_config = [
            ("analytics_001", AnalyticsAgent),
            ("optimizer_001", OptimizationAgent),
            ("security_001", SecurityAgent),
            ("learner_001", LearningAgent),
            ("data_001", DataAgent),
            ("monitor_001", MonitoringAgent),
            ("evolving_001", SelfEvolvingAgent),
            ("ai_optimizer_001", AIOptimizationAgent),
        ]
        
        # Criar cada agente
        for agent_id, agent_class in agents_config:
            try:
                if agent_class in [SelfEvolvingAgent, AIOptimizationAgent]:
                    # Agentes com IA precisam de parâmetros especiais
                    agent = agent_class(agent_id, self.network.message_bus, redis_url=None)
                else:
                    agent = agent_class(agent_id, self.network.message_bus)
                
                self.network.add_agent(agent)
                self.agents[agent_id] = agent
                
                logger.info(f"✅ Agente {agent_id} ({agent_class.__name__}) criado e adicionado")
                
            except Exception as e:
                logger.error(f"❌ Erro criando agente {agent_id}: {e}")
                continue
        
        logger.info(f"🎯 Total de {len(self.agents)} agentes especializados criados")
    
    def _log_system_status(self):
        """Log detalhado do status do sistema"""
        status = self.network.get_network_status()
        
        logger.info("=" * 60)
        logger.info("📊 STATUS DO SISTEMA SUNA-ALSHAM")
        logger.info("=" * 60)
        logger.info(f"🤖 Agentes Registrados: {status.get('network_metrics', {}).get('total_agents', 0)}")
        logger.info(f"✅ Agentes Ativos: {status.get('network_metrics', {}).get('active_agents', 0)}")
        logger.info(f"📨 Message Bus Stats: {status.get('message_bus_stats', {})}")
        
        logger.info("\n🤖 AGENTES ESPECIALIZADOS:")
        for agent_id, agent in self.agents.items():
            capabilities = [cap.name for cap in agent.capabilities]
            logger.info(f"  • {agent_id}: {agent.agent_type.value} - {len(capabilities)} capacidades")
        
        logger.info("=" * 60)
    
    def run_system_demo(self, duration_seconds: int = 60):
        """Executa demonstração do sistema"""
        logger.info(f"🚀 Iniciando demonstração do sistema por {duration_seconds} segundos...")
        
        start_time = time.time()
        demo_tasks = []
        
        try:
            while time.time() - start_time < duration_seconds and not self.shutdown_requested:
                # Simular tarefas do sistema
                if time.time() - start_time > 5:  # Após 5 segundos
                    self._simulate_system_tasks()
                
                # Log status a cada 15 segundos
                elapsed = time.time() - start_time
                if int(elapsed) % 15 == 0 and int(elapsed) > 0:
                    self._log_demo_progress(elapsed, duration_seconds)
                
                time.sleep(1)
            
            logger.info("✅ Demonstração concluída com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro durante demonstração: {e}")
    
    def _simulate_system_tasks(self):
        """Simula tarefas do sistema"""
        try:
            # Atribuir tarefa de otimização
            if "optimizer_001" in self.agents:
                task_id = self.network.assign_task("performance_optimization", {
                    "metrics": {"cpu_usage": 75, "memory_usage": 60, "response_time": 800},
                    "target_improvement": 0.15
                })
                if task_id:
                    logger.info(f"📋 Tarefa de otimização {task_id} atribuída")
            
            # Atribuir tarefa de segurança
            if "security_001" in self.agents:
                task_id = self.network.assign_task("security_scan", {
                    "scan_type": "full",
                    "data": {"failed_logins": 8, "network_requests": 850}
                })
                if task_id:
                    logger.info(f"🛡️ Tarefa de segurança {task_id} atribuída")
            
            # Atribuir tarefa de análise de dados
            if "data_001" in self.agents:
                task_id = self.network.assign_task("data_processing", {
                    "data": list(range(100)),
                    "processing_type": "numerical"
                })
                if task_id:
                    logger.info(f"📊 Tarefa de processamento {task_id} atribuída")
            
        except Exception as e:
            logger.error(f"❌ Erro simulando tarefas: {e}")
    
    def _log_demo_progress(self, elapsed: float, total: int):
        """Log do progresso da demonstração"""
        progress = (elapsed / total) * 100
        metrics = self.metrics_collector.get_metrics()
        
        logger.info(f"⏱️ Progresso: {progress:.1f}% ({elapsed:.0f}/{total}s)")
        logger.info(f"📈 Performance Score: {metrics['performance_score']:.1f}%")
        logger.info(f"🤖 Agentes Ativos: {metrics['active_agents']}/{metrics['total_agents']}")
    
    def shutdown_system(self):
        """Shutdown graceful do sistema"""
        logger.info("🛑 Iniciando shutdown do sistema...")
        
        try:
            # Parar coleta de métricas
            self.metrics_collector.stop_collection()
            
            # Parar rede
            if self.network:
                self.network.stop()
            
            logger.info("✅ Sistema SUNA-ALSHAM encerrado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro durante shutdown: {e}")


def main():
    """Função principal do sistema"""
    logger.info("🌟 INICIANDO SUNA-ALSHAM MULTI-AGENT SYSTEM v2.0")
    logger.info("🔧 Versão com melhorias dos colaboradores")
    
    # Criar gerenciador do sistema
    system_manager = EnhancedSystemManager()
    
    try:
        # Inicializar sistema
        if not system_manager.initialize_system():
            logger.error("❌ Falha na inicialização do sistema")
            sys.exit(1)
        
        # Executar demonstração
        demo_duration = int(os.getenv("DEMO_DURATION", "120"))  # 2 minutos padrão
        system_manager.run_system_demo(demo_duration)
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupção pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro crítico no sistema: {e}")
    finally:
        # Shutdown graceful
        system_manager.shutdown_system()


if __name__ == "__main__":
    main()

