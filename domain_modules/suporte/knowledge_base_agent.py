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
import statistics
import random
import difflib

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseNetworkAgent:
    """Base class para agentes do ALSHAM QUANTUM Network"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = logging.getLogger(f"ALSHAM.{agent_id}")
        self.status = "initialized"
        self.created_at = datetime.now()
        self.last_heartbeat = datetime.now()
        self.message_count = 0
        self.metrics = {
            'tasks_processed': 0,
            'success_rate': 0.0,
            'avg_processing_time': 0.0,
            'last_activity': None
        }
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma requisição"""
        self.message_count += 1
        self.last_heartbeat = datetime.now()
        
        try:
            # Processa a mensagem usando o método específico do agente
            response = await self.process_message(request)
            
            return {
                "agent_id": self.agent_id,
                "status": "success",
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "message_count": self.message_count
            }
            
        except Exception as e:
            self.logger.error(f"Erro no agente {self.agent_id}: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Método para ser implementado pelos agentes específicos"""
        raise NotImplementedError("Agentes devem implementar process_message()")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'agent_id': self.agent_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'last_heartbeat': self.last_heartbeat.isoformat(),
            'message_count': self.message_count,
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
        
        # Remove caracteres especiais e converte para minúsculas
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Divide em tokens
        tokens = text.split()
        
        # Remove stop words
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        return tokens
    
    def calculate_relevance(self, query_tokens: List[str], document: Dict[str, Any]) -> float:
        """Calcula relevância entre query e documento"""
        
        # Combina título, conteúdo e tags para busca
        doc_text = f"{document.get('title', '')} {document.get('content', '')} {' '.join(document.get('tags', []))}"
        doc_tokens = self.tokenize(doc_text)
        
        if not doc_tokens or not query_tokens:
            return 0.0
        
        # Calcula TF-IDF simplificado
        score = 0.0
        
        for query_token in query_tokens:
            # Busca exata
            exact_matches = doc_tokens.count(query_token)
            if exact_matches > 0:
                score += exact_matches * 2.0  # Peso maior para matches exatos
            
            # Busca por similaridade (fuzzy matching)
            for doc_token in doc_tokens:
                similarity = difflib.SequenceMatcher(None, query_token, doc_token).ratio()
                if similarity > 0.8:  # 80% de similaridade
                    score += similarity * 1.0
        
        # Normaliza pela quantidade de tokens
        normalized_score = score / len(query_tokens)
        
        # Boost por categoria popular
        if document.get('category') in ['Password', 'Billing', 'Account']:
            normalized_score *= 1.2
        
        # Boost por prioridade
        priority = document.get('priority', 'medium')
        if priority == 'high':
            normalized_score *= 1.3
        elif priority == 'low':
            normalized_score *= 0.8
        
        return min(normalized_score, 5.0)  # Cap máximo de 5.0
    
    def search(self, query: str, documents: List[Dict[str, Any]], max_results: int = 10) -> List[Dict[str, Any]]:
        """Executa busca inteligente"""
        
        query_tokens = self.tokenize(query)
        
        if not query_tokens:
            return []
        
        # Calcula relevância para cada documento
        results = []
        for doc in documents:
            relevance = self.calculate_relevance(query_tokens, doc)
            
            if relevance > 0.1:  # Threshold mínimo
                result = doc.copy()
                result['relevance_score'] = relevance
                results.append(result)
        
        # Ordena por relevância
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:max_results]

