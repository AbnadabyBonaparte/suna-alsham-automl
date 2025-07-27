#!/usr/bin/env python3
"""
Módulo do Disaster Recovery Agent - SUNA-ALSHAM

Define o agente Enterprise de Recuperação de Desastres, responsável por garantir
a continuidade do negócio através de snapshots do sistema e planos de recuperação.
"""

import asyncio
import hashlib
import json
import logging
import shutil
import zipfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class DisasterType(Enum):
    """Tipos de desastres que o agente pode tratar."""
    SYSTEM_CRASH = "system_crash"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_BREACH = "security_breach"
    HARDWARE_FAILURE = "hardware_failure"


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
    Cria snapshots do sistema e orquestra a execução de planos de recuperação
    para garantir a continuidade das operações.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DisasterRecoveryAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend([
            "full_system_backup",
            "state_snapshot",
            "instant_recovery",
            "disaster_detection",
            "automated_restoration",
        ])
        
        self.backup_root = Path("./disaster_recovery_backups")
        self.backup_root.mkdir(exist_ok=True)
        
        self.system_snapshots: Dict[str, SystemSnapshot] = {}
        self.recovery_plans: Dict[str, RecoveryPlan] = self._initialize_recovery_plans()
        
        logger.info(f"🛡️ {self.agent_id} (Recuperação de Desastres) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de recuperação de desastres."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "create_snapshot": self.create_system_snapshot,
                "restore_system": self.restore_system,
            }.get(request_type)

            if handler:
                result = await handler(message.content)
                await self.message_bus.publish(self.create_response(message, result))
        elif message.message_type == MessageType.EMERGENCY:
            await self._handle_emergency(message)

    async def _handle_emergency(self, message: AgentMessage):
        """Inicia um plano de recuperação em resposta a uma emergência."""
        disaster_type_str = message.content.get("disaster_type", "system_crash")
        disaster_type = DisasterType(disaster_type_str)
        
        logger.critical(f"🚨 EMERGÊNCIA DETECTADA: {disaster_type.value}. Iniciando recuperação.")
        
        # Encontrar e executar o plano de recuperação apropriado
        plan_to_execute = next((p for p in self.recovery_plans.values() if p.disaster_type == disaster_type), None)

        if plan_to_execute:
            await self._execute_recovery_plan(plan_to_execute)
        else:
            logger.error(f"Nenhum plano de recuperação encontrado para o desastre: {disaster_type.value}")

    def _initialize_recovery_plans(self) -> Dict[str, RecoveryPlan]:
        """Carrega os planos de recuperação padrão do sistema."""
        plans = [
            RecoveryPlan(
                plan_id="PLAN_SYSTEM_CRASH",
                disaster_type=DisasterType.SYSTEM_CRASH,
                recovery_steps=[
                    {"action": "assess_system_state"},
                    {"action": "restore_latest_snapshot"},
                    {"action": "restart_critical_agents"},
                    {"action": "validate_system_integrity"},
                ],
                estimated_rto_minutes=30,
            ),
            RecoveryPlan(
                plan_id="PLAN_DATA_CORRUPTION",
                disaster_type=DisasterType.DATA_CORRUPTION,
                recovery_steps=[
                    {"action": "isolate_corrupted_data"},
                    {"action": "identify_clean_backup"},
                    {"action": "restore_from_clean_backup"},
                    {"action": "verify_data_integrity"},
                ],
                estimated_rto_minutes=45,
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
            
            # [AUTENTICIDADE] Na Fase 2, esta seção será integrada com outros agentes
            # para coletar o estado real do sistema, configurações e arquivos críticos.
            logger.info("  -> [Simulação] Coletando estado do sistema e arquivos críticos...")
            # Criar um arquivo de exemplo para simular o backup
            with open(snapshot_path / "system_state.json", "w") as f:
                json.dump({"status": "healthy", "active_agents": 39}, f)
            
            checksums = self._calculate_checksums_for_dir(snapshot_path)
            
            # Comprimir o snapshot
            compressed_path = shutil.make_archive(str(snapshot_path), 'zip', str(snapshot_path))
            shutil.rmtree(snapshot_path) # Remove a pasta original após compressão
            
            snapshot = SystemSnapshot(
                snapshot_id=snapshot_id,
                timestamp=datetime.now(),
                backup_path=compressed_path,
                size_mb=Path(compressed_path).stat().st_size / (1024 * 1024),
                file_checksums=checksums,
            )
            
            self.system_snapshots[snapshot_id] = snapshot
            
            return {
                "status": "completed",
                "snapshot_id": snapshot_id,
                "size_mb": round(snapshot.size_mb, 2),
            }
        except Exception as e:
            logger.error(f"❌ Erro criando snapshot {snapshot_id}: {e}", exc_info=True)
            # Limpeza em caso de falha
            if snapshot_path.exists():
                shutil.rmtree(snapshot_path)
            return {"status": "error", "message": str(e)}

    def _calculate_checksums_for_dir(self, directory: Path) -> Dict[str, str]:
        """Calcula o checksum SHA256 para todos os arquivos em um diretório."""
        checksums = {}
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                checksums[str(file_path.relative_to(directory))] = file_hash
        return checksums

    async def restore_system(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Restaura o sistema a partir de um snapshot especificado."""
        snapshot_id = request_data.get("snapshot_id")
        if not snapshot_id or snapshot_id not in self.system_snapshots:
            return {"status": "error", "message": f"Snapshot '{snapshot_id}' não encontrado."}
        
        snapshot = self.system_snapshots[snapshot_id]
        logger.info(f"🔄 Iniciando restauração do snapshot {snapshot_id}")

        # [AUTENTICIDADE] A lógica de restauração real (parar serviços,
        # descompactar arquivos, reiniciar agentes) será implementada na Fase 2.
        logger.info("  -> [Simulação] Executando passos de restauração...")
        await asyncio.sleep(5) # Simula o tempo de restauração
        
        logger.info(f"✅ Restauração do snapshot {snapshot_id} concluída (simulada).")
        return {"status": "completed_simulated", "restored_from": snapshot_id}

    async def _execute_recovery_plan(self, plan: RecoveryPlan):
        """Executa os passos de um plano de recuperação."""
        logger.info(f"🔧 Executando plano de recuperação: {plan.plan_id}")
        for step in plan.recovery_steps:
            logger.info(f"  -> Passo: {step['action']}")
            # [AUTENTICIDADE] Lógica real para cada ação será implementada na Fase 2.
            await asyncio.sleep(1)
        logger.info(f"✅ Plano {plan.plan_id} executado (simulado).")


def create_disaster_recovery_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Recuperação de Desastres."""
    agents = []
    logger.info("🛡️ Criando DisasterRecoveryAgent...")
    try:
        agent = DisasterRecoveryAgent("disaster_recovery_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DisasterRecoveryAgent: {e}", exc_info=True)
    return agents
