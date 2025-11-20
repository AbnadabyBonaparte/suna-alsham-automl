"""
ALSHAM QUANTUM - Engagement Maximizer Agent (Social Media Module)
Versão Nativa - Sem dependências SUNA-ALSHAM
Corrigido em: 07/08/2025

Agente especializado em:
- Maximização de engajamento em redes sociais
- Análise de sentimento de comentários
- Respostas automáticas inteligentes
- Estratégias de growth hacking
- Monitoramento de métricas de engajamento
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import statistics
from collections import defaultdict, Counter

class BaseNetworkAgent:
    """Classe base nativa para agentes da rede ALSHAM QUANTUM"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.active = True
        self.logger = logging.getLogger(f"alsham_quantum.{agent_id}")
        
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Método base para processamento - deve ser sobrescrito"""
        raise NotImplementedError
        
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "active": self.active,
            "timestamp": datetime.now().isoformat()
        }

class SentimentType(Enum):
    """Tipos de sentimento detectados"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    QUESTION = "question"
    COMPLAINT = "complaint"
    PRAISE = "praise"
    SUGGESTION = "suggestion"
    SPAM = "spam"

class EngagementAction(Enum):
    """Ações de engajamento disponíveis"""
    LIKE = "like"
    REPLY = "reply"
    SHARE = "share"
    FOLLOW = "follow"
    SAVE = "save"
    TAG_USERS = "tag_users"
    CREATE_STORY = "create_story"
    DIRECT_MESSAGE = "direct_message"

class Platform(Enum):
    """Plataformas de mídia social"""
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"

class EngagementStrategy(Enum):
    """Estratégias de engajamento"""
    REACTIVE = "reactive"          # Responder a comentários
    PROACTIVE = "proactive"        # Iniciar conversas
    COMMUNITY_BUILDING = "community_building"
    INFLUENCER_OUTREACH = "influencer_outreach"
    USER_GENERATED_CONTENT = "user_generated_content"

@dataclass
class Comment:
    """Estrutura de comentário"""
    comment_id: str
    post_id: str
    user_id: str
    username: str
    text: str
    timestamp: datetime
    likes: int
    replies: int
    platform: Platform
    sentiment: Optional[SentimentType] = None
    engagement_score: float = 0.0

@dataclass
class EngagementInsight:
    """Insights de engajamento"""
    insight_id: str
    post_id: str
    platform: Platform
    total_comments: int
    sentiment_distribution: Dict[str, int]
    top_keywords: List[str]
    engagement_rate: float
    response_rate: float
    best_performing_replies: List[str]
    recommendations: List[str]

@dataclass
class AutomatedReply:
    """Resposta automatizada"""
    reply_id: str
    original_comment_id: str
    reply_text: str
    strategy: str
    confidence_score: float
    personalization_level: str
    expected_engagement_boost: float

@dataclass
class EngagementCampaign:
    """Campanha de engajamento"""
    campaign_id: str
    name: str
    platform: Platform
    strategy: EngagementStrategy
    target_metrics: Dict[str, float]
    duration_days: int
    actions: List[Dict[str, Any]]
    expected_results: Dict[str, float]