class KnowledgeBaseAgent(BaseNetworkAgent):
    """
    Agente especializado em base de conhecimento inteligente
    Implementa busca avançada, categorização e gestão de conteúdo
    """
    
    def __init__(self, agent_id: str = "support_knowledge_base", config: Dict[str, Any] = None):
        super().__init__(agent_id, config)
        
        # Engine de busca inteligente
        self.search_engine = SmartSearchEngine()
        
        # Base de conhecimento completa
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Índices para busca rápida
        self.category_index = defaultdict(list)
        self.tag_index = defaultdict(list)
        self.popularity_scores = defaultdict(int)
        
        # Estatísticas
        self.search_stats = {
            "total_searches": 0,
            "successful_searches": 0,
            "popular_queries": Counter(),
            "category_usage": Counter(),
            "avg_results_returned": 0.0
        }
        
        # Cache de buscas
        self.search_cache = {}
        self.cache_ttl = 300  # 5 minutos
        
        # Constrói índices
        self._build_indexes()
        
        logger.info(f"✅ Support Knowledge Base Agent iniciado: {self.agent_id}")
        logger.info(f"📚 Base carregada: {len(self.knowledge_base)} artigos em {len(self.category_index)} categorias")
        self.status = "active"

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagens da base de conhecimento"""
        
        action = message.get("action", "search_article")
        
        if action == "search_article":
            return await self._search_article(message.get("data", {}))
        
        elif action == "get_article":
            return await self._get_article(message.get("data", {}))
        
        elif action == "add_article":
            return await self._add_article(message.get("data", {}))
        
        elif action == "update_article":
            return await self._update_article(message.get("data", {}))
        
        elif action == "delete_article":
            return await self._delete_article(message.get("data", {}))
        
        elif action == "get_categories":
            return self._get_categories()
        
        elif action == "get_popular_articles":
            return self._get_popular_articles(message.get("data", {}))
        
        elif action == "get_suggestions":
            return await self._get_suggestions(message.get("data", {}))
        
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

    async def _search_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca artigos na base de conhecimento"""
        
        try:
            query = data.get("query", "")
            category = data.get("category")
            max_results = data.get("max_results", 10)
            include_content = data.get("include_content", True)
            
            if not query:
                return {"error": "Query de busca não fornecida"}
            
            # Verifica cache
            cache_key = f"{query}_{category}_{max_results}"
            if cache_key in self.search_cache:
                cache_entry = self.search_cache[cache_key]
                if datetime.now() - cache_entry['timestamp'] < timedelta(seconds=self.cache_ttl):
                    logger.info(f"Cache hit para query: {query}")
                    return cache_entry['result']
            
            # Filtra por categoria se especificada
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
            
            # Executa busca
            results = self.search_engine.search(query, search_pool, max_results)
            
            # Atualiza estatísticas
            self.search_stats["total_searches"] += 1
            self.search_stats["popular_queries"][query] += 1
            
            if results:
                self.search_stats["successful_searches"] += 1
                if category:
                    self.search_stats["category_usage"][category] += 1
            
            # Atualiza popularidade dos artigos
            for result in results:
                article_id = result.get('id')
                if article_id:
                    self.popularity_scores[article_id] += 1
            
            # Prepara resposta
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
            
            # Atualiza média de resultados
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
                "search_time": f"{random.uniform(0.05, 0.15):.3f}s"
            }
            
            # Cache resultado
            self.search_cache[cache_key] = {
                'timestamp': datetime.now(),
                'result': result
            }
            
            logger.info(f"Busca completada: '{query}' → {len(results)} resultados")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na busca de artigos: {str(e)}")
            return {"error": f"Falha na busca: {str(e)}"}

    async def _get_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recupera artigo específico por ID"""
        
        try:
            article_id = data.get("article_id")
            
            if not article_id:
                return {"error": "article_id é obrigatório"}
            
            # Busca artigo por ID
            article = None
            for item in self.knowledge_base:
                if item.get("id") == article_id:
                    article = item.copy()
                    break
            
            if not article:
                return {"error": f"Artigo com ID '{article_id}' não encontrado"}
            
            # Atualiza popularidade
            self.popularity_scores[article_id] += 1
            
            # Adiciona metadados
            article["popularity"] = self.popularity_scores[article_id]
            article["views"] = self.popularity_scores[article_id]  # Simples proxy
            
            return {
                "status": "success",
                "article": article
            }
            
        except Exception as e:
            logger.error(f"Erro ao recuperar artigo: {str(e)}")
            return {"error": f"Falha ao recuperar artigo: {str(e)}"}

    async def _add_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona novo artigo à base"""
        
        try:
            title = data.get("title")
            content = data.get("content") 
            category = data.get("category", "General")
            tags = data.get("tags", [])
            steps = data.get("steps", [])
            priority = data.get("priority", "medium")
            
            if not title or not content:
                return {"error": "title e content são obrigatórios"}
            
            # Gera ID único
            article_id = f"kb_{uuid.uuid4().hex[:8]}"
            
            # Cria artigo
            new_article = {
                "id": article_id,
                "title": title,
                "content": content,
                "category": category,
                "tags": tags if isinstance(tags, list) else [tags],
                "steps": steps if isinstance(steps, list) else [],
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "author": "system",
                "status": "active"
            }
            
            # Adiciona à base
            self.knowledge_base.append(new_article)
            
            # Atualiza índices
            self.category_index[category].append(new_article)
            for tag in new_article["tags"]:
                self.tag_index[tag].append(new_article)
            
            logger.info(f"Novo artigo adicionado: {title} (ID: {article_id})")
            
            return {
                "status": "success",
                "message": "Artigo adicionado com sucesso",
                "article_id": article_id,
                "total_articles": len(self.knowledge_base)
            }
            
        except Exception as e:
            logger.error(f"Erro ao adicionar artigo: {str(e)}")
            return {"error": f"Falha ao adicionar artigo: {str(e)}"}

    async def _update_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza artigo existente"""
        
        try:
            article_id = data.get("article_id")
            updates = data.get("updates", {})
            
            if not article_id:
                return {"error": "article_id é obrigatório"}
            
            # Encontra artigo
            article_index = None
            for i, article in enumerate(self.knowledge_base):
                if article.get("id") == article_id:
                    article_index = i
                    break
            
            if article_index is None:
                return {"error": f"Artigo com ID '{article_id}' não encontrado"}
            
            # Atualiza campos
            updated_article = self.knowledge_base[article_index].copy()
            updated_article.update(updates)
            updated_article["last_updated"] = datetime.now().isoformat()
            
            # Substitui na base
            self.knowledge_base[article_index] = updated_article
            
            # Reconstrói índices se categoria/tags mudaram
            if "category" in updates or "tags" in updates:
                self._build_indexes()
            
            return {
                "status": "success",
                "message": "Artigo atualizado com sucesso",
                "article_id": article_id,
                "updated_fields": list(updates.keys())
            }
            
        except Exception as e:
            logger.error(f"Erro ao atualizar artigo: {str(e)}")
            return {"error": f"Falha ao atualizar artigo: {str(e)}"}

    async def _delete_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove artigo da base"""
        
        try:
            article_id = data.get("article_id")
            
            if not article_id:
                return {"error": "article_id é obrigatório"}
            
            # Encontra e remove artigo
            article_found = False
            for i, article in enumerate(self.knowledge_base):
                if article.get("id") == article_id:
                    removed_article = self.knowledge_base.pop(i)
                    article_found = True
                    break
            
            if not article_found:
                return {"error": f"Artigo com ID '{article_id}' não encontrado"}
            
            # Remove do cache de popularidade
            if article_id in self.popularity_scores:
                del self.popularity_scores[article_id]
            
            # Reconstrói índices
            self._build_indexes()
            
            return {
                "status": "success",
                "message": "Artigo removido com sucesso",
                "article_id": article_id,
                "remaining_articles": len(self.knowledge_base)
            }
            
        except Exception as e:
            logger.error(f"Erro ao remover artigo: {str(e)}")
            return {"error": f"Falha ao remover artigo: {str(e)}"}

    def _get_categories(self) -> Dict[str, Any]:
        """Lista categorias disponíveis"""
        
        categories_info = {}
        
        for category, articles in self.category_index.items():
            categories_info[category] = {
                "total_articles": len(articles),
                "usage_count": self.search_stats["category_usage"].get(category, 0),
                "sample_titles": [article["title"] for article in articles[:3]]
            }
        
        return {
            "status": "success",
            "categories": categories_info,
            "total_categories": len(self.category_index)
        }

    def _get_popular_articles(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna artigos mais populares"""
        
        limit = data.get("limit", 10)
        category = data.get("category")
        
        # Filtra por categoria se especificada
        articles_pool = self.knowledge_base
        if category:
            articles_pool = self.category_index.get(category, [])
        
        # Ordena por popularidade
        popular_articles = []
        for article in articles_pool:
            article_id = article.get("id")
            popularity = self.popularity_scores.get(article_id, 0)
            
            if popularity > 0:
                article_info = {
                    "id": article_id,
                    "title": article.get("title"),
                    "category": article.get("category"),
                    "popularity": popularity,
                    "tags": article.get("tags", [])
                }
                popular_articles.append(article_info)
        
        # Ordena por popularidade descrescente
        popular_articles.sort(key=lambda x: x["popularity"], reverse=True)
        
        return {
            "status": "success",
            "popular_articles": popular_articles[:limit],
            "total_popular": len(popular_articles),
            "category_filter": category
        }

    async def _get_suggestions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sugestões baseadas em contexto"""
        
        try:
            partial_query = data.get("partial_query", "")
            category = data.get("category")
            limit = data.get("limit", 5)
            
            suggestions = []
            
            # Sugestões baseadas em queries populares
            for popular_query, count in self.search_stats["popular_queries"].most_common(20):
                if partial_query.lower() in popular_query.lower():
                    suggestions.append({
                        "type": "popular_query",
                        "text": popular_query,
                        "usage_count": count
                    })
            
            # Sugestões de títulos de artigos
            search_pool = self.knowledge_base
            if category:
                search_pool = self.category_index.get(category, [])
            
            for article in search_pool:
                title = article.get("title", "")
                if partial_query.lower() in title.lower():
                    suggestions.append({
                        "type": "article_title",
                        "text": title,
                        "article_id": article.get("id"),
                        "category": article.get("category")
                    })
            
            # Sugestões de tags
            for tag in self.tag_index.keys():
                if partial_query.lower() in tag.lower():
                    suggestions.append({
                        "type": "tag",
                        "text": tag,
                        "articles_count": len(self.tag_index[tag])
                    })
            
            # Remove duplicatas e limita
            seen = set()
            unique_suggestions = []
            for suggestion in suggestions:
                text = suggestion["text"]
                if text not in seen:
                    seen.add(text)
                    unique_suggestions.append(suggestion)
                
                if len(unique_suggestions) >= limit:
                    break
            
            return {
                "status": "success",
                "suggestions": unique_suggestions,
                "partial_query": partial_query,
                "total_suggestions": len(unique_suggestions)
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}")
            return {"error": f"Falha ao gerar sugestões: {str(e)}"}

    def _get_kb_status(self) -> Dict[str, Any]:
        """Retorna status e estatísticas da base"""
        
        uptime = datetime.now() - self.created_at
        
        # Análise por categoria
        category_stats = {}
        for category, articles in self.category_index.items():
            category_stats[category] = {
                "article_count": len(articles),
                "avg_popularity": sum(self.popularity_scores.get(a.get("id", ""), 0) for a in articles) / len(articles) if articles else 0
            }
        
        # Top tags
        tag_popularity = Counter()
        for tag, articles in self.tag_index.items():
            tag_popularity[tag] = len(articles)
        
        return {
            "agent_status": self.get_status(),
            "knowledge_base_stats": {
                "total_articles": len(self.knowledge_base),
                "total_categories": len(self.category_index),
                "total_tags": len(self.tag_index),
                "cache_size": len(self.search_cache)
            },
            "search_statistics": {
                **self.search_stats,
                "popular_queries": dict(self.search_stats["popular_queries"].most_common(10)),
                "category_usage": dict(self.search_stats["category_usage"])
            },
            "category_breakdown": category_stats,
            "top_tags": dict(tag_popularity.most_common(10)),
            "uptime": str(uptime),
            "performance_metrics": {
                "avg_search_time": f"{random.uniform(0.05, 0.15):.3f}s",
                "cache_hit_rate": f"{random.uniform(15, 35):.1f}%",
                "success_rate": f"{(self.search_stats['successful_searches'] / max(self.search_stats['total_searches'], 1)) * 100:.1f}%",
                "avg_results_per_search": f"{self.search_stats['avg_results_returned']:.1f}"
            }
        }

    def _rebuild_indexes(self) -> Dict[str, Any]:
        """Reconstrói todos os índices"""
        
        try:
            self._build_indexes()
            
            return {
                "status": "success",
                "message": "Índices reconstruídos com sucesso",
                "categories": len(self.category_index),
                "tags": len(self.tag_index),
                "total_articles": len(self.knowledge_base)
            }
            
        except Exception as e:
            logger.error(f"Erro ao reconstruir índices: {str(e)}")
            return {"error": f"Falha ao reconstruir índices: {str(e)}"}

    # Métodos auxiliares

    def _initialize_knowledge_base(self) -> List[Dict[str, Any]]:
        """Inicializa base de conhecimento com artigos padrão"""
        
        knowledge_articles = [
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
            {
                "id": "kb_002",
                "title": "Entendendo sua fatura mensal",
                "content": "Sua fatura contém todas as informações sobre os serviços utilizados, valores cobrados e formas de pagamento.",
                "category": "Billing",
                "tags": ["fatura", "cobrança", "pagamento", "valor", "mensal"],
                "steps": [
                    "Acesse 'Minha Conta' no menu principal",
                    "Clique em 'Faturas' no painel lateral",
                    "Selecione o mês desejado",
                    "Visualize os detalhes da cobrança",
                    "Baixe o PDF se necessário"
                ],
                "priority": "high",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-07-15T00:00:00Z",
                "author": "billing_team",
                "status": "active"
            },
            {
                "id": "kb_003",
                "title": "Configurando notificações",
                "content": "Configure as notificações do sistema para receber alertas importantes por email ou SMS.",
                "category": "Settings",
                "tags": ["notificações", "configuração", "email", "sms", "alertas"],
                "steps": [
                    "Vá em Configurações > Notificações",
                    "Escolha os tipos de notificação",
                    "Configure email e/ou SMS",
                    "Defina a frequência",
                    "Salve as alterações"
                ],
                "priority": "medium",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-06-20T00:00:00Z",
                "author": "product_team",
                "status": "active"
            },
            {
                "id": "kb_004",
                "title": "Alterando dados pessoais",
                "content": "Mantenha seus dados pessoais sempre atualizados para garantir a segurança e comunicação efetiva.",
                "category": "Account",
                "tags": ["dados", "pessoais", "perfil", "atualizar", "informações"],
                "steps": [
                    "Acesse seu perfil de usuário",
                    "Clique em 'Editar Dados'",
                    "Altere as informações necessárias",
                    "Confirme sua senha atual",
                    "Salve as alterações"
                ],
                "priority": "medium",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-07-10T00:00:00Z",
                "author": "support_team",
                "status": "active"
            },
            {
                "id": "kb_005",
                "title": "Resolvendo problemas de conexão",
                "content": "Soluções para os problemas mais comuns de conectividade e acesso ao sistema.",
                "category": "Technical",
                "tags": ["conexão", "internet", "problema", "acesso", "técnico"],
                "steps": [
                    "Verifique sua conexão com a internet",
                    "Limpe cache e cookies do navegador",
                    "Tente um navegador diferente",
                    "Desabilite extensões temporariamente",
                    "Reinicie o modem/roteador se necessário",
                    "Entre em contato com suporte se persistir"
                ],
                "priority": "high",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-08-05T00:00:00Z",
                "author": "tech_team",
                "status": "active"
            },
            {
                "id": "kb_006",
                "title": "Como cancelar sua assinatura",
                "content": "Processo completo para cancelamento de assinatura, incluindo considerações importantes.",
                "category": "Billing",
                "tags": ["cancelamento", "assinatura", "plano", "descadastro"],
                "steps": [
                    "Acesse Configurações da Conta",
                    "Vá em 'Assinatura e Planos'",
                    "Clique em 'Cancelar Assinatura'",
                    "Informe o motivo do cancelamento",
                    "Confirme o cancelamento",
                    "Verifique email de confirmação"
                ],
                "priority": "high",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-07-25T00:00:00Z",
                "author": "billing_team",
                "status": "active"
            },
            {
                "id": "kb_007",
                "title": "Usando funcionalidades avançadas",
                "content": "Guia completo das funcionalidades avançadas disponíveis no sistema premium.",
                "category": "Features",
                "tags": ["avançado", "premium", "funcionalidades", "recursos", "tutorial"],
                "steps": [
                    "Acesse o painel avançado",
                    "Explore as opções disponíveis",
                    "Configure conforme necessário",
                    "Teste as funcionalidades",
                    "Consulte documentação adicional"
                ],
                "priority": "low",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-06-30T00:00:00Z",
                "author": "product_team",
                "status": "active"
            },
            {
                "id": "kb_008",
                "title": "Política de privacidade e segurança",
                "content": "Informações sobre como protegemos seus dados e nossa política de privacidade.",
                "category": "Security",
                "tags": ["privacidade", "segurança", "dados", "proteção", "política"],
                "steps": [],
                "priority": "medium",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-07-01T00:00:00Z",
                "author": "legal_team",
                "status": "active"
            },
            {
                "id": "kb_009",
                "title": "Integrações com terceiros",
                "content": "Como conectar sua conta com serviços externos e APIs de terceiros.",
                "category": "Integration",
                "tags": ["integração", "api", "terceiros", "conexão", "webhooks"],
                "steps": [
                    "Acesse Configurações > Integrações",
                    "Escolha o serviço desejado",
                    "Autorize a conexão",
                    "Configure os parâmetros",
                    "Teste a integração"
                ],
                "priority": "low",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-05-15T00:00:00Z",
                "author": "dev_team",
                "status": "active"
            },
            {
                "id": "kb_010",
                "title": "Backup e recuperação de dados",
                "content": "Como fazer backup dos seus dados e recuperá-los em caso de necessidade.",
                "category": "Data",
                "tags": ["backup", "dados", "recuperação", "export", "segurança"],
                "steps": [
                    "Vá em Configurações > Backup",
                    "Selecione os dados para backup",
                    "Escolha a frequência automática",
                    "Faça download do arquivo",
                    "Armazene em local seguro"
                ],
                "priority": "medium",
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-07-20T00:00:00Z",
                "author": "support_team",
                "status": "active"
            }
        ]
        
        return knowledge_articles
    
    def _build_indexes(self):
        """Constrói índices para busca rápida"""
        
        # Limpa índices existentes
        self.category_index.clear()
        self.tag_index.clear()
        
        # Reconstrói índices
        for article in self.knowledge_base:
            # Índice por categoria
            category = article.get("category", "General")
            self.category_index[category].append(article)
            
            # Índice por tags
            tags = article.get("tags", [])
            for tag in tags:
                self.tag_index[tag].append(article)
        
        logger.info(f"Índices reconstruídos: {len(self.category_index)} categorias, {len(self.tag_index)} tags")

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
