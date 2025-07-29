#!/usr/bin/env python3
"""
Módulo da Rede Multi-Agente - O Coração do Núcleo SUNA-ALSHAM
"""
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    # ... (resto do enum)

class Priority(Enum):
    LOW = 3
    # ... (resto do enum)

class AgentType(Enum):
    """Define os tipos de agentes no sistema."""
    CORE = "core"
    SPECIALIZED = "specialized"
    SERVICE = "service"
    SYSTEM = "system"
    META_COGNITIVE = "meta_cognitive"
    BUSINESS_DOMAIN = "business_domain"
    AI_POWERED = "ai_powered"         # <-- ADICIONADO AQUI
    ORCHESTRATOR = "orchestrator"     # <-- ADICIONADO AQUI

# ... (O RESTO DO ARQUIVO CONTINUA EXATAMENTE IGUAL)
# ... (Para economizar espaço, não vou colar o resto, apenas adicione as duas linhas acima)
