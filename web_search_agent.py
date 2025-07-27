import logging
import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from urllib.parse import quote_plus
from collections import defaultdict
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class SearchType(Enum):
    """Tipos de busca"""
    CODE_SOLUTION = "code_solution"
    BEST_PRACTICES = "best_practices"
    SECURITY_FIX = "security_fix"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    LIBRARY_UPDATE = "library_update"
    DOCUMENTATION = "documentation"
    TUTORIAL = "tutorial"
    TECHNOLOGY_TRENDS = "technology_trends"

class SourceType(Enum):
    """Tipos de fontes de busca"""
    GITHUB = "github"
    STACKOVERFLOW = "stackoverflow"
    DOCUMENTATION = "documentation"
    PYPI = "pypi"
    SECURITY_DB = "security_db"
    TECH_BLOGS = "tech_blogs"
    FORUMS = "forums"

@dataclass
class SearchResult:
    """Resultado de busca"""
    result_id: str
    source: SourceType
    title: str
    url: str
    description: str
    relevance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    code_snippets: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Solution:
    """Solução encontrada para um problema"""
    solution_id: str
    problem_description: str
    search_results: List[SearchResult]
    recommended_action: str
    implementation_steps: List[str]
    confidence_score: float
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TechnologyTrend:
    """Tendência tecnológica identificada"""
    trend_id: str
    technology: str
    description: str
    adoption_rate: float
    relevance_to_project: float
    sources: List[str]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

