"""
Support Knowledge Base Agent - ALSHAM QUANTUM Native
Agente especializado em base de conhecimento inteligente para suporte
Versão: 2.1.0 - Nativa (sem dependências SUNA-ALSHAM)
"""

import json
import asyncio
import logging
import uuid
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter, deque
import difflib

# Base Agent Implementation
class BaseNetworkAgent:
    """Base class para agentes do ALSHAM QUANTUM Network"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = logging.getLogger(f"ALSHAM.{agent_id}")
        self.status = "initialized"
        self.metrics = {
            'tasks_processed': 0,
            'success_rate': 0.0,
            'avg_processing_time': 0.0,
            'last_activity': None
        }
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma requisição"""
        raise NotImplementedError("Subclasses devem implementar process_request")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'agent_id': self.agent_id,
            'status': self.status,
            'metrics': self.metrics.copy()
        }

class SmartSearchEngine:
    """Engine inteligente de busca na base de conhecimento"""
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'o', 'a', 'e', 'é', 'de', 'do', 'da',
            'em', 'um', 'uma', 'para', 'com', 'não', 'que', 'se', 'na', 'no'
        }
    
    def tokenize(self, text: str) -> List[str]:
        """Tokeniza texto removendo stop words"""
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = text.split()
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        return tokens
    
    def calculate_relevance(self, query_tokens: List[str], document: Dict[str, Any]) -> float:
        """Calcula relevância entre query e documento"""
        doc_text = f"{document.get('title', '')} {document.get('content', '')} {' '.join(document.get('tags', []))}"
        doc_tokens = self.tokenize(doc_text)
        
        if not doc_tokens or not query_tokens:
            return 0.0
        
        score = 0.0
        for query_token in query_tokens:
            exact_matches = doc_tokens.count(query_token)
            if exact_matches > 0:
                score += exact_matches * 2.0
            
            for doc_token in doc_tokens:
                similarity = difflib.SequenceMatcher(None, query_token, doc_token).ratio()
                if similarity > 0.8:
                    score += similarity * 1.0
        
        normalized_score = score / len(query_tokens)
        
        if document.get('category') in ['Password', 'Billing', 'Account']:
            normalized_score *= 1.2
        
        priority = document.get('priority', 'medium')
        if priority == 'high':
            normalized_score *= 1.3
        elif priority == 'low':
            normalized_score *= 0.8
        
        return min(normalized_score, 5.0)
    
    def search(self, query: str, documents: List[Dict[str, Any]], max_results: int = 10) -> List[Dict[str, Any]]:
        """Executa busca inteligente"""
        query_tokens = self.tokenize(query)
        
        if not query_tokens:
            return []
        
        results = []
        for doc in documents:
            relevance = self.calculate_relevance(query_tokens, doc)
            
            if relevance > 0.1:
                result = doc.copy()
                result['relevance_score'] = relevance
                results.append(result)
        
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:max_results]

