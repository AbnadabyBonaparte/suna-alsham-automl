import logging
from typing import Dict, List
from multi_agent_network import BaseNetworkAgent, AgentType
import time

logger = logging.getLogger(__name__)

class PerformanceMonitorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['performance_monitoring', 'optimization_validation']
        self.status = 'active'  # ✅ ADICIONADO
        logger.info(f"✅ {self.agent_id} inicializado")

    def monitor_performance(self, file_path: str) -> Dict:
        try:
            start_time = time.time()
            # Simulação de medição (substituir por lógica real)
            time.sleep(1)  # Simula execução
            end_time = time.time()
            latency = end_time - start_time
            logger.info(f"📊 Performance de {file_path}: Latência {latency:.2f}s")
            return {"file": file_path, "latency": latency, "status": "optimized" if latency < 1 else "needs_improvement"}
        except Exception as e:
            logger.error(f"❌ Erro monitorando performance de {file_path}: {e}")
            return {"file": file_path, "status": "error", "error": str(e)}

def create_performance_monitor_agent(message_bus, num_instances=1) -> List['PerformanceMonitorAgent']:  # ✅ CORRIGIDO
    """Cria agente de monitoramento de performance"""
    agents = []
    try:
        logger.info("📊 Criando PerformanceMonitorAgent...")
        
        agent_id = "performance_monitor_001"  # ✅ ID fixo
        agent = PerformanceMonitorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Registrar no MessageBus
        if hasattr(message_bus, 'register_agent'):
            message_bus.register_agent(agent_id, agent)
        
        agents.append(agent)  # ✅ ADICIONADO À LISTA
        logger.info(f"✅ {len(agents)} agente de monitoramento criado")
        return agents  # ✅ RETORNA LISTA
        
    except Exception as e:
        logger.error(f"❌ Erro criando PerformanceMonitorAgent: {e}")
        return []  # ✅ RETORNA LISTA VAZIA
