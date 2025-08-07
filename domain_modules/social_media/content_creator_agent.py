"""
ALSHAM QUANTUM - Content Creator Agent (Social Media Module)
Versão Nativa - Sem dependências SUNA-ALSHAM
Corrigido em: 07/08/2025

Agente especializado em:
- Geração de conteúdo multi-formato
- Criação de campanhas de marketing
- Copywriting otimizado para conversão
- Personalização de conteúdo por audiência
- A/B testing de mensagens
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
import hashlib
from collections import defaultdict

# Imports opcionais para IA generativa
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

import os

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

class ContentType(Enum):
    """Tipos de conteúdo suportados"""
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA_POST = "social_media_post"
    EMAIL_CAMPAIGN = "email_campaign"
    AD_COPY = "ad_copy"
    PRODUCT_DESCRIPTION = "product_description"
    PRESS_RELEASE = "press_release"
    LANDING_PAGE = "landing_page"
    VIDEO_SCRIPT = "video_script"
    PODCAST_SCRIPT = "podcast_script"
    NEWSLETTER = "newsletter"

class Platform(Enum):
    """Plataformas de mídia social"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"

class Tone(Enum):
    """Tom de voz do conteúdo"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    URGENT = "urgent"
    EDUCATIONAL = "educational"

class Audience(Enum):
    """Tipos de audiência"""
    B2B_EXECUTIVES = "b2b_executives"
    B2B_TECHNICAL = "b2b_technical"
    B2C_MILLENNIALS = "b2c_millennials"
    B2C_GEN_Z = "b2c_gen_z"
    B2C_GEN_X = "b2c_gen_x"
    ENTERPRISE = "enterprise"
    SMB = "smb"
    GENERAL_PUBLIC = "general_public"

@dataclass
class ContentRequest:
    """Requisição de criação de conteúdo"""
    request_id: str
    content_type: ContentType
    platform: Optional[Platform]
    tone: Tone
    audience: Audience
    topic: str
    key_messages: List[str]
    call_to_action: str
    constraints: Dict[str, Any]  # character limits, keywords, etc.
    context_data: Dict[str, Any]
    brand_guidelines: Dict[str, Any]

@dataclass
class GeneratedContent:
    """Conteúdo gerado"""
    content_id: str
    content_type: ContentType
    platform: Optional[Platform]
    title: str
    body: str
    hashtags: List[str]
    call_to_action: str
    metadata: Dict[str, Any]
    performance_prediction: Dict[str, float]
    variations: List[Dict[str, str]]  # A/B test variations
    seo_score: float
    readability_score: float

@dataclass
class ContentVariation:
    """Variação de conteúdo para A/B testing"""
    variation_id: str
    title: str
    body: str
    test_hypothesis: str
    expected_improvement: str
    target_metric: str

@dataclass
class ContentAnalysis:
    """Análise de qualidade do conteúdo"""
    analysis_id: str
    content_id: str
    sentiment_score: float
    engagement_prediction: float
    conversion_prediction: float
    seo_keywords: List[str]
    readability_issues: List[str]
    suggestions: List[str]

class ContentCreatorAgent(BaseNetworkAgent):
    """Agente Criador de Conteúdo nativo do ALSHAM QUANTUM"""
    
    def __init__(self):
        super().__init__("content_creator_agent", "Content Creator Agent")
        
        # Configuração da OpenAI (opcional)
        self.openai_client = None
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            self.ai_enabled = True
            self.logger.info("OpenAI integração ativada")
        else:
            self.ai_enabled = False
            self.logger.info("Modo nativo sem OpenAI - usando templates inteligentes")
        
        # Templates de conteúdo por tipo
        self.content_templates = {
            ContentType.SOCIAL_MEDIA_POST: {
                "structure": ["hook", "value", "cta"],
                "max_length": {"twitter": 280, "instagram": 2200, "facebook": 63206, "linkedin": 3000}
            },
            ContentType.BLOG_POST: {
                "structure": ["headline", "intro", "body", "conclusion", "cta"],
                "min_words": 800,
                "max_words": 2500
            },
            ContentType.EMAIL_CAMPAIGN: {
                "structure": ["subject", "preview", "greeting", "body", "cta", "signature"],
                "subject_max_chars": 50
            },
            ContentType.AD_COPY: {
                "structure": ["headline", "description", "cta"],
                "headline_max_chars": 30,
                "description_max_chars": 90
            }
        }
        
        # Configurações por plataforma
        self.platform_configs = {
            Platform.INSTAGRAM: {
                "hashtag_limit": 30,
                "character_limit": 2200,
                "optimal_hashtags": 11,
                "best_times": ["11:00", "13:00", "17:00"]
            },
            Platform.TWITTER: {
                "character_limit": 280,
                "hashtag_limit": 2,
                "optimal_length": 100,
                "best_times": ["12:00", "15:00", "17:00"]
            },
            Platform.LINKEDIN: {
                "character_limit": 3000,
                "hashtag_limit": 3,
                "optimal_length": 150,
                "best_times": ["08:00", "12:00", "17:00"]
            },
            Platform.FACEBOOK: {
                "character_limit": 63206,
                "optimal_length": 80,
                "hashtag_limit": 2,
                "best_times": ["13:00", "15:00", "19:00"]
            }
        }
        
        # Cache de conteúdo gerado
        self.content_cache = {}
        
        # Base de conhecimento
        self.knowledge_base = {
            "power_words": {
                "urgency": ["agora", "limitado", "último", "exclusivo", "urgente"],
                "emotion": ["incrível", "fantástico", "surpreendente", "revolucionário"],
                "credibility": ["comprovado", "garantido", "testado", "aprovado"]
            },
            "cta_templates": {
                "sales": ["Compre Agora", "Garanta o Seu", "Aproveite a Oferta"],
                "engagement": ["Saiba Mais", "Descubra", "Explore"],
                "conversion": ["Cadastre-se", "Baixe Grátis", "Comece Hoje"]
            },
            "hashtag_categories": {
                "marketing": ["#marketing", "#digitalmarketing", "#contentmarketing"],
                "business": ["#business", "#entrepreneur", "#startup"],
                "tech": ["#technology", "#innovation", "#ai"]
            }
        }
        
        self.logger.info("Content Creator Agent inicializado com engine nativo")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de criação de conteúdo"""
        try:
            action = data.get("action", "generate_content")
            
            if action == "generate_content":
                return await self._generate_content(data)
            elif action == "create_campaign":
                return await self._create_campaign(data)
            elif action == "generate_variations":
                return await self._generate_content_variations(data)
            elif action == "analyze_content":
                return await self._analyze_content(data)
            elif action == "optimize_for_platform":
                return await self._optimize_for_platform(data)
            elif action == "generate_hashtags":
                return await self._generate_hashtags(data)
            elif action == "content_calendar":
                return await self._generate_content_calendar(data)
            elif action == "competitor_analysis":
                return await self._analyze_competitor_content(data)
            else:
                return {"error": f"Ação não reconhecida: {action}"}
                
        except Exception as e:
            self.logger.error(f"Erro na criação de conteúdo: {str(e)}")
            return {"error": str(e)}

    async def _generate_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera conteúdo baseado na requisição"""
        
        # Criar requisição estruturada
        content_request = self._build_content_request(data)
        
        # Gerar conteúdo principal
        if self.ai_enabled:
            generated_content = await self._generate_with_ai(content_request)
        else:
            generated_content = await self._generate_with_templates(content_request)
        
        # Gerar variações para A/B testing
        variations = await self._create_ab_variations(generated_content, content_request)
        
        # Análise de qualidade
        content_analysis = await self._perform_content_analysis(generated_content)
        
        # Otimizações por plataforma
        platform_optimizations = {}
        if content_request.platform:
            platform_optimizations = await self._optimize_for_specific_platform(
                generated_content, content_request.platform
            )
        
        # Salvar no cache
        content_id = str(uuid.uuid4())
        self.content_cache[content_id] = {
            "request": asdict(content_request),
            "content": asdict(generated_content),
            "analysis": asdict(content_analysis),
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "content_id": content_id,
            "content": {
                "title": generated_content.title,
                "body": generated_content.body,
                "hashtags": generated_content.hashtags,
                "call_to_action": generated_content.call_to_action,
                "metadata": generated_content.metadata
            },
            "variations": [
                {
                    "variation_id": var.variation_id,
                    "title": var.title,
                    "body": var.body,
                    "hypothesis": var.test_hypothesis,
                    "target_metric": var.target_metric
                } for var in variations
            ],
            "analysis": {
                "sentiment_score": content_analysis.sentiment_score,
                "engagement_prediction": content_analysis.engagement_prediction,
                "conversion_prediction": content_analysis.conversion_prediction,
                "seo_score": generated_content.seo_score,
                "readability_score": generated_content.readability_score,
                "suggestions": content_analysis.suggestions
            },
            "platform_optimizations": platform_optimizations,
            "performance_prediction": generated_content.performance_prediction,
            "timestamp": datetime.now().isoformat()
        }

    async def _generate_with_ai(self, request: ContentRequest) -> GeneratedContent:
        """Gera conteúdo usando IA (OpenAI)"""
        
        # Construir prompt contextual
        prompt = self._build_ai_prompt(request)
        
        try:
            # Chamada para OpenAI
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em criação de conteúdo e marketing digital."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            generated_text = response.choices[0].message.content
            
            # Processar resposta estruturada
            content_parts = self._parse_ai_response(generated_text, request.content_type)
            
        except Exception as e:
            self.logger.error(f"Erro na geração com IA: {str(e)}")
            # Fallback para templates
            return await self._generate_with_templates(request)
        
        # Gerar hashtags inteligentes
        hashtags = self._generate_intelligent_hashtags(request.topic, request.platform)
        
        # Calcular scores
        seo_score = self._calculate_seo_score(content_parts["body"], request.topic)
        readability_score = self._calculate_readability_score(content_parts["body"])
        
        return GeneratedContent(
            content_id=str(uuid.uuid4()),
            content_type=request.content_type,
            platform=request.platform,
            title=content_parts.get("title", ""),
            body=content_parts.get("body", ""),
            hashtags=hashtags,
            call_to_action=content_parts.get("cta", request.call_to_action),
            metadata={
                "word_count": len(content_parts.get("body", "").split()),
                "character_count": len(content_parts.get("body", "")),
                "generated_with": "openai",
                "model": "gpt-4o-mini"
            },
            performance_prediction={
                "engagement_rate": 0.05 + (seo_score * 0.02),
                "click_through_rate": 0.02 + (readability_score * 0.01),
                "conversion_rate": 0.01 + (seo_score * readability_score * 0.005)
            },
            variations=[],
            seo_score=seo_score,
            readability_score=readability_score
        )

    async def _generate_with_templates(self, request: ContentRequest) -> GeneratedContent:
        """Gera conteúdo usando templates inteligentes"""
        
        # Obter template para o tipo de conteúdo
        template_config = self.content_templates.get(request.content_type, {})
        
        # Gerar título
        title = self._generate_template_title(request)
        
        # Gerar corpo do conteúdo
        body = self._generate_template_body(request, template_config)
        
        # Gerar hashtags
        hashtags = self._generate_intelligent_hashtags(request.topic, request.platform)
        
        # Calcular scores
        seo_score = self._calculate_seo_score(body, request.topic)
        readability_score = self._calculate_readability_score(body)
        
        return GeneratedContent(
            content_id=str(uuid.uuid4()),
            content_type=request.content_type,
            platform=request.platform,
            title=title,
            body=body,
            hashtags=hashtags,
            call_to_action=request.call_to_action,
            metadata={
                "word_count": len(body.split()),
                "character_count": len(body),
                "generated_with": "templates",
                "template_used": request.content_type.value
            },
            performance_prediction={
                "engagement_rate": 0.03 + (seo_score * 0.015),
                "click_through_rate": 0.015 + (readability_score * 0.008),
                "conversion_rate": 0.008 + (seo_score * readability_score * 0.003)
            },
            variations=[],
            seo_score=seo_score,
            readability_score=readability_score
        )

    def _build_ai_prompt(self, request: ContentRequest) -> str:
        """Constrói prompt para IA generativa"""
        
        platform_info = ""
        if request.platform:
            config = self.platform_configs.get(request.platform, {})
            platform_info = f"""
