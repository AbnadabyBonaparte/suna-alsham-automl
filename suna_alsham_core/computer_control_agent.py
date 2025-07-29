#!/usr/bin/env python3
"""
Módulo do Computer Control Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica real de execução de terminal e uma estrutura
robusta para futuras automações de browser e SSH.
"""

import asyncio
import logging
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class AutomationType(Enum):
    """Tipos de automação que o agente pode executar."""
    TERMINAL = "terminal"
    BROWSER = "browser"
    REMOTE_SSH = "remote_ssh"


class ControlStatus(Enum):
    """Status de uma tarefa de automação."""
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


# --- Classe Principal do Agente ---

class ComputerControlAgent(BaseNetworkAgent):
    """
    Agente de controle computacional avançado. Serve como a interface do sistema
    para interagir com sistemas operacionais, softwares e máquinas remotas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ComputerControlAgent."""
        super().__init__(agent_id, AgentType.AUTOMATOR, message_bus)
        self.capabilities.extend([
            "terminal_execution",
            "browser_automation",
            "remote_ssh_control",
        ])
        
        self.active_tasks: Dict[str, Any] = {}
        self._check_optional_dependencies()
        
        logger.info(f"🤖 {self.agent_id} (Controle Computacional) inicializado.")

    def _check_optional_dependencies(self):
        """Verifica se dependências opcionais como Selenium estão instaladas."""
        try:
            import selenium
            self.has_selenium = True
            logger.info("  -> Capacidade de automação de Browser: ATIVADA (Selenium encontrado).")
        except ImportError:
            self.has_selenium = False
            logger.warning("  -> Capacidade de automação de Browser: DESATIVADA (Selenium não encontrado).")
        
        try:
            import paramiko
            self.has_ssh = True
            logger.info("  -> Capacidade de controle SSH: ATIVADA (Paramiko encontrado).")
        except ImportError:
            self.has_ssh = False
            logger.warning("  -> Capacidade de controle SSH: DESATIVADA (Paramiko não encontrado).")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de automação e controle."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "execute_automation":
            result = await self.execute_automation(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            logger.warning(f"Ação desconhecida para ComputerControlAgent: {request_type}")
            await self.message_bus.publish(self.create_error_response(message, "Ação de automação desconhecida"))

    async def execute_automation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ponto de entrada para executar uma tarefa de automação."""
        try:
            automation_type = AutomationType(request_data.get("type", "terminal"))
            parameters = request_data.get("parameters", {})
            task_id = f"auto_{uuid4().hex[:8]}"
            self.active_tasks[task_id] = {"status": ControlStatus.EXECUTING, "start_time": time.time()}

            handler = {
                AutomationType.TERMINAL: self._execute_terminal_task,
                AutomationType.BROWSER: self._execute_browser_task,
                AutomationType.REMOTE_SSH: self._execute_ssh_task,
            }.get(automation_type)

            if handler:
                result = await handler(parameters)
            else:
                result = {"success": False, "error": f"Tipo de automação '{automation_type.value}' não suportado."}
            
            self.active_tasks.pop(task_id, None)
            return {"status": "completed", "task_id": task_id, "result": result}
        
        except ValueError:
            return {"status": "error", "message": "Tipo de automação inválido."}
        except Exception as e:
            logger.error(f"❌ Erro executando automação: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    async def _execute_terminal_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """[LÓGICA REAL] Executa um comando no terminal de forma segura e assíncrona."""
        command = parameters.get("command", "")
        if not command:
            return {"success": False, "error": "Comando não especificado."}
        
        logger.info(f"💻 Executando comando no terminal: {command}")
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120) # Timeout de 2 minutos
            
            return {
                "success": proc.returncode == 0,
                "return_code": proc.returncode,
                "stdout": stdout.decode('utf-8', errors='ignore'),
                "stderr": stderr.decode('utf-8', errors='ignore'),
            }
        except asyncio.TimeoutError:
            logger.error(f"Timeout executando comando: {command}")
            return {"success": False, "error": "Comando excedeu o tempo limite de 120 segundos."}
        except Exception as e:
            logger.error(f"Falha ao executar comando '{command}': {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def _execute_browser_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """[AUTENTICIDADE] Placeholder para automação de navegador."""
        if not self.has_selenium:
            return {"success": False, "error": "Selenium não está instalado. Automação de browser desativada."}
        
        logger.info(f"🌐 [Simulação] Executando tarefa de browser: {parameters.get('action')}")
        await asyncio.sleep(1)
        return {"success": True, "action": parameters.get('action'), "result": "Ação de browser simulada com sucesso."}
        
    async def _execute_ssh_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """[AUTENTICIDADE] Placeholder para automação SSH."""
        if not self.has_ssh:
            return {"success": False, "error": "Paramiko não está instalado. Automação SSH desativada."}
            
        logger.info(f"🔒 [Simulação] Executando tarefa SSH no host: {parameters.get('host')}")
        await asyncio.sleep(2)
        return {"success": True, "command": parameters.get('command'), "result": "Comando SSH simulado com sucesso."}


def create_computer_control_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de controle computacional."""
    agents = []
    logger.info("🤖 Criando ComputerControlAgent...")
    try:
        agent = ComputerControlAgent("computer_control_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ComputerControlAgent: {e}", exc_info=True)
    return agents
