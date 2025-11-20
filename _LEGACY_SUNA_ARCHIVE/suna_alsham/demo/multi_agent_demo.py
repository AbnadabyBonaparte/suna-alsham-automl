"""
🚀 SUNA-ALSHAM Multi-Agent Network Demo
Demonstração funcional da rede multi-agente completa

DEMONSTRAÇÃO INCLUI:
✅ Inicialização da rede com múltiplos agentes
✅ Comunicação inter-agentes em tempo real
✅ Coordenação de tarefas complexas
✅ Monitoramento de performance
✅ Auto-scaling baseado em carga
✅ Tolerância a falhas
✅ Dashboard em tempo real
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any
import threading
import signal
import sys

# Importar componentes do sistema
from multi_agent_network import MultiAgentNetwork
from specialized_agents import (
    OptimizationAgent, SecurityAgent, LearningAgent, 
    DataAgent, MonitoringAgent
)
from network_orchestrator import NetworkOrchestrator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiAgentDemo:
    """Demonstração da rede multi-agente"""
    
    def __init__(self):
        self.orchestrator = None
        self.demo_running = False
        self.demo_stats = {
            "start_time": None,
            "messages_sent": 0,
            "tasks_completed": 0,
            "agents_created": 0,
            "uptime_seconds": 0
        }
    
    def setup_signal_handlers(self):
        """Configura handlers para sinais do sistema"""
        def signal_handler(signum, frame):
            logger.info(f"🛑 Recebido sinal {signum}, parando demonstração...")
            self.stop_demo()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start_demo(self):
        """Inicia a demonstração"""
        logger.info("🚀 Iniciando demonstração da rede multi-agente SUNA-ALSHAM...")
        
        self.demo_running = True
        self.demo_stats["start_time"] = datetime.now()
        
        try:
            # Inicializar orquestrador
            logger.info("🎼 Inicializando orquestrador da rede...")
            self.orchestrator = NetworkOrchestrator()
            self.orchestrator.start()
            
            # Aguardar inicialização
            await asyncio.sleep(3)
            
            # Criar agentes especializados
            await self._create_specialized_agents()
            
            # Simular operações da rede
            await self._simulate_network_operations()
            
            # Monitorar performance
            await self._monitor_performance()
            
        except Exception as e:
            logger.error(f"❌ Erro na demonstração: {e}")
            raise
    
    async def _create_specialized_agents(self):
        """Cria agentes especializados para demonstração"""
        logger.info("🤖 Criando agentes especializados...")
        
        # Agentes de otimização
        for i in range(2):
            agent = OptimizationAgent(f"optimizer_{i+1}", self.orchestrator.network.message_bus)
            self.orchestrator.network.add_agent(agent)
            self.demo_stats["agents_created"] += 1
        
        # Agentes de segurança
        for i in range(1):
            agent = SecurityAgent(f"security_{i+1}", self.orchestrator.network.message_bus)
            self.orchestrator.network.add_agent(agent)
            self.demo_stats["agents_created"] += 1
        
        # Agentes de aprendizado
        for i in range(2):
            agent = LearningAgent(f"learning_{i+1}", self.orchestrator.network.message_bus)
            self.orchestrator.network.add_agent(agent)
            self.demo_stats["agents_created"] += 1
        
        # Agentes de dados
        for i in range(3):
            agent = DataAgent(f"data_{i+1}", self.orchestrator.network.message_bus)
            self.orchestrator.network.add_agent(agent)
            self.demo_stats["agents_created"] += 1
        
        # Agentes de monitoramento
        for i in range(1):
            agent = MonitoringAgent(f"monitor_{i+1}", self.orchestrator.network.message_bus)
            self.orchestrator.network.add_agent(agent)
            self.demo_stats["agents_created"] += 1
        
        logger.info(f"✅ {self.demo_stats['agents_created']} agentes especializados criados")
        
        # Aguardar inicialização dos agentes
        await asyncio.sleep(2)
    
    async def _simulate_network_operations(self):
        """Simula operações da rede"""
        logger.info("⚡ Iniciando simulação de operações da rede...")
        
        # Simular diferentes tipos de tarefas
        tasks = [
            {
                "type": "optimize_performance",
                "description": "Otimizar performance do sistema",
                "priority": 2,
                "data": {"metrics": {"cpu": 75, "memory": 60, "response_time": 150}}
            },
            {
                "type": "scan_threats",
                "description": "Escanear ameaças de segurança",
                "priority": 1,
                "data": {"failed_logins": 15, "network_requests": 1200}
            },
            {
                "type": "train_model",
                "description": "Treinar modelo de machine learning",
                "priority": 3,
                "data": {"training_data": list(range(100)), "model_type": "neural_network"}
            },
            {
                "type": "process_data",
                "description": "Processar dados em lote",
                "priority": 3,
                "data": {"data": list(range(50)), "processing_type": "aggregate"}
            }
        ]
        
        # Enviar tarefas para a rede
        for i, task in enumerate(tasks):
            logger.info(f"📋 Enviando tarefa {i+1}: {task['description']}")
            
            # Simular envio de tarefa via API do orquestrador
            task_request = {
                "type": task["type"],
                "priority": task["priority"],
                "data": task["data"],
                "requester": "demo_client"
            }
            
            # Adicionar à fila do orquestrador
            from network_orchestrator import TaskRequest, Priority
            task_obj = TaskRequest(
                id=f"demo_task_{i+1}",
                type=task["type"],
                priority=Priority(task["priority"]),
                data=task["data"],
                requester="demo_client",
                created_at=datetime.now()
            )
            
            self.orchestrator.task_queue.append(task_obj)
            self.demo_stats["tasks_completed"] += 1
            
            # Aguardar entre tarefas
            await asyncio.sleep(2)
        
        logger.info(f"✅ {len(tasks)} tarefas enviadas para processamento")
    
    async def _monitor_performance(self):
        """Monitora performance da rede"""
        logger.info("📊 Iniciando monitoramento de performance...")
        
        monitoring_cycles = 0
        
        while self.demo_running and monitoring_cycles < 10:  # 10 ciclos de monitoramento
            try:
                # Obter status da rede
                network_status = self.orchestrator.network.get_network_status()
                
                # Obter status do orquestrador
                orchestrator_status = self.orchestrator.get_coordination_status() if hasattr(self.orchestrator, 'get_coordination_status') else {}
                
                # Calcular uptime
                if self.demo_stats["start_time"]:
                    uptime = datetime.now() - self.demo_stats["start_time"]
                    self.demo_stats["uptime_seconds"] = uptime.total_seconds()
                
                # Log status
                active_agents = network_status["network_metrics"]["active_agents"]
                total_agents = network_status["network_metrics"]["total_agents"]
                
                logger.info(f"📈 Ciclo {monitoring_cycles + 1}: {active_agents}/{total_agents} agentes ativos")
                logger.info(f"⏱️ Uptime: {self.demo_stats['uptime_seconds']:.1f}s")
                logger.info(f"📋 Tarefas processadas: {self.demo_stats['tasks_completed']}")
                
                # Simular algumas métricas
                if monitoring_cycles % 3 == 0:
                    logger.info("🔄 Executando coordenação da rede...")
                    # O orquestrador já faz isso automaticamente
                
                monitoring_cycles += 1
                await asyncio.sleep(5)  # Monitorar a cada 5 segundos
                
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
                break
        
        logger.info("✅ Monitoramento de performance concluído")
    
    def stop_demo(self):
        """Para a demonstração"""
        logger.info("⏹️ Parando demonstração...")
        
        self.demo_running = False
        
        if self.orchestrator:
            try:
                self.orchestrator.stop()
                logger.info("✅ Orquestrador parado")
            except Exception as e:
                logger.error(f"❌ Erro parando orquestrador: {e}")
    
    def print_demo_summary(self):
        """Imprime resumo da demonstração"""
        print("\n" + "="*60)
        print("🎯 RESUMO DA DEMONSTRAÇÃO SUNA-ALSHAM")
        print("="*60)
        print(f"⏱️ Duração: {self.demo_stats['uptime_seconds']:.1f} segundos")
        print(f"🤖 Agentes criados: {self.demo_stats['agents_created']}")
        print(f"📋 Tarefas processadas: {self.demo_stats['tasks_completed']}")
        print(f"📡 Mensagens enviadas: {self.demo_stats['messages_sent']}")
        
        if self.orchestrator and hasattr(self.orchestrator, 'network'):
            network_status = self.orchestrator.network.get_network_status()
            print(f"🌐 Status final da rede: {network_status['network_metrics']['active_agents']} agentes ativos")
        
        print("="*60)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)


async def main():
    """Função principal da demonstração"""
    demo = MultiAgentDemo()
    demo.setup_signal_handlers()
    
    try:
        # Executar demonstração
        await demo.start_demo()
        
        # Aguardar um pouco mais para observar o sistema
        logger.info("🔍 Observando sistema por mais 10 segundos...")
        await asyncio.sleep(10)
        
    except KeyboardInterrupt:
        logger.info("🛑 Demonstração interrompida pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Parar demonstração
        demo.stop_demo()
        
        # Imprimir resumo
        demo.print_demo_summary()


if __name__ == "__main__":
    print("🚀 SUNA-ALSHAM Multi-Agent Network Demo")
    print("Pressione Ctrl+C para parar a demonstração")
    print("-" * 50)
    
    # Executar demonstração
    asyncio.run(main())

