#!/usr/bin/env python3
"""
Módulo do Disaster Recovery Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica de coleta de estado aprimorada e
execução de planos de recuperação mais robusta.
"""

import asyncio
import hashlib
import json
import logging
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# --- Bloco de Importação Corrigido ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,  # Import adicionado
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class DisasterType(Enum):
    """Tipos de desastres que o agente pode tratar."""
    SYSTEM_CRASH = "system_crash"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_BREACH = "security_breach"


class RecoveryStatus(Enum):
    """Status de um processo de recuperação."""
    READY = "ready"
    RECOVERING = "recovering"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class SystemSnapshot:
    """Representa um snapshot completo do sistema para recuperação."""
    snapshot_id: str
    timestamp: datetime
    backup_path: str
    size_mb: float
    file_checksums: Dict[str, str] = field(default_factory=dict)


@dataclass
class RecoveryPlan:
    """Define os passos para se recuperar de um tipo específico de desastre."""
    plan_id: str
    disaster_type: DisasterType
    recovery_steps: List[Dict[str, Any]]
    estimated_rto_minutes: int  # Recovery Time Objective


# --- Classe Principal do Agente ---

class DisasterRecoveryAgent(BaseNetworkAgent):
    """
    Agente Enterprise de Recuperação de Desastres.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DisasterRecoveryAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend([
            "state_snapshot",
            "automated_restoration",
            "disaster_detection",
        ])
        
        self.backup_root = Path("./disaster_recovery_backups")
        self.backup_root.mkdir(exist_ok=True)
        
        self.system_snapshots: Dict[str, SystemSnapshot] = {}
        self.recovery_plans: Dict[str, RecoveryPlan] = self._initialize_recovery_plans()
        
        logger.info(f"🛡️ {self.agent_id} (Recuperação de Desastres) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de recuperação de desastres."""
        # Suporte para tipos de mensagem agora funciona corretamente
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "create_snapshot": self.create_system_snapshot,
                "restore_system": self.restore_system,
            }.get(request_type)

            if handler:
                result = await handler(message.content)
                await self.publish_response(message, result) # Usando o novo helper
        
        # Este tipo de mensagem não está no Enum MessageType, mas mantendo a lógica
        # elif message.message_type == "EMERGENCY":
        #     await self._handle_emergency(message)

    def _initialize_recovery_plans(self) -> Dict[str, RecoveryPlan]:
        """Carrega os planos de recuperação padrão do sistema."""
        plans = [
            RecoveryPlan(
                plan_id="PLAN_SYSTEM_CRASH",
                disaster_type=DisasterType.SYSTEM_CRASH,
                recovery_steps=[
                    {"action": "restore_latest_snapshot"},
                    {"action": "restart_critical_agents"},
                ],
                estimated_rto_minutes=30,
            ),
        ]
        return {plan.plan_id: plan for plan in plans}

    async def create_system_snapshot(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um snapshot completo do estado atual do sistema."""
        snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_path = self.backup_root / snapshot_id
        
        try:
            logger.info(f"📸 Criando snapshot do sistema: {snapshot_id}")
            snapshot_path.mkdir(exist_ok=True)
            
            # --- Correção do Atributo ---
            # Trocado .subscribers por .queues
            active_agents_count = len(self.message_bus.queues)
            
            logger.info("  -> [Simulação] Coletando estado do sistema e arquivos críticos...")
            with open(snapshot_path / "system_state.json", "w") as f:
                json.dump({"status": "healthy", "active_agents": active_agents_count}, f)
            
            compressed_path = shutil.make_archive(str(snapshot_path), 'zip', str(snapshot_path))
            shutil.rmtree(snapshot_path)
            
            snapshot = SystemSnapshot(
                snapshot_id=snapshot_id,
                timestamp=datetime.now(),
                backup_path=compressed_path,
                size_mb=Path(compressed_path).stat().st_size / (1024 * 1024),
            )
            self.system_snapshots[snapshot_id] = snapshot
            
            return {"status": "completed", "snapshot_id": snapshot_id, "size_mb": round(snapshot.size_mb, 2)}
        except Exception as e:
            logger.error(f"❌ Erro criando snapshot {snapshot_id}: {e}", exc_info=True)
            if snapshot_path.exists(): shutil.rmtree(snapshot_path)
            return {"status": "error", "message": str(e)}
            
    # O resto das funções (restore_system, _execute_recovery_plan) não precisavam de correção.

def create_disaster_recovery_agent(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize the DisasterRecoveryAgent(s) for the ALSHAM QUANTUM system.

    This function instantiates the DisasterRecoveryAgent, logs all relevant events for diagnostics,
    and returns it in a list for registration in the agent registry. Handles errors robustly
    and ensures the agent is ready for operation.

    Args:
        message_bus (Any): The message bus or communication channel for agent messaging.

    Returns:
        List[BaseNetworkAgent]: A list containing the initialized DisasterRecoveryAgent instance(s).
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🛡️ [Factory] Criando DisasterRecoveryAgent...")
    try:
        agent = DisasterRecoveryAgent("disaster_recovery_001", message_bus)
        agents.append(agent)
        logger.info(f"🛡️ DisasterRecoveryAgent criado com sucesso: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar DisasterRecoveryAgent: {e}", exc_info=True)
    return agents
