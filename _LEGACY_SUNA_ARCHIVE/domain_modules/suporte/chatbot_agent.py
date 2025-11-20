"""
ALSHAM QUANTUM - Support Chatbot Agent
Agente especializado em chatbot inteligente para suporte automatizado
Versão: 2.0 - Implementação nativa sem dependências externas
"""

import json
import asyncio
import logging
import uuid
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
import random

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseNetworkAgent:
    """Classe base para todos os agentes da rede ALSHAM QUANTUM"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "active"
        self.created_at = datetime.now()
        self.last_heartbeat = datetime.now()
        self.message_count = 0
        
    async def _internal_handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Método interno obrigatório para processamento de mensagens"""
        self.message_count += 1
        self.last_heartbeat = datetime.now()
        
        try:
            # Processa a mensagem usando o método específico do agente
            response = await self.process_message(message)
            
            return {
                "agent_id": self.agent_id,
                "status": "success",
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "message_count": self.message_count
            }
            
        except Exception as e:
            logger.error(f"Erro no agente {self.agent_id}: {str(e)}")
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
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "message_count": self.message_count
        }

class NaturalLanguageEngine:
    """Engine nativo de processamento de linguagem natural"""
    
    def __init__(self):
        # Dicionário de intenções e padrões
        self.intent_patterns = {
            "greeting": [
                r"olá|oi|bom dia|boa tarde|boa noite|hey|hello",
                r"preciso de ajuda|posso falar com alguém"
            ],
            "password_reset": [
                r"esqueci.*senha|resetar.*senha|redefinir.*senha",
                r"não consigo.*login|não.*entrar|senha.*expirou",
                r"trocar.*senha|mudar.*senha|alterar.*senha"
            ],
            "billing_question": [
                r"fatura|cobrança|pagamento|valor|preço",
                r"cartão.*crédito|débito|boleto|pix",
                r"cancelar.*assinatura|plano|mensalidade"
            ],
            "feature_info": [
                r"como.*funciona|como.*usar|tutorial",
                r"função|recurso|ferramenta|feature",
                r"configurar|setup|instalação"
            ],
            "technical_support": [
                r"erro|bug|falha|problema|não.*funciona",
                r"sistema.*lento|travando|crash",
                r"suporte.*técnico|help.*desk"
            ],
            "account_info": [
                r"minha.*conta|perfil|dados.*pessoais",
                r"atualizar.*informações|alterar.*dados",
                r"excluir.*conta|deletar.*perfil"
            ],
            "complaint": [
                r"reclamação|insatisfeito|problema.*atendimento",
                r"demora|lento|ruim|péssimo|horrível",
                r"quero.*cancelar|sair.*sistema"
            ],
            "praise": [
                r"parabéns|excelente|ótimo|muito.*bom",
                r"satisfeito|gostei|recomendo|perfeito"
            ]
        }
        
        # Entidades nomeadas
        self.entities = {
            "product_names": ["premium", "basic", "pro", "enterprise", "starter"],
            "time_expressions": ["hoje", "ontem", "semana", "mês", "ano"],
            "payment_methods": ["cartão", "boleto", "pix", "débito", "crédito"]
        }
        
        # Respostas por intenção
        self.intent_responses = {
            "greeting": [
                "Olá! Como posso ajudá-lo hoje?",
                "Oi! Em que posso ser útil?",
                "Bem-vindo ao suporte! Como posso auxiliá-lo?",
                "Olá! Estou aqui para ajudar. Qual é sua dúvida?"
            ],
            "password_reset": [
                "Vou ajudá-lo com a redefinição de senha. Por favor, forneça seu email de cadastro.",
                "Para resetar sua senha, acesse o link 'Esqueci minha senha' na tela de login.",
                "Posso ajudar com a senha. Você tem acesso ao email cadastrado?"
            ],
            "billing_question": [
                "Sobre questões financeiras, vou verificar sua conta. Pode me informar seu CPF?",
                "Para dúvidas de cobrança, preciso validar alguns dados. Qual o email da sua conta?",
                "Questões de faturamento são importantes. Vou transferir para o financeiro."
            ],
            "feature_info": [
                "Posso explicar como usar nossos recursos. Qual funcionalidade específica?",
                "Temos tutoriais completos. Sobre qual ferramenta gostaria de saber?",
                "Vou ajudá-lo a entender melhor. Qual recurso tem dúvidas?"
            ],
            "technical_support": [
                "Problemas técnicos são nossa prioridade. Pode descrever o erro em detalhes?",
                "Vou ajudar a resolver o problema técnico. Quando começou a acontecer?",
                "Suporte técnico especializado. Em qual sistema está ocorrendo?"
            ],
            "account_info": [
                "Para alterações na conta, preciso confirmar sua identidade. Qual seu email?",
                "Dados da conta são sensíveis. Vou precisar de algumas informações de segurança.",
                "Posso ajudar com informações da conta. O que gostaria de alterar?"
            ],
            "complaint": [
                "Lamento pelo inconveniente. Sua opinião é importante para nós.",
                "Entendo sua insatisfação. Vou encaminhar para nossa supervisão.",
                "Peço desculpas pelo problema. Como podemos melhorar sua experiência?"
            ],
            "praise": [
                "Muito obrigado pelo feedback positivo! Ficamos felizes em ajudar.",
                "Que bom saber que estamos no caminho certo! Sua opinião é valiosa.",
                "Agradecemos o reconhecimento! Continuamos à disposição."
            ],
            "unknown": [
                "Não entendi completamente sua solicitação. Pode reformular?",
                "Desculpe, pode ser mais específico sobre o que precisa?",
                "Vou transferir para um atendente humano que pode ajudar melhor."
            ]
        }

    def analyze_intent(self, text: str) -> Dict[str, Any]:
        """Analisa a intenção do usuário"""
        
        text_lower = text.lower()
        
        # Pontuação por intenção
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches * 10  # Peso por match
            
            if score > 0:
                intent_scores[intent] = score
        
        # Determina a intenção com maior pontuação
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 10, 1.0)  # Normaliza
        else:
            best_intent = "unknown"
            confidence = 0.1
        
        # Extrai entidades
        entities = self.extract_entities(text_lower)
        
        return {
            "intent": best_intent,
            "confidence": confidence,
            "entities": entities,
            "all_scores": intent_scores
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extrai entidades nomeadas do texto"""
        
        found_entities = {}
        
        for entity_type, entity_list in self.entities.items():
            found = []
            for entity in entity_list:
                if entity in text:
                    found.append(entity)
            
            if found:
                found_entities[entity_type] = found
        
        # Extrai emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            found_entities["emails"] = emails
        
        # Extrai números (possível CPF, telefone, etc.)
        number_pattern = r'\b\d{10,11}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
        numbers = re.findall(number_pattern, text)
        if numbers:
            found_entities["numbers"] = numbers
        
        return found_entities
    
    def get_response(self, intent: str, entities: Dict = None) -> str:
        """Retorna resposta baseada na intenção"""
        
        responses = self.intent_responses.get(intent, self.intent_responses["unknown"])
        base_response = random.choice(responses)
        
        # Personaliza resposta com entidades
        if entities:
            if "product_names" in entities:
                product = entities["product_names"][0]
                base_response += f" Vejo que você está interessado no plano {product}."
            
            if "emails" in entities:
                base_response += " Vou verificar as informações em nosso sistema."
        
        return base_response

class ConversationManager:
    """Gerenciador de conversas e contexto"""
    
    def __init__(self):
        self.conversations = {}  # conversation_id -> conversation_data
        self.user_sessions = {}  # user_id -> conversation_id
        
    def start_conversation(self, user_id: str, initial_message: str) -> str:
        """Inicia nova conversa"""
        
        conversation_id = str(uuid.uuid4())
        
        conversation_data = {
            "id": conversation_id,
            "user_id": user_id,
            "start_time": datetime.now(),
            "last_activity": datetime.now(),
            "messages": [],
            "context": {},
            "state": "active",
            "satisfaction": None,
            "resolved": False
        }
        
        # Adiciona mensagem inicial
        conversation_data["messages"].append({
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
            "message": initial_message,
            "intent": None
        })
        
        self.conversations[conversation_id] = conversation_data
        self.user_sessions[user_id] = conversation_id
        
        return conversation_id
    
    def add_message(self, conversation_id: str, sender: str, message: str, intent: str = None, metadata: Dict = None):
        """Adiciona mensagem à conversa"""
        
        if conversation_id not in self.conversations:
            return False
        
        message_data = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "message": message,
            "intent": intent,
            "metadata": metadata or {}
        }
        
        self.conversations[conversation_id]["messages"].append(message_data)
        self.conversations[conversation_id]["last_activity"] = datetime.now()
        
        return True
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Recupera dados da conversa"""
        return self.conversations.get(conversation_id)
    
    def get_user_conversation(self, user_id: str) -> Optional[Dict]:
        """Recupera conversa ativa do usuário"""
        
        conversation_id = self.user_sessions.get(user_id)
        if conversation_id:
            return self.conversations.get(conversation_id)
        return None
    
    def end_conversation(self, conversation_id: str, satisfaction_rating: int = None):
        """Finaliza conversa"""
        
        if conversation_id in self.conversations:
            self.conversations[conversation_id]["state"] = "ended"
            self.conversations[conversation_id]["end_time"] = datetime.now()
            self.conversations[conversation_id]["satisfaction"] = satisfaction_rating
            
            # Remove do session mapping
            user_id = self.conversations[conversation_id]["user_id"]
            if user_id in self.user_sessions:
                del self.user_sessions[user_id]
    
    def cleanup_old_conversations(self, max_age_hours: int = 24):
        """Remove conversas antigas"""
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        to_remove = []
        for conv_id, conv_data in self.conversations.items():
            if conv_data["last_activity"] < cutoff_time:
                to_remove.append(conv_id)
        
        for conv_id in to_remove:
            del self.conversations[conv_id]
        
        return len(to_remove)

class ChatbotAgent(BaseNetworkAgent):
    """
    Agente especializado em chatbot inteligente para suporte automatizado
    Implementa processamento de linguagem natural e gerenciamento de conversas
    """
    
    def __init__(self):
        super().__init__(
            agent_id="support_chatbot",
            agent_type="chatbot"
        )
        
        # Engine de processamento de linguagem natural
        self.nlp_engine = NaturalLanguageEngine()
        
        # Gerenciador de conversas
        self.conversation_manager = ConversationManager()
        
        # Configurações do chatbot
        self.config = {
            "max_conversation_length": 50,
            "auto_escalation_threshold": 3,  # 3 mensagens sem resolver
            "session_timeout_minutes": 30,
            "enable_sentiment_analysis": True,
            "enable_auto_responses": True
        }
        
        # Base de conhecimento simulada
        self.knowledge_base = {
            "password_reset": {
                "steps": [
                    "1. Acesse a página de login",
                    "2. Clique em 'Esqueci minha senha'",
                    "3. Digite seu email cadastrado",
                    "4. Verifique sua caixa de entrada",
                    "5. Clique no link recebido",
                    "6. Crie uma nova senha"
                ],
                "faq": "Como resetar minha senha?",
                "category": "Account"
            },
            "billing_question": {
                "info": "Para questões de faturamento, consulte 'Minha Conta > Faturas'",
                "contact": "Financeiro: (11) 99999-9999",
                "category": "Billing"
            },
            "feature_info": {
                "resources": "Acesse nosso tutorial em: help.exemplo.com",
                "video": "Vídeos explicativos disponíveis na plataforma",
                "category": "Help"
            }
        }
        
        # Estatísticas do chatbot
        self.stats = {
            "total_conversations": 0,
            "active_conversations": 0,
            "resolved_conversations": 0,
            "escalated_conversations": 0,
            "average_satisfaction": 0.0,
            "intents_detected": defaultdict(int),
            "response_times": deque(maxlen=1000)
        }
        
        logger.info(f"✅ Support Chatbot Agent iniciado: {self.agent_id}")

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagens do chatbot"""
        
        action = message.get("action", "chat")
        
        if action == "chat":
            return await self._process_chat_message(message.get("data", {}))
        
        elif action == "start_conversation":
            return await self._start_conversation(message.get("data", {}))
        
        elif action == "end_conversation":
            return await self._end_conversation(message.get("data", {}))
        
        elif action == "get_conversation":
            return self._get_conversation_data(message.get("data", {}))
        
        elif action == "analyze_intent":
            return await self._analyze_intent(message.get("data", {}))
        
        elif action == "escalate_conversation":
            return await self._escalate_conversation(message.get("data", {}))
        
        elif action == "get_suggestions":
            return await self._get_suggestions(message.get("data", {}))
        
        elif action == "get_chatbot_status":
            return self._get_chatbot_status()
        
        elif action == "update_knowledge_base":
            return await self._update_knowledge_base(message.get("data", {}))
        
        else:
            return {
                "error": f"Ação não reconhecida: {action}",
                "available_actions": [
                    "chat", "start_conversation", "end_conversation",
                    "get_conversation", "analyze_intent", "escalate_conversation",
                    "get_suggestions", "get_chatbot_status", "update_knowledge_base"
                ]
            }

    async def _process_chat_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem de chat do usuário"""
        
        try:
            user_id = data.get("user_id")
            message_text = data.get("message", "")
            conversation_id = data.get("conversation_id")
            
            if not user_id or not message_text:
                return {"error": "user_id e message são obrigatórios"}
            
            start_time = datetime.now()
            
            # Se não há conversation_id, inicia nova conversa
            if not conversation_id:
                conversation_id = self.conversation_manager.start_conversation(user_id, message_text)
                self.stats["total_conversations"] += 1
                self.stats["active_conversations"] += 1
            else:
                # Adiciona mensagem à conversa existente
                self.conversation_manager.add_message(
                    conversation_id, "user", message_text
                )
            
            # Analisa intenção da mensagem
            intent_analysis = self.nlp_engine.analyze_intent(message_text)
            intent = intent_analysis["intent"]
            confidence = intent_analysis["confidence"]
            entities = intent_analysis["entities"]
            
            # Atualiza estatísticas
            self.stats["intents_detected"][intent] += 1
            
            # Gera resposta baseada na intenção
            if confidence > 0.7:
                response_text = self.nlp_engine.get_response(intent, entities)
                
                # Adiciona informações da base de conhecimento se relevante
                if intent in self.knowledge_base:
                    kb_info = self.knowledge_base[intent]
                    if "steps" in kb_info:
                        response_text += "\n\nPassos detalhados:\n" + "\n".join(kb_info["steps"])
                    elif "info" in kb_info:
                        response_text += f"\n\nInformação adicional: {kb_info['info']}"
                
                escalation_needed = False
                
            elif confidence > 0.4:
                # Confiança média - pede esclarecimento
                response_text = "Entendo que você precisa de ajuda, mas pode ser mais específico sobre o que precisa?"
                escalation_needed = False
                
            else:
                # Baixa confiança - sugere escalonamento
                response_text = "Vou transferir você para um atendente humano que pode ajudar melhor."
                escalation_needed = True
            
            # Adiciona resposta do bot à conversa
            self.conversation_manager.add_message(
                conversation_id, "bot", response_text, intent,
                {"confidence": confidence, "entities": entities}
            )
            
            # Calcula tempo de resposta
            response_time = (datetime.now() - start_time).total_seconds()
            self.stats["response_times"].append(response_time)
            
            # Verifica se precisa escalonar
            conversation = self.conversation_manager.get_conversation(conversation_id)
            user_messages = [m for m in conversation["messages"] if m["sender"] == "user"]
            
            if len(user_messages) >= self.config["auto_escalation_threshold"] and not conversation.get("resolved"):
                escalation_needed = True
            
            result = {
                "status": "success",
                "conversation_id": conversation_id,
                "response": response_text,
                "intent_detected": intent,
                "confidence": confidence,
                "entities": entities,
                "escalation_needed": escalation_needed,
                "response_time": f"{response_time:.2f}s",
                "suggestions": self._generate_suggestions(intent, entities)
            }
            
            if escalation_needed:
                result["escalation_reason"] = "Low confidence or multiple attempts"
                self.stats["escalated_conversations"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Erro no processamento de chat: {str(e)}")
            return {"error": f"Falha no processamento: {str(e)}"}

    async def _start_conversation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Inicia nova conversa"""
        
        try:
            user_id = data.get("user_id")
            initial_message = data.get("message", "Olá, preciso de ajuda")
            
            if not user_id:
                return {"error": "user_id é obrigatório"}
            
            # Verifica se usuário já tem conversa ativa
            existing_conversation = self.conversation_manager.get_user_conversation(user_id)
            if existing_conversation and existing_conversation["state"] == "active":
                return {
                    "status": "existing_conversation",
                    "conversation_id": existing_conversation["id"],
                    "message": "Você já tem uma conversa ativa. Continuando..."
                }
            
            # Cria nova conversa
            conversation_id = self.conversation_manager.start_conversation(user_id, initial_message)
            
            # Gera mensagem de boas-vindas
            welcome_message = "Olá! Sou seu assistente virtual. Como posso ajudá-lo hoje?"
            
            self.conversation_manager.add_message(
                conversation_id, "bot", welcome_message, "greeting"
            )
            
            self.stats["total_conversations"] += 1
            self.stats["active_conversations"] += 1
            
            return {
                "status": "success",
                "conversation_id": conversation_id,
                "welcome_message": welcome_message,
                "available_commands": [
                    "Digite sua dúvida ou problema",
                    "Digite 'ajuda' para ver opções",
                    "Digite 'humano' para falar com atendente"
                ]
            }
            
        except Exception as e:
            logger.error(f"Erro ao iniciar conversa: {str(e)}")
            return {"error": f"Falha ao iniciar conversa: {str(e)}"}

    async def _end_conversation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Finaliza conversa"""
        
        try:
            conversation_id = data.get("conversation_id")
            satisfaction_rating = data.get("satisfaction_rating")
            reason = data.get("reason", "user_request")
            
            if not conversation_id:
                return {"error": "conversation_id é obrigatório"}
            
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if not conversation:
                return {"error": "Conversa não encontrada"}
            
            # Finaliza conversa
            self.conversation_manager.end_conversation(conversation_id, satisfaction_rating)
            
            # Atualiza estatísticas
            if conversation["state"] == "active":
                self.stats["active_conversations"] -= 1
            
            if reason == "resolved":
                self.stats["resolved_conversations"] += 1
            
            if satisfaction_rating:
                # Atualiza média de satisfação
                current_avg = self.stats["average_satisfaction"]
                total_rated = self.stats["resolved_conversations"]
                
                if total_rated > 1:
                    new_avg = ((current_avg * (total_rated - 1)) + satisfaction_rating) / total_rated
                else:
                    new_avg = satisfaction_rating
                
                self.stats["average_satisfaction"] = new_avg
            
            # Gera resumo da conversa
            messages = conversation["messages"]
            duration = (datetime.now() - conversation["start_time"]).total_seconds() / 60
            
            conversation_summary = {
                "conversation_id": conversation_id,
                "duration_minutes": round(duration, 1),
                "total_messages": len(messages),
                "user_messages": len([m for m in messages if m["sender"] == "user"]),
                "bot_messages": len([m for m in messages if m["sender"] == "bot"]),
                "intents_detected": list(set(m["intent"] for m in messages if m.get("intent"))),
                "satisfaction_rating": satisfaction_rating,
                "resolution_status": reason
            }
            
            return {
                "status": "success",
                "message": "Conversa finalizada com sucesso",
                "summary": conversation_summary
            }
            
        except Exception as e:
            logger.error(f"Erro ao finalizar conversa: {str(e)}")
            return {"error": f"Falha ao finalizar conversa: {str(e)}"}

    async def _analyze_intent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa intenção de uma mensagem"""
        
        try:
            text = data.get("text", "")
            
            if not text:
                return {"error": "Texto não fornecido"}
            
            analysis = self.nlp_engine.analyze_intent(text)
            
            # Adiciona sugestões de resposta
            suggested_responses = self.nlp_engine.intent_responses.get(
                analysis["intent"], 
                self.nlp_engine.intent_responses["unknown"]
            )
            
            return {
                "status": "success",
                "analysis": analysis,
                "suggested_responses": suggested_responses[:3],  # Top 3 sugestões
                "knowledge_base_match": analysis["intent"] in self.knowledge_base
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de intenção: {str(e)}")
            return {"error": f"Falha na análise: {str(e)}"}

    async def _escalate_conversation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Escalona conversa para atendente humano"""
        
        try:
            conversation_id = data.get("conversation_id")
            reason = data.get("reason", "user_request")
            priority = data.get("priority", "normal")
            
            if not conversation_id:
                return {"error": "conversation_id é obrigatório"}
            
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if not conversation:
                return {"error": "Conversa não encontrada"}
            
            # Marca conversa como escalada
            conversation["state"] = "escalated"
            conversation["escalation"] = {
                "timestamp": datetime.now().isoformat(),
                "reason": reason,
                "priority": priority
            }
            
            # Adiciona mensagem de escalação
            escalation_message = "Transferindo você para um atendente humano. Aguarde um momento..."
            
            self.conversation_manager.add_message(
                conversation_id, "bot", escalation_message, "escalation",
                {"reason": reason, "priority": priority}
            )
            
            # Atualiza estatísticas
            self.stats["escalated_conversations"] += 1
            
            # Prepara contexto para o atendente
            context = {
                "conversation_id": conversation_id,
                "user_id": conversation["user_id"],
                "messages": conversation["messages"][-10:],  # Últimas 10 mensagens
                "intents_detected": list(set(m["intent"] for m in conversation["messages"] if m.get("intent"))),
                "escalation_reason": reason,
                "priority": priority
            }
            
            return {
                "status": "success",
                "message": "Conversa escalada com sucesso",
                "escalation_id": f"ESC_{conversation_id[:8]}",
                "estimated_wait_time": "5-10 minutos",
                "context_for_agent": context
            }
            
        except Exception as e:
            logger.error(f"Erro no escalonamento: {str(e)}")
            return {"error": f"Falha no escalonamento: {str(e)}"}

    async def _get_suggestions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sugestões baseadas no contexto"""
        
        try:
            conversation_id = data.get("conversation_id")
            intent = data.get("intent")
            entities = data.get("entities", {})
            
            suggestions = []
            
            if intent:
                # Sugestões baseadas na intenção
                if intent == "password_reset":
                    suggestions.extend([
                        "Você tem acesso ao email cadastrado?",
                        "Já tentou usar a opção 'Esqueci minha senha'?",
                        "Quer que eu envie um link de redefinição?"
                    ])
                
                elif intent == "billing_question":
                    suggestions.extend([
                        "Qual é sua dúvida específica sobre a fatura?",
                        "Precisa alterar a forma de pagamento?",
                        "Gostaria de ver o histórico de cobranças?"
                    ])
                
                elif intent == "technical_support":
                    suggestions.extend([
                        "Pode descrever o erro em detalhes?",
                        "Quando o problema começou?",
                        "Já tentou reiniciar o sistema?"
                    ])
            
            # Sugestões baseadas em entidades
            if "emails" in entities:
                suggestions.append("Vou verificar as informações deste email em nosso sistema")
            
            if "product_names" in entities:
                product = entities["product_names"][0]
                suggestions.append(f"Posso ajudar com questões específicas do plano {product}")
            
            # Sugestões gerais se não há contexto específico
            if not suggestions:
                suggestions.extend([
                    "Como posso ajudá-lo hoje?",
                    "Tem alguma dúvida específica?",
                    "Precisa de ajuda com alguma funcionalidade?"
                ])
            
            return {
                "status": "success",
                "suggestions": suggestions,
                "context_based": bool(intent or entities),
                "total_suggestions": len(suggestions)
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {str(e)}")
            return {"error": f"Falha ao gerar sugestões: {str(e)}"}

    def _get_conversation_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recupera dados da conversa"""
        
        try:
            conversation_id = data.get("conversation_id")
            user_id = data.get("user_id")
            
            if conversation_id:
                conversation = self.conversation_manager.get_conversation(conversation_id)
            elif user_id:
                conversation = self.conversation_manager.get_user_conversation(user_id)
            else:
                return {"error": "conversation_id ou user_id é obrigatório"}
            
            if not conversation:
                return {"error": "Conversa não encontrada"}
            
            return {
                "status": "success",
                "conversation": conversation
            }
            
        except Exception as e:
            logger.error(f"Erro ao recuperar conversa: {str(e)}")
            return {"error": f"Falha ao recuperar conversa: {str(e)}"}

    async def _update_knowledge_base(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza base de conhecimento"""
        
        try:
            intent = data.get("intent")
            content = data.get("content", {})
            
            if not intent:
                return {"error": "intent é obrigatório"}
            
            # Atualiza ou adiciona na base de conhecimento
            if intent in self.knowledge_base:
                self.knowledge_base[intent].update(content)
            else:
                self.knowledge_base[intent] = content
            
            return {
                "status": "success",
                "message": f"Base de conhecimento atualizada para intent: {intent}",
                "total_intents": len(self.knowledge_base)
            }
            
        except Exception as e:
            logger.error(f"Erro ao atualizar base de conhecimento: {str(e)}")
            return {"error": f"Falha na atualização: {str(e)}"}

    def _get_chatbot_status(self) -> Dict[str, Any]:
        """Retorna status e estatísticas do chatbot"""
        
        uptime = datetime.now() - self.created_at
        
        # Calcula tempo médio de resposta
        avg_response_time = 0
        if self.stats["response_times"]:
            avg_response_time = sum(self.stats["response_times"]) / len(self.stats["response_times"])
        
        return {
            "agent_status": self.get_status(),
            "chatbot_statistics": {
                **self.stats,
                "intents_detected": dict(self.stats["intents_detected"]),
                "response_times": list(self.stats["response_times"])[-10:]  # Últimos 10
            },
            "configuration": self.config,
            "knowledge_base": {
                "total_intents": len(self.knowledge_base),
                "available_intents": list(self.knowledge_base.keys())
            },
            "uptime": str(uptime),
            "performance_metrics": {
                "avg_response_time": f"{avg_response_time:.2f}s",
                "resolution_rate": f"{(self.stats['resolved_conversations'] / max(self.stats['total_conversations'], 1)) * 100:.1f}%",
                "escalation_rate": f"{(self.stats['escalated_conversations'] / max(self.stats['total_conversations'], 1)) * 100:.1f}%",
                "avg_satisfaction": f"{self.stats['average_satisfaction']:.1f}/5",
                "active_conversations": self.stats["active_conversations"]
            }
        }

    # Métodos auxiliares
    
    def _generate_suggestions(self, intent: str, entities: Dict) -> List[str]:
        """Gera sugestões rápidas baseadas no contexto"""
        
        suggestions = []
        
        if intent == "greeting":
            suggestions = ["Como posso ajudar?", "Qual sua dúvida?", "Em que posso ser útil?"]
        
        elif intent == "password_reset":
            suggestions = ["Enviar link por email", "Verificar email cadastrado", "Falar com suporte"]
        
        elif intent == "billing_question":
            suggestions = ["Ver fatura atual", "Alterar pagamento", "Falar com financeiro"]
        
        else:
            suggestions = ["Precisa de mais ajuda?", "Posso esclarecer algo?", "Falar com atendente"]
        
        return suggestions

# Função obrigatória para o Agent Loader
def create_agents() -> List[BaseNetworkAgent]:
    """
    Função obrigatória para criação dos agentes deste módulo
    Retorna lista de agentes instanciados
    """
    try:
        # Cria instância do agente chatbot
        chatbot_agent = ChatbotAgent()
        
        logger.info("✅ Support Chatbot Agent criado com sucesso")
        
        return [chatbot_agent]
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar Support Chatbot Agent: {str(e)}")
        return []

# Teste standalone
if __name__ == "__main__":
    async def test_chatbot_agent():
        """Teste completo do agente chatbot"""
        print("🧪 Testando Support Chatbot Agent...")
        
        # Cria agente
        agents = create_agents()
        if not agents:
            print("❌ Falha na criação do agente")
            return
        
        agent = agents[0]
        print(f"✅ Agente criado: {agent.agent_id}")
        
        # Teste 1: Iniciar conversa
        print("\n💬 Teste 1: Iniciando conversa...")
        
        message = {
            "action": "start_conversation",
            "data": {
                "user_id": "user123",
                "message": "Oi, preciso de ajuda"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            conversation_id = response['conversation_id']
            print(f"  • Conversa iniciada: {conversation_id}")
            print(f"  • Mensagem de boas-vindas: {response['welcome_message']}")
        
        # Teste 2: Chat sobre reset de senha
        print("\n🔐 Teste 2: Chat sobre reset de senha...")
        
        message = {
            "action": "chat",
            "data": {
                "user_id": "user123",
                "conversation_id": conversation_id,
                "message": "Esqueci minha senha, como faço para resetar?"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Intent detectado: {response['intent_detected']}")
            print(f"  • Confiança: {response['confidence']:.2f}")
            print(f"  • Resposta: {response['response'][:100]}...")
            print(f"  • Escalação necessária: {response['escalation_needed']}")
        
        # Teste 3: Chat sobre cobrança
        print("\n💰 Teste 3: Chat sobre cobrança...")
        
        message = {
            "action": "chat",
            "data": {
                "user_id": "user123",
                "conversation_id": conversation_id,
                "message": "Minha fatura veio com valor errado, como posso contestar?"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Intent: {response['intent_detected']}")
            print(f"  • Entidades encontradas: {response.get('entities', {})}")
            print(f"  • Sugestões: {response.get('suggestions', [])}")
        
        # Teste 4: Análise de intenção
        print("\n🔍 Teste 4: Análise de intenção...")
        
        message = {
            "action": "analyze_intent",
            "data": {
                "text": "O sistema está travando e não consigo acessar minha conta"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            analysis = response['analysis']
            print(f"  • Intent detectado: {analysis['intent']}")
            print(f"  • Confiança: {analysis['confidence']:.2f}")
            print(f"  • Todas as pontuações: {analysis.get('all_scores', {})}")
            print(f"  • Match na KB: {response['knowledge_base_match']}")
        
        # Teste 5: Escalonamento
        print("\n🔄 Teste 5: Escalonamento para humano...")
        
        message = {
            "action": "escalate_conversation",
            "data": {
                "conversation_id": conversation_id,
                "reason": "complex_technical_issue",
                "priority": "high"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Escalação ID: {response['escalation_id']}")
            print(f"  • Tempo estimado: {response['estimated_wait_time']}")
            print(f"  • Contexto preparado: {len(response['context_for_agent']['messages'])} mensagens")
        
        # Teste 6: Finalizar conversa
        print("\n✅ Teste 6: Finalizando conversa...")
        
        message = {
            "action": "end_conversation",
            "data": {
                "conversation_id": conversation_id,
                "satisfaction_rating": 4,
                "reason": "resolved"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            summary = response['summary']
            print(f"  • Duração: {summary['duration_minutes']} minutos")
            print(f"  • Total mensagens: {summary['total_messages']}")
            print(f"  • Intents detectados: {summary['intents_detected']}")
            print(f"  • Satisfação: {summary['satisfaction_rating']}/5")
        
        # Teste 7: Status do chatbot
        print("\n📊 Teste 7: Status do chatbot...")
        
        message = {"action": "get_chatbot_status"}
        result = await agent._internal_handle_message(message)
        
        if result['status'] == 'success':
            response = result['response']
            stats = response['chatbot_statistics']
            performance = response['performance_metrics']
            
            print(f"  • Conversas totais: {stats['total_conversations']}")
            print(f"  • Conversas ativas: {stats['active_conversations']}")
            print(f"  • Taxa de resolução: {performance['resolution_rate']}")
            print(f"  • Taxa de escalonamento: {performance['escalation_rate']}")
            print(f"  • Satisfação média: {performance['avg_satisfaction']}")
            print(f"  • Tempo médio resposta: {performance['avg_response_time']}")
            
            kb = response['knowledge_base']
            print(f"  • Intents na base: {kb['total_intents']}")
            print(f"  • Intents disponíveis: {', '.join(kb['available_intents'])}")
        
        print(f"\n✅ Todos os testes concluídos! Agente funcionando perfeitamente.")
        print(f"🎯 Support Chatbot Agent - Status: OPERACIONAL")
    
    # Executa teste
    asyncio.run(test_chatbot_agent())