Plataforma: {request.platform.value}
Limite de caracteres: {config.get('character_limit', 'N/A')}
Hashtags recomendadas: {config.get('optimal_hashtags', 'N/A')}
"""
        
        constraints_info = ""
        if request.constraints:
            constraints_info = f"Restrições: {json.dumps(request.constraints, ensure_ascii=False)}"
        
        prompt = f"""
Crie conteúdo de alta qualidade para {request.content_type.value} com as seguintes especificações:

TÓPICO: {request.topic}
TOM: {request.tone.value}
AUDIÊNCIA: {request.audience.value}
MENSAGENS-CHAVE: {', '.join(request.key_messages)}
CALL-TO-ACTION: {request.call_to_action}

{platform_info}
{constraints_info}

DADOS CONTEXTUAIS:
{json.dumps(request.context_data, ensure_ascii=False, indent=2)}

DIRETRIZES DA MARCA:
{json.dumps(request.brand_guidelines, ensure_ascii=False, indent=2)}

Por favor, forneça:
1. TÍTULO: Um título impactante e otimizado
2. CORPO: Conteúdo principal seguindo as melhores práticas
3. CTA: Call-to-action otimizado (pode melhorar o fornecido)

Formato de resposta:
TÍTULO: [título aqui]
CORPO: [conteúdo principal aqui]
CTA: [call to action aqui]
"""
        
        return prompt

    def _parse_ai_response(self, response_text: str, content_type: ContentType) -> Dict[str, str]:
        """Parseia resposta estruturada da IA"""
        
        parts = {}
        current_section = None
        current_content = []
        
        for line in response_text.split('\n'):
            line = line.strip()
            
            if line.startswith('TÍTULO:'):
                if current_section:
                    parts[current_section] = '\n'.join(current_content).strip()
                current_section = 'title'
                current_content = [line.replace('TÍTULO:', '').strip()]
                
            elif line.startswith('CORPO:'):
                if current_section:
                    parts[current_section] = '\n'.join(current_content).strip()
                current_section = 'body'
                current_content = [line.replace('CORPO:', '').strip()]
                
            elif line.startswith('CTA:'):
                if current_section:
                    parts[current_section] = '\n'.join(current_content).strip()
                current_section = 'cta'
                current_content = [line.replace('CTA:', '').strip()]
                
            else:
                if current_section:
                    current_content.append(line)
                    
        # Adicionar última seção
        if current_section:
            parts[current_section] = '\n'.join(current_content).strip()
        
        # Fallbacks se parsing falhar
        if 'title' not in parts:
            parts['title'] = response_text[:100] + "..." if len(response_text) > 100 else response_text
        if 'body' not in parts:
            parts['body'] = response_text
        if 'cta' not in parts:
            parts['cta'] = "Saiba mais"
            
        return parts

    def _generate_template_title(self, request: ContentRequest) -> str:
        """Gera título usando templates"""
        
        # Templates por tipo de conteúdo
        title_templates = {
            ContentType.BLOG_POST: [
                f"Como {request.topic} Pode Transformar Seu Negócio",
                f"O Guia Definitivo de {request.topic}",
                f"5 Estratégias Poderosas para {request.topic}"
            ],
            ContentType.SOCIAL_MEDIA_POST: [
                f"🚀 Descubra o poder de {request.topic}",
                f"💡 {request.topic}: A chave para o sucesso",
                f"✨ Transforme seu negócio com {request.topic}"
            ],
            ContentType.EMAIL_CAMPAIGN: [
                f"Exclusivo: Novidades sobre {request.topic}",
                f"Última chance: {request.topic}",
                f"Descubra como {request.topic} pode ajudar você"
            ]
        }
        
        templates = title_templates.get(request.content_type, [f"Tudo sobre {request.topic}"])
        
        # Adicionar power words baseado no tom
        if request.tone == Tone.URGENT:
            return f"🚨 URGENTE: {templates[0]}"
        elif request.tone == Tone.INSPIRATIONAL:
            return f"💫 {templates[0]}"
        else:
            return templates[0]

    def _generate_template_body(self, request: ContentRequest, template_config: Dict) -> str:
        """Gera corpo do conteúdo usando templates"""
        
        # Estrutura base por tipo
        if request.content_type == ContentType.SOCIAL_MEDIA_POST:
            return self._generate_social_post_body(request)
        elif request.content_type == ContentType.BLOG_POST:
            return self._generate_blog_post_body(request)
        elif request.content_type == ContentType.EMAIL_CAMPAIGN:
            return self._generate_email_body(request)
        else:
            return self._generate_generic_body(request)

    def _generate_social_post_body(self, request: ContentRequest) -> str:
        """Gera corpo para post de mídia social"""
        
        # Hook inicial
        hooks = [
            "Você sabia que...",
            "Imagine se você pudesse...",
            "A maioria das pessoas não percebe que...",
            "Existe um segredo que..."
        ]
        
        hook = hooks[hash(request.topic) % len(hooks)]
        
        # Corpo principal com mensagens-chave
        key_messages_text = " ".join([f"✅ {msg}" for msg in request.key_messages[:3]])
        
        body = f"""{hook} {request.topic} pode revolucionar a forma como você trabalha!

