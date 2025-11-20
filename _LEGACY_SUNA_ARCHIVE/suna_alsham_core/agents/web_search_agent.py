#!/usr/bin/env python3
"""
Web Search Agent - Agente de Pesquisa Web do ALSHAM QUANTUM
Especializado em pesquisas reais na internet com múltiplos mecanismos de busca.
Versão corrigida com implementação completa e funcionalidades avançadas.
"""

import asyncio
import logging
import time
import urllib.parse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Importações para web scraping
import requests
from bs4 import BeautifulSoup
import aiohttp

# Importações corrigidas para compatibilidade
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent,
    AgentType,
    MessageType,
    Priority,
    AgentMessage
)

logger = logging.getLogger(__name__)

class SearchEngine(Enum):
    """Mecanismos de busca disponíveis."""
    GOOGLE = "google"
    BING = "bing"
    DUCKDUCKGO = "duckduckgo"
    YAHOO = "yahoo"

class SearchType(Enum):
    """Tipos de pesquisa disponíveis."""
    WEB = "web"
    NEWS = "news"
    IMAGES = "images"
    ACADEMIC = "academic"
    SOCIAL = "social"

@dataclass
class SearchResult:
    """Resultado de uma pesquisa web."""
    title: str
    url: str
    description: str = ""
    domain: str = ""
    search_engine: SearchEngine = SearchEngine.GOOGLE
    rank: int = 0
    extracted_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    found_at: datetime = field(default_factory=datetime.now)

@dataclass
class SearchQuery:
    """Estrutura de uma query de pesquisa."""
    query: str
    search_engine: SearchEngine = SearchEngine.GOOGLE
    search_type: SearchType = SearchType.WEB
    max_results: int = 10
    language: str = "pt-BR"
    region: str = "BR"
    safe_search: bool = True
    extract_content: bool = False

@dataclass
class SearchStats:
    """Estatísticas de pesquisa."""
    total_searches: int = 0
    successful_searches: int = 0
    failed_searches: int = 0
    total_results_found: int = 0
    average_response_time: float = 0.0
    last_search_time: Optional[datetime] = None