class WebSearchAgent(BaseNetworkAgent):
    """Agente especializado em buscar soluções e melhorias na web"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'web_search',
            'technology_trends',
            'solution_finding',
            'library_research',
            'security_advisories',
            'best_practices_search',
            'documentation_lookup',
            'code_examples_search'
        ]
        self.status = 'active'
        
        # Estado do agente
        self.search_queue = asyncio.Queue()
        self.search_history = []
        self.solutions_cache = {}  # Cache de soluções
        self.api_keys = self._load_api_keys()
        
        # Configurações
        self.max_results_per_source = 10
        self.cache_duration = timedelta(hours=24)
        self.search_timeout = 30  # segundos
        self.min_relevance_score = 0.6
        
        # Estatísticas
        self.search_metrics = {
            'searches_performed': 0,
            'solutions_found': 0,
            'api_calls_made': 0,
            'cache_hits': 0,
            'average_relevance': 0.0
        }
        
        # Padrões de busca otimizados
        self.search_patterns = self._load_search_patterns()
        
        # Tasks de background
        self._search_task = None
        self._trend_monitoring_task = None
        
        logger.info(f"🌐 {self.agent_id} inicializado com busca web avançada")
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Carrega chaves de API (simulado)"""
        return {
            'github': 'github_api_key',
            'stackoverflow': 'stackoverflow_key',
            # Adicionar outras APIs conforme necessário
        }
    
    def _load_search_patterns(self) -> Dict[str, List[str]]:
        """Carrega padrões de busca otimizados"""
        return {
            'python_error': [
                '{error_type} python solution',
                'fix {error_type} python',
                'python {error_type} best practice'
            ],
            'security_vulnerability': [
                '{vulnerability} security fix',
                '{vulnerability} CVE patch',
                'secure alternative {vulnerability}'
            ],
            'performance': [
                'optimize {code_pattern} python',
                'python {code_pattern} performance',
                'faster alternative {code_pattern}'
            ],
            'best_practice': [
                '{topic} python best practices',
                '{topic} design patterns python',
                'pythonic way {topic}'
            ]
        }
    
    async def start_search_service(self):
        """Inicia serviço de busca"""
        if not self._search_task:
            self._search_task = asyncio.create_task(self._search_loop())
            self._trend_monitoring_task = asyncio.create_task(self._trend_monitoring_loop())
            logger.info(f"🔍 {self.agent_id} iniciou serviço de busca")
    
    async def stop_search_service(self):
        """Para serviço de busca"""
        if self._search_task:
            self._search_task.cancel()
            self._search_task = None
        if self._trend_monitoring_task:
            self._trend_monitoring_task.cancel()
            self._trend_monitoring_task = None
        logger.info(f"🛑 {self.agent_id} parou serviço de busca")
    
    async def _search_loop(self):
        """Loop principal de busca"""
        while True:
            try:
                if not self.search_queue.empty():
                    search_request = await self.search_queue.get()
                    await self._process_search_request(search_request)
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de busca: {e}")
    
    async def _trend_monitoring_loop(self):
        """Loop de monitoramento de tendências"""
        while True:
            try:
                # Buscar tendências tecnológicas
                trends = await self._search_technology_trends()
                
                if trends:
                    await self._process_trends(trends)
                
                await asyncio.sleep(3600)  # Verificar a cada hora
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro monitorando tendências: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'search_solutions':
                result = await self.search_solutions(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'find_best_practices':
                result = await self.find_best_practices(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'search_security_fixes':
                result = await self.search_security_fixes(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'search_performance_tips':
                result = await self.search_performance_optimizations(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'check_library_updates':
                result = await self.check_library_updates(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_trends':
                result = await self.get_technology_trends()
                await self._send_response(message, result)
    
    async def search_solutions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca soluções para problemas de código"""
        try:
            problems = request_data.get('problems', [])
            context = request_data.get('context', '')
            
            logger.info(f"🔍 Buscando soluções para {len(problems)} problemas")
            
            solutions = []
            
            for problem in problems:
                # Verificar cache
                cache_key = self._generate_cache_key(problem)
                if cache_key in self.solutions_cache:
                    cached = self.solutions_cache[cache_key]
                    if datetime.now() - cached['timestamp'] < self.cache_duration:
                        solutions.append(cached['solution'])
                        self.search_metrics['cache_hits'] += 1
                        continue
                
                # Buscar nova solução
                solution = await self._find_solution_for_problem(problem, context)
                solutions.append(solution)
                
                # Cachear resultado
                self.solutions_cache[cache_key] = {
                    'solution': solution,
                    'timestamp': datetime.now()
                }
            
            self.search_metrics['solutions_found'] += len(solutions)
            
            return {
                'status': 'completed',
                'solutions': [self._solution_to_dict(s) for s in solutions],
                'total_found': len(solutions),
                'search_quality': self._calculate_search_quality(solutions)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro buscando soluções: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _find_solution_for_problem(self, problem: Dict[str, Any], context: str) -> Solution:
        """Encontra solução para um problema específico"""
        problem_desc = problem.get('problem', str(problem))
        problem_type = problem.get('type', 'general')
        
        # Determinar tipo de busca
        search_type = self._determine_search_type(problem_type)
        
        # Gerar queries de busca
        search_queries = self._generate_search_queries(problem_desc, search_type)
        
        # Executar buscas em paralelo
        search_tasks = []
        for query in search_queries[:3]:  # Limitar a 3 queries
            search_tasks.extend([
                self._search_github(query),
                self._search_stackoverflow(query),
                self._search_documentation(query)
            ])
        
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Filtrar e rankear resultados
        valid_results = []
        for result in results:
            if isinstance(result, list):
                valid_results.extend(result)
        
        ranked_results = self._rank_search_results(valid_results, problem_desc)
        
        # Gerar solução
        solution = self._generate_solution(problem_desc, ranked_results[:5])
        
        return solution
    
    def _determine_search_type(self, problem_type: str) -> SearchType:
        """Determina tipo de busca baseado no problema"""
        type_mapping = {
            'syntax_error': SearchType.CODE_SOLUTION,
            'security': SearchType.SECURITY_FIX,
            'performance': SearchType.PERFORMANCE_OPTIMIZATION,
            'style': SearchType.BEST_PRACTICES,
            'complexity': SearchType.BEST_PRACTICES,
            'deprecated': SearchType.LIBRARY_UPDATE
        }
        
        return type_mapping.get(problem_type, SearchType.CODE_SOLUTION)
    
    def _generate_search_queries(self, problem: str, search_type: SearchType) -> List[str]:
        """Gera queries de busca otimizadas"""
        queries = []
        
        # Extrair palavras-chave
        keywords = self._extract_keywords(problem)
        
        # Usar padrões de busca
        if search_type == SearchType.CODE_SOLUTION:
            queries.append(f"python {problem} solution")
            queries.append(f"fix {keywords[0]} python")
        elif search_type == SearchType.SECURITY_FIX:
            queries.append(f"{problem} security vulnerability fix")
            queries.append(f"python secure {keywords[0]}")
        elif search_type == SearchType.PERFORMANCE_OPTIMIZATION:
            queries.append(f"optimize {problem} python")
            queries.append(f"python performance {keywords[0]}")
        elif search_type == SearchType.BEST_PRACTICES:
            queries.append(f"python best practices {keywords[0]}")
            queries.append(f"{problem} pythonic way")
        
        return queries
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave do texto"""
        # Remover palavras comuns
        stopwords = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were', 'in', 'to'}
        
        # Tokenizar e filtrar
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        
        # Priorizar termos técnicos
        tech_terms = [w for w in keywords if w in {
            'error', 'exception', 'function', 'class', 'module', 'loop',
            'performance', 'security', 'async', 'api', 'database', 'cache'
        }]
        
        return tech_terms[:3] if tech_terms else keywords[:3]
    
    async def _search_github(self, query: str) -> List[SearchResult]:
        """Busca no GitHub"""
        try:
            encoded_query = quote_plus(query)
            url = f"https://api.github.com/search/code?q={encoded_query}+language:python"
            
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'SUNA-ALSHAM-Agent'
            }
            
            if self.api_keys.get('github'):
                headers['Authorization'] = f"token {self.api_keys['github']}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        
                        for item in data.get('items', [])[:self.max_results_per_source]:
                            result = SearchResult(
                                result_id=f"gh_{item['sha'][:8]}",
                                source=SourceType.GITHUB,
                                title=item['name'],
                                url=item['html_url'],
                                description=f"Repository: {item['repository']['full_name']}",
                                relevance_score=self._calculate_relevance(query, item['name']),
                                metadata={
                                    'repository': item['repository']['full_name'],
                                    'path': item['path'],
                                    'score': item.get('score', 0)
                                },
                                tags=['github', 'code']
                            )
                            results.append(result)
                        
                        self.search_metrics['api_calls_made'] += 1
                        return results
                    else:
                        logger.warning(f"GitHub API returned {response.status}")
                        return []
                        
        except asyncio.TimeoutError:
            logger.error("GitHub search timeout")
            return []
        except Exception as e:
            logger.error(f"Erro buscando no GitHub: {e}")
            return []
    
    async def _search_stackoverflow(self, query: str) -> List[SearchResult]:
        """Busca no Stack Overflow"""
        try:
            encoded_query = quote_plus(query)
            url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={encoded_query}&tagged=python&site=stackoverflow"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        
                        for item in data.get('items', [])[:self.max_results_per_source]:
                            result = SearchResult(
                                result_id=f"so_{item['question_id']}",
                                source=SourceType.STACKOVERFLOW,
                                title=item['title'],
                                url=item['link'],
                                description=self._clean_html(item.get('body', '')[:200]),
                                relevance_score=self._calculate_relevance(query, item['title']),
                                metadata={
                                    'score': item.get('score', 0),
                                    'answer_count': item.get('answer_count', 0),
                                    'is_answered': item.get('is_answered', False),
                                    'view_count': item.get('view_count', 0)
                                },
                                tags=item.get('tags', [])
                            )
                            results.append(result)
                        
                        self.search_metrics['api_calls_made'] += 1
                        return results
                    else:
                        logger.warning(f"StackOverflow API returned {response.status}")
                        return []
                        
        except asyncio.TimeoutError:
            logger.error("StackOverflow search timeout")
            return []
        except Exception as e:
            logger.error(f"Erro buscando no StackOverflow: {e}")
            return []
    
    async def _search_documentation(self, query: str) -> List[SearchResult]:
        """Busca em documentação Python"""
        try:
            # Simular busca em docs.python.org e outras documentações
            # Em produção, usar API real ou web scraping
            
            results = []
            
            # Busca simulada
            if any(keyword in query.lower() for keyword in ['async', 'asyncio', 'await']):
                result = SearchResult(
                    result_id="doc_asyncio",
                    source=SourceType.DOCUMENTATION,
                    title="Python asyncio Documentation",
                    url="https://docs.python.org/3/library/asyncio.html",
                    description="Asynchronous I/O documentation",
                    relevance_score=0.9,
                    metadata={'official': True},
                    tags=['asyncio', 'async', 'documentation']
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Erro buscando documentação: {e}")
            return []
    
    def _calculate_relevance(self, query: str, title: str) -> float:
        """Calcula relevância do resultado"""
        query_words = set(query.lower().split())
        title_words = set(title.lower().split())
        
        # Interseção de palavras
        common_words = query_words & title_words
        
        if not query_words:
            return 0.0
        
        relevance = len(common_words) / len(query_words)
        
        # Boost para correspondências exatas
        if query.lower() in title.lower():
            relevance += 0.3
        
        return min(1.0, relevance)
    
    def _rank_search_results(self, results: List[SearchResult], problem: str) -> List[SearchResult]:
        """Rankeia resultados por relevância"""
        # Calcular score composto
        for result in results:
            # Relevância base
            score = result.relevance_score
            
            # Boost por fonte
            if result.source == SourceType.DOCUMENTATION:
                score *= 1.2
            elif result.source == SourceType.STACKOVERFLOW:
                # Boost por respostas aceitas
                if result.metadata.get('is_answered'):
                    score *= 1.1
            
            # Boost por popularidade
            if result.source == SourceType.GITHUB:
                repo_score = result.metadata.get('score', 0)
                score += min(0.2, repo_score / 100)
            
            result.relevance_score = min(1.0, score)
        
        # Ordenar por relevância
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Filtrar por relevância mínima
        filtered = [r for r in results if r.relevance_score >= self.min_relevance_score]
        
        return filtered
    
    def _generate_solution(self, problem: str, search_results: List[SearchResult]) -> Solution:
        """Gera solução baseada nos resultados"""
        if not search_results:
            return Solution(
                solution_id=f"sol_{len(self.search_history)}",
                problem_description=problem,
                search_results=[],
                recommended_action="Nenhuma solução encontrada. Considere reformular o problema.",
                implementation_steps=["Revisar o código", "Consultar documentação oficial"],
                confidence_score=0.1
            )
        
        # Analisar resultados
        best_result = search_results[0]
        
        # Gerar passos de implementação baseados nos resultados
        implementation_steps = []
        
        if best_result.source == SourceType.GITHUB:
            implementation_steps.extend([
                f"Examinar código em: {best_result.url}",
                "Adaptar solução ao seu contexto",
                "Testar implementação"
            ])
        elif best_result.source == SourceType.STACKOVERFLOW:
            implementation_steps.extend([
                f"Revisar resposta em: {best_result.url}",
                "Verificar se aplica ao seu caso",
                "Implementar com adaptações necessárias"
            ])
        elif best_result.source == SourceType.DOCUMENTATION:
            implementation_steps.extend([
                f"Estudar documentação: {best_result.url}",
                "Seguir exemplos oficiais",
                "Implementar seguindo boas práticas"
            ])
        
        # Extrair alternativas
        alternatives = []
        for result in search_results[1:3]:
            alternatives.append({
                'title': result.title,
                'url': result.url,
                'relevance': result.relevance_score
            })
        
        # Calcular confiança
        confidence = sum(r.relevance_score for r in search_results[:3]) / min(3, len(search_results))
        
        solution = Solution(
            solution_id=f"sol_{len(self.search_history)}",
            problem_description=problem,
            search_results=search_results,
            recommended_action=f"Implementar solução baseada em: {best_result.title}",
            implementation_steps=implementation_steps,
            confidence_score=confidence,
            alternatives=alternatives,
            warnings=self._generate_warnings(search_results)
        )
        
        self.search_history.append(solution)
        return solution
    
    def _generate_warnings(self, results: List[SearchResult]) -> List[str]:
        """Gera avisos baseados nos resultados"""
        warnings = []
        
        # Verificar idade dos resultados
        old_results = [r for r in results if self._is_outdated(r)]
        if old_results:
            warnings.append("Alguns resultados podem estar desatualizados")
        
        # Verificar confiabilidade baixa
        low_confidence = [r for r in results if r.relevance_score < 0.7]
        if len(low_confidence) > len(results) / 2:
            warnings.append("Resultados têm relevância moderada - verificar cuidadosamente")
        
        return warnings
    
    def _is_outdated(self, result: SearchResult) -> bool:
        """Verifica se resultado está desatualizado"""
        # Implementar lógica real baseada em metadados
        return False
    
    async def find_best_practices(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca melhores práticas"""
        try:
            topic = request_data.get('topic', '')
            context = request_data.get('context', '')
            
            logger.info(f"🔍 Buscando best practices para: {topic}")
            
            # Gerar queries específicas
            queries = [
                f"python {topic} best practices",
                f"{topic} design patterns python",
                f"pythonic {topic}",
                f"{topic} anti-patterns to avoid"
            ]
            
            all_results = []
            for query in queries:
                results = await asyncio.gather(
                    self._search_github(query),
                    self._search_stackoverflow(query),
                    self._search_documentation(query)
                )
                
                for result_list in results:
                    if isinstance(result_list, list):
                        all_results.extend(result_list)
            
            # Rankear e filtrar
            ranked = self._rank_search_results(all_results, topic)
            
            # Agrupar por tipo de prática
            practices = self._group_best_practices(ranked)
            
            return {
                'status': 'completed',
                'topic': topic,
                'best_practices': practices,
                'sources': len(set(r.source for r in ranked)),
                'confidence': self._calculate_practice_confidence(ranked)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro buscando best practices: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _group_best_practices(self, results: List[SearchResult]) -> Dict[str, List[Dict]]:
        """Agrupa práticas por categoria"""
        practices = {
            'recommended': [],
            'avoid': [],
            'patterns': [],
            'examples': []
        }
        
        for result in results[:10]:
            practice = {
                'title': result.title,
                'url': result.url,
                'description': result.description,
                'source': result.source.value
            }
            
            # Categorizar baseado no título/conteúdo
            title_lower = result.title.lower()
            if any(word in title_lower for word in ['best', 'good', 'recommended']):
                practices['recommended'].append(practice)
            elif any(word in title_lower for word in ['avoid', 'anti', 'bad', 'don\'t']):
                practices['avoid'].append(practice)
            elif any(word in title_lower for word in ['pattern', 'design', 'architecture']):
                practices['patterns'].append(practice)
            else:
                practices['examples'].append(practice)
        
        return practices
    
    async def search_security_fixes(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca correções de segurança"""
        try:
            vulnerabilities = request_data.get('vulnerabilities', [])
            
            logger.info(f"🔍 Buscando fixes de segurança para {len(vulnerabilities)} vulnerabilidades")
            
            fixes = []
            
            for vulnerability in vulnerabilities:
                vuln_type = vulnerability.get('type', '')
                description = vulnerability.get('description', '')
                
                # Buscar em bases de segurança
                security_results = await self._search_security_databases(vuln_type, description)
                
                # Buscar fixes gerais
                general_results = await asyncio.gather(
                    self._search_github(f"{vuln_type} security fix python"),
                    self._search_stackoverflow(f"fix {vuln_type} vulnerability python")
                )
                
                all_results = security_results
                for result_list in general_results:
                    if isinstance(result_list, list):
                        all_results.extend(result_list)
                
                # Gerar fix
                fix = self._generate_security_fix(vulnerability, all_results)
                fixes.append(fix)
            
            return {
                'status': 'completed',
                'security_fixes': fixes,
                'total_fixes': len(fixes),
                'urgent_count': sum(1 for f in fixes if f.get('urgency') == 'critical')
            }
            
        except Exception as e:
            logger.error(f"❌ Erro buscando security fixes: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _search_security_databases(self, vuln_type: str, description: str) -> List[SearchResult]:
        """Busca em bases de dados de segurança"""
        results = []
        
        # Simular busca em CVE, OWASP, etc.
        # Em produção, usar APIs reais
        
        if 'sql' in vuln_type.lower():
            result = SearchResult(
                result_id="sec_sql_injection",
                source=SourceType.SECURITY_DB,
                title="SQL Injection Prevention - OWASP",
                url="https://owasp.org/www-community/attacks/SQL_Injection",
                description="Comprehensive guide to preventing SQL injection",
                relevance_score=0.95,
                metadata={'severity': 'critical', 'cve': 'Multiple'},
                tags=['security', 'sql-injection', 'owasp']
            )
            results.append(result)
        
        return results
    
    def _generate_security_fix(self, vulnerability: Dict, results: List[SearchResult]) -> Dict[str, Any]:
        """Gera correção de segurança"""
        if not results:
            return {
                'vulnerability': vulnerability.get('type'),
                'fix_available': False,
                'recommendation': 'Consultar especialista em segurança',
                'urgency': 'high'
            }
        
        best_result = max(results, key=lambda x: x.relevance_score)
        
        fix = {
            'vulnerability': vulnerability.get('type'),
            'fix_available': True,
            'primary_source': {
                'title': best_result.title,
                'url': best_result.url,
                'confidence': best_result.relevance_score
            },
            'implementation_steps': [
                'Validar todos os inputs',
                'Usar prepared statements ou ORM',
                'Implementar princípio do menor privilégio',
                'Adicionar logging de segurança'
            ],
            'urgency': self._determine_urgency(vulnerability),
            'additional_resources': [
                {'title': r.title, 'url': r.url}
                for r in results[1:4]
            ]
        }
        
        return fix
    
    def _determine_urgency(self, vulnerability: Dict) -> str:
        """Determina urgência da correção"""
        severity = vulnerability.get('severity', '').lower()
        
        if severity in ['critical', 'high']:
            return 'critical'
        elif severity == 'medium':
            return 'high'
        else:
            return 'medium'
    
    async def search_performance_optimizations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca otimizações de performance"""
        try:
            performance_issues = request_data.get('issues', [])
            
            logger.info(f"🔍 Buscando otimizações para {len(performance_issues)} issues")
            
            optimizations = []
            
            for issue in performance_issues:
                issue_type = issue.get('type', '')
                description = issue.get('description', '')
                
                # Buscar otimizações
                queries = [
                    f"python optimize {issue_type}",
                    f"python {issue_type} performance improvement",
                    f"faster {issue_type} python"
                ]
                
                all_results = []
                for query in queries:
                    results = await self._search_github(query)
                    all_results.extend(results)
                
                # Gerar otimização
                optimization = self._generate_optimization(issue, all_results)
                optimizations.append(optimization)
            
            return {
                'status': 'completed',
                'optimizations': optimizations,
                'estimated_improvement': self._estimate_improvement(optimizations)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro buscando otimizações: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_optimization(self, issue: Dict, results: List[SearchResult]) -> Dict[str, Any]:
        """Gera sugestão de otimização"""
        optimization = {
            'issue': issue.get('description'),
            'suggestions': [],
            'expected_impact': 'medium',
            'implementation_difficulty': 'medium'
        }
        
        if results:
            for result in results[:3]:
                optimization['suggestions'].append({
                    'title': result.title,
                    'url': result.url,
                    'relevance': result.relevance_score
                })
        else:
            optimization['suggestions'].append({
                'title': 'Considere usar profiling tools',
                'description': 'Use cProfile ou line_profiler para identificar gargalos'
            })
        
        return optimization
    
    async def check_library_updates(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica atualizações de bibliotecas"""
        try:
            libraries = request_data.get('libraries', [])
            
            logger.info(f"🔍 Verificando updates para {len(libraries)} bibliotecas")
            
            updates = []
            
            for library in libraries:
                name = library.get('name', '')
                current_version = library.get('version', '')
                
                # Buscar informações no PyPI
                update_info = await self._check_pypi_updates(name, current_version)
                updates.append(update_info)
            
            return {
                'status': 'completed',
                'updates': updates,
                'updates_available': sum(1 for u in updates if u.get('update_available'))
            }
            
        except Exception as e:
            logger.error(f"❌ Erro verificando updates: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _check_pypi_updates(self, library_name: str, current_version: str) -> Dict[str, Any]:
        """Verifica atualizações no PyPI"""
        try:
            url = f"https://pypi.org/pypi/{library_name}/json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        latest_version = data['info']['version']
                        
                        return {
                            'library': library_name,
                            'current_version': current_version,
                            'latest_version': latest_version,
                            'update_available': current_version != latest_version,
                            'release_date': data['releases'].get(latest_version, [{}])[0].get('upload_time', ''),
                            'homepage': data['info'].get('home_page', ''),
                            'changelog_url': data['info'].get('release_url', '')
                        }
                    else:
                        return {
                            'library': library_name,
                            'error': f'PyPI returned {response.status}'
                        }
                        
        except Exception as e:
            logger.error(f"Erro verificando {library_name}: {e}")
            return {
                'library': library_name,
                'error': str(e)
            }
    
    async def _search_technology_trends(self) -> List[TechnologyTrend]:
        """Busca tendências tecnológicas"""
        trends = []
        
        # Queries para tendências
        trend_queries = [
            "python trends 2024",
            "emerging python libraries",
            "python best practices 2024",
            "new python features"
        ]
        
        for query in trend_queries:
            results = await self._search_github(query)
            
            # Analisar resultados para extrair tendências
            for result in results[:3]:
                trend = TechnologyTrend(
                    trend_id=f"trend_{len(trends)}",
                    technology=self._extract_technology_name(result.title),
                    description=result.description,
                    adoption_rate=0.5,  # Seria calculado com mais dados
                    relevance_to_project=0.7,
                    sources=[result.url],
                    recommendations=["Avaliar aplicabilidade ao projeto"]
                )
                trends.append(trend)
        
        return trends
    
    def _extract_technology_name(self, title: str) -> str:
        """Extrai nome da tecnologia do título"""
        # Implementar extração mais sofisticada
        words = title.split()
        tech_keywords = ['framework', 'library', 'tool', 'api', 'service']
        
        for i, word in enumerate(words):
            if word.lower() in tech_keywords and i > 0:
                return words[i-1]
        
        return words[0] if words else "Unknown"
    
    async def _process_trends(self, trends: List[TechnologyTrend]):
        """Processa tendências identificadas"""
        if not trends:
            return
        
        # Notificar sobre tendências relevantes
        relevant_trends = [t for t in trends if t.relevance_to_project > 0.7]
        
        if relevant_trends:
            notification = AgentMessage(
                id=str(uuid4()),
                sender_id=self.agent_id,
                recipient_id="orchestrator_001",
                message_type=MessageType.NOTIFICATION,
                priority=Priority.LOW,
                content={
                    'notification_type': 'technology_trends',
                    'trends': [
                        {
                            'technology': t.technology,
                            'description': t.description,
                            'relevance': t.relevance_to_project
                        }
                        for t in relevant_trends
                    ]
                },
                timestamp=datetime.now()
            )
            await self.message_bus.publish(notification)
    
    async def get_technology_trends(self) -> Dict[str, Any]:
        """Retorna tendências tecnológicas atuais"""
        try:
            trends = await self._search_technology_trends()
            
            return {
                'status': 'completed',
                'trends': [
                    {
                        'technology': t.technology,
                        'description': t.description,
                        'adoption_rate': t.adoption_rate,
                        'relevance': t.relevance_to_project,
                        'sources': t.sources
                    }
                    for t in trends
                ],
                'total_trends': len(trends)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo trends: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_cache_key(self, problem: Any) -> str:
        """Gera chave de cache para problema"""
        if isinstance(problem, dict):
            key_parts = [str(problem.get('type', '')), str(problem.get('problem', ''))]
        else:
            key_parts = [str(problem)]
        
        return ":".join(key_parts)
    
    def _calculate_search_quality(self, solutions: List[Solution]) -> float:
        """Calcula qualidade geral da busca"""
        if not solutions:
            return 0.0
        
        total_confidence = sum(s.confidence_score for s in solutions)
        avg_confidence = total_confidence / len(solutions)
        
        # Atualizar métrica
        self.search_metrics['average_relevance'] = (
            self.search_metrics['average_relevance'] * 0.9 + avg_confidence * 0.1
        )
        
        return avg_confidence
    
    def _solution_to_dict(self, solution: Solution) -> Dict[str, Any]:
        """Converte solução para dicionário"""
        return {
            'solution_id': solution.solution_id,
            'problem': solution.problem_description,
            'recommended_action': solution.recommended_action,
            'implementation_steps': solution.implementation_steps,
            'confidence': solution.confidence_score,
            'search_results': [
                {
                    'title': r.title,
                    'url': r.url,
                    'source': r.source.value,
                    'relevance': r.relevance_score
                }
                for r in solution.search_results[:3]
            ],
            'alternatives': solution.alternatives,
            'warnings': solution.warnings
        }
    
    def _clean_html(self, text: str) -> str:
        """Remove tags HTML do texto"""
        # Implementação simples - usar BeautifulSoup em produção
        clean = re.sub('<.*?>', '', text)
        return clean.strip()
    
    def _estimate_improvement(self, optimizations: List[Dict]) -> str:
        """Estima melhoria potencial"""
        if not optimizations:
            return "0%"
        
        # Análise simplificada
        high_impact = sum(1 for o in optimizations if o.get('expected_impact') == 'high')
        medium_impact = sum(1 for o in optimizations if o.get('expected_impact') == 'medium')
        
        estimated = high_impact * 20 + medium_impact * 10
        
        return f"{min(estimated, 50)}%"
    
    async def _process_search_request(self, request: Dict[str, Any]):
        """Processa requisição de busca da fila"""
        request_type = request.get('type')
        
        if request_type == 'solution_search':
            await self.search_solutions(request)
    
    def _calculate_practice_confidence(self, results: List[SearchResult]) -> float:
        """Calcula confiança nas práticas encontradas"""
        if not results:
            return 0.0
        
        # Considerar fonte e relevância
        doc_results = [r for r in results if r.source == SourceType.DOCUMENTATION]
        so_results = [r for r in results if r.source == SourceType.STACKOVERFLOW]
        
        confidence = 0.5  # Base
        
        if doc_results:
            confidence += 0.3  # Documentação oficial
        
        if len(so_results) > 3:
            confidence += 0.2  # Múltiplas soluções validadas
        
        return min(1.0, confidence)
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

# Importações necessárias
from uuid import uuid4

def create_web_search_agent(message_bus, num_instances=1) -> List[WebSearchAgent]:
    """
    Cria agente de busca web
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de busca web
    """
    agents = []
    
    try:
        logger.info("🌐 Criando WebSearchAgent para autoevolução...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "web_search_001"
        
        if agent_id not in existing_agents:
            try:
                agent = WebSearchAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de busca
                asyncio.create_task(agent.start_search_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com busca web avançada")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de busca web criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando WebSearchAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
