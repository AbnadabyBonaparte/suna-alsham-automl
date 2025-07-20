"""
SUNA-ALSHAM Integration
Sistema de integração e orquestração de agentes
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .core_agent import CoreAgent
from .config import SUNAAlshamConfig

logger = logging.getLogger(__name__)


class SUNAAlshamIntegration:
    """
    Sistema de integração SUNA-ALSHAM
    Orquestra todos os agentes e componentes do sistema
    """
    
    def __init__(self, config: Optional[SUNAAlshamConfig] = None):
        self.config = config if config else SUNAAlshamConfig()
        self.system_id = "suna-alsham-integration"
        self.version = "2.1.0"
        self.created_at = datetime.utcnow()
        
        # Inicializar agentes
        self.core_agent = None
        self._initialize_agents()
        
        logger.info(f"🔗 SUNA-ALSHAM Integration inicializado - Versão: {self.version}")
    
    def _initialize_agents(self):
        """Inicializa todos os agentes do sistema."""
        try:
            # Core Agent AutoML
            if self.config.core_agent.enabled:
                self.core_agent = CoreAgent(self.config.core_agent)
                logger.info("✅ Core Agent AutoML inicializado")
            else:
                logger.info("⚠️ Core Agent desabilitado na configuração")
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar agentes: {e}")
    
    def run_evolution_cycle(self) -> Dict[str, Any]:
        """Executa ciclo de evolução completo do sistema."""
        cycle_start = datetime.utcnow()
        results = {
            "cycle_id": f"integration_{int(cycle_start.timestamp())}",
            "start_time": cycle_start.isoformat(),
            "agents_results": {},
            "overall_success": False
        }
        
        try:
            logger.info("🔄 Iniciando ciclo de evolução integrado...")
            
            # Executar Core Agent
            if self.core_agent:
                logger.info("🤖 Executando Core Agent AutoML...")
                core_result = self.core_agent.run_evolution_cycle()
                results["agents_results"]["core_agent"] = core_result
                
                if core_result.get("success"):
                    logger.info("✅ Core Agent executado com sucesso")
                else:
                    logger.warning("⚠️ Core Agent teve problemas")
            
            # Determinar sucesso geral
            results["overall_success"] = any(
                result.get("success", False) 
                for result in results["agents_results"].values()
            )
            
            results["end_time"] = datetime.utcnow().isoformat()
            results["duration_seconds"] = (datetime.utcnow() - cycle_start).total_seconds()
            
            if results["overall_success"]:
                logger.info("✅ Ciclo de evolução integrado concluído com sucesso")
            else:
                logger.warning("⚠️ Ciclo de evolução integrado teve problemas")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro durante ciclo de evolução integrado: {e}")
            results["error"] = str(e)
            results["end_time"] = datetime.utcnow().isoformat()
            return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema."""
        return {
            "system_id": self.system_id,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "config": {
                "auto_start": self.config.auto_start,
                "evolution_interval": self.config.evolution_interval,
                "environment": self.config.core_agent.environment
            },
            "agents": {
                "core_agent": self.core_agent.get_status() if self.core_agent else None
            }
        }

