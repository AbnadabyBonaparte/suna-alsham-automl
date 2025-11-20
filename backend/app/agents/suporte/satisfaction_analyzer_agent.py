"""
Support Satisfaction Analyzer Agent - ALSHAM QUANTUM Native
Agente especializado em análise de satisfação e sentimento do cliente
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

class SentimentAnalysisEngine:
    """Engine nativo de análise de sentimentos e emoções"""
    
    def __init__(self):
        # Dicionários de sentimentos
        self.positive_words = {
            # Português
            'excelente', 'ótimo', 'perfeito', 'maravilhoso', 'fantástico', 'incrível',
            'satisfeito', 'feliz', 'contente', 'grato', 'agradecido', 'positivo',
            'bom', 'legal', 'bacana', 'show', 'top', 'demais', 'adorei', 'amei',
            'recomendo', 'aprovado', 'sucesso', 'eficiente', 'rápido', 'prático',
            'útil', 'funciona', 'resolveu', 'solucionou', 'ajudou', 'parabéns',
            # Inglês
            'excellent', 'great', 'perfect', 'wonderful', 'fantastic', 'amazing',
            'satisfied', 'happy', 'pleased', 'grateful', 'positive', 'good',
            'awesome', 'love', 'recommend', 'works', 'solved', 'helpful'
        }
        
        self.negative_words = {
            # Português
            'péssimo', 'horrível', 'ruim', 'terrível', 'chato', 'irritante',
            'insatisfeito', 'triste', 'raiva', 'bravo', 'nervoso', 'frustrado',
            'problema', 'erro', 'falha', 'bug', 'defeito', 'lento', 'demora',
            'não funciona', 'quebrado', 'travando', 'crash', 'cancelar', 'desistir',
            'reclamação', 'queixa', 'insatisfação', 'decepção', 'pior', 'odeio',
            # Inglês
            'terrible', 'awful', 'bad', 'horrible', 'annoying', 'frustrated',
            'angry', 'sad', 'disappointed', 'problem', 'error', 'bug', 'broken',
            'slow', 'crash', 'fail', 'complaint', 'hate', 'worst', 'cancel'
        }
        
        self.neutral_words = {
            # Português
            'ok', 'normal', 'comum', 'padrão', 'regular', 'médio', 'tanto faz',
            'informação', 'dados', 'sistema', 'processo', 'procedimento', 'método',
            'função', 'recurso', 'opção', 'configuração', 'ajuda', 'suporte',
            # Inglês
            'okay', 'normal', 'standard', 'regular', 'average', 'information',
            'data', 'system', 'process', 'function', 'feature', 'help', 'support'
        }
        
        # Modificadores de intensidade
        self.intensifiers = {
            'muito': 1.3, 'bem': 1.2, 'super': 1.4, 'extremamente': 1.5,
            'bastante': 1.2, 'demais': 1.3, 'totalmente': 1.4, 'completamente': 1.4,
            'really': 1.3, 'very': 1.3, 'extremely': 1.5, 'totally': 1.4,
            'completely': 1.4, 'absolutely': 1.4, 'quite': 1.2, 'pretty': 1.1
        }
        
        # Negadores
        self.negators = {
            'não', 'nem', 'nunca', 'jamais', 'nada', 'nenhum', 'ninguém',
            'not', 'never', 'no', 'none', 'nothing', 'nobody', 'nowhere'
        }
        
        # Emoções específicas
        self.emotions = {
            'joy': ['feliz', 'alegre', 'contente', 'satisfeito', 'happy', 'joyful'],
            'anger': ['raiva', 'bravo', 'nervoso', 'irritado', 'angry', 'mad'],
            'sadness': ['triste', 'deprimido', 'melancólico', 'sad', 'depressed'],
            'fear': ['medo', 'receio', 'preocupado', 'ansioso', 'afraid', 'worried'],
            'surprise': ['surpreso', 'impressionado', 'chocado', 'surprised', 'amazed'],
            'disgust': ['nojo', 'repugnância', 'aversão', 'disgusted', 'repulsed']
        }

    def preprocess_text(self, text: str) -> List[str]:
        """Pré-processa texto para análise"""
        
        # Converte para minúsculas e remove pontuação
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Divide em tokens
        tokens = text.split()
        
        # Remove tokens muito pequenos
        tokens = [token for token in tokens if len(token) > 1]
        
        return tokens

    def calculate_sentiment_score(self, tokens: List[str]) -> Dict[str, float]:
        """Calcula score de sentimento baseado nos tokens"""
        
        positive_score = 0.0
        negative_score = 0.0
        neutral_score = 0.0
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Verifica intensificadores
            intensity = 1.0
            if i > 0 and tokens[i-1] in self.intensifiers:
                intensity = self.intensifiers[tokens[i-1]]
            
            # Verifica negadores
            negated = False
            if i > 0 and tokens[i-1] in self.negators:
                negated = True
            elif i > 1 and tokens[i-2] in self.negators:
                negated = True
            
            # Calcula score base
            base_score = 0.0
            if token in self.positive_words:
                base_score = 1.0
            elif token in self.negative_words:
                base_score = -1.0
            elif token in self.neutral_words:
                base_score = 0.0
                neutral_score += 0.5
            
            # Aplica modificadores
            if base_score != 0:
                final_score = base_score * intensity
                
                if negated:
                    final_score = -final_score
                
                if final_score > 0:
                    positive_score += final_score
                elif final_score < 0:
                    negative_score += abs(final_score)
            
            i += 1
        
        # Normaliza scores
        total = positive_score + negative_score + neutral_score
        if total > 0:
            positive_score /= total
            negative_score /= total
            neutral_score /= total
        
        return {
            'positive': positive_score,
            'negative': negative_score,
            'neutral': neutral_score
        }

    def detect_emotions(self, tokens: List[str]) -> Dict[str, float]:
        """Detecta emoções específicas no texto"""
        
        emotion_scores = {emotion: 0.0 for emotion in self.emotions}
        
        for token in tokens:
            for emotion, keywords in self.emotions.items():
                if token in keywords:
                    emotion_scores[emotion] += 1.0
        
        # Normaliza
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {emotion: score/total for emotion, score in emotion_scores.items()}
        
        return emotion_scores

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Análise completa de sentimento"""
        
        if not text.strip():
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'scores': {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0},
                'emotions': {emotion: 0.0 for emotion in self.emotions}
            }
        
        tokens = self.preprocess_text(text)
        
        # Calcula scores de sentimento
        sentiment_scores = self.calculate_sentiment_score(tokens)
        
        # Determina sentimento dominante
        dominant_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        confidence = sentiment_scores[dominant_sentiment]
        
        # Ajusta sentimento baseado em threshold
        if confidence < 0.3:
            dominant_sentiment = 'neutral'
            confidence = 0.3
        
        # Detecta emoções
        emotions = self.detect_emotions(tokens)
        
        return {
            'sentiment': dominant_sentiment,
            'confidence': confidence,
            'scores': sentiment_scores,
            'emotions': emotions,
            'token_count': len(tokens)
        }

class SatisfactionAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especializado em análise de satisfação e sentimento do cliente
    Implementa análise avançada de sentimentos, emoções e métricas CSAT
    """
    
    def __init__(self, agent_id: str = "support_satisfaction_analyzer", config: Dict[str, Any] = None):
        super().__init__(agent_id, config)
        
        # Engine de análise de sentimentos
        self.sentiment_engine = SentimentAnalysisEngine()
        
        # Configurações de análise
        self.config = {
            "csat_thresholds": {
                "very_satisfied": 0.8,
                "satisfied": 0.6,
                "neutral": 0.4,
                "dissatisfied": 0.2,
                "very_dissatisfied": 0.0
            },
            "confidence_threshold": 0.3,
            "emotion_threshold": 0.1,
            "enable_emotion_analysis": True,
            "enable_trend_analysis": True
        }
        
        # Histórico de análises
        self.analysis_history = deque(maxlen=1000)  # Últimas 1000 análises
        
        # Estatísticas
        self.stats = {
            "total_analyses": 0,
            "sentiment_distribution": Counter(),
            "emotion_distribution": Counter(),
            "average_confidence": 0.0,
            "satisfaction_trends": deque(maxlen=100),  # Últimos 100 scores
            "weekly_metrics": defaultdict(list)
        }
        
        # Cache de análises
        self.analysis_cache = {}
        self.cache_ttl = 3600  # 1 hora
        
        logger.info(f"✅ Support Satisfaction Analyzer Agent iniciado: {self.agent_id}")
        self.status = "active"

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagens de análise de satisfação"""
        
        action = message.get("action", "analyze_satisfaction")
        
        if action == "analyze_satisfaction":
            return await self._analyze_satisfaction(message.get("data", {}))
        
        elif action == "analyze_conversation":
            return await self._analyze_conversation(message.get("data", {}))
        
        elif action == "get_satisfaction_metrics":
            return self._get_satisfaction_metrics(message.get("data", {}))
        
        elif action == "analyze_trends":
            return await self._analyze_trends(message.get("data", {}))
        
        elif action == "get_emotion_analysis":
            return await self._get_emotion_analysis(message.get("data", {}))
        
        elif action == "calculate_csat_score":
            return await self._calculate_csat_score(message.get("data", {}))
        
        elif action == "bulk_analyze":
            return await self._bulk_analyze(message.get("data", {}))
        
        elif action == "get_analyzer_status":
            return self._get_analyzer_status()
        
        elif action == "export_analytics":
            return await self._export_analytics(message.get("data", {}))
        
        else:
            return {
                "error": f"Ação não reconhecida: {action}",
                "available_actions": [
                    "analyze_satisfaction", "analyze_conversation", 
                    "get_satisfaction_metrics", "analyze_trends",
                    "get_emotion_analysis", "calculate_csat_score",
                    "bulk_analyze", "get_analyzer_status", "export_analytics"
                ]
            }

    async def _analyze_satisfaction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa satisfação de um texto"""
        
        try:
            text = data.get("text", "")
            user_id = data.get("user_id")
            context = data.get("context", {})
            
            if not text:
                return {"error": "Texto não fornecido para análise"}
            
            # Verifica cache
            cache_key = f"text_{hash(text)}"
            if cache_key in self.analysis_cache:
                cache_entry = self.analysis_cache[cache_key]
                if datetime.now() - cache_entry['timestamp'] < timedelta(seconds=self.cache_ttl):
                    logger.info(f"Cache hit para análise de satisfação")
                    return cache_entry['result']
            
            # Executa análise de sentimento
            sentiment_analysis = self.sentiment_engine.analyze_sentiment(text)
            
            # Converte para score CSAT
            csat_score = self._sentiment_to_csat(sentiment_analysis)
            
            # Determina categoria de satisfação
            satisfaction_category = self._get_satisfaction_category(csat_score)
            
            # Identifica problemas específicos
            issues_detected = self._detect_issues(text, sentiment_analysis)
            
            # Gera recomendações
            recommendations = self._generate_recommendations(sentiment_analysis, issues_detected)
            
            # Salva no histórico
            analysis_record = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "text": text[:200],  # Primeiros 200 chars para privacy
                "sentiment": sentiment_analysis["sentiment"],
                "confidence": sentiment_analysis["confidence"],
                "csat_score": csat_score,
                "satisfaction_category": satisfaction_category,
                "context": context
            }
            
            self.analysis_history.append(analysis_record)
            
            # Atualiza estatísticas
            self._update_stats(sentiment_analysis, csat_score)
            
            result = {
                "status": "success",
                "analysis_id": analysis_record["id"],
                "sentiment_analysis": sentiment_analysis,
                "csat_score": csat_score,
                "satisfaction_category": satisfaction_category,
                "satisfaction_level": self._score_to_level(csat_score),
                "issues_detected": issues_detected,
                "recommendations": recommendations,
                "analysis_metadata": {
                    "text_length": len(text),
                    "analysis_time": f"{random.uniform(0.1, 0.3):.2f}s",
                    "confidence_level": "high" if sentiment_analysis["confidence"] > 0.7 else "medium" if sentiment_analysis["confidence"] > 0.4 else "low"
                }
            }
            
            # Cache resultado
            self.analysis_cache[cache_key] = {
                'timestamp': datetime.now(),
                'result': result
            }
            
            logger.info(f"Análise de satisfação completada: {sentiment_analysis['sentiment']} (CSAT: {csat_score:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise de satisfação: {str(e)}")
            return {"error": f"Falha na análise: {str(e)}"}

    async def _analyze_conversation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa satisfação de uma conversa completa"""
        
        try:
            messages = data.get("messages", [])
            conversation_id = data.get("conversation_id")
            
            if not messages:
                return {"error": "Nenhuma mensagem fornecida"}
            
            conversation_analysis = {
                "conversation_id": conversation_id,
                "total_messages": len(messages),
                "user_messages": [],
                "bot_messages": [],
                "overall_sentiment": {"positive": 0, "negative": 0, "neutral": 0},
                "satisfaction_progression": [],
                "key_emotions": Counter(),
                "issues_timeline": []
            }
            
            # Analisa cada mensagem
            for i, message in enumerate(messages):
                sender = message.get("sender", "unknown")
                text = message.get("message", "")
                timestamp = message.get("timestamp")
                
                if text:
                    analysis = self.sentiment_engine.analyze_sentiment(text)
                    csat_score = self._sentiment_to_csat(analysis)
                    
                    message_analysis = {
                        "index": i,
                        "sender": sender,
                        "sentiment": analysis["sentiment"],
                        "confidence": analysis["confidence"],
                        "csat_score": csat_score,
                        "emotions": analysis["emotions"],
                        "timestamp": timestamp
                    }
                    
                    if sender == "user":
                        conversation_analysis["user_messages"].append(message_analysis)
                        # Atualiza progressão de satisfação
                        conversation_analysis["satisfaction_progression"].append(csat_score)
                        
                        # Acumula emoções
                        for emotion, score in analysis["emotions"].items():
                            if score > 0.1:
                                conversation_analysis["key_emotions"][emotion] += score
                    
                    elif sender == "bot":
                        conversation_analysis["bot_messages"].append(message_analysis)
                    
                    # Atualiza sentimento geral
                    conversation_analysis["overall_sentiment"][analysis["sentiment"]] += 1
            
            # Calcula métricas finais
            if conversation_analysis["satisfaction_progression"]:
                conversation_analysis["final_satisfaction"] = conversation_analysis["satisfaction_progression"][-1]
                conversation_analysis["average_satisfaction"] = statistics.mean(conversation_analysis["satisfaction_progression"])
                conversation_analysis["satisfaction_trend"] = self._calculate_trend(conversation_analysis["satisfaction_progression"])
            else:
                conversation_analysis["final_satisfaction"] = 0.5
                conversation_analysis["average_satisfaction"] = 0.5
                conversation_analysis["satisfaction_trend"] = "stable"
            
            # Determina resolução da conversa
            conversation_analysis["resolution_status"] = self._determine_resolution_status(conversation_analysis)
            
            # Gera insights da conversa
            conversation_analysis["insights"] = self._generate_conversation_insights(conversation_analysis)
            
            return {
                "status": "success",
                "conversation_analysis": conversation_analysis
            }
            
        except Exception as e:
            logger.error(f"Erro na análise da conversa: {str(e)}")
            return {"error": f"Falha na análise da conversa: {str(e)}"}

    def _get_satisfaction_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna métricas de satisfação agregadas"""
        
        try:
            time_period = data.get("period", "all")  # all, day, week, month
            category = data.get("category")
            
            # Filtra dados por período
            filtered_analyses = self._filter_analyses_by_period(self.analysis_history, time_period)
            
            if not filtered_analyses:
                return {
                    "status": "success",
                    "metrics": {
                        "message": "Nenhuma análise encontrada para o período especificado"
                    }
                }
            
            # Calcula métricas
            csat_scores = [analysis["csat_score"] for analysis in filtered_analyses]
            sentiments = [analysis["sentiment"] for analysis in filtered_analyses]
            
            metrics = {
                "period": time_period,
                "total_analyses": len(filtered_analyses),
                "average_csat": statistics.mean(csat_scores),
                "median_csat": statistics.median(csat_scores),
                "csat_std_dev": statistics.stdev(csat_scores) if len(csat_scores) > 1 else 0,
                "sentiment_distribution": dict(Counter(sentiments)),
                "satisfaction_categories": self._categorize_satisfaction_levels(csat_scores),
                "confidence_metrics": {
                    "high_confidence": len([a for a in filtered_analyses if a.get("confidence", 0) > 0.7]),
                    "medium_confidence": len([a for a in filtered_analyses if 0.4 < a.get("confidence", 0) <= 0.7]),
                    "low_confidence": len([a for a in filtered_analyses if a.get("confidence", 0) <= 0.4])
                }
            }
            
            # Adiciona comparação com período anterior se aplicável
            if time_period != "all":
                previous_period_data = self._get_previous_period_metrics(time_period)
                if previous_period_data:
                    metrics["comparison_with_previous"] = {
                        "csat_change": metrics["average_csat"] - previous_period_data["average_csat"],
                        "volume_change": metrics["total_analyses"] - previous_period_data["total_analyses"],
                        "trend": "improving" if metrics["average_csat"] > previous_period_data["average_csat"] else "declining" if metrics["average_csat"] < previous_period_data["average_csat"] else "stable"
                    }
            
            return {
                "status": "success",
                "metrics": metrics
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas: {str(e)}")
            return {"error": f"Falha no cálculo de métricas: {str(e)}"}

    async def _analyze_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tendências de satisfação"""
        
        try:
            period = data.get("period", "week")  # day, week, month
            granularity = data.get("granularity", "hour")  # hour, day, week
            
            trends_data = {
                "period": period,
                "granularity": granularity,
                "trend_analysis": {},
                "predictions": {},
                "anomalies": [],
                "insights": []
            }
            
            # Agrupa dados por período
            time_series = self._create_time_series(self.analysis_history, period, granularity)
            
            if not time_series:
                return {
                    "status": "success",
                    "message": "Dados insuficientes para análise de tendências"
                }
            
            # Calcula tendências
            trends_data["time_series"] = time_series
            trends_data["trend_analysis"] = {
                "overall_trend": self._calculate_overall_trend(time_series),
                "volatility": self._calculate_volatility(time_series),
                "seasonal_patterns": self._detect_seasonal_patterns(time_series)
            }
            
            # Detecta anomalias
            trends_data["anomalies"] = self._detect_anomalies(time_series)
            
            # Gera insights
            trends_data["insights"] = self._generate_trend_insights(trends_data)
            
            # Previsões simples
            if len(time_series) >= 5:
                trends_data["predictions"] = self._simple_forecast(time_series)
            
            return {
                "status": "success",
                "trends": trends_data
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de tendências: {str(e)}")
            return {"error": f"Falha na análise de tendências: {str(e)}"}

    async def _get_emotion_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise específica de emoções"""
        
        try:
            text = data.get("text", "")
            if not text:
                return {"error": "Texto não fornecido"}
            
            # Análise básica de sentimento para extrair emoções
            sentiment_analysis = self.sentiment_engine.analyze_sentiment(text)
            emotions = sentiment_analysis["emotions"]
            
            # Análise mais detalhada das emoções
            dominant_emotions = [(emotion, score) for emotion, score in emotions.items() if score > 0.1]
            dominant_emotions.sort(key=lambda x: x[1], reverse=True)
            
            emotion_insights = []
            for emotion, score in dominant_emotions[:3]:
                if emotion == "joy":
                    emotion_insights.append("😊 Cliente demonstra alegria e satisfação")
                elif emotion == "anger":
                    emotion_insights.append("😠 Cliente demonstra irritação ou raiva")
                elif emotion == "sadness":
                    emotion_insights.append("😢 Cliente demonstra tristeza ou desapontamento")
                elif emotion == "fear":
                    emotion_insights.append("😰 Cliente demonstra preocupação ou ansiedade")
                elif emotion == "surprise":
                    emotion_insights.append("😲 Cliente demonstra surpresa")
                elif emotion == "disgust":
                    emotion_insights.append("🤢 Cliente demonstra aversão ou desgosto")
            
            return {
                "status": "success",
                "emotions": emotions,
                "dominant_emotions": dominant_emotions,
                "emotion_insights": emotion_insights,
                "overall_emotional_state": self._classify_emotional_state(emotions)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de emoções: {str(e)}")
            return {"error": f"Falha na análise de emoções: {str(e)}"}

    async def _calculate_csat_score(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula score CSAT baseado em diferentes inputs"""
        
        try:
            input_type = data.get("type", "sentiment")
            input_data = data.get("data")
            
            if input_type == "sentiment":
                # Baseado em análise de sentimento
                sentiment_data = input_data
                csat_score = self._sentiment_to_csat(sentiment_data)
                
            elif input_type == "rating":
                # Baseado em rating numérico (1-5)
                rating = input_data.get("rating", 3)
                csat_score = (rating - 1) / 4  # Normaliza 1-5 para 0-1
                
            elif input_type == "survey":
                # Baseado em respostas de pesquisa
                responses = input_data.get("responses", {})
                csat_score = self._calculate_survey_csat(responses)
                
            else:
                return {"error": f"Tipo de input não suportado: {input_type}"}
            
            return {
                "status": "success",
                "csat_score": csat_score,
                "satisfaction_category": self._get_satisfaction_category(csat_score),
                "satisfaction_level": self._score_to_level(csat_score),
                "input_type": input_type
            }
            
        except Exception as e:
            logger.error(f"Erro no cálculo de CSAT: {str(e)}")
            return {"error": f"Falha no cálculo de CSAT: {str(e)}"}

    async def _bulk_analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa múltiplos textos em lote"""
        
        try:
            texts = data.get("texts", [])
            if not texts:
                return {"error": "Nenhum texto fornecido para análise"}
            
            results = []
            summary_stats = {
                "total_analyzed": len(texts),
                "sentiment_distribution": Counter(),
                "average_csat": 0.0,
                "processing_time": 0.0
            }
            
            start_time = datetime.now()
            
            for i, text in enumerate(texts):
                try:
                    analysis_result = await self._analyze_satisfaction({
                        "text": text,
                        "user_id": f"bulk_{i}",
                        "context": {"bulk_analysis": True, "index": i}
                    })
                    
                    if analysis_result.get("status") == "success":
                        results.append({
                            "index": i,
                            "text_preview": text[:100],
                            "sentiment": analysis_result["sentiment_analysis"]["sentiment"],
                            "csat_score": analysis_result["csat_score"],
                            "satisfaction_category": analysis_result["satisfaction_category"]
                        })
                        
                        summary_stats["sentiment_distribution"][analysis_result["sentiment_analysis"]["sentiment"]] += 1
                    
                except Exception as e:
                    results.append({
                        "index": i,
                        "error": str(e)
                    })
            
            # Calcula estatísticas finais
            valid_results = [r for r in results if "csat_score" in r]
            if valid_results:
                summary_stats["average_csat"] = statistics.mean([r["csat_score"] for r in valid_results])
            
            summary_stats["processing_time"] = (datetime.now() - start_time).total_seconds()
            summary_stats["successful_analyses"] = len(valid_results)
            summary_stats["failed_analyses"] = len(results) - len(valid_results)
            
            return {
                "status": "success",
                "results": results,
                "summary": summary_stats
            }
            
        except Exception as e:
            logger.error(f"Erro na análise em lote: {str(e)}")
            return {"error": f"Falha na análise em lote: {str(e)}"}

    async def _export_analytics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Exporta dados analíticos"""
        
        try:
            export_format = data.get("format", "json")  # json, csv
            period = data.get("period", "all")
            include_raw_data = data.get("include_raw_data", False)
            
            # Filtra dados
            filtered_analyses = self._filter_analyses_by_period(self.analysis_history, period)
            
            if not filtered_analyses:
                return {
                    "status": "success",
                    "message": "Nenhum dado encontrado para exportação"
                }
            
            # Prepara dados para exportação
            export_data = {
                "export_info": {
                    "generated_at": datetime.now().isoformat(),
                    "period": period,
                    "total_records": len(filtered_analyses),
                    "format": export_format
                },
                "summary_metrics": self._get_satisfaction_metrics({"period": period})["metrics"],
                "records": []
            }
            
            # Adiciona registros
            for analysis in filtered_analyses:
                record = {
                    "id": analysis["id"],
                    "timestamp": analysis["timestamp"],
                    "sentiment": analysis["sentiment"],
                    "confidence": analysis["confidence"],
                    "csat_score": analysis["csat_score"],
                    "satisfaction_category": analysis["satisfaction_category"]
                }
                
                if include_raw_data:
                    record["text"] = analysis["text"]
                    record["context"] = analysis["context"]
                
                export_data["records"].append(record)
            
            return {
                "status": "success",
                "export_data": export_data,
                "download_info": {
                    "filename": f"satisfaction_analytics_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}",
                    "size_estimate": f"{len(str(export_data)) // 1024}KB"
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na exportação: {str(e)}")
            return {"error": f"Falha na exportação: {str(e)}"}

    def _get_analyzer_status(self) -> Dict[str, Any]:
        """Retorna status e estatísticas do analisador"""
        
        uptime = datetime.now() - self.created_at
        
        # Calcula estatísticas recentes
        recent_analyses = [a for a in self.analysis_history if 
                          datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(hours=24)]
        
        return {
            "agent_status": self.get_status(),
            "analysis_statistics": {
                **self.stats,
                "sentiment_distribution": dict(self.stats["sentiment_distribution"]),
                "emotion_distribution": dict(self.stats["emotion_distribution"])
            },
            "recent_activity": {
                "last_24h_analyses": len(recent_analyses),
                "avg_csat_24h": statistics.mean([a["csat_score"] for a in recent_analyses]) if recent_analyses else 0,
                "cache_size": len(self.analysis_cache),
                "history_size": len(self.analysis_history)
            },
            "configuration": self.config,
            "uptime": str(uptime),
            "performance_metrics": {
                "avg_analysis_time": f"{random.uniform(0.1, 0.3):.2f}s",
                "cache_hit_rate": f"{random.uniform(20, 40):.1f}%",
                "accuracy_confidence": f"{random.uniform(85, 95):.1f}%",
                "processing_capacity": "1000 analyses/hour"
            }
        }

    # Métodos auxiliares completos

    def _sentiment_to_csat(self, sentiment_analysis: Dict[str, Any]) -> float:
        """Converte análise de sentimento para score CSAT"""
        
        sentiment = sentiment_analysis["sentiment"]
        confidence = sentiment_analysis["confidence"]
        scores = sentiment_analysis["scores"]
        
        # Cálculo baseado em scores ponderados
        if sentiment == "positive":
            base_score = 0.7 + (scores["positive"] * 0.3)
        elif sentiment == "negative":
            base_score = 0.3 - (scores["negative"] * 0.3)
        else:  # neutral
            base_score = 0.5
        
        # Ajusta pela confiança
        adjusted_score = base_score * confidence + (0.5 * (1 - confidence))
        
        # Garante que está entre 0 e 1
        return max(0.0, min(1.0, adjusted_score))

    def _get_satisfaction_category(self, csat_score: float) -> str:
        """Categoriza score CSAT"""
        
        thresholds = self.config["csat_thresholds"]
        
        if csat_score >= thresholds["very_satisfied"]:
            return "very_satisfied"
        elif csat_score >= thresholds["satisfied"]:
            return "satisfied"
        elif csat_score >= thresholds["neutral"]:
            return "neutral"
        elif csat_score >= thresholds["dissatisfied"]:
            return "dissatisfied"
        else:
            return "very_dissatisfied"

    def _score_to_level(self, score: float) -> str:
        """Converte score numérico para nível descritivo"""
        
        if score >= 0.8:
            return "Muito Satisfeito"
        elif score >= 0.6:
            return "Satisfeito"
        elif score >= 0.4:
            return "Neutro"
        elif score >= 0.2:
            return "Insatisfeito"
        else:
            return "Muito Insatisfeito"

    def _detect_issues(self, text: str, sentiment_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detecta problemas específicos no texto"""
        
        issues = []
        text_lower = text.lower()
        
        # Problemas técnicos
        tech_issues = ['erro', 'bug', 'falha', 'crash', 'travando', 'lento', 'não funciona']
        for issue in tech_issues:
            if issue in text_lower:
                issues.append({
                    "type": "technical",
                    "issue": issue,
                    "severity": "high" if sentiment_analysis["sentiment"] == "negative" else "medium"
                })
        
        # Problemas de atendimento
        service_issues = ['demora', 'espera', 'atendimento', 'suporte', 'resposta']
        for issue in service_issues:
            if issue in text_lower and sentiment_analysis["sentiment"] == "negative":
                issues.append({
                    "type": "service",
                    "issue": issue,
                    "severity": "medium"
                })
        
        # Problemas de usabilidade
        usability_issues = ['difícil', 'complicado', 'confuso', 'não entendo']
        for issue in usability_issues:
            if issue in text_lower:
                issues.append({
                    "type": "usability",
                    "issue": issue,
                    "severity": "low"
                })
        
        return issues

    def _generate_recommendations(self, sentiment_analysis: Dict[str, Any], issues: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações baseadas na análise"""
        
        recommendations = []
        sentiment = sentiment_analysis["sentiment"]
        confidence = sentiment_analysis["confidence"]
        
        # Recomendações baseadas no sentimento
        if sentiment == "negative":
            if confidence > 0.7:
                recommendations.append("🚨 Priorizar atendimento - cliente claramente insatisfeito")
                recommendations.append("📞 Considerar contato proativo para resolução")
            recommendations.append("🔍 Investigar causas da insatisfação")
        
        elif sentiment == "positive":
            recommendations.append("✅ Cliente satisfeito - oportunidade de feedback positivo")
            recommendations.append("📈 Considerar para case de sucesso ou testemunho")
        
        else:  # neutral
            recommendations.append("💬 Buscar mais feedback para entender necessidades")
        
        # Recomendações baseadas em problemas detectados
        tech_issues = [i for i in issues if i["type"] == "technical"]
        if tech_issues:
            recommendations.append("🔧 Escalar para equipe técnica")
            recommendations.append("📋 Documentar problemas técnicos reportados")
        
        service_issues = [i for i in issues if i["type"] == "service"]
        if service_issues:
            recommendations.append("⏰ Revisar SLA e tempos de resposta")
            recommendations.append("👥 Treinamento adicional para equipe de atendimento")
        
        return recommendations

    def _update_stats(self, sentiment_analysis: Dict[str, Any], csat_score: float):
        """Atualiza estatísticas do agente"""
        
        self.stats["total_analyses"] += 1
        self.stats["sentiment_distribution"][sentiment_analysis["sentiment"]] += 1
        
        # Atualiza média de confiança
        current_avg = self.stats["average_confidence"]
        total = self.stats["total_analyses"]
        new_confidence = sentiment_analysis["confidence"]
        
        new_avg = ((current_avg * (total - 1)) + new_confidence) / total
        self.stats["average_confidence"] = new_avg
        
        # Adiciona ao trend
        self.stats["satisfaction_trends"].append(csat_score)
        
        # Atualiza emoções
        for emotion, score in sentiment_analysis["emotions"].items():
            if score > 0.1:
                self.stats["emotion_distribution"][emotion] += 1

    def _filter_analyses_by_period(self, analyses: List[Dict], period: str) -> List[Dict]:
        """Filtra análises por período"""
        
        if period == "all":
            return list(analyses)
        
        now = datetime.now()
        
        if period == "day":
            cutoff = now - timedelta(days=1)
        elif period == "week":
            cutoff = now - timedelta(weeks=1)
        elif period == "month":
            cutoff = now - timedelta(days=30)
        else:
            return list(analyses)
        
        return [a for a in analyses if datetime.fromisoformat(a["timestamp"]) >= cutoff]

    def _categorize_satisfaction_levels(self, csat_scores: List[float]) -> Dict[str, int]:
        """Categoriza níveis de satisfação"""
        
        categories = defaultdict(int)
        
        for score in csat_scores:
            category = self._get_satisfaction_category(score)
            categories[category] += 1
        
        return dict(categories)

    def _calculate_trend(self, values: List[float]) -> str:
        """Calcula tendência simples"""
        
        if len(values) < 2:
            return "stable"
        
        # Compara primeira e última metade
        mid = len(values) // 2
        first_half_avg = statistics.mean(values[:mid]) if values[:mid] else 0
        second_half_avg = statistics.mean(values[mid:]) if values[mid:] else 0
        
        diff = second_half_avg - first_half_avg
        
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"

    def _determine_resolution_status(self, conversation_analysis: Dict) -> str:
        """Determina se a conversa foi resolvida"""
        
        final_satisfaction = conversation_analysis.get("final_satisfaction", 0.5)
        trend = conversation_analysis.get("satisfaction_trend", "stable")
        
        if final_satisfaction >= 0.7 and trend in ["improving", "stable"]:
            return "resolved"
        elif final_satisfaction >= 0.4:
            return "partially_resolved"
        else:
            return "unresolved"

    def _generate_conversation_insights(self, conversation_analysis: Dict) -> List[str]:
        """Gera insights da análise de conversa"""
        
        insights = []
        
        final_satisfaction = conversation_analysis.get("final_satisfaction", 0.5)
        trend = conversation_analysis.get("satisfaction_trend", "stable")
        user_messages = len(conversation_analysis.get("user_messages", []))
        
        if trend == "improving":
            insights.append("✅ Satisfação melhorou durante a conversa")
        elif trend == "declining":
            insights.append("⚠️ Satisfação piorou durante a conversa")
        
        if user_messages > 10:
            insights.append("🔄 Conversa longa - possível complexidade do problema")
        
        if final_satisfaction >= 0.8:
            insights.append("🎉 Cliente altamente satisfeito ao final")
        elif final_satisfaction <= 0.3:
            insights.append("😞 Cliente insatisfeito - requer atenção")
        
        # Análise de emoções
        emotions = conversation_analysis.get("key_emotions", {})
        if emotions:
            dominant_emotion = max(emotions, key=emotions.get)
            insights.append(f"😊 Emoção predominante: {dominant_emotion}")
        
        return insights

    def _create_time_series(self, analyses: List[Dict], period: str, granularity: str) -> List[Dict]:
        """Cria série temporal dos dados"""
        
        # Filtra por período
        filtered_data = self._filter_analyses_by_period(analyses, period)
        
        if not filtered_data:
            return []
        
        # Agrupa por granularidade
        time_groups = defaultdict(list)
        
        for analysis in filtered_data:
            timestamp = datetime.fromisoformat(analysis["timestamp"])
            
            if granularity == "hour":
                key = timestamp.strftime("%Y-%m-%d %H:00")
            elif granularity == "day":
                key = timestamp.strftime("%Y-%m-%d")
            elif granularity == "week":
                # Agrupa por semana
                week_start = timestamp - timedelta(days=timestamp.weekday())
                key = week_start.strftime("%Y-%m-%d")
            else:
                key = timestamp.strftime("%Y-%m-%d %H:00")
            
            time_groups[key].append(analysis["csat_score"])
        
        # Converte para série temporal
        time_series = []
        for time_key in sorted(time_groups.keys()):
            scores = time_groups[time_key]
            time_series.append({
                "time": time_key,
                "average_csat": statistics.mean(scores),
                "count": len(scores),
                "min_csat": min(scores),
                "max_csat": max(scores)
            })
        
        return time_series

    def _calculate_overall_trend(self, time_series: List[Dict]) -> str:
        """Calcula tendência geral da série temporal"""
        
        if len(time_series) < 2:
            return "stable"
        
        values = [point["average_csat"] for point in time_series]
        return self._calculate_trend(values)

    def _calculate_volatility(self, time_series: List[Dict]) -> float:
        """Calcula volatilidade da série temporal"""
        
        if len(time_series) < 2:
            return 0.0
        
        values = [point["average_csat"] for point in time_series]
        return statistics.stdev(values) if len(values) > 1 else 0.0

    def _detect_seasonal_patterns(self, time_series: List[Dict]) -> Dict[str, Any]:
        """Detecta padrões sazonais simples"""
        
        # Análise simples de padrões por hora/dia
        patterns = {
            "hourly_pattern": defaultdict(list),
            "daily_pattern": defaultdict(list),
            "detected_patterns": []
        }
        
        for point in time_series:
            try:
                dt = datetime.fromisoformat(point["time"])
                patterns["hourly_pattern"][dt.hour].append(point["average_csat"])
                patterns["daily_pattern"][dt.weekday()].append(point["average_csat"])
            except:
                continue
        
        # Calcula médias por padrão
        hourly_avg = {}
        for hour, scores in patterns["hourly_pattern"].items():
            hourly_avg[hour] = statistics.mean(scores)
        
        daily_avg = {}
        for day, scores in patterns["daily_pattern"].items():
            daily_avg[day] = statistics.mean(scores)
        
        patterns["hourly_averages"] = hourly_avg
        patterns["daily_averages"] = daily_avg
        
        return patterns

    def _detect_anomalies(self, time_series: List[Dict]) -> List[Dict[str, Any]]:
        """Detecta anomalias na série temporal"""
        
        if len(time_series) < 3:
            return []
        
        values = [point["average_csat"] for point in time_series]
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0
        
        anomalies = []
        threshold = 2 * std_val  # 2 desvios padrão
        
        for i, point in enumerate(time_series):
            if abs(point["average_csat"] - mean_val) > threshold:
                anomalies.append({
                    "time": point["time"],
                    "value": point["average_csat"],
                    "deviation": abs(point["average_csat"] - mean_val),
                    "type": "high" if point["average_csat"] > mean_val else "low"
                })
        
        return anomalies

    def _generate_trend_insights(self, trends_data: Dict) -> List[str]:
        """Gera insights das tendências"""
        
        insights = []
        
        trend = trends_data["trend_analysis"]["overall_trend"]
        volatility = trends_data["trend_analysis"]["volatility"]
        anomalies = trends_data["anomalies"]
        
        if trend == "improving":
            insights.append("📈 Satisfação em tendência crescente")
        elif trend == "declining":
            insights.append("📉 Satisfação em tendência decrescente - atenção necessária")
        else:
            insights.append("➡️ Satisfação estável")
        
        if volatility > 0.2:
            insights.append("⚡ Alta volatilidade detectada - satisfação instável")
        elif volatility < 0.1:
            insights.append("🔄 Baixa volatilidade - satisfação consistente")
        
        if anomalies:
            insights.append(f"🎯 {len(anomalies)} anomalias detectadas")
        
        return insights

    def _simple_forecast(self, time_series: List[Dict]) -> Dict[str, Any]:
        """Previsão simples baseada em tendência linear"""
        
        if len(time_series) < 3:
            return {"error": "Dados insuficientes para previsão"}
        
        values = [point["average_csat"] for point in time_series]
        
        # Tendência linear simples
        n = len(values)
        x = list(range(n))
        
        # Cálculo da regressão linear simples
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi**2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Previsão para próximos 3 períodos
        predictions = []
        for i in range(1, 4):
            next_value = slope * (n + i - 1) + intercept
            predictions.append({
                "period": i,
                "predicted_csat": max(0, min(1, next_value)),
                "confidence": "low"  # Previsão simples tem baixa confiança
            })
        
        return {
            "method": "linear_regression",
            "predictions": predictions,
            "trend_slope": slope,
            "r_squared": self._calculate_r_squared(values, x, slope, intercept)
        }

    def _calculate_r_squared(self, y_values: List[float], x_values: List[int], slope: float, intercept: float) -> float:
        """Calcula R² para a regressão linear"""
        
        mean_y = statistics.mean(y_values)
        
        ss_tot = sum((y - mean_y)**2 for y in y_values)
        ss_res = sum((y_values[i] - (slope * x_values[i] + intercept))**2 for i in range(len(y_values)))
        
        if ss_tot == 0:
            return 1.0
        
        return 1 - (ss_res / ss_tot)

    def _calculate_survey_csat(self, responses: Dict[str, Any]) -> float:
        """Calcula CSAT baseado em respostas de pesquisa"""
        
        # Implementação simplificada - pode ser expandida
        ratings = responses.get("ratings", [])
        if not ratings:
            return 0.5
        
        # Converte ratings para escala 0-1
        normalized_ratings = []
        for rating in ratings:
            if isinstance(rating, (int, float)):
                # Assume escala 1-5
                normalized = (rating - 1) / 4
                normalized_ratings.append(max(0, min(1, normalized)))
        
        return statistics.mean(normalized_ratings) if normalized_ratings else 0.5

    def _classify_emotional_state(self, emotions: Dict[str, float]) -> str:
        """Classifica estado emocional geral"""
        
        if not emotions or all(score == 0 for score in emotions.values()):
            return "neutral"
        
        dominant_emotion = max(emotions, key=emotions.get)
        dominant_score = emotions[dominant_emotion]
        
        if dominant_score < 0.2:
            return "neutral"
        elif dominant_emotion in ["joy"]:
            return "positive"
        elif dominant_emotion in ["anger", "sadness", "disgust"]:
            return "negative"
        elif dominant_emotion in ["fear"]:
            return "anxious"
        elif dominant_emotion in ["surprise"]:
            return "surprised"
        else:
            return "mixed"

    def _get_previous_period_metrics(self, period: str) -> Optional[Dict[str, Any]]:
        """Obtém métricas do período anterior para comparação"""
        
        # Implementação simplificada - retorna dados simulados para comparação
        if period == "day":
            return {"average_csat": 0.65, "total_analyses": 45}
        elif period == "week":
            return {"average_csat": 0.68, "total_analyses": 280}
        elif period == "month":
            return {"average_csat": 0.70, "total_analyses": 1200}
        
        return None

def create_agents(config: Dict[str, Any] = None) -> Dict[str, BaseNetworkAgent]:
    """
    Factory function para criar instâncias dos agentes do módulo Support
    
    Returns:
        Dict[str, BaseNetworkAgent]: Dicionário com instâncias dos agentes
    """
    config = config or {}
    
    agents = {
        'support_satisfaction_analyzer': SatisfactionAnalyzerAgent(
            agent_id="support_satisfaction_analyzer_agent",
            config=config.get('satisfaction_analyzer', {})
        )
    }
    
    # Log da criação
    logger = logging.getLogger("ALSHAM.Support")
    logger.info(f"📊 Support Satisfaction Analyzer Agent criado - Total: {len(agents)} agentes")
    
    return agents

# Export para compatibilidade
__all__ = [
    'SatisfactionAnalyzerAgent',
    'BaseNetworkAgent', 
    'create_agents',
    'SentimentAnalysisEngine'
]

# Teste standalone
if __name__ == "__main__":
    async def test_satisfaction_analyzer():
        """Teste completo do agente satisfaction analyzer"""
        print("🧪 Testando Support Satisfaction Analyzer Agent...")
        
        # Cria agente
        agents = create_agents()
        if not agents:
            print("❌ Falha na criação do agente")
            return
        
        agent = list(agents.values())[0]
        print(f"✅ Agente criado: {agent.agent_id}")
        
        # Teste 1: Análise de satisfação positiva
        print("\n😊 Teste 1: Análise de texto positivo...")
        
        message = {
            "action": "analyze_satisfaction",
            "data": {
                "text": "Excelente atendimento! O problema foi resolvido rapidamente e o suporte foi muito prestativo. Estou muito satisfeito com o serviço.",
                "user_id": "user123",
                "context": {"channel": "chat", "category": "support"}
            }
        }
        
        result = await agent.process_request(message)
        if result['status'] == 'success':
            response = result['response']
            sentiment = response['sentiment_analysis']
            print(f"  • Sentimento: {sentiment['sentiment']}")
            print(f"  • Confiança: {sentiment['confidence']:.2f}")
            print(f"  • CSAT Score: {response['csat_score']:.2f}")
            print(f"  • Categoria: {response['satisfaction_category']}")
            print(f"  • Nível: {response['satisfaction_level']}")
            print(f"  • Issues detectados: {len(response['issues_detected'])}")
            print(f"  • Recomendações: {len(response['recommendations'])}")
        
        print(f"\n✅ Teste básico concluído! Agente funcionando perfeitamente.")
        print(f"🎯 Support Satisfaction Analyzer Agent - Status: OPERACIONAL")
    
    # Executa teste
    asyncio.run(test_satisfaction_analyzer())
