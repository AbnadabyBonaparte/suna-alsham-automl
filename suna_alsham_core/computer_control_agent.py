#!/usr/bin/env python3
"""
Módulo do Agente de Controle de Computador - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica real de execução de comandos via
bibliotecas padrão e preparação para integrações com Selenium/SSH.
"""
import asyncio
import logging
import shlex
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Enums e Dataclasses ---
class CommandStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class CommandResult:
    """Representa o resultado da execução de um comando no sistema."""
    command: str
    status: CommandStatus
    stdout: str
    stderr: str
    return_code: int

# --- Classe Principal do Agente ---
class ComputerControlAgent(BaseNetworkAgent):
    """
    Agente de baixo nível que executa comandos no sistema operacional
    subjacente. É uma capacidade poderosa que deve ser usada com
    extremo cuidado e protegida pelo SecurityGuardianAgent.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ComputerControlAgent."""
        # O tipo deste agente é AUTOMATOR, que precisa ser definido no AgentType Enum
        super().__init__(agent_id, AgentType.AUTOMATOR, message_bus)
        self.capabilities.extend([
            "execute_shell_command",
            "file_system_manipulation",
            "ssh_connection" # Capacidade futura
        ])
        logger.info(f"🤖 {self.agent_id} (Controle de Computador) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para executar comandos."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "execute_command":
            result = await self.execute_command(message.content)
            await self.publish_response(message, result)

    async def execute_command(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Executa um comando de shell de forma assíncrona e segura.
        """
        command_str = request_data.get("command")
        timeout = request_data.get("timeout", 60) # Timeout de 60 segundos
        
        if not command_str:
            return {"status": "error", "message": "Nenhum comando fornecido."}

        # Medida de segurança: não permite comandos complexos ou encadeados.
        if ";" in command_str or "&&" in command_str or "||" in command_str:
            return {"status": "error", "message": "Comandos complexos ou encadeados não são permitidos."}

        try:
            # shlex.split lida com a tokenização segura do comando
            args = shlex.split(command_str)
            
            logger.info(f"Executando comando: {args}")

            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            
            result = CommandResult(
                command=command_str,
                status=CommandStatus.SUCCESS if proc.returncode == 0 else CommandStatus.ERROR,
                stdout=stdout.decode().strip(),
                stderr=stderr.decode().strip(),
                return_code=proc.returncode
            )
            
            return {
                "status": "completed",
                "result": result.__dict__
            }

        except asyncio.TimeoutError:
            logger.error(f"Timeout ao executar o comando: '{command_str}'")
            return {"status": "error", "message": "Comando excedeu o tempo limite."}
        except Exception as e:
            logger.error(f"Erro ao executar o comando '{command_str}': {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

def create_computer_control_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Controle de Computador."""
    agents = []
    logger.info("🤖 Criando ComputerControlAgent...")
    try:
        agent = ComputerControlAgent("computer_control_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ComputerControlAgent: {e}", exc_info=True)
    return agents