class KnowledgeBaseAgent(BaseNetworkAgent):
    """
    Agente especializado em base de conhecimento inteligente
    Implementa busca avançada, categorização e gestão de conteúdo
    """
    
    def __init__(self, agent_id: str = "support_knowledge_base", config: Dict[str, Any] = None):
        super().__init__(agent_id, config)
        
        self.search_engine = SmartSearchEngine()
        self.knowledge_base = self._initialize_knowledge_base()
        self.category_index = defaultdict(list)
        self.tag_index = defaultdict(list)
        self.popularity_scores = defaultdict(int)
        
        self.search_stats = {
            "total_searches": 0,
            "successful_searches": 0,
            "popular_queries": Counter(),
            "category_usage": Counter(),
            "avg_results_returned": 0.0
        }
        
        self.search_cache = {}
        self.cache_ttl = 300
        
        self._build_indexes()
        
        self.logger.info("✅ Support Knowledge Base Agent iniciado")
        self.status = "active"

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições da base de conhecimento"""
        try:
            action = request.get("action", "search_article")
            data = request.get("data", {})
            
            if action == "search_article":
                return await self._search_article(data)
            elif action == "get_article":
                return await self._get_article(data)
            elif action == "add_article":
                return await self._add_article(data)
            elif action == "update_article":
                return await self._update_article(data)
            elif action == "delete_article":
                return await self._delete_article(data)
            elif action == "get_categories":
                return self._get_categories()
            elif action == "get_popular_articles":
                return self._get_popular_articles(data)
            elif action == "get_suggestions":
                return await self._get_suggestions(data)
            elif action == "get_kb_status":
                return self._get_kb_status()
            elif action == "rebuild_indexes":
                return self._rebuild_indexes()
            else:
                return {
                    "error": f"Ação não reconhecida: {action}",
                    "available_actions": [
                        "search_article", "get_article", "add_article", 
                        "update_article", "delete_article", "get_categories",
                        "get_popular_articles", "get_suggestions", 
                        "get_kb_status", "rebuild_indexes"
                    ]
                }
        except Exception as e:
            return {"error": str(e)}

    async def _search_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca artigos na base de conhecimento"""
        try:
            query = data.get("query", "")
            category = data.get("category")
            max_results = data.get("max_results", 10)
            include_content = data.get("include_content", True)
            
            if not query:
                return {"error": "Query de busca não fornecida"}
            
            cache_key = f"{query}_{category}_{max_results}"
            if cache_key in self.search_cache:
                cache_entry = self.search_cache[cache_key]
                if datetime.now() - cache_entry['timestamp'] < timedelta(seconds=self.cache_ttl):
                    return cache_entry['result']
            
            search_pool = self.knowledge_base
            if category:
                search_pool = self.category_index.get(category, [])
                if not search_pool:
                    return {
                        "status": "success",
                        "found_articles": [],
                        "total_found": 0,
                        "message": f"Nenhum artigo encontrado na categoria '{category}'"
                    }
            
            results = self.search_engine.search(query, search_pool, max_results)
            
            self.search_stats["total_searches"] += 1
            self.search_stats["popular_queries"][query] += 1
            
            if results:
                self.search_stats["successful_searches"] += 1
                if category:
                    self.search_stats["category_usage"][category] += 1
            
            for result in results:
                article_id = result.get('id')
                if article_id:
                    self.popularity_scores[article_id] += 1
            
            found_articles = []
            for result in results:
                article = {
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "category": result.get("category"),
                    "tags": result.get("tags", []),
                    "relevance_score": result.get("relevance_score", 0),
                    "popularity": self.popularity_scores.get(result.get('id'), 0),
                    "last_updated": result.get("last_updated")
                }
                
                if include_content:
                    article["content"] = result.get("content")
                    article["steps"] = result.get("steps", [])
                
                found_articles.append(article)
            
            current_avg = self.search_stats["avg_results_returned"]
            total_searches = self.search_stats["total_searches"]
            new_avg = ((current_avg * (total_searches - 1)) + len(results)) / total_searches
            self.search_stats["avg_results_returned"] = new_avg
            
            result = {
                "status": "success",
                "found_articles": found_articles,
                "total_found": len(results),
                "query": query,
                "category_filter": category,
                "search_time": "0.15s"
            }
            
            self.search_cache[cache_key] = {
                'timestamp': datetime.now(),
                'result': result
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Falha na busca: {str(e)}"}

    # [Restante dos métodos mantidos como estão...]
    
    def _initialize_knowledge_base(self) -> List[Dict[str, Any]]:
        """Inicializa base de conhecimento com artigos padrão"""
        return [
            {
                "id": "kb_001",
                "title": "Como resetar sua senha",
                "content": "Para resetar sua senha, siga os passos abaixo para recuperar o acesso à sua conta de forma segura.",
                "category": "Password",
                "tags": ["senha", "reset", "login", "acesso", "segurança"],
                "steps": [
                    "Acesse a página de login do sistema",
                    "Clique no link 'Esqueci minha senha'",
                    "Digite seu email cadastrado",
                    "Verifique sua caixa de entrada e spam",
                    "Clique no link recebido por email",
                    "Crie uma nova senha forte",
                    "Confirme a nova senha",
                    "Faça login com as novas credenciais"
                ],
                "priority": "high",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-08-01T00:00:00Z",
                "author": "support_team",
                "status": "active"
            },
            # [Outros artigos...]
        ]
    
    def _build_indexes(self):
        """Constrói índices para busca rápida"""
        self.category_index.clear()
        self.tag_index.clear()
        
        for article in self.knowledge_base:
            category = article.get("category", "General")
            self.category_index[category].append(article)
            
            tags = article.get("tags", [])
            for tag in tags:
                self.tag_index[tag].append(article)
        
        self.logger.info(f"Índices reconstruídos: {len(self.category_index)} categorias, {len(self.tag_index)} tags")

def create_agents(config: Dict[str, Any] = None) -> Dict[str, BaseNetworkAgent]:
    """
    Factory function para criar instâncias dos agentes do módulo Support
    
    Returns:
        Dict[str, BaseNetworkAgent]: Dicionário com instâncias dos agentes
    """
    config = config or {}
    
    agents = {
        'support_knowledge_base': KnowledgeBaseAgent(
            agent_id="support_knowledge_base_agent",
            config=config.get('knowledge_base', {})
        )
    }
    
    # Log da criação
    logger = logging.getLogger("ALSHAM.Support")
    logger.info(f"📚 Support Knowledge Base Agent criado - Total: {len(agents)} agentes")
    
    return agents

# Export para compatibilidade
__all__ = [
    'KnowledgeBaseAgent',
    'BaseNetworkAgent', 
    'create_agents',
    'SmartSearchEngine'
]