class EngagementMaximizerAgent(BaseNetworkAgent):
    """Agente Maximizador de Engajamento nativo do ALSHAM QUANTUM"""
    
    def __init__(self):
        super().__init__("engagement_maximizer_agent", "Engagement Maximizer Agent")
        
        # Base de conhecimento para análise de sentimento
        self.sentiment_keywords = {
            SentimentType.POSITIVE: [
                "ótimo", "incrível", "amei", "perfeito", "excelente", "fantástico",
                "maravilhoso", "adorei", "sucesso", "parabéns", "top", "show"
            ],
            SentimentType.NEGATIVE: [
                "ruim", "péssimo", "horrível", "decepcionante", "pior", "odeio",
                "terrível", "lixo", "fracasso", "não gostei", "problema"
            ],
            SentimentType.QUESTION: [
                "como", "quando", "onde", "por que", "qual", "quem", "?",
                "me ajuda", "dúvida", "não entendi", "explica"
            ],
            SentimentType.COMPLAINT: [
                "reclamação", "problema", "bug", "erro", "não funciona",
                "demora", "lento", "difícil", "complicado", "insatisfeito"
            ],
            SentimentType.PRAISE: [
                "parabéns", "sucesso", "inspirador", "motivador", "exemplo",
                "referência", "melhor", "líder", "inovador"
            ]
        }
        
        # Templates de respostas por tipo de sentimento
        self.reply_templates = {
            SentimentType.POSITIVE: [
                "Ficamos muito felizes que você gostou! 😊",
                "Obrigado pelo feedback positivo! 🙏",
                "Que bom que você aprovou! ✨",
                "Seu apoio significa muito para nós! ❤️"
            ],
            SentimentType.NEGATIVE: [
                "Sentimos muito pela experiência negativa. Como podemos melhorar?",
                "Obrigado pelo feedback. Vamos trabalhar para melhorar! 💪",
                "Sua opinião é importante. Nos envie uma DM para conversarmos melhor.",
                "Agradecemos a sinceridade. Estamos sempre evoluindo!"
            ],
            SentimentType.QUESTION: [
                "Ótima pergunta! Te enviamos mais informações na DM 📩",
                "Que pergunta interessante! Vamos te ajudar 🤝",
                "Adoramos curiosidade! Te respondemos em detalhes na DM",
                "Excelente dúvida! Preparamos uma resposta especial para você"
            ],
            SentimentType.COMPLAINT: [
                "Obrigado por nos alertar. Vamos investigar e resolver! 🔍",
                "Sentimos muito pelo inconveniente. Nossa equipe vai analisar.",
                "Sua reclamação é válida. Como podemos resolver juntos?",
                "Agradecemos o feedback. Nos mande uma DM para resolvermos!"
            ]
        }
        
        # Configurações por plataforma
        self.platform_configs = {
            Platform.INSTAGRAM: {
                "max_reply_length": 2200,
                "optimal_reply_length": 150,
                "best_engagement_times": ["11:00", "15:00", "20:00"],
                "emoji_usage": "high",
                "hashtag_in_reply": True
            },
            Platform.FACEBOOK: {
                "max_reply_length": 8000,
                "optimal_reply_length": 200,
                "best_engagement_times": ["13:00", "15:00", "19:00"],
                "emoji_usage": "medium",
                "hashtag_in_reply": False
            },
            Platform.TWITTER: {
                "max_reply_length": 280,
                "optimal_reply_length": 100,
                "best_engagement_times": ["12:00", "15:00", "17:00"],
                "emoji_usage": "medium",
                "hashtag_in_reply": True
            },
            Platform.LINKEDIN: {
                "max_reply_length": 3000,
                "optimal_reply_length": 300,
                "best_engagement_times": ["08:00", "12:00", "17:00"],
                "emoji_usage": "low",
                "hashtag_in_reply": False
            }
        }
        
        # Estratégias de growth hacking
        self.growth_strategies = {
            "viral_triggers": [
                "Marque 3 amigos que precisam ver isso!",
                "Compartilhe se você concorda!",
                "Salve este post para consultar depois!",
                "Qual sua opinião sobre isso?"
            ],
            "community_builders": [
                "Vamos criar uma comunidade sobre isso!",
                "Quem mais tem interesse neste assunto?",
                "Adoraria conhecer sua experiência!",
                "Vamos trocar ideias sobre isso!"
            ],
            "value_adds": [
                "Te enviamos material complementar na DM!",
                "Quer saber mais? Confira nosso guia completo!",
                "Preparamos conteúdo exclusivo sobre isso!",
                "Tem mais dicas como essa no nosso perfil!"
            ]
        }
        
        # Cache de análises
        self.engagement_cache = {}
        self.reply_history = defaultdict(list)
        
        # Métricas de performance
        self.performance_metrics = {
            "total_interactions": 0,
            "automated_replies": 0,
            "sentiment_analyzed": 0,
            "engagement_boost": 0.0,
            "response_rate": 0.0
        }
        
        self.logger.info("Engagement Maximizer Agent inicializado com engine nativo")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de engajamento"""
        try:
            action = data.get("action", "analyze_and_engage_comment")
            
            if action == "analyze_and_engage_comment":
                return await self._analyze_and_engage_comment(data)
            elif action == "analyze_post_engagement":
                return await self._analyze_post_engagement(data)
            elif action == "generate_reply":
                return await self._generate_automated_reply(data)
            elif action == "create_engagement_strategy":
                return await self._create_engagement_strategy(data)
            elif action == "monitor_sentiment":
                return await self._monitor_sentiment_trends(data)
            elif action == "optimize_timing":
                return await self._optimize_engagement_timing(data)
            elif action == "growth_hack_campaign":
                return await self._create_growth_hack_campaign(data)
            elif action == "competitor_engagement_analysis":
                return await self._analyze_competitor_engagement(data)
            elif action == "engagement_metrics":
                return await self._calculate_engagement_metrics(data)
            else:
                return {"error": f"Ação não reconhecida: {action}"}
                
        except Exception as e:
            self.logger.error(f"Erro na maximização de engajamento: {str(e)}")
            return {"error": str(e)}

    async def _analyze_and_engage_comment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa comentário e executa ação de engajamento"""
        
        # Extrair dados do comentário
        comment = self._build_comment_object(data)
        
        # Análise de sentimento
        sentiment_analysis = await self._analyze_comment_sentiment(comment)
        comment.sentiment = sentiment_analysis["sentiment"]
        comment.engagement_score = sentiment_analysis["engagement_score"]
        
        # Determinar ação apropriada
        recommended_action = await self._determine_engagement_action(comment, sentiment_analysis)
        
        # Executar ação se apropriado
        action_result = await self._execute_engagement_action(comment, recommended_action)
        
        # Gerar resposta automática se necessário
        automated_reply = None
        if recommended_action["action"] == EngagementAction.REPLY:
            automated_reply = await self._generate_contextual_reply(comment, sentiment_analysis)
        
        # Atualizar métricas
        self.performance_metrics["total_interactions"] += 1
        self.performance_metrics["sentiment_analyzed"] += 1
        if automated_reply:
            self.performance_metrics["automated_replies"] += 1
        
        # Salvar no cache
        engagement_id = str(uuid.uuid4())
        self.engagement_cache[engagement_id] = {
            "comment": asdict(comment),
            "sentiment_analysis": sentiment_analysis,
            "recommended_action": recommended_action,
            "action_result": action_result,
            "automated_reply": asdict(automated_reply) if automated_reply else None,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "engagement_id": engagement_id,
            "comment_id": comment.comment_id,
            "sentiment_detected": sentiment_analysis["sentiment"].value,
            "confidence_score": sentiment_analysis["confidence"],
            "engagement_score": comment.engagement_score,
            "recommended_action": {
                "action": recommended_action["action"].value,
                "priority": recommended_action["priority"],
                "reasoning": recommended_action["reasoning"]
            },
            "action_executed": action_result["executed"],
            "action_details": action_result["details"],
            "automated_reply": {
                "reply_text": automated_reply.reply_text,
                "strategy": automated_reply.strategy,
                "confidence": automated_reply.confidence_score
            } if automated_reply else None,
            "engagement_insights": {
                "user_engagement_history": self._get_user_engagement_history(comment.user_id),
                "trending_topics": sentiment_analysis.get("keywords", []),
                "platform_optimization": self._get_platform_optimization_tips(comment.platform)
            },
            "timestamp": datetime.now().isoformat()
        }

    async def _analyze_comment_sentiment(self, comment: Comment) -> Dict[str, Any]:
        """Analisa sentimento do comentário usando NLP nativo"""
        
        text_lower = comment.text.lower()
        sentiment_scores = {}
        
        # Calcular scores para cada tipo de sentimento
        for sentiment_type, keywords in self.sentiment_keywords.items():
            score = 0
            for keyword in keywords:
                score += text_lower.count(keyword.lower())
            sentiment_scores[sentiment_type] = score
        
        # Determinar sentimento dominante
        dominant_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        max_score = sentiment_scores[dominant_sentiment]
        
        # Se nenhuma palavra-chave foi encontrada, analisar estrutura
        if max_score == 0:
            if "?" in comment.text:
                dominant_sentiment = SentimentType.QUESTION
                max_score = 1
            elif len([word for word in text_lower.split() if len(word) > 6]) > 3:
                dominant_sentiment = SentimentType.NEUTRAL
                max_score = 0.5
            else:
                dominant_sentiment = SentimentType.NEUTRAL
                max_score = 0.1
        
        # Calcular confiança
        total_score = sum(sentiment_scores.values()) or 1
        confidence = max_score / total_score
        
        # Calcular engagement score
        engagement_factors = {
            "length": min(len(comment.text.split()) / 20, 1.0),  # Comentários mais longos = maior engajamento
            "emojis": len(re.findall(r'[😀-🿿]', comment.text)) * 0.1,
            "questions": comment.text.count('?') * 0.15,
            "mentions": comment.text.count('@') * 0.2,
            "caps": len(re.findall(r'[A-Z]{2,}', comment.text)) * 0.05
        }
        
        engagement_score = min(sum(engagement_factors.values()), 1.0)
        
        # Extrair palavras-chave
        words = [word for word in text_lower.split() if len(word) > 3]
        word_freq = Counter(words)
        keywords = [word for word, freq in word_freq.most_common(5)]
        
        return {
            "sentiment": dominant_sentiment,
            "confidence": confidence,
            "sentiment_scores": {k.value: v for k, v in sentiment_scores.items()},
            "engagement_score": engagement_score,
            "keywords": keywords,
            "analysis_details": {
                "word_count": len(comment.text.split()),
                "emoji_count": len(re.findall(r'[😀-🿿]', comment.text)),
                "question_marks": comment.text.count('?'),
                "mentions": comment.text.count('@'),
                "all_caps_words": len(re.findall(r'[A-Z]{2,}', comment.text))
            }
        }

    async def _determine_engagement_action(self, comment: Comment, sentiment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Determina a melhor ação de engajamento"""
        
        sentiment = sentiment_analysis["sentiment"]
        confidence = sentiment_analysis["confidence"]
        engagement_score = sentiment_analysis["engagement_score"]
        
        # Lógica de decisão baseada em sentimento
        if sentiment == SentimentType.POSITIVE:
            if engagement_score > 0.7:
                action = EngagementAction.REPLY
                priority = "high"
                reasoning = "Comentário muito positivo com alto engajamento - responder para amplificar"
            else:
                action = EngagementAction.LIKE
                priority = "medium"
                reasoning = "Comentário positivo - curtir para reconhecimento"
                
        elif sentiment == SentimentType.NEGATIVE:
            if "problema" in comment.text.lower() or "bug" in comment.text.lower():
                action = EngagementAction.REPLY
                priority = "high"
                reasoning = "Comentário negativo com problema técnico - resposta necessária"
            else:
                action = EngagementAction.REPLY
                priority = "medium"
                reasoning = "Comentário negativo - responder para melhorar relacionamento"
                
        elif sentiment == SentimentType.QUESTION:
            action = EngagementAction.REPLY
            priority = "high"
            reasoning = "Pergunta detectada - resposta esperada pela audiência"
            
        elif sentiment == SentimentType.COMPLAINT:
            action = EngagementAction.REPLY
            priority = "critical"
            reasoning = "Reclamação detectada - resposta urgente necessária"
            
        elif sentiment == SentimentType.PRAISE:
            action = EngagementAction.REPLY
            priority = "medium"
            reasoning = "Elogio recebido - responder para fortalecer relacionamento"
            
        else:  # NEUTRAL
            if engagement_score > 0.5:
                action = EngagementAction.LIKE
                priority = "low"
                reasoning = "Comentário neutro com algum engajamento - curtir"
            else:
                action = EngagementAction.LIKE
                priority = "low"
                reasoning = "Comentário neutro - curtir para mostrar presença"
        
        # Ajustes baseados na plataforma
        platform_config = self.platform_configs.get(comment.platform, {})
        
        # Ajustes baseados no histórico do usuário
        user_history = self._get_user_engagement_history(comment.user_id)
        if user_history.get("frequent_commenter", False):
            if priority == "low":
                priority = "medium"
            reasoning += " (usuário frequente)"
        
        return {
            "action": action,
            "priority": priority,
            "reasoning": reasoning,
            "confidence": confidence,
            "platform_considerations": platform_config,
            "estimated_impact": self._estimate_action_impact(action, sentiment, engagement_score)
        }

    async def _execute_engagement_action(self, comment: Comment, recommended_action: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a ação de engajamento (simulado)"""
        
        action = recommended_action["action"]
        
        # Simulação de execução
        await asyncio.sleep(0.1)  # Simular latência
        
        if action == EngagementAction.LIKE:
            result = {
                "executed": True,
                "details": f"Comentário {comment.comment_id} curtido",
                "api_call": f"like_comment({comment.comment_id})",
                "timestamp": datetime.now().isoformat()
            }
        elif action == EngagementAction.REPLY:
            result = {
                "executed": True,
                "details": f"Resposta será gerada para comentário {comment.comment_id}",
                "api_call": f"reply_to_comment({comment.comment_id})",
                "timestamp": datetime.now().isoformat()
            }
        else:
            result = {
                "executed": False,
                "details": f"Ação {action.value} não implementada ainda",
                "reason": "Funcionalidade em desenvolvimento"
            }
        
        # Atualizar métricas
        if result["executed"]:
            self.performance_metrics["engagement_boost"] += recommended_action.get("estimated_impact", 0.1)
        
        return result

    async def _generate_contextual_reply(self, comment: Comment, sentiment_analysis: Dict[str, Any]) -> AutomatedReply:
        """Gera resposta automática contextual"""
        
        sentiment = sentiment_analysis["sentiment"]
        keywords = sentiment_analysis["keywords"]
        
        # Selecionar template base
        templates = self.reply_templates.get(sentiment, ["Obrigado pelo comentário!"])
        base_template = templates[hash(comment.comment_id) % len(templates)]
        
        # Personalização baseada no contexto
        reply_text = base_template
        personalization_level = "basic"
        
        # Adicionar personalização avançada
        if comment.username and len(comment.username) > 0:
            if not any(word in base_template for word in ["@", comment.username]):
                reply_text = f"Oi {comment.username}! {reply_text}"
                personalization_level = "medium"
        
        # Adicionar contexto baseado em palavras-chave
        if keywords:
            context_additions = {
                "preço": "Te enviamos informações sobre preços na DM! 💰",
                "produto": "Quer saber mais detalhes? Confira nosso catálogo! 📦",
                "entrega": "Informações sobre entrega disponíveis no nosso site! 🚚",
                "dúvida": "Ficamos felizes em esclarecer qualquer dúvida! 💡"
            }
            
            for keyword in keywords:
                if keyword in context_additions:
                    reply_text += f" {context_additions[keyword]}"
                    personalization_level = "high"
                    break
        
        # Ajustar para plataforma
        platform_config = self.platform_configs.get(comment.platform, {})
        
        if platform_config.get("emoji_usage") == "high" and "😊" not in reply_text:
            reply_text += " 😊"
        
        if platform_config.get("hashtag_in_reply") and comment.platform in [Platform.INSTAGRAM, Platform.TWITTER]:
            if len(reply_text) < platform_config.get("optimal_reply_length", 150):
                reply_text += " #alshamquantum"
        
        # Truncar se necessário
        max_length = platform_config.get("max_reply_length", 2000)
        if len(reply_text) > max_length:
            reply_text = reply_text[:max_length-3] + "..."
        
        # Calcular confidence score
        confidence_factors = {
            "sentiment_confidence": sentiment_analysis["confidence"],
            "template_match": 0.8 if sentiment != SentimentType.NEUTRAL else 0.5,
            "personalization": {"basic": 0.6, "medium": 0.8, "high": 1.0}[personalization_level],
            "keyword_relevance": len(keywords) * 0.1
        }
        
        confidence_score = min(sum(confidence_factors.values()) / len(confidence_factors), 1.0)
        
        # Determinar estratégia
        if sentiment in [SentimentType.QUESTION, SentimentType.COMPLAINT]:
            strategy = "problem_solving"
        elif sentiment == SentimentType.POSITIVE:
            strategy = "amplification"
        elif sentiment == SentimentType.NEGATIVE:
            strategy = "damage_control"
        else:
            strategy = "engagement_maintenance"
        
        # Calcular boost esperado
        expected_boost = self._calculate_expected_engagement_boost(
            comment.platform, personalization_level, sentiment, confidence_score
        )
        
        return AutomatedReply(
            reply_id=str(uuid.uuid4()),
            original_comment_id=comment.comment_id,
            reply_text=reply_text,
            strategy=strategy,
            confidence_score=confidence_score,
            personalization_level=personalization_level,
            expected_engagement_boost=expected_boost
        )

    def _calculate_expected_engagement_boost(self, platform: Platform, personalization: str, 
                                           sentiment: SentimentType, confidence: float) -> float:
        """Calcula boost esperado de engajamento"""
        
        base_boost = 0.1  # 10% boost base
        
        # Multipliers por plataforma
        platform_multipliers = {
            Platform.INSTAGRAM: 1.3,
            Platform.FACEBOOK: 1.1,
            Platform.TWITTER: 1.2,
            Platform.LINKEDIN: 1.0,
            Platform.YOUTUBE: 1.15,
            Platform.TIKTOK: 1.4
        }
        
        # Multipliers por personalização
        personalization_multipliers = {
            "basic": 1.0,
            "medium": 1.2,
            "high": 1.5
        }
        
        # Multipliers por sentimento
        sentiment_multipliers = {
            SentimentType.POSITIVE: 1.3,
            SentimentType.QUESTION: 1.4,
            SentimentType.COMPLAINT: 1.2,
            SentimentType.PRAISE: 1.3,
            SentimentType.NEGATIVE: 1.1,
            SentimentType.NEUTRAL: 1.0
        }
        
        # Calcular boost final
        final_boost = (
            base_boost * 
            platform_multipliers.get(platform, 1.0) *
            personalization_multipliers.get(personalization, 1.0) *
            sentiment_multipliers.get(sentiment, 1.0) *
            confidence
        )
        
        return min(final_boost, 1.0)  # Cap at 100%

    def _estimate_action_impact(self, action: EngagementAction, sentiment: SentimentType, 
                               engagement_score: float) -> float:
        """Estima impacto da ação de engajamento"""
        
        base_impacts = {
            EngagementAction.LIKE: 0.05,
            EngagementAction.REPLY: 0.15,
            EngagementAction.SHARE: 0.25,
            EngagementAction.FOLLOW: 0.30,
            EngagementAction.SAVE: 0.10,
            EngagementAction.TAG_USERS: 0.20,
            EngagementAction.CREATE_STORY: 0.35,
            EngagementAction.DIRECT_MESSAGE: 0.40
        }
        
        base_impact = base_impacts.get(action, 0.05)
        
        # Ajustar baseado no sentimento
        sentiment_modifiers = {
            SentimentType.POSITIVE: 1.2,
            SentimentType.NEGATIVE: 1.4,  # Maior impacto ao resolver problemas
            SentimentType.QUESTION: 1.3,
            SentimentType.COMPLAINT: 1.5,
            SentimentType.PRAISE: 1.1,
            SentimentType.NEUTRAL: 1.0
        }
        
        # Ajustar baseado no engagement score
        engagement_modifier = 1.0 + engagement_score
        
        return base_impact * sentiment_modifiers.get(sentiment, 1.0) * engagement_modifier

    def _get_user_engagement_history(self, user_id: str) -> Dict[str, Any]:
        """Obtém histórico de engajamento do usuário"""
        
        # Simulação de histórico
        user_history = {
            "total_comments": hash(user_id) % 50,
            "avg_sentiment": ["positive", "neutral", "negative"][hash(user_id) % 3],
            "frequent_commenter": (hash(user_id) % 10) > 7,
            "engagement_score": (hash(user_id) % 100) / 100,
            "last_interaction": (datetime.now() - timedelta(days=hash(user_id) % 30)).isoformat(),
            "preferred_content_types": ["educational", "entertainment", "promotional"][:(hash(user_id) % 3) + 1]
        }
        
        return user_history

    def _get_platform_optimization_tips(self, platform: Platform) -> List[str]:
        """Retorna dicas de otimização por plataforma"""
        
        optimization_tips = {
            Platform.INSTAGRAM: [
                "Use emojis para aumentar engajamento",
                "Responda dentro das primeiras 2 horas",
                "Adicione hashtags relevantes nas respostas",
                "Crie Stories sobre comentários interessantes"
            ],
            Platform.FACEBOOK: [
                "Respostas longas geram mais discussão",
                "Use reactions além do like",
                "Compartilhe comentários positivos",
                "Monitore comentários em tempo real"
            ],
            Platform.TWITTER: [
                "Seja conciso e direto",
                "Use threads para respostas longas",
                "Retweete com comentário",
                "Responda rapidamente"
            ],
            Platform.LINKEDIN: [
                "Mantenha tom profissional",
                "Ofereça valor em cada resposta",
                "Conecte com comentaristas ativos",
                "Compartilhe insights relevantes"
            ]
        }
        
        return optimization_tips.get(platform, ["Mantenha engajamento consistente"])

    def _build_comment_object(self, data: Dict[str, Any]) -> Comment:
        """Constrói objeto Comment a partir dos dados"""
        
        return Comment(
            comment_id=data.get("comment_id", str(uuid.uuid4())),
            post_id=data.get("post_id", "unknown"),
            user_id=data.get("user_id", "unknown"),
            username=data.get("username", "user"),
            text=data.get("comment_text", ""),
            timestamp=datetime.now(),
            likes=data.get("likes", 0),
            replies=data.get("replies", 0),
            platform=Platform(data.get("platform", "instagram"))
        )

    async def _analyze_post_engagement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa engajamento completo de um post"""
        
        post_id = data.get("post_id")
        comments_data = data.get("comments", [])
        platform = Platform(data.get("platform", "instagram"))
        
        if not comments_data:
            return {"error": "Nenhum comentário fornecido para análise"}
        
        # Analisar todos os comentários
        comment_analyses = []
        sentiment_distribution = defaultdict(int)
        total_engagement_score = 0
        keywords_all = []
        
        for comment_data in comments_data:
            comment = self._build_comment_object({**comment_data, "platform": platform.value})
            sentiment_analysis = await self._analyze_comment_sentiment(comment)
            
            comment_analyses.append({
                "comment_id": comment.comment_id,
                "sentiment": sentiment_analysis["sentiment"].value,
                "engagement_score": sentiment_analysis["engagement_score"],
                "keywords": sentiment_analysis["keywords"]
            })
            
            sentiment_distribution[sentiment_analysis["sentiment"].value] += 1
            total_engagement_score += sentiment_analysis["engagement_score"]
            keywords_all.extend(sentiment_analysis["keywords"])
        
        # Calcular métricas agregadas
        total_comments = len(comments_data)
        avg_engagement_score = total_engagement_score / total_comments if total_comments > 0 else 0
        
        # Top keywords
        keyword_counter = Counter(keywords_all)
        top_keywords = [keyword for keyword, count in keyword_counter.most_common(10)]
        
        # Taxa de engajamento
        positive_comments = sentiment_distribution.get("positive", 0)
        engagement_rate = positive_comments / total_comments if total_comments > 0 else 0
        
        # Taxa de resposta necessária
        questions = sentiment_distribution.get("question", 0)
        complaints = sentiment_distribution.get("complaint", 0)
        negative = sentiment_distribution.get("negative", 0)
        needs_response = questions + complaints + negative
        response_rate_needed = needs_response / total_comments if total_comments > 0 else 0
        
        # Melhores respostas (simulado)
        best_performing_replies = [
            "Obrigado pelo feedback! Que bom que você gostou! 😊",
            "Ótima pergunta! Te enviamos mais detalhes na DM 📩",
            "Agradecemos a sugestão! Nossa equipe vai analisar 💡"
        ]
        
        # Recomendações
        recommendations = []
        if engagement_rate < 0.3:
            recommendations.append("Aumentar engajamento com perguntas e calls-to-action")
        if response_rate_needed > 0.2:
            recommendations.append("Priorizar respostas a perguntas e reclamações")
        if sentiment_distribution.get("negative", 0) > total_comments * 0.15:
            recommendations.append("Implementar estratégia de damage control")
        
        insight = EngagementInsight(
            insight_id=str(uuid.uuid4()),
            post_id=post_id,
            platform=platform,
            total_comments=total_comments,
            sentiment_distribution=dict(sentiment_distribution),
            top_keywords=top_keywords,
            engagement_rate=engagement_rate,
            response_rate=response_rate_needed,
            best_performing_replies=best_performing_replies,
            recommendations=recommendations
        )
        
        return {
            "insight": asdict(insight),
            "detailed_analysis": comment_analyses,
            "engagement_summary": {
                "avg_engagement_score": avg_engagement_score,
                "sentiment_breakdown": dict(sentiment_distribution),
                "requires_immediate_attention": needs_response > total_comments * 0.3,
                "overall_sentiment": max(sentiment_distribution, key=sentiment_distribution.get) if sentiment_distribution else "neutral"
            },
            "action_plan": self._generate_post_action_plan(insight),
            "timestamp": datetime.now().isoformat()
        }

    def _generate_post_action_plan(self, insight: EngagementInsight) -> List[Dict[str, Any]]:
        """Gera plano de ação para o post"""
        
        action_plan = []
        
        # Ações baseadas na distribuição de sentimentos
        if insight.sentiment_distribution.get("question", 0) > 0:
            action_plan.append({
                "action": "answer_questions",
                "priority": "high",
                "timeline": "2 hours",
                "description": f"Responder {insight.sentiment_distribution['question']} perguntas pendentes"
            })
        
        if insight.sentiment_distribution.get("complaint", 0) > 0:
            action_plan.append({
                "action": "address_complaints",
                "priority": "critical",
                "timeline": "1 hour",
                "description": f"Resolver {insight.sentiment_distribution['complaint']} reclamações"
            })
        
        if insight.engagement_rate < 0.3:
            action_plan.append({
                "action": "boost_engagement",
                "priority": "medium",
                "timeline": "24 hours",
                "description": "Implementar estratégias para aumentar engajamento positivo"
            })
        
        # Ações de crescimento
        if insight.sentiment_distribution.get("positive", 0) > insight.total_comments * 0.5:
            action_plan.append({
                "action": "amplify_success",
                "priority": "medium",
                "timeline": "12 hours",
                "description": "Criar conteúdo derivado para amplificar sucesso"
            })
        
        return action_plan

    async def _create_engagement_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria estratégia personalizada de engajamento"""
        
        strategy_type = EngagementStrategy(data.get("strategy_type", "reactive"))
        platform = Platform(data.get("platform", "instagram"))
        target_metrics = data.get("target_metrics", {
            "engagement_rate": 0.05,
            "response_rate": 0.8,
            "sentiment_improvement": 0.2
        })
        duration_days = data.get("duration_days", 30)
        
        # Gerar ações específicas da estratégia
        strategy_actions = []
        
        if strategy_type == EngagementStrategy.REACTIVE:
            strategy_actions = [
                {
                    "action": "automated_sentiment_monitoring",
                    "frequency": "continuous",
                    "description": "Monitorar comentários em tempo real e responder automaticamente"
                },
                {
                    "action": "priority_response_system",
                    "frequency": "hourly",
                    "description": "Sistema de priorização para comentários que precisam de resposta"
                },
                {
                    "action": "sentiment_analysis_reports",
                    "frequency": "daily",
                    "description": "Relatórios diários de análise de sentimento"
                }
            ]
        elif strategy_type == EngagementStrategy.PROACTIVE:
            strategy_actions = [
                {
                    "action": "engagement_bait_posts",
                    "frequency": "3x_week",
                    "description": "Posts designados para gerar conversação e engagement"
                },
                {
                    "action": "community_questions",
                    "frequency": "daily",
                    "description": "Fazer perguntas para a comunidade nas stories/posts"
                },
                {
                    "action": "user_spotlight",
                    "frequency": "weekly",
                    "description": "Destacar comentários e usuários mais engajados"
                }
            ]
        
        # Calcular resultados esperados
        expected_results = self._calculate_expected_strategy_results(
            strategy_type, platform, target_metrics, duration_days
        )
        
        campaign = EngagementCampaign(
            campaign_id=str(uuid.uuid4()),
            name=f"{strategy_type.value.title()} Engagement Campaign",
            platform=platform,
            strategy=strategy_type,
            target_metrics=target_metrics,
            duration_days=duration_days,
            actions=strategy_actions,
            expected_results=expected_results
        )
        
        return {
            "campaign": asdict(campaign),
            "implementation_guide": self._generate_implementation_guide(campaign),
            "success_metrics": self._define_success_metrics(campaign),
            "timeline": self._create_campaign_timeline(campaign),
            "timestamp": datetime.now().isoformat()
        }

    def _calculate_expected_strategy_results(self, strategy: EngagementStrategy, platform: Platform,
                                           targets: Dict[str, float], duration: int) -> Dict[str, float]:
        """Calcula resultados esperados da estratégia"""
        
        base_improvements = {
            EngagementStrategy.REACTIVE: {
                "engagement_rate": 0.02,
                "response_rate": 0.3,
                "sentiment_improvement": 0.15
            },
            EngagementStrategy.PROACTIVE: {
                "engagement_rate": 0.05,
                "response_rate": 0.1,
                "sentiment_improvement": 0.25
            },
            EngagementStrategy.COMMUNITY_BUILDING: {
                "engagement_rate": 0.08,
                "response_rate": 0.2,
                "sentiment_improvement": 0.3
            }
        }
        
        base_improvement = base_improvements.get(strategy, base_improvements[EngagementStrategy.REACTIVE])
        
        # Ajustar por duração (melhorias se acumulam com o tempo)
        duration_multiplier = min(duration / 30, 2.0)  # Cap em 2x para 60+ dias
        
        # Ajustar por plataforma
        platform_multipliers = {
            Platform.INSTAGRAM: 1.2,
            Platform.FACEBOOK: 1.0,
            Platform.TWITTER: 1.1,
            Platform.LINKEDIN: 0.9,
            Platform.YOUTUBE: 1.0,
            Platform.TIKTOK: 1.3
        }
        
        platform_mult = platform_multipliers.get(platform, 1.0)
        
        expected_results = {}
        for metric, base_value in base_improvement.items():
            expected_results[metric] = base_value * duration_multiplier * platform_mult
        
        return expected_results

    def _generate_implementation_guide(self, campaign: EngagementCampaign) -> List[str]:
        """Gera guia de implementação da campanha"""
        
        guide_steps = [
            "1. Configure monitoramento automático de comentários",
            "2. Defina templates de resposta por tipo de sentimento",
            "3. Estabeleça SLAs de resposta por prioridade",
            "4. Configure dashboards de métricas em tempo real",
            "5. Treine equipe nos novos processos"
        ]
        
        if campaign.strategy == EngagementStrategy.PROACTIVE:
            guide_steps.extend([
                "6. Crie calendário de posts de engajamento",
                "7. Desenvolva banco de perguntas para a comunidade",
                "8. Configure sistema de user-generated content"
            ])
        
        return guide_steps

    def _define_success_metrics(self, campaign: EngagementCampaign) -> Dict[str, str]:
        """Define métricas de sucesso da campanha"""
        
        return {
            "primary_kpi": "Engagement Rate",
            "secondary_kpis": ["Response Rate", "Sentiment Score", "Comment Volume"],
            "measurement_frequency": "Weekly",
            "success_threshold": f">{campaign.target_metrics.get('engagement_rate', 0.05)*100}% engagement rate",
            "tracking_tools": ["Native Analytics", "Sentiment Analysis", "Response Time Monitoring"]
        }

    def _create_campaign_timeline(self, campaign: EngagementCampaign) -> List[Dict[str, str]]:
        """Cria timeline da campanha"""
        
        timeline = []
        
        # Fase 1: Setup (primeira semana)
        timeline.append({
            "phase": "Setup & Launch",
            "duration": "Week 1",
            "activities": "Configure tools, train team, launch monitoring",
            "deliverables": "Automated systems active, team trained"
        })
        
        # Fase 2: Execução (semanas 2-4)
        timeline.append({
            "phase": "Active Execution",
            "duration": "Weeks 2-4", 
            "activities": "Execute strategy actions, monitor metrics, adjust tactics",
            "deliverables": "Daily engagement reports, weekly optimizations"
        })
        
        # Fase 3: Análise (última semana)
        if campaign.duration_days >= 28:
            timeline.append({
                "phase": "Analysis & Optimization", 
                "duration": "Final Week",
                "activities": "Analyze results, identify improvements, plan next phase",
                "deliverables": "Campaign results report, optimization recommendations"
            })
        
        return timeline

def create_agents() -> List[EngagementMaximizerAgent]:
    """
    Função obrigatória para criação de agentes.
    Retorna lista de agentes Engagement Maximizer para o módulo Social Media.
    """
    return [EngagementMaximizerAgent()]

# Função de inicialização para compatibilidade
def initialize_engagement_maximizer_agent():
    """Inicializa o agente Engagement Maximizer"""
    return EngagementMaximizerAgent()

# Ponto de entrada para testes
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = EngagementMaximizerAgent()
        
        # Teste de análise de comentário
        comment_test = {
            "action": "analyze_and_engage_comment",
            "comment_id": "COMM_001",
            "post_id": "POST_001",
            "user_id": "USER_001",
            "username": "joao_silva",
            "comment_text": "Adorei esse post! Como posso saber mais sobre esse produto? 😍",
            "platform": "instagram",
            "likes": 5,
            "replies": 2
        }
        
        result = await agent.process(comment_test)
        print("Teste Engagement Maximizer Agent:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Teste de análise de post
        post_analysis_test = {
            "action": "analyze_post_engagement",
            "post_id": "POST_002",
            "platform": "instagram",
            "comments": [
                {
                    "comment_id": "COMM_002",
                    "user_id": "USER_002",
                    "username": "maria_santos",
                    "comment_text": "Excelente conteúdo! Muito útil 👏",
                    "likes": 3
                },
                {
                    "comment_id": "COMM_003",
                    "user_id": "USER_003", 
                    "username": "pedro_lima",
                    "comment_text": "Não funcionou para mim. Podem ajudar?",
                    "likes": 1
                },
                {
                    "comment_id": "COMM_004",
                    "user_id": "USER_004",
                    "username": "ana_costa",
                    "comment_text": "Quando vocês vão lançar a versão premium?",
                    "likes": 2
                }
            ]
        }
        
        post_result = await agent.process(post_analysis_test)
        print("\nTeste Análise de Post:")
        print(json.dumps(post_result, indent=2, ensure_ascii=False))
        
    # Executar teste
    asyncio.run(test_agent())