{key_messages_text}

{request.context_data.get('additional_info', 'Descubra mais sobre esta incrível oportunidade.')}

Não perca essa chance! 👇"""
        
        return body

    def _generate_blog_post_body(self, request: ContentRequest) -> str:
        """Gera corpo para blog post"""
        
        intro = f"Nos últimos anos, {request.topic} tem se tornado cada vez mais importante para empresas que buscam crescimento sustentável."
        
        # Seções principais
        sections = []
        for i, message in enumerate(request.key_messages[:3], 1):
            sections.append(f"""
## {i}. {message}

{request.context_data.get(f'section_{i}', f'Esta seção explora como {message.lower()} pode impactar positivamente seu negócio. Com as estratégias certas, você pode alcançar resultados extraordinários.')}
""")
        
        conclusion = f"""
## Conclusão

{request.topic} representa uma oportunidade única de transformação. As empresas que adotarem essas práticas estarão melhor posicionadas para o futuro.

Pronto para começar sua jornada?
"""
        
        return f"{intro}\n{''.join(sections)}\n{conclusion}"

    def _generate_email_body(self, request: ContentRequest) -> str:
        """Gera corpo para email"""
        
        greeting = f"Olá {request.context_data.get('recipient_name', 'amigo')}!"
        
        body = f"""{greeting}

