import logging
from typing import Dict
from multi_agent_network import BaseNetworkAgent, AgentType
from uuid import uuid4
import time

logger = logging.getLogger(__name__)

class PerformanceMonitorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['performance_monitoring', 'optimization_validation']
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

def create_performance_monitor_agent(message_bus) -> 'PerformanceMonitorAgent':
    try:
        agent_id = f"performance_monitor_{uuid4()}"
        agent = PerformanceMonitorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        message_bus.register_agent(agent_id, agent)
        logger.info(f"✅ {agent_id} criado")
        return agent
    except Exception as e:
        logger.error(f"❌ Erro criando PerformanceMonitorAgent: {e}")
        return None
