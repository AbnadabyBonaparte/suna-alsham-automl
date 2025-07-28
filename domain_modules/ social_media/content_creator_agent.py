#!/usr/bin/env python3
"""
Módulo do Content Creator Agent - ALSHAM GLOBAL

[Fase 3] - Fortalecido com cache inteligente e melhor tratamento de erros.
Este super agente de negócio é responsável por gerar conteúdo de alta qualidade
(posts, artigos, scripts) usando IA, adaptado para diferentes plataformas.
"""

import asyncio
import logging
import os
from typing import Any, Dict, List

# [AUTENTICIDADE] A biblioteca da OpenAI é importada de forma segura.
try:
    import openai
    from openai import error as openai_error
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Importa a classe base e as ferramentas do nosso núcleo fortalecido
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Configuração da API OpenAI ---
if OPENAI_AVAILABLE:
    openai.api_key = os.getenv("OPENAI_API_KEY")


class ContentCreatorAgent(BaseNetworkAgent):
    """
    Gera conteúdo viral automaticamente, cria posts, artigos e scripts,
    e adapta o tom e estilo por plataforma.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ContentCreatorAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        self.capabilities.extend([
            "content_generation",
            "style_adaptation",
            "viral_content_creation",
        ])

        if not OPENAI_AVAILABLE or not openai.api_key:
            self.status = "degraded"
            logger.warning(f"Agente {agent_id} operando em modo degradado: OpenAI não configurado.")
        
        # [LÓGICA REAL] Cache para evitar chamadas repetidas à API.
        self.content_cache = {}
        
        logger.info(f"✍️ {self.agent_id} (Criador de Conteúdo) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para criação de conteúdo."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "generate_content":
            result = await self._generate_content_handler(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de criação desconhecida"))

    async def _generate_content_handler(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Gera conteúdo utilizando a API da OpenAI com prompts inteligentes,
        cache e tratamento de erros aprimorado.
        """
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de IA indisponível."}

        content_type = request_data.get("content_type", "tweet")
        topic = request_data.get("topic", "tecnologia")
        tone = request_data.get("tone", "informativo")
        target_audience = request_data.get("target_audience", "entusiastas de tecnologia")

        # Gera uma chave única para o cache
        cache_key = f"{content_type}:{topic}:{tone}:{target_audience}"
        if cache_key in self.content_cache:
            logger.info(f"Cache HIT para: {cache_key}")
            return {"status": "completed_from_cache", "generated_content": self.content_cache[cache_key]}
        
        logger.info(f"Cache MISS. Gerando conteúdo novo para: {cache_key}")

        try:
            prompt = self._build_intelligent_prompt(content_type, topic, tone, target_audience)
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um especialista em marketing digital e criação de conteúdo viral."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            
            generated_content = response.choices[0].message.content.strip()
            self.content_cache[cache_key] = generated_content # Salva no cache
            
            return {"status": "completed", "generated_content": generated_content}

        except openai_error.RateLimitError:
            logger.error("❌ Erro de Rate Limit da API OpenAI. Aguardando para tentar novamente.")
            return {"status": "error", "message": "API da OpenAI com excesso de requisições. Tente mais tarde."}
        except Exception as e:
            logger.error(f"❌ Erro ao gerar conteúdo com IA: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _build_intelligent_prompt(self, content_type: str, topic: str, tone: str, audience: str) -> str:
        """Constrói um prompt otimizado para a geração de conteúdo."""
        prompt = f"Crie um conteúdo do tipo '{content_type}' para o público '{audience}' sobre o tópico '{topic}'. O tom deve ser '{tone}'."
        if content_type == "tweet":
            prompt += " O conteúdo deve ser curto, impactante e incluir 2-3 hashtags relevantes. Não exceda 280 caracteres."
        elif content_type == "post_linkedin":
            prompt += " O post deve ser profissional, começar com uma frase de gancho forte, usar parágrafos curtos e emojis para escaneabilidade, e terminar com uma pergunta para engajar. Inclua 3-5 hashtags de negócio."
        elif content_type == "article_script":
            prompt += " Crie um roteiro para um artigo de blog ou vídeo curto (1 minuto). A estrutura deve ser: Introdução com gancho, 3 pontos principais com exemplos, e uma conclusão com uma chamada para ação (call to action)."
        return prompt


def create_content_creator_agent(message_bus) -> List[ContentCreatorAgent]:
    """Cria o agente Criador de Conteúdo."""
    agents = []
    logger.info("✍️ Criando ContentCreatorAgent...")
    try:
        agent = ContentCreatorAgent("content_creator_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ContentCreatorAgent: {e}", exc_info=True)
    return agents