Espero que você esteja bem! Quero compartilhar com você algo que pode fazer uma grande diferença: {request.topic}.

{request.key_messages[0] if request.key_messages else 'Uma oportunidade incrível está esperando por você.'}

Aqui está o que você precisa saber:

{chr(10).join([f"• {msg}" for msg in request.key_messages[:5]])}

{request.context_data.get('additional_details', 'Esta é uma oportunidade limitada, então não perca tempo.')}

Abraços,
{request.brand_guidelines.get('sender_name', 'Equipe ALSHAM QUANTUM')}"""
        
        return body

    def _generate_generic_body(self, request: ContentRequest) -> str:
        """Gera corpo genérico"""
        return f"""
{request.topic} é fundamental para o sucesso no mundo atual.

{chr(10).join(request.key_messages)}

{request.context_data.get('description', 'Descubra como isso pode transformar sua experiência.')}
        """.strip()

    def _generate_intelligent_hashtags(self, topic: str, platform: Optional[Platform]) -> List[str]:
        """Gera hashtags inteligentes baseadas no tópico e plataforma"""
        
        hashtags = []
        
        # Hashtags baseadas no tópico
        topic_lower = topic.lower()
        
        # Mapeamento inteligente de tópicos
        topic_mappings = {
            "marketing": ["marketing", "digitalmarketing", "contentmarketing", "socialmedia"],
            "vendas": ["sales", "vendas", "b2b", "conversion"],
            "tecnologia": ["tech", "innovation", "digital", "future"],
            "negócios": ["business", "entrepreneur", "startup", "success"],
            "educação": ["education", "learning", "knowledge", "growth"]
        }
        
        # Encontrar categoria mais próxima
        for category, category_hashtags in topic_mappings.items():
            if category in topic_lower or any(word in topic_lower for word in category_hashtags):
                hashtags.extend([f"#{tag}" for tag in category_hashtags[:3]])
                break
        
        # Hashtags genéricas sempre úteis
        hashtags.extend(["#alshamquantum", "#inovacao", "#sucesso"])
        
        # Otimizar por plataforma
        if platform:
            platform_config = self.platform_configs.get(platform, {})
            max_hashtags = platform_config.get("hashtag_limit", 10)
            hashtags = hashtags[:max_hashtags]
        
        return list(set(hashtags))  # Remove duplicatas

    def _calculate_seo_score(self, text: str, topic: str) -> float:
        """Calcula score SEO do conteúdo"""
        score = 0.0
        text_lower = text.lower()
        topic_lower = topic.lower()
        
        # Presença do tópico no texto
        topic_count = text_lower.count(topic_lower)
        score += min(topic_count * 0.1, 0.3)
        
        # Densidade de palavras-chave (ideal 1-3%)
        word_count = len(text.split())
        if word_count > 0:
            keyword_density = topic_count / word_count
            if 0.01 <= keyword_density <= 0.03:
                score += 0.3
            elif keyword_density > 0:
                score += 0.1
        
        # Comprimento do texto
        if 300 <= word_count <= 2000:
            score += 0.2
        elif word_count > 100:
            score += 0.1
            
        # Estrutura (parágrafos, listas)
        if '\n\n' in text:
            score += 0.1
        if any(marker in text for marker in ['•', '-', '1.', '2.']):
            score += 0.1
            
        return min(score, 1.0)

    def _calculate_readability_score(self, text: str) -> float:
        """Calcula score de legibilidade"""
        
        if not text.strip():
            return 0.0
            
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        if not words or not sentences:
            return 0.5
        
        # Métricas básicas de legibilidade
        avg_words_per_sentence = len(words) / max(sentences, 1)
        avg_chars_per_word = sum(len(word) for word in words) / len(words)
        
        # Score baseado em métricas ideais
        score = 0.0
        
        # Sentenças nem muito curtas nem muito longas (ideal 15-20 palavras)
        if 10 <= avg_words_per_sentence <= 25:
            score += 0.4
        elif 5 <= avg_words_per_sentence <= 35:
            score += 0.2
            
        # Palavras nem muito curtas nem muito longas (ideal 4-6 caracteres)
        if 4 <= avg_chars_per_word <= 6:
            score += 0.4
        elif 3 <= avg_chars_per_word <= 8:
            score += 0.2
            
        # Bônus por estrutura clara
        if '\n' in text:  # Parágrafos
            score += 0.1
        if any(word in text.lower() for word in ['primeiro', 'segundo', 'finalmente', 'além disso']):
            score += 0.1
            
        return min(score, 1.0)

    async def _create_ab_variations(self, content: GeneratedContent, request: ContentRequest) -> List[ContentVariation]:
        """Cria variações para teste A/B"""
        
        variations = []
        
        # Variação 1: Tom mais urgente
        urgent_title = f"🚨 {content.title}"
        urgent_body = content.body.replace("você pode", "você DEVE").replace("Descubra", "DESCUBRA AGORA")
        
        variations.append(ContentVariation(
            variation_id=str(uuid.uuid4()),
            title=urgent_title,
            body=urgent_body,
            test_hypothesis="Tom urgente aumenta conversão",
            expected_improvement="15-25% mais cliques",
            target_metric="click_through_rate"
        ))
        
        # Variação 2: Mais social proof
        social_title = f"✅ {content.title} (Comprovado por 10.000+ usuários)"
        social_body = f"Mais de 10.000 pessoas já transformaram seus resultados!\n\n{content.body}\n\n⭐ 'Incrível resultado!' - Cliente satisfeito"
        
        variations.append(ContentVariation(
            variation_id=str(uuid.uuid4()),
            title=social_title,
            body=social_body,
            test_hypothesis="Social proof aumenta credibilidade",
            expected_improvement="20-30% mais engajamento",
            target_metric="engagement_rate"
        ))
        
        return variations

    async def _perform_content_analysis(self, content: GeneratedContent) -> ContentAnalysis:
        """Realiza análise detalhada do conteúdo"""
        
        # Análise de sentimento simplificada
        positive_words = ["excelente", "incrível", "fantástico", "melhor", "ótimo", "sucesso"]
        negative_words = ["ruim", "pior", "problema", "difícil", "falha"]
        
        text_lower = content.body.lower()
        positive_count = sum(word in text_lower for word in positive_words)
        negative_count = sum(word in text_lower for word in negative_words)
        
        sentiment_score = (positive_count - negative_count) / max(len(content.body.split()), 1)
        sentiment_score = max(-1, min(1, sentiment_score))  # Normalizar entre -1 e 1
        
        # Predições baseadas em scores
        engagement_prediction = (content.seo_score + content.readability_score + abs(sentiment_score)) / 3
        conversion_prediction = engagement_prediction * 0.7  # Conversão tipicamente menor que engagement
        
        # Extrair palavras-chave SEO
        words = content.body.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignorar palavras muito curtas
                word_freq[word] = word_freq.get(word, 0) + 1
        
        seo_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        seo_keywords = [word for word, freq in seo_keywords if freq > 1]
        
        # Identificar problemas de legibilidade
        readability_issues = []
        if content.readability_score < 0.5:
            readability_issues.append("Texto muito complexo - simplifique sentenças")
        if len(content.body.split()) < 50:
            readability_issues.append("Conteúdo muito curto - expanda com mais detalhes")
        if content.body.count('\n') < 2:
            readability_issues.append("Adicione quebras de parágrafo para melhor leitura")
            
        # Gerar sugestões
        suggestions = []
        if content.seo_score < 0.6:
            suggestions.append("Inclua mais palavras-chave relevantes")
        if len(content.hashtags) < 3:
            suggestions.append("Adicione mais hashtags relevantes")
        if "!" not in content.body and "?" not in content.body:
            suggestions.append("Use pontuação expressiva para maior engajamento")
            
        return ContentAnalysis(
            analysis_id=str(uuid.uuid4()),
            content_id=content.content_id,
            sentiment_score=sentiment_score,
            engagement_prediction=engagement_prediction,
            conversion_prediction=conversion_prediction,
            seo_keywords=seo_keywords,
            readability_issues=readability_issues,
            suggestions=suggestions
        )

    async def _optimize_for_specific_platform(self, content: GeneratedContent, platform: Platform) -> Dict[str, Any]:
        """Otimiza conteúdo para plataforma específica"""
        
        config = self.platform_configs.get(platform, {})
        optimizations = {}
        
        # Ajustar comprimento
        char_limit = config.get("character_limit")
        if char_limit and len(content.body) > char_limit:
            truncated_body = content.body[:char_limit-3] + "..."
            optimizations["body_truncated"] = truncated_body
            optimizations["truncation_needed"] = True
        
        # Otimizar hashtags
        hashtag_limit = config.get("hashtag_limit", 10)
        if len(content.hashtags) > hashtag_limit:
            optimizations["hashtags_optimized"] = content.hashtags[:hashtag_limit]
        
        # Sugerir melhor horário de postagem
        best_times = config.get("best_times", [])
        if best_times:
            optimizations["recommended_posting_times"] = best_times
        
        # Adaptações específicas por plataforma
        if platform == Platform.TWITTER:
            optimizations["thread_suggestion"] = self._create_twitter_thread(content.body)
        elif platform == Platform.INSTAGRAM:
            optimizations["story_version"] = self._create_instagram_story_version(content)
        elif platform == Platform.LINKEDIN:
            optimizations["professional_tone"] = self._adapt_for_linkedin(content.body)
            
        return optimizations

    def _create_twitter_thread(self, text: str) -> List[str]:
        """Cria thread do Twitter a partir do texto"""
        
        sentences = text.split('. ')
        thread = []
        current_tweet = ""
        
        for sentence in sentences:
            if len(current_tweet + sentence + '. ') <= 280:
                current_tweet += sentence + '. '
            else:
                if current_tweet:
                    thread.append(current_tweet.strip())
                current_tweet = sentence + '. '
        
        if current_tweet:
            thread.append(current_tweet.strip())
            
        # Adicionar numeração
        return [f"{i+1}/{len(thread)} {tweet}" for i, tweet in enumerate(thread)]

    def _create_instagram_story_version(self, content: GeneratedContent) -> str:
        """Cria versão para Instagram Stories"""
        
        # Versão mais visual e concisa
        story_text = f"💫 {content.title}\n\n"
        
        # Pegar primeira frase do corpo
        first_sentence = content.body.split('.')[0] + '.'
        story_text += f"{first_sentence}\n\n"
        
        # Adicionar emojis e call-to-action
        story_text += f"Deslize para cima! 👆\n{content.call_to_action}"
        
        return story_text

    def _adapt_for_linkedin(self, text: str) -> str:
        """Adapta texto para tom profissional do LinkedIn"""
        
        # Substituições para tom mais profissional
        professional_replacements = {
            "incrível": "notável",
            "fantástico": "excepcional",
            "você": "profissionais",
            "pessoal": "colegas",
        }
        
        adapted_text = text
        for informal, formal in professional_replacements.items():
            adapted_text = adapted_text.replace(informal, formal)
            
        return adapted_text

    def _build_content_request(self, data: Dict[str, Any]) -> ContentRequest:
        """Constrói objeto ContentRequest dos dados de entrada"""
        
        return ContentRequest(
            request_id=str(uuid.uuid4()),
            content_type=ContentType(data.get("content_type", "social_media_post")),
            platform=Platform(data["platform"]) if data.get("platform") else None,
            tone=Tone(data.get("tone", "professional")),
            audience=Audience(data.get("audience", "general_public")),
            topic=data.get("topic", "Tópico padrão"),
            key_messages=data.get("key_messages", []),
            call_to_action=data.get("call_to_action", "Saiba mais"),
            constraints=data.get("constraints", {}),
            context_data=data.get("context_data", {}),
            brand_guidelines=data.get("brand_guidelines", {})
        )

    async def _create_campaign(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma campanha completa com múltiplos conteúdos"""
        
        campaign_name = data.get("campaign_name", "Nova Campanha")
        platforms = data.get("platforms", ["instagram", "facebook", "linkedin"])
        base_topic = data.get("topic", "Marketing Digital")
        
        campaign_contents = []
        
        for platform in platforms:
            # Criar conteúdo específico para cada plataforma
            platform_data = {
                **data,
                "platform": platform,
                "topic": f"{base_topic} - Otimizado para {platform.title()}"
            }
            
            content_result = await self._generate_content(platform_data)
            campaign_contents.append({
                "platform": platform,
                "content": content_result
            })
        
        return {
            "campaign_id": str(uuid.uuid4()),
            "campaign_name": campaign_name,
            "total_contents": len(campaign_contents),
            "contents": campaign_contents,
            "estimated_reach": sum(1000 * (i+1) for i in range(len(platforms))),  # Simulado
            "estimated_engagement": len(platforms) * 50,  # Simulado
            "timestamp": datetime.now().isoformat()
        }

    async def _generate_content_variations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera variações de um conteúdo existente"""
        
        content_id = data.get("content_id")
        variation_count = data.get("variation_count", 3)
        
        if content_id not in self.content_cache:
            return {"error": "Conteúdo não encontrado"}
        
        original_content = self.content_cache[content_id]["content"]
        
        variations = []
        for i in range(variation_count):
            # Diferentes estratégias para cada variação
            if i == 0:
                # Variação com mais emojis
                variation_title = f"🎯 {original_content['title']}"
                variation_body = original_content['body'].replace(".", ". ✨")
            elif i == 1:
                # Variação com pergunta
                variation_title = f"Como {original_content['title'].lower()}?"
                variation_body = f"Você já se perguntou: {original_content['body']}"
            else:
                # Variação com listagem
                variation_title = f"📋 {original_content['title']}"
                variation_body = f"Principais pontos sobre {original_content['title']}:\n\n" + original_content['body']
            
            variations.append({
                "variation_id": str(uuid.uuid4()),
                "title": variation_title,
                "body": variation_body,
                "strategy": f"Estratégia {i+1}",
                "expected_difference": f"Abordagem mais {'visual' if i == 0 else 'questionadora' if i == 1 else 'estruturada'}"
            })
        
        return {
            "original_content_id": content_id,
            "variations": variations,
            "total_variations": len(variations),
            "timestamp": datetime.now().isoformat()
        }

    async def _analyze_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa conteúdo existente"""
        
        text = data.get("text", "")
        if not text:
            return {"error": "Texto é obrigatório para análise"}
        
        # Criar conteúdo temporário para análise
        temp_content = GeneratedContent(
            content_id=str(uuid.uuid4()),
            content_type=ContentType.SOCIAL_MEDIA_POST,
            platform=None,
            title=text[:50] + "..." if len(text) > 50 else text,
            body=text,
            hashtags=[],
            call_to_action="",
            metadata={},
            performance_prediction={},
            variations=[],
            seo_score=self._calculate_seo_score(text, data.get("topic", "")),
            readability_score=self._calculate_readability_score(text)
        )
        
        analysis = await self._perform_content_analysis(temp_content)
        
        return {
            "analysis_id": analysis.analysis_id,
            "text_analyzed": text[:100] + "..." if len(text) > 100 else text,
            "metrics": {
                "sentiment_score": analysis.sentiment_score,
                "engagement_prediction": analysis.engagement_prediction,
                "conversion_prediction": analysis.conversion_prediction,
                "seo_score": temp_content.seo_score,
                "readability_score": temp_content.readability_score
            },
            "insights": {
                "seo_keywords": analysis.seo_keywords,
                "readability_issues": analysis.readability_issues,
                "suggestions": analysis.suggestions
            },
            "timestamp": datetime.now().isoformat()
        }

    async def _optimize_for_platform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Otimiza conteúdo existente para uma plataforma específica"""
        
        text = data.get("text", "")
        platform_str = data.get("platform")
        
        if not text or not platform_str:
            return {"error": "Texto e plataforma são obrigatórios"}
        
        try:
            platform = Platform(platform_str)
        except ValueError:
            return {"error": f"Plataforma '{platform_str}' não suportada"}
        
        # Criar conteúdo temporário
        temp_content = GeneratedContent(
            content_id=str(uuid.uuid4()),
            content_type=ContentType.SOCIAL_MEDIA_POST,
            platform=platform,
            title="",
            body=text,
            hashtags=self._generate_intelligent_hashtags(data.get("topic", ""), platform),
            call_to_action=data.get("call_to_action", "Saiba mais"),
            metadata={},
            performance_prediction={},
            variations=[],
            seo_score=0,
            readability_score=0
        )
        
        optimizations = await self._optimize_for_specific_platform(temp_content, platform)
        
        return {
            "optimization_id": str(uuid.uuid4()),
            "original_text": text,
            "platform": platform.value,
            "optimizations": optimizations,
            "recommended_hashtags": temp_content.hashtags,
            "platform_limits": self.platform_configs.get(platform, {}),
            "timestamp": datetime.now().isoformat()
        }

    async def _generate_hashtags(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera hashtags inteligentes para um tópico"""
        
        topic = data.get("topic", "")
        platform_str = data.get("platform")
        count = data.get("count", 10)
        
        if not topic:
            return {"error": "Tópico é obrigatório"}
        
        platform = Platform(platform_str) if platform_str else None
        hashtags = self._generate_intelligent_hashtags(topic, platform)
        
        # Expandir hashtags se necessário
        while len(hashtags) < count:
            # Adicionar hashtags genéricas
            generic_hashtags = ["#inovacao", "#crescimento", "#sucesso", "#futuro", "#digital"]
            for tag in generic_hashtags:
                if tag not in hashtags and len(hashtags) < count:
                    hashtags.append(tag)
        
        return {
            "hashtag_set_id": str(uuid.uuid4()),
            "topic": topic,
            "platform": platform.value if platform else "any",
            "hashtags": hashtags[:count],
            "total_generated": len(hashtags[:count]),
            "recommendations": [
                "Use hashtags específicos para maior relevância",
                "Misture hashtags populares com nichos",
                "Monitore performance para otimizar"
            ],
            "timestamp": datetime.now().isoformat()
        }

    async def _generate_content_calendar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera calendário de conteúdo"""
        
        days = data.get("days", 7)
        posts_per_day = data.get("posts_per_day", 1)
        topics = data.get("topics", ["Marketing Digital"])
        platforms = data.get("platforms", ["instagram"])
        
        calendar = []
        start_date = datetime.now()
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            day_posts = []
            
            for post_num in range(posts_per_day):
                topic = topics[post_num % len(topics)]
                platform = platforms[post_num % len(platforms)]
                
                # Gerar conteúdo para o dia
                content_data = {
                    "content_type": "social_media_post",
                    "platform": platform,
                    "topic": f"{topic} - Dia {day + 1}",
                    "tone": "professional",
                    "audience": "general_public",
                    "key_messages": [f"Mensagem do dia sobre {topic}"],
                    "call_to_action": "Saiba mais"
                }
                
                content = await self._generate_content(content_data)
                
                day_posts.append({
                    "post_id": str(uuid.uuid4()),
                    "scheduled_time": f"{current_date.strftime('%Y-%m-%d')} 10:00",
                    "platform": platform,
                    "topic": topic,
                    "content_preview": content["content"]["title"][:50] + "...",
                    "hashtags_count": len(content["content"]["hashtags"]),
                    "status": "scheduled"
                })
            
            calendar.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "day_of_week": current_date.strftime('%A'),
                "posts": day_posts
            })
        
        return {
            "calendar_id": str(uuid.uuid4()),
            "period": f"{days} dias",
            "total_posts": days * posts_per_day,
            "calendar": calendar,
            "summary": {
                "platforms_covered": list(set(platforms)),
                "topics_covered": topics,
                "posting_frequency": f"{posts_per_day} posts/dia"
            },
            "timestamp": datetime.now().isoformat()
        }

    async def _analyze_competitor_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa conteúdo de concorrentes (simulado)"""
        
        competitor_urls = data.get("competitor_urls", [])
        analysis_type = data.get("analysis_type", "engagement")
        
        # Simulação de análise competitiva
        competitor_analysis = []
        
        for i, url in enumerate(competitor_urls[:5]):  # Máximo 5 concorrentes
            analysis = {
                "competitor_id": f"COMP_{i+1:03d}",
                "url": url,
                "content_analysis": {
                    "average_post_length": 120 + (i * 20),
                    "hashtags_per_post": 8 + i,
                    "posting_frequency": f"{2 + i} posts/semana",
                    "engagement_rate": 0.03 + (i * 0.01),
                    "top_content_types": ["image", "carousel", "video"][i:i+2]
                },
                "strengths": [
                    "Conteúdo visual atrativo",
                    "Engajamento consistente",
                    "Presença em múltiplas plataformas"
                ][i:i+2],
                "opportunities": [
                    "Aumentar frequência de posts",
                    "Melhorar call-to-actions",
                    "Diversificar formatos"
                ][i:i+2]
            }
            competitor_analysis.append(analysis)
        
        # Insights consolidados
        insights = [
            "Concorrentes focam em conteúdo visual",
            "Hashtags estratégicas são fundamentais",
            "Consistência na postagem gera melhores resultados",
            "Oportunidade de diferenciação em conteúdo educacional"
        ]
        
        recommendations = [
            "Investir em produção visual de qualidade",
            "Desenvolver calendário editorial consistente",
            "Testar novos formatos de conteúdo",
            "Monitorar performance dos concorrentes regularmente"
        ]
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "competitors_analyzed": len(competitor_analysis),
            "competitor_analysis": competitor_analysis,
            "market_insights": insights,
            "strategic_recommendations": recommendations,
            "next_analysis_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "timestamp": datetime.now().isoformat()
        }

