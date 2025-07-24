import logging
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import re
from multi_agent_network import BaseNetworkAgent, AgentType

logger = logging.getLogger(__name__)

class WebSearchAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['web_search', 'github_analysis', 'best_practices_discovery']
        self.status = 'active'
        self.search_history = []
        logger.info(f"✅ {self.agent_id} inicializado com capacidades de busca web")

    def search_better_code_patterns(self, current_code: str, language: str = "python") -> Dict:
        """Busca por padrões de código melhores na internet"""
        try:
            # Extrair palavras-chave do código atual
            keywords = self._extract_keywords_from_code(current_code)
            
            # Buscar no GitHub por implementações melhores
            github_results = self._search_github_repositories(keywords, language)
            
            # Buscar melhores práticas
            best_practices = self._search_best_practices(keywords, language)
            
            # Analisar bibliotecas modernas
            modern_libraries = self._search_modern_libraries(keywords, language)
            
            search_result = {
                "timestamp": datetime.now().isoformat(),
                "keywords": keywords,
                "github_results": github_results,
                "best_practices": best_practices,
                "modern_libraries": modern_libraries,
                "improvement_suggestions": self._generate_improvement_suggestions(
                    github_results, best_practices, modern_libraries
                )
            }
            
            self.search_history.append(search_result)
            logger.info(f"🔍 Busca concluída: {len(github_results)} repos, {len(best_practices)} práticas encontradas")
            
            return search_result
            
        except Exception as e:
            logger.error(f"❌ Erro na busca web: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def _extract_keywords_from_code(self, code: str) -> List[str]:
        """Extrai palavras-chave relevantes do código"""
        keywords = []
        
        # Extrair imports
        import_pattern = r'import\s+(\w+)|from\s+(\w+)\s+import'
        imports = re.findall(import_pattern, code)
        for imp in imports:
            keywords.extend([i for i in imp if i])
        
        # Extrair nomes de funções
        function_pattern = r'def\s+(\w+)'
        functions = re.findall(function_pattern, code)
        keywords.extend(functions)
        
        # Extrair nomes de classes
        class_pattern = r'class\s+(\w+)'
        classes = re.findall(class_pattern, code)
        keywords.extend(classes)
        
        # Filtrar palavras-chave relevantes
        relevant_keywords = [k for k in keywords if len(k) > 2 and k not in ['def', 'class', 'import', 'from']]
        
        return list(set(relevant_keywords))[:10]  # Limitar a 10 keywords

    def _search_github_repositories(self, keywords: List[str], language: str) -> List[Dict]:
        """Busca repositórios relevantes no GitHub"""
        try:
            results = []
            
            # Simular busca no GitHub (em produção, usaria GitHub API)
            search_queries = [
                f"{' '.join(keywords[:3])} {language} optimization",
                f"{keywords[0]} best practices {language}",
                f"efficient {keywords[0]} implementation"
            ]
            
            for query in search_queries:
                # Em produção, faria requisição real para GitHub API
                # Por agora, retorna dados simulados baseados na query
                mock_result = {
                    "repository": f"awesome-{keywords[0] if keywords else 'python'}-lib",
                    "description": f"High-performance {language} library for {keywords[0] if keywords else 'general'} operations",
                    "stars": 1500 + len(query) * 10,
                    "url": f"https://github.com/example/{keywords[0] if keywords else 'python'}-{language}",
                    "last_updated": "2024-01-15",
                    "relevance_score": 0.85,
                    "suggested_improvement": f"Consider using {keywords[0] if keywords else 'modern'} patterns from this repository"
                }
                results.append(mock_result)
            
            return results[:5]  # Limitar a 5 resultados
            
        except Exception as e:
            logger.error(f"❌ Erro buscando no GitHub: {e}")
            return []

    def _search_best_practices(self, keywords: List[str], language: str) -> List[Dict]:
        """Busca melhores práticas para as tecnologias identificadas"""
        try:
            practices = []
            
            # Práticas baseadas nas keywords encontradas
            for keyword in keywords[:3]:
                practice = {
                    "technology": keyword,
                    "practice": f"Use {keyword} with context managers for better resource management",
                    "example": f"# Better approach\nwith {keyword}_context() as ctx:\n    ctx.process_data()",
                    "benefit": "Improved memory management and error handling",
                    "source": f"Python Enhancement Proposal for {keyword}",
                    "confidence": 0.9
                }
                practices.append(practice)
            
            # Práticas gerais de Python
            general_practices = [
                {
                    "technology": "general",
                    "practice": "Use list comprehensions instead of loops when possible",
                    "example": "# Better: [x*2 for x in data]\n# Avoid: [append(x*2) for x in data]",
                    "benefit": "3x faster execution, more readable code",
                    "source": "Python Performance Best Practices",
                    "confidence": 0.95
                },
                {
                    "technology": "general", 
                    "practice": "Use f-strings for string formatting",
                    "example": 'f"Value: {value}" instead of "Value: {}".format(value)',
                    "benefit": "Faster and more readable than other formatting methods",
                    "source": "PEP 498 - Literal String Interpolation",
                    "confidence": 0.9
                }
            ]
            
            practices.extend(general_practices)
            return practices
            
        except Exception as e:
            logger.error(f"❌ Erro buscando melhores práticas: {e}")
            return []

    def _search_modern_libraries(self, keywords: List[str], language: str) -> List[Dict]:
        """Busca bibliotecas modernas que podem substituir as atuais"""
        try:
            libraries = []
            
            # Mapeamento de bibliotecas modernas
            modern_alternatives = {
                "requests": {
                    "alternative": "httpx",
                    "benefit": "Async support, HTTP/2, better performance",
                    "migration_effort": "low",
                    "compatibility": 0.9
                },
                "json": {
                    "alternative": "orjson", 
                    "benefit": "5x faster JSON parsing",
                    "migration_effort": "minimal",
                    "compatibility": 0.95
                },
                "datetime": {
                    "alternative": "pendulum",
                    "benefit": "Better timezone handling, more intuitive API",
                    "migration_effort": "medium", 
                    "compatibility": 0.8
                },
                "urllib": {
                    "alternative": "httpx",
                    "benefit": "Modern async API, better error handling",
                    "migration_effort": "medium",
                    "compatibility": 0.85
                }
            }
            
            # Verificar se alguma keyword tem alternativa moderna
            for keyword in keywords:
                if keyword.lower() in modern_alternatives:
                    alt = modern_alternatives[keyword.lower()]
                    library = {
                        "current": keyword,
                        "modern_alternative": alt["alternative"],
                        "improvement_reason": alt["benefit"],
                        "migration_complexity": alt["migration_effort"],
                        "compatibility_score": alt["compatibility"],
                        "recommendation": f"Consider upgrading {keyword} to {alt['alternative']}",
                        "priority": "high" if alt["compatibility"] > 0.9 else "medium"
                    }
                    libraries.append(library)
            
            return libraries
            
        except Exception as e:
            logger.error(f"❌ Erro buscando bibliotecas modernas: {e}")
            return []

    def _generate_improvement_suggestions(self, github_results: List, practices: List, libraries: List) -> List[Dict]:
        """Gera sugestões de melhoria baseadas nos resultados da busca"""
        suggestions = []
        
        # Sugestões baseadas no GitHub
        for repo in github_results[:2]:
            suggestion = {
                "type": "repository_pattern",
                "priority": "medium",
                "description": f"Implement patterns from {repo['repository']}",
                "expected_benefit": "Improved code organization and performance",
                "implementation_effort": "medium",
                "source": repo["url"]
            }
            suggestions.append(suggestion)
        
        # Sugestões baseadas em práticas
        for practice in practices[:3]:
            if practice["confidence"] > 0.8:
                suggestion = {
                    "type": "best_practice",
                    "priority": "high" if practice["confidence"] > 0.9 else "medium",
                    "description": practice["practice"],
                    "expected_benefit": practice["benefit"],
                    "implementation_effort": "low",
                    "source": practice["source"]
                }
                suggestions.append(suggestion)
        
        # Sugestões baseadas em bibliotecas
        for library in libraries:
            if library["compatibility_score"] > 0.8:
                suggestion = {
                    "type": "library_upgrade",
                    "priority": library["priority"],
                    "description": library["recommendation"],
                    "expected_benefit": library["improvement_reason"],
                    "implementation_effort": library["migration_complexity"],
                    "source": f"Modern alternative analysis"
                }
                suggestions.append(suggestion)
        
        return suggestions

    def get_search_history(self) -> List[Dict]:
        """Retorna histórico de buscas realizadas"""
        return self.search_history

    def generate_search_report(self) -> str:
        """Gera relatório das buscas realizadas"""
        if not self.search_history:
            return "📊 Nenhuma busca realizada ainda"
        
        report = f"📊 RELATÓRIO DE BUSCA WEB - {self.agent_id}\n"
        report += "=" * 60 + "\n\n"
        
        total_searches = len(self.search_history)
        total_suggestions = sum(len(search.get("improvement_suggestions", [])) for search in self.search_history)
        
        report += f"🔍 Total de buscas: {total_searches}\n"
        report += f"💡 Sugestões encontradas: {total_suggestions}\n\n"
        
        for i, search in enumerate(self.search_history[-3:], 1):  # Últimas 3 buscas
            report += f"🔍 BUSCA {i} - {search['timestamp'][:19]}:\n"
            report += f"   📋 Keywords: {', '.join(search['keywords'])}\n"
            report += f"   📚 Repositórios: {len(search.get('github_results', []))}\n"
            report += f"   ✅ Práticas: {len(search.get('best_practices', []))}\n"
            report += f"   📦 Bibliotecas: {len(search.get('modern_libraries', []))}\n"
            
            suggestions = search.get("improvement_suggestions", [])
            if suggestions:
                report += f"   💡 Principais sugestões:\n"
                for sugg in suggestions[:2]:
                    report += f"      - {sugg['description']} (Prioridade: {sugg['priority']})\n"
            
            report += "\n"
        
        return report

def create_web_search_agent(message_bus, num_instances=1) -> List['WebSearchAgent']:
    """Cria agente de busca web"""
    agents = []
    try:
        logger.info("🔍 Criando WebSearchAgent...")
        
        agent_id = "web_search_001"
        agent = WebSearchAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Registrar no MessageBus
        if hasattr(message_bus, 'register_agent'):
            message_bus.register_agent(agent_id, agent)
        
        agents.append(agent)
        logger.info(f"✅ {len(agents)} agente de busca web criado")
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando WebSearchAgent: {e}")
        return []
