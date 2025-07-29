#!/usr/bin/env python3
"""
Módulo do Web Search Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica de busca real via aiohttp e melhor
processamento de resultados.
"""

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

# [AUTENTICIDADE] aiohttp é usado para chamadas de API assíncronas reais.
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

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
    relevance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


# --- Classe Principal do Agente ---

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
        ])

        if not AIOHTTP_AVAILABLE:
            self.status = "degraded"
            logger.critical("Biblioteca 'aiohttp' não encontrada. O WebSearchAgent operará em modo degradado.")
        
        logger.info(f"🌐 {self.agent_id} (Busca Web) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de busca."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "search_solutions":
            result = await self.search_solutions(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            logger.warning(f"Ação de busca desconhecida: {request_type}")
            await self.message_bus.publish(self.create_error_response(message, "Ação de busca desconhecida"))

    async def search_solutions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Busca soluções para um problema específico em múltiplas fontes.
        """
        problem_desc = request_data.get("problem_description", "")
        if not problem_desc:
            return {"status": "error", "message": "Descrição do problema não fornecida."}

        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de busca indisponível (dependências faltando)."}

        logger.info(f"🔍 Buscando soluções para: '{problem_desc[:50]}...'")
        
        try:
            # Executa buscas em paralelo
            search_tasks = [
                self._search_stackoverflow(problem_desc),
                self._search_github(problem_desc)
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

    async def _search_github(self, query: str) -> List[SearchResult]:
        """
        [AUTENTICIDADE] Placeholder para busca real no GitHub.
        A implementação real na Fase 3 usará a API do GitHub com autenticação.
        """
        logger.info(f"-> [Simulação] Buscando no GitHub: '{query}'")
        await asyncio.sleep(0.5)
        return [
            SearchResult(
                source=SourceType.GITHUB,
                title="Exemplo de Solução no GitHub",
                url="https://github.com/example/repo/blob/main/solution.py",
                relevance_score=0.85,
            )
        ]

    async def _search_stackoverflow(self, query: str) -> List[SearchResult]:
        """
        [LÓGICA REAL] Busca no Stack Overflow usando a API pública.
        """
        logger.info(f"-> Buscando no Stack Overflow: '{query}'")
        encoded_query = quote_plus(query)
        url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={encoded_query}&tagged=python&site=stackoverflow"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            SearchResult(
                                source=SourceType.STACKOVERFLOW,
                                title=item['title'],
                                url=item['link'],
                                relevance_score=item.get('score', 0) / 100.0, # Normaliza score
                                metadata={"is_answered": item.get('is_answered', False)},
                            ) for item in data.get('items', [])[:5] # Pega os top 5
                        ]
                    else:
                        logger.warning(f"API do StackOverflow retornou status {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Erro na busca do StackOverflow: {e}", exc_info=True)
            return []

    def _rank_search_results(self, results: List[SearchResult], problem: str) -> List[SearchResult]:
        """Rankeia os resultados da busca por relevância."""
        # Lógica de ranking aprimorada
        for result in results:
            if result.source == SourceType.STACKOVERFLOW and result.metadata.get("is_answered"):
                result.relevance_score *= 1.5
        
        return sorted(results, key=lambda r: r.relevance_score, reverse=True)

    def _generate_solution(self, problem: str, ranked_results: List[SearchResult]) -> Dict[str, Any]:
        """Gera uma solução consolidada a partir dos resultados da busca."""
        if not ranked_results:
            return {"recommended_action": "Nenhuma solução clara encontrada."}

        best_result = ranked_results[0]
        return {
            "recommended_action": f"Implementar solução baseada em '{best_result.title}'",
            "source": best_result.source.value,
            "url": best_result.url,
            "confidence_score": best_result.relevance_score,
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