def create_agents() -> List[ContentCreatorAgent]:
    """
    Função obrigatória para criação de agentes.
    Retorna lista de agentes Content Creator para o módulo Social Media.
    """
    return [ContentCreatorAgent()]

# Função de inicialização para compatibilidade
def initialize_content_creator_agent():
    """Inicializa o agente Content Creator"""
    return ContentCreatorAgent()

# Ponto de entrada para testes
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = ContentCreatorAgent()
        
        # Teste de geração de conteúdo
        content_test = {
            "action": "generate_content",
            "content_type": "social_media_post",
            "platform": "instagram",
            "tone": "inspirational",
            "audience": "b2c_millennials",
            "topic": "Transformação Digital",
            "key_messages": [
                "A tecnologia pode simplificar sua vida",
                "Inovação está ao alcance de todos",
                "O futuro começa hoje"
            ],
            "call_to_action": "Descubra como transformar seu negócio",
            "context_data": {
                "industry": "technology",
                "target_age": "25-35",
                "pain_points": ["complexidade", "custo", "tempo"]
            },
            "brand_guidelines": {
                "voice": "inspirational",
                "colors": ["blue", "white"],
                "sender_name": "ALSHAM QUANTUM"
            }
        }
        
        result = await agent.process(content_test)
        print("Teste Content Creator Agent:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Teste de campanha
        campaign_test = {
            "action": "create_campaign",
            "campaign_name": "Lançamento ALSHAM QUANTUM",
            "platforms": ["instagram", "linkedin", "facebook"],
            "topic": "Revolução da IA",
            "tone": "professional",
            "audience": "b2b_executives"
        }
        
        campaign_result = await agent.process(campaign_test)
        print("\nTeste Campanha Multi-plataforma:")
        print(json.dumps(campaign_result, indent=2, ensure_ascii=False))
        
    # Executar teste
    asyncio.run(test_agent())