class WebSearchAgent(BaseNetworkAgent):
    """
    Agente de Pesquisa Web do ALSHAM QUANTUM.
    Especializado em pesquisas reais na internet com múltiplos engines.
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Configuração do agente
        self.capabilities.extend([
            "real_web_search",
            "multi_engine_search",
            "content_extraction",
            "url_analysis",
            "search_optimization",
            "result_filtering",
            "domain_analysis",
            "metadata_extraction",
            "news_search",
            "academic_search"
        ])
        
        # Configuração de headers para requisições
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        # Estado interno
        self.search_stats = SearchStats()
        self.search_history: List[Dict[str, Any]] = []
        self.blocked_domains: set = {"example.com", "test.com"}
        self.rate_limit_delay = 1.0  # Segundos entre pesquisas
        self.last_search_time = 0
        
        # Configuração de engines
        self.search_engines = {
            SearchEngine.GOOGLE: self._search_google,
            SearchEngine.BING: self._search_bing,
            SearchEngine.DUCKDUCKGO: self._search_duckduckgo,
            SearchEngine.YAHOO: self._search_yahoo
        }
        
        logger.info(f"🔎 {self.agent_id} (Web Search Agent) inicializado com múltiplos engines")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo agente de pesquisa."""
        try:
            content = message.content
            message_type = content.get("type", "search")
            
            if message_type == "search" or message_type == "web_search":
                await self._handle_web_search(message)
            elif message_type == "multi_engine_search":
                await self._handle_multi_engine_search(message)
            elif message_type == "extract_content":
                await self._handle_extract_content(message)
            elif message_type == "analyze_url":
                await self._handle_analyze_url(message)
            elif message_type == "news_search":
                await self._handle_news_search(message)
            elif message_type == "get_search_stats":
                await self._handle_get_search_stats(message)
            elif message_type == "get_search_history":
                await self._handle_get_search_history(message)
            elif message_type == "advanced_search":
                await self._handle_advanced_search(message)
            else:
                logger.debug(f"🔎 Tipo de mensagem não reconhecido: {message_type}")
                await self.publish_error_response(message, f"Tipo não reconhecido: {message_type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno: {str(e)}")

    async def _handle_web_search(self, message: AgentMessage):
        """Realiza pesquisa web básica."""
        try:
            content = message.content
            query = content.get("query")
            if not query:
                await self.publish_error_response(message, "Query de pesquisa não fornecida")
                return
            
            max_results = content.get("max_results", 10)
            search_engine = content.get("search_engine", "google")
            extract_content = content.get("extract_content", False)
            
            # Criar objeto de pesquisa
            search_query = SearchQuery(
                query=query,
                search_engine=SearchEngine(search_engine),
                max_results=max_results,
                extract_content=extract_content
            )
            
            # Executar pesquisa
            start_time = time.time()
            results = await self._perform_search(search_query)
            response_time = time.time() - start_time
            
            # Atualizar estatísticas
            self._update_search_stats(len(results), response_time, success=True)
            
            # Registrar no histórico
            self._record_search_history(search_query, len(results), response_time)
            
            await self.publish_response(message, {
                "status": "success",
                "query": query,
                "results_count": len(results),
                "results": [self._serialize_search_result(result) for result in results],
                "response_time": response_time,
                "search_engine": search_engine
            })
            
        except Exception as e:
            self._update_search_stats(0, 0, success=False)
            await self.publish_error_response(message, f"Erro na pesquisa web: {str(e)}")

    async def _handle_multi_engine_search(self, message: AgentMessage):
        """Realiza pesquisa em múltiplos engines."""
        try:
            content = message.content
            query = content.get("query")
            if not query:
                await self.publish_error_response(message, "Query de pesquisa não fornecida")
                return
            
            engines = content.get("engines", ["google", "bing", "duckduckgo"])
            max_results_per_engine = content.get("max_results_per_engine", 5)
            
            all_results = []
            engine_results = {}
            
            # Pesquisar em cada engine
            for engine_name in engines:
                try:
                    search_query = SearchQuery(
                        query=query,
                        search_engine=SearchEngine(engine_name),
                        max_results=max_results_per_engine
                    )
                    
                    results = await self._perform_search(search_query)
                    engine_results[engine_name] = len(results)
                    all_results.extend(results)
                    
                    # Rate limiting entre engines
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.warning(f"Erro ao pesquisar no {engine_name}: {e}")
                    engine_results[engine_name] = 0
            
            # Remover duplicatas baseado na URL
            unique_results = []
            seen_urls = set()
            
            for result in all_results:
                if result.url not in seen_urls:
                    unique_results.append(result)
                    seen_urls.add(result.url)
            
            await self.publish_response(message, {
                "status": "success",
                "query": query,
                "engines_used": engines,
                "engine_results": engine_results,
                "total_results": len(unique_results),
                "unique_results": len(unique_results),
                "results": [self._serialize_search_result(result) for result in unique_results]
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na pesquisa multi-engine: {str(e)}")

    async def _handle_extract_content(self, message: AgentMessage):
        """Extrai conteúdo de URLs específicas."""
        try:
            content = message.content
            urls = content.get("urls", [])
            if not urls:
                await self.publish_error_response(message, "Lista de URLs não fornecida")
                return
            
            extracted_content = []
            
            for url in urls:
                try:
                    content_data = await self._extract_url_content(url)
                    extracted_content.append({
                        "url": url,
                        "status": "success",
                        "content": content_data
                    })
                except Exception as e:
                    logger.warning(f"Erro ao extrair conteúdo de {url}: {e}")
                    extracted_content.append({
                        "url": url,
                        "status": "error",
                        "error": str(e)
                    })
            
            await self.publish_response(message, {
                "extracted_content": extracted_content,
                "urls_processed": len(urls),
                "successful_extractions": len([c for c in extracted_content if c["status"] == "success"])
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na extração de conteúdo: {str(e)}")

    async def _handle_analyze_url(self, message: AgentMessage):
        """Analisa URLs específicas."""
        try:
            content = message.content
            url = content.get("url")
            if not url:
                await self.publish_error_response(message, "URL não fornecida")
                return
            
            analysis = await self._analyze_url(url)
            
            await self.publish_response(message, {
                "url": url,
                "analysis": analysis,
                "analyzed_at": datetime.now().isoformat()
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na análise de URL: {str(e)}")

    async def _handle_news_search(self, message: AgentMessage):
        """Realiza pesquisa de notícias."""
        try:
            content = message.content
            query = content.get("query")
            if not query:
                await self.publish_error_response(message, "Query de pesquisa não fornecida")
                return
            
            search_query = SearchQuery(
                query=query,
                search_type=SearchType.NEWS,
                max_results=content.get("max_results", 10)
            )
            
            results = await self._perform_search(search_query)
            
            await self.publish_response(message, {
                "status": "success",
                "query": query,
                "news_results": [self._serialize_search_result(result) for result in results],
                "results_count": len(results)
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na pesquisa de notícias: {str(e)}")

    async def _handle_get_search_stats(self, message: AgentMessage):
        """Retorna estatísticas de pesquisa."""
        try:
            stats = {
                "total_searches": self.search_stats.total_searches,
                "successful_searches": self.search_stats.successful_searches,
                "failed_searches": self.search_stats.failed_searches,
                "success_rate": (self.search_stats.successful_searches / max(self.search_stats.total_searches, 1)) * 100,
                "total_results_found": self.search_stats.total_results_found,
                "average_response_time": self.search_stats.average_response_time,
                "last_search_time": self.search_stats.last_search_time.isoformat() if self.search_stats.last_search_time else None
            }
            
            await self.publish_response(message, {"search_stats": stats})
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter estatísticas: {str(e)}")

    async def _handle_get_search_history(self, message: AgentMessage):
        """Retorna histórico de pesquisas."""
        try:
            content = message.content
            limit = content.get("limit", 20)
            
            recent_history = self.search_history[-limit:] if self.search_history else []
            
            await self.publish_response(message, {
                "search_history": recent_history,
                "total_history_entries": len(self.search_history),
                "returned_entries": len(recent_history)
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter histórico: {str(e)}")

    async def _handle_advanced_search(self, message: AgentMessage):
        """Realiza pesquisa avançada com filtros."""
        try:
            content = message.content
            query = content.get("query")
            if not query:
                await self.publish_error_response(message, "Query de pesquisa não fornecida")
                return
            
            # Filtros avançados
            domain_filter = content.get("site")
            file_type = content.get("filetype")
            date_range = content.get("date_range")
            language = content.get("language", "pt-BR")
            
            # Construir query avançada
            advanced_query = query
            if domain_filter:
                advanced_query += f" site:{domain_filter}"
            if file_type:
                advanced_query += f" filetype:{file_type}"
            
            search_query = SearchQuery(
                query=advanced_query,
                language=language,
                max_results=content.get("max_results", 10)
            )
            
            results = await self._perform_search(search_query)
            
            await self.publish_response(message, {
                "status": "success",
                "original_query": query,
                "advanced_query": advanced_query,
                "filters_applied": {
                    "domain": domain_filter,
                    "file_type": file_type,
                    "language": language
                },
                "results": [self._serialize_search_result(result) for result in results],
                "results_count": len(results)
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na pesquisa avançada: {str(e)}")

    async def _perform_search(self, search_query: SearchQuery) -> List[SearchResult]:
        """Executa pesquisa usando o engine especificado."""
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_search_time < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - (current_time - self.last_search_time))
        
        self.last_search_time = time.time()
        
        # Executar pesquisa
        search_function = self.search_engines.get(search_query.search_engine, self._search_google)
        
        try:
            results = await search_function(search_query)
            
            # Extrair conteúdo se solicitado
            if search_query.extract_content:
                for result in results:
                    try:
                        content_data = await self._extract_url_content(result.url)
                        result.extracted_text = content_data.get("text", "")[:1000]  # Limitar a 1000 chars
                    except Exception as e:
                        logger.debug(f"Erro ao extrair conteúdo de {result.url}: {e}")
            
            return results
            
        except Exception as e:
            logger.error(f"Erro na pesquisa com {search_query.search_engine.value}: {e}")
            raise

    async def _search_google(self, search_query: SearchQuery) -> List[SearchResult]:
        """Pesquisa no Google."""
        encoded_query = urllib.parse.quote_plus(search_query.query)
        
        if search_query.search_type == SearchType.NEWS:
            url = f"https://www.google.com/search?q={encoded_query}&tbm=nws&num={search_query.max_results}"
        else:
            url = f"https://www.google.com/search?q={encoded_query}&num={search_query.max_results}"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._make_request, url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Seletores para resultados do Google
        result_divs = soup.find_all('div', class_='g') or soup.find_all('div', {'data-ved': True})
        
        for i, div in enumerate(result_divs[:search_query.max_results]):
            try:
                # Título
                title_elem = div.find('h3') or div.find('a')
                title = title_elem.get_text(strip=True) if title_elem else "Sem título"
                
                # URL
                link_elem = div.find('a')
                if not link_elem or not link_elem.get('href'):
                    continue
                
                url = link_elem['href']
                if url.startswith('/url?q='):
                    url = urllib.parse.unquote(url.split('/url?q=')[1].split('&')[0])
                
                # Descrição
                desc_elem = div.find('span') or div.find('div', class_='VwiC3b')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Domínio
                domain = urllib.parse.urlparse(url).netloc
                
                if domain not in self.blocked_domains:
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        description=description,
                        domain=domain,
                        search_engine=SearchEngine.GOOGLE,
                        rank=i + 1
                    ))
                    
            except Exception as e:
                logger.debug(f"Erro ao processar resultado Google: {e}")
                continue
        
        return results

    async def _search_bing(self, search_query: SearchQuery) -> List[SearchResult]:
        """Pesquisa no Bing."""
        encoded_query = urllib.parse.quote_plus(search_query.query)
        url = f"https://www.bing.com/search?q={encoded_query}&count={search_query.max_results}"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._make_request, url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        result_divs = soup.find_all('li', class_='b_algo')
        
        for i, div in enumerate(result_divs[:search_query.max_results]):
            try:
                title_elem = div.find('h2')
                if not title_elem:
                    continue
                    
                link_elem = title_elem.find('a')
                if not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                url = link_elem.get('href', '')
                
                desc_elem = div.find('p') or div.find('div', class_='b_caption')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                domain = urllib.parse.urlparse(url).netloc
                
                if domain not in self.blocked_domains and url.startswith('http'):
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        description=description,
                        domain=domain,
                        search_engine=SearchEngine.BING,
                        rank=i + 1
                    ))
                    
            except Exception as e:
                logger.debug(f"Erro ao processar resultado Bing: {e}")
                continue
        
        return results

    async def _search_duckduckgo(self, search_query: SearchQuery) -> List[SearchResult]:
        """Pesquisa no DuckDuckGo."""
        encoded_query = urllib.parse.quote_plus(search_query.query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._make_request, url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        result_divs = soup.find_all('div', class_='result')
        
        for i, div in enumerate(result_divs[:search_query.max_results]):
            try:
                title_elem = div.find('a', class_='result__a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                url = title_elem.get('href', '')
                
                desc_elem = div.find('a', class_='result__snippet')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                domain = urllib.parse.urlparse(url).netloc
                
                if domain not in self.blocked_domains and url.startswith('http'):
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        description=description,
                        domain=domain,
                        search_engine=SearchEngine.DUCKDUCKGO,
                        rank=i + 1
                    ))
                    
            except Exception as e:
                logger.debug(f"Erro ao processar resultado DuckDuckGo: {e}")
                continue
        
        return results

    async def _search_yahoo(self, search_query: SearchQuery) -> List[SearchResult]:
        """Pesquisa no Yahoo."""
        encoded_query = urllib.parse.quote_plus(search_query.query)
        url = f"https://search.yahoo.com/search?p={encoded_query}&n={search_query.max_results}"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._make_request, url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        result_divs = soup.find_all('div', class_='Sr')
        
        for i, div in enumerate(result_divs[:search_query.max_results]):
            try:
                title_elem = div.find('h3')
                if not title_elem:
                    continue
                    
                link_elem = title_elem.find('a')
                if not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                url = link_elem.get('href', '')
                
                desc_elem = div.find('span', class_='compText')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                domain = urllib.parse.urlparse(url).netloc
                
                if domain not in self.blocked_domains and url.startswith('http'):
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        description=description,
                        domain=domain,
                        search_engine=SearchEngine.YAHOO,
                        rank=i + 1
                    ))
                    
            except Exception as e:
                logger.debug(f"Erro ao processar resultado Yahoo: {e}")
                continue
        
        return results

    def _make_request(self, url: str) -> requests.Response:
        """Faz requisição HTTP síncrona."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Erro na requisição para {url}: {e}")
            raise

    async def _extract_url_content(self, url: str) -> Dict[str, Any]:
        """Extrai conteúdo de uma URL."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self._make_request, url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remover scripts e styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extrair texto
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            text = '\n'.join(line for line in lines if line)
            
            # Extrair metadados
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content', '') if meta_description else ""
            
            return {
                "url": url,
                "title": title_text,
                "description": description,
                "text": text[:5000],  # Limitar texto
                "word_count": len(text.split()),
                "extracted_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair conteúdo de {url}: {e}")
            raise

    async def _analyze_url(self, url: str) -> Dict[str, Any]:
        """Analisa uma URL específica."""
        try:
            parsed_url = urllib.parse.urlparse(url)
            
            # Fazer requisição HEAD primeiro
            loop = asyncio.get_event_loop()
            try:
                head_response = await loop.run_in_executor(
                    None, 
                    lambda: requests.head(url, headers=self.headers, timeout=5)
                )
                status_code = head_response.status_code
                content_type = head_response.headers.get('content-type', '')
                content_length = head_response.headers.get('content-length', '0')
            except:
                status_code = 0
                content_type = ""
                content_length = "0"
            
            # Análise básica da URL
            analysis = {
                "url": url,
                "domain": parsed_url.netloc,
                "path": parsed_url.path,
                "scheme": parsed_url.scheme,
                "status_code": status_code,
                "content_type": content_type,
                "content_length": content_length,
                "is_secure": parsed_url.scheme == 'https',
                "has_subdomain": len(parsed_url.netloc.split('.')) > 2,
                "path_depth": len([p for p in parsed_url.path.split('/') if p]),
                "has_query": bool(parsed_url.query),
                "has_fragment": bool(parsed_url.fragment)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro ao analisar URL {url}: {e}")
            return {"url": url, "error": str(e)}

    def _serialize_search_result(self, result: SearchResult) -> Dict[str, Any]:
        """Serializa resultado de pesquisa para JSON."""
        return {
            "title": result.title,
            "url": result.url,
            "description": result.description,
            "domain": result.domain,
            "search_engine": result.search_engine.value,
            "rank": result.rank,
            "extracted_text": result.extracted_text,
            "metadata": result.metadata,
            "found_at": result.found_at.isoformat()
        }

    def _update_search_stats(self, results_count: int, response_time: float, success: bool):
        """Atualiza estatísticas de pesquisa."""
        self.search_stats.total_searches += 1
        
        if success:
            self.search_stats.successful_searches += 1
            self.search_stats.total_results_found += results_count
        else:
            self.search_stats.failed_searches += 1
        
        # Atualizar tempo médio de resposta
        if self.search_stats.successful_searches > 0:
            self.search_stats.average_response_time = (
                (self.search_stats.average_response_time * (self.search_stats.successful_searches - 1) + response_time) 
                / self.search_stats.successful_searches
            )
        
        self.search_stats.last_search_time = datetime.now()

    def _record_search_history(self, search_query: SearchQuery, results_count: int, response_time: float):
        """Registra pesquisa no histórico."""
        history_entry = {
            "query": search_query.query,
            "search_engine": search_query.search_engine.value,
            "search_type": search_query.search_type.value,
            "results_count": results_count,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        
        self.search_history.append(history_entry)
        
        # Manter apenas últimas 100 pesquisas
        if len(self.search_history) > 100:
            self.search_history = self.search_history[-100:]


def create_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function para criar o WebSearchAgent.
    
    Cria e inicializa o agente de pesquisa web do sistema ALSHAM QUANTUM.
    
    Args:
        message_bus: MessageBus para comunicação entre agentes.
        
    Returns:
        List[BaseNetworkAgent]: Lista contendo o WebSearchAgent.
    """
    agents: List[BaseNetworkAgent] = []
    
    try:
        logger.info("🔎 [Factory] Criando WebSearchAgent...")
        
        # Criar o agente
        agent = WebSearchAgent("web_search_001", message_bus)
        agents.append(agent)
        
        logger.info(f"✅ WebSearchAgent criado: {agent.agent_id}")
        logger.info(f"🔧 Capabilities: {', '.join(agent.capabilities)}")
        
    except Exception as e:
        logger.critical(f"❌ Erro ao criar WebSearchAgent: {e}", exc_info=True)
    
    return agents
