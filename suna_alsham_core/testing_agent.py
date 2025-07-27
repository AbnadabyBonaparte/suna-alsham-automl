#!/usr/bin/env python3
"""
Módulo do Testing Agent - SUNA-ALSHAM

Define o agente de testes automatizados avançado, responsável por executar
testes, monitorar cobertura de código e detectar regressões no sistema.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
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

class TestType(Enum):
    """Tipos de testes que o agente pode executar."""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    REGRESSION = "regression"


class TestStatus(Enum):
    """Status de uma execução de teste."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class TestRun:
    """Representa uma execução completa de uma suíte de testes."""
    run_id: str
    test_type: TestType
    status: TestStatus = TestStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    summary: Dict[str, int] = field(default_factory=dict)
    coverage_percentage: float = 0.0
    report_path: Optional[str] = None


# --- Classe Principal do Agente ---

class TestingAgent(BaseNetworkAgent):
    """
    Agente especializado em testes automatizados e validação de qualidade.
    Orquestra a execução de testes, mede cobertura e detecta regressões.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o TestingAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "automated_testing",
            "code_coverage",
            "regression_testing",
            "test_generation",
            "quality_assurance",
        ])
        
        # Configurações do ambiente de teste
        self.test_directory = Path("./tests")
        self.reports_directory = self.test_directory / "reports"
        self.test_directory.mkdir(exist_ok=True)
        self.reports_directory.mkdir(exist_ok=True)

        self.test_queue = asyncio.Queue()
        self.active_test_runs: Dict[str, TestRun] = {}
        
        self._testing_task = None
        logger.info(f"🧪 {self.agent_id} (Agente de Testes) inicializado.")

    async def start_testing_service(self):
        """Inicia os serviços de background do agente."""
        if not self._testing_task:
            self._testing_task = asyncio.create_task(self._testing_loop())
            logger.info(f"🧪 {self.agent_id} iniciou serviço de testes.")

    async def _testing_loop(self):
        """Loop principal que processa a fila de execuções de teste."""
        while True:
            try:
                test_request = await self.test_queue.get()
                await self._process_test_request(test_request)
            except asyncio.CancelledError:
                logger.info(f"Loop de testes do {self.agent_id} cancelado.")
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de testes: {e}", exc_info=True)

    async def handle_message(self, message: AgentMessage):
        """Processa requisições para execução de testes."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "run_tests":
                result = await self.run_tests(message.content)
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de teste desconhecida: {request_type}")

    async def run_tests(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria e enfileira um novo trabalho de execução de testes.
        """
        try:
            test_type = TestType(request_data.get("type", "unit"))
            pattern = request_data.get("pattern", "test_*.py")
            
            run_id = f"test_run_{int(time.time())}"
            test_run = TestRun(run_id=run_id, test_type=test_type)
            
            await self.test_queue.put({"run": test_run, "pattern": pattern})
            
            logger.info(f"📥 Novo job de teste enfileirado: {run_id} ({test_type.value})")
            return {"status": "queued", "run_id": run_id}
        except Exception as e:
            logger.error(f"❌ Erro ao criar job de teste: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    async def _process_test_request(self, request: Dict[str, Any]):
        """Processa uma requisição da fila de testes."""
        run: TestRun = request["pattern"]
        pattern: str = request["pattern"]
        
        self.active_test_runs[run.run_id] = run
        run.status = TestStatus.RUNNING
        run.start_time = datetime.now()

        try:
            # Comando para executar pytest com cobertura e relatório JSON
            report_path = self.reports_directory / f"{run.run_id}.json"
            cmd = [
                sys.executable, "-m", "pytest",
                "--cov=suna_alsham_core", # Medir cobertura do nosso núcleo
                f"--cov-report=json:{report_path}",
                "-q", # Modo quieto para saída limpa
                self.test_directory.as_posix() # Diretório de testes
            ]
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)

            if proc.returncode == 0:
                run.status = TestStatus.PASSED
            else:
                run.status = TestStatus.FAILED
            
            # Processar o relatório de cobertura
            if report_path.exists():
                with open(report_path) as f:
                    coverage_data = json.load(f)
                run.coverage_percentage = coverage_data.get("totals", {}).get("percent_covered", 0)
                run.report_path = str(report_path)
        
        except asyncio.TimeoutError:
            run.status = TestStatus.TIMEOUT
            logger.error(f"❌ Teste {run.run_id} excedeu o tempo limite.")
        except Exception as e:
            run.status = TestStatus.ERROR
            logger.error(f"❌ Erro executando testes para {run.run_id}: {e}", exc_info=True)

        finally:
            run.end_time = datetime.now()
            if run.run_id in self.active_test_runs:
                del self.active_test_runs[run.run_id]


def create_testing_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Testes Automatizados."""
    agents = []
    logger.info("🧪 Criando TestingAgent...")
    try:
        agent = TestingAgent("testing_001", message_bus)
        asyncio.create_task(agent.start_testing_service())
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando TestingAgent: {e}", exc_info=True)
    return agents
