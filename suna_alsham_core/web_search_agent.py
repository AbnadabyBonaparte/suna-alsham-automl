#!/usr/bin/env python3
"""
Módulo do Web Search Agent - SUNA-ALSHAM

Define o agente especializado em buscar soluções, melhores práticas e tendências
na web, utilizando fontes como GitHub, Stack Overflow e documentações oficiais.
"""

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import aiohttp

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


class SourceType(Enum):
    """Tipos de fontes de busca."""
    GITHUB = "github"
    STACKOVERFLOW = "stackoverflow"
    DOCUMENTATION = "documentation"


@dataclass
class SearchResult:
    """Representa um único resultado de busca encontrado."""
    source: SourceType
    title: str
    url: str
    description: str
    relevance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class WebSearchAgent(BaseNetworkAgent):
    """
    Agente que atua como a interface do sistema com a web para pesquisa de
    informações, soluções de código e tendências tecnológicas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o WebSearchAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "web_search",
            "solution_finding",
            "documentation_lookup",
            "technology_trends",
        ])
        self.search_history = []
        logger.info(f"🌐 {self.agent_id} (Busca Web) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de busca."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "search_solutions":
                result = await self.search_solutions(message.content)
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação desconhecida para WebSearchAgent: {request_type}")

    async def search_solutions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Busca soluções para um problema específico em múltiplas fontes.

        Args:
            request_data: Dicionário contendo a descrição do problema.

        Returns:
            Um dicionário com a solução encontrada ou um status de erro.
        """
        try:
            problem_desc = request_data.get("problem_description", "")
            if not problem_desc:
                return {"status": "error", "message": "Descrição do problema não fornecida."}

            logger.info(f"🔍 Buscando soluções para: '{problem_desc[:50]}...'")

            search_queries = self._generate_search_queries(problem_desc)
            
            # Executa buscas em paralelo
            search_tasks = [
                self._search_github(query) for query in search_queries
            ] + [
                self._search_stackoverflow(query) for query in search_queries
            ]
            
            all_results_lists = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Aplaina e filtra resultados válidos
            all_results = []
            for res_list in all_results_lists:
                if isinstance(res_list, list):
                    all_results.extend(res_list)
            
            ranked_results = self._rank_search_results(all_results, problem_desc)
            solution = self._generate_solution(problem_desc, ranked_results)

            return {"status": "completed", "solution": solution}

        except Exception as e:
            logger.error(f"❌ Erro buscando soluções: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _generate_search_queries(self, problem_desc: str) -> List[str]:
        """Gera múltiplas queries de busca para um problema."""
        # Extrai palavras-chave para criar buscas mais eficazes
        keywords = " ".join(re.findall(r"\b\w{3,}\b", problem_desc))
        return [
            f"python {problem_desc}",
            f"fix python {keywords}",
            f"{keywords} stackoverflow",
        ]

    async def _search_github(self, query: str) -> List[SearchResult]:
        """
        [SIMULAÇÃO] Busca no GitHub por exemplos de código e soluções.
        Na Fase 2, será substituído por uma chamada real à API do GitHub.
        """
        logger.info(f"-> [Simulação] Buscando no GitHub: '{query}'")
        await asyncio.sleep(0.5) # Simula latência da rede
        return [
            SearchResult(
                source=SourceType.GITHUB,
                title="Exemplo de Solução no GitHub",
                url="https://github.com/example/repo/blob/main/solution.py",
                description="Repositório de exemplo com implementação relevante.",
                relevance_score=0.85,
            )
        ]

    async def _search_stackoverflow(self, query: str) -> List[SearchResult]:
        """
        [SIMULAÇÃO] Busca no Stack Overflow por perguntas e respostas.
        Na Fase 2, será substituído por uma chamada real à API do Stack Exchange.
        """
        logger.info(f"-> [Simulação] Buscando no Stack Overflow: '{query}'")
        await asyncio.sleep(0.5)
        return [
            SearchResult(
                source=SourceType.STACKOVERFLOW,
                title="Como resolver [problema similar]? - Stack Overflow",
                url="https://stackoverflow.com/questions/12345",
                description="Pergunta com resposta aceita e alta pontuação.",
                relevance_score=0.90,
                metadata={"is_answered": True, "score": 150},
            )
        ]

    def _rank_search_results(
        self, results: List[SearchResult], problem: str
    ) -> List[SearchResult]:
        """Rankeia os resultados da busca por relevância."""
        # Lógica de ranking (pode ser aprimorada com ML no futuro)
        for result in results:
            if result.source == SourceType.STACKOVERFLOW and result.metadata.get("is_answered"):
                result.relevance_score *= 1.2  # Aumenta a relevância de respostas aceitas
        
        return sorted(results, key=lambda r: r.relevance_score, reverse=True)

    def _generate_solution(
        self, problem: str, ranked_results: List[SearchResult]
    ) -> Dict[str, Any]:
        """Gera uma solução consolidada a partir dos resultados da busca."""
        if not ranked_results:
            return {
                "recommended_action": "Nenhuma solução clara encontrada. Recomenda-se reformular a busca.",
                "confidence_score": 0.1,
            }

        best_result = ranked_results[0]
        return {
            "recommended_action": f"Implementar solução baseada em '{best_result.title}'",
            "source": best_result.source.value,
            "url": best_result.url,
            "confidence_score": best_result.relevance_score,
            "implementation_steps": [
                f"Analisar a solução encontrada em: {best_result.url}",
                "Adaptar o código de exemplo ao contexto do sistema.",
                "Implementar testes para validar a nova solução.",
            ],
        }


def create_web_search_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de busca na web."""
    agents = []
    logger.info("🌐 Criando WebSearchAgent...")
    try:
        agent = WebSearchAgent("web_search_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando WebSearchAgent: {e}", exc_info=True)
    return agents
