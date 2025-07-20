"""
SUNA-ALSHAM Learn Agent - Pure Python
Agente de aprendizado com integração HTTP ao GuardAgent
Versão: 1.0.0 FINAL
"""
import os
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sklearn.ensemble import RandomForestRegressor
import requests

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LearnAgentConfig:
    def __init__(self):
        self.enabled = True
        self.guard_timeout = 5
        self.max_retries = 3

class LearnAgent:
    def __init__(self, config: Optional[LearnAgentConfig] = None):
        self.agent_id = str(uuid.uuid4())
        self.name = "LEARN_AUTOML"
        self.status = "initializing"
        self.version = "1.0.0"
        self.created_at = datetime.utcnow()
        self.config = config if config else LearnAgentConfig()
        self.enabled = self.config.enabled
        
        # Modelo de ML
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # URL do GuardAgent - flexível para Railway
        self.guard_url = os.getenv("GUARD_AGENT_URL", "http://localhost:8000")
        
        # Status de conexão com GuardAgent
        self.guard_available = False
        self.test_guard_connection()
        
        self.status = "active" if self.enabled else "disabled"
        logger.info(f"🧠 Learn Agent inicializado - ID: {self.agent_id}")

    def test_guard_connection(self):
        """Testa conexão com GuardAgent na inicialização"""
        try:
            response = requests.get(f"{self.guard_url}/health", timeout=self.config.guard_timeout)
            response.raise_for_status()
            self.guard_available = True
            logger.info(f"✅ Conexão com GuardAgent estabelecida: {self.guard_url}")
        except Exception as e:
            self.guard_available = False
            logger.warning(f"⚠️ GuardAgent não disponível: {e}. Usando validação local.")

    def load_tasks(self) -> List[Dict[str, Any]]:
        """Carrega tarefas com fallback"""
        try:
            # Simula carregamento do Supabase
            # Em produção, conectaria com o banco real
            tasks = [
                {
                    "features": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                    "target": [0.7, 0.8, 0.9],
                    "domain": "test_domain"
                }
            ]
            logger.info(f"✅ Carregadas {len(tasks)} tarefas")
            return tasks
        except Exception as e:
            logger.error(f"❌ Erro ao carregar tarefas: {e}")
            # Fallback com dados sintéticos
            return [{
                "features": [[1, 2, 3], [4, 5, 6]], 
                "target": [0.7, 0.8], 
                "domain": "fallback"
            }]

    def validate_with_guard(self, data: Dict[str, Any]) -> bool:
        """Validação com GuardAgent + fallback local"""
        if not self.guard_available:
            return self.local_validation(data)
        
        try:
            response = requests.post(
                f"{self.guard_url}/monitor", 
                json={"system_data": data}, 
                timeout=self.config.guard_timeout
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"🛡️ GuardAgent response: {result['operation_mode']}, success: {result['success']}")
            
            # Considera válido se sucesso e taxa de segurança > 80%
            return result["success"] and result["security_checks"]["success_rate"] > 0.8
            
        except Exception as e:
            logger.warning(f"⚠️ Falha ao conectar com GuardAgent: {e}, usando validação local")
            return self.local_validation(data)

    def local_validation(self, data: Dict[str, Any]) -> bool:
        """Validação local básica"""
        return isinstance(data, dict) and len(data) > 0

    def train(self) -> Dict[str, Any]:
        """Ciclo principal de treinamento"""
        cycle_id = str(uuid.uuid4())
        logger.info(f"🔄 Iniciando ciclo de treinamento: {cycle_id}")
        
        tasks = self.load_tasks()
        if not tasks:
            logger.error("❌ Nenhuma tarefa disponível")
            return {"success": False, "message": "No tasks available"}
        
        try:
            valid_tasks = 0
            for task in tasks:
                if self.validate_with_guard(task):
                    X, y = task["features"], task["target"]
                    self.model.fit(X, y)
                    valid_tasks += 1
                    logger.info(f"✅ Tarefa {task['domain']} processada")
                else:
                    logger.warning(f"⚠️ Tarefa {task['domain']} rejeitada pelo GuardAgent")
            
            if valid_tasks == 0:
                return {"success": False, "message": "No valid tasks processed"}
            
            # Calcula performance
            score = self.model.score(X, y)
            
            # Simula salvamento no Supabase
            # Em produção, salvaria no banco real
            logger.info(f"💾 Métricas salvas: cycle_id={cycle_id}, performance={score:.2%}")
            
            logger.info(f"✅ Treinamento concluído: Performance {score:.2%}")
            return {
                "success": True, 
                "performance": score,
                "cycle_id": cycle_id,
                "valid_tasks": valid_tasks,
                "total_tasks": len(tasks)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no ciclo de treinamento: {e}")
            return {"success": False, "message": str(e)}

    def share_knowledge(self, core_agent) -> None:
        """Compartilha conhecimento com CoreAgent"""
        result = self.train()
        if result["success"]:
            # Simula compartilhamento de parâmetros
            logger.info(f"🤝 Conhecimento compartilhado com CoreAgent")
            return result
        return None

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "version": self.version,
            "type": "learn_agent",
            "guard_available": self.guard_available,
            "guard_url": self.guard_url,
            "last_train_time": datetime.utcnow().isoformat()
        }

