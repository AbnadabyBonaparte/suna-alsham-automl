#!/usr/bin/env python3
"""
Módulo do Video Automation Agent - ALSHAM GLOBAL

[Fase 3] - Fortalecido com lógica real de renderização de vídeo usando MoviePy.
"""

import asyncio
import logging
from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime

# [AUTENTICIDADE] Bibliotecas de edição de vídeo são importadas de forma segura.
try:
    from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
    VIDEO_LIBS_AVAILABLE = True
except ImportError:
    VIDEO_LIBS_AVAILABLE = False

# Importa a classe base e as ferramentas do nosso núcleo fortalecido
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class VideoAutomationAgent(BaseNetworkAgent):
    """
    Cria vídeos automaticamente, edita, renderiza e gera thumbnails otimizadas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o VideoAutomationAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        self.capabilities.extend([
            "video_creation",
            "automatic_editing",
            "thumbnail_generation",
        ])

        if not VIDEO_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.warning(f"Agente {agent_id} operando em modo degradado: bibliotecas de vídeo (moviepy) não encontradas.")
        
        self.output_path = Path("./video_outputs")
        self.output_path.mkdir(exist_ok=True)
        
        logger.info(f"🎬 {self.agent_id} (Automação de Vídeo) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para criação de vídeo."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "create_video":
            result = await self._create_video_handler(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de vídeo desconhecida"))

    async def _create_video_handler(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Orquestra a criação de um vídeo a partir de um roteiro.
        """
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de vídeo indisponível (dependências faltando)."}

        script_scenes = request_data.get("script_scenes", [])
        video_format = request_data.get("format", "reels")
        
        if not script_scenes:
            return {"status": "error", "message": "Nenhum roteiro (script_scenes) fornecido."}

        logger.info(f"🎬 Iniciando criação de vídeo formato '{video_format}' com {len(script_scenes)} cenas.")

        try:
            video_clips = []
            total_duration = 0
            for i, scene_text in enumerate(script_scenes):
                logger.info(f"  -> Processando cena {i+1}: '{scene_text[:30]}...'")
                # Define a duração de cada clipe, por exemplo, 3 segundos
                clip_duration = 3
                clip = self._create_text_clip(scene_text, duration=clip_duration)
                if clip:
                    # Define o tempo de início de cada clipe
                    clip = clip.set_start(total_duration)
                    video_clips.append(clip)
                    total_duration += clip_duration
            
            if not video_clips:
                return {"status": "error", "message": "Nenhum clipe de vídeo pôde ser criado."}

            final_video_path = self._render_video(video_clips, total_duration, video_format)

            return {
                "status": "completed", 
                "video_path": str(final_video_path),
                "message": "Vídeo renderizado com sucesso."
            }

        except Exception as e:
            logger.error(f"❌ Erro ao criar vídeo: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _create_text_clip(self, text: str, duration: int) -> Any:
        """
        [LÓGICA REAL] Cria um clipe de vídeo com texto usando MoviePy.
        """
        try:
            logger.info(f"    -> Criando clipe de texto para: '{text}'")
            video_size = (1080, 1920) # Formato Reels/Shorts/TikTok
            
            # Cria um clipe de texto
            text_clip = TextClip(
                txt=text,
                fontsize=70,
                color='white',
                font='Arial-Bold', # Use uma fonte disponível no seu sistema
                size=video_size,
                method='caption'
            ).set_duration(duration)
            
            return text_clip
        except Exception as e:
            logger.error(f"Erro ao criar clipe de texto: {e}")
            return None

    def _render_video(self, clips: List[Any], total_duration: int, video_format: str) -> Path:
        """
        [LÓGICA REAL] Renderiza o vídeo final usando MoviePy.
        """
        logger.info(f"  -> Renderizando {len(clips)} clipes para o vídeo final.")
        
        video_filename = f"{video_format}_{int(datetime.now().timestamp())}.mp4"
        final_video_path = self.output_path / video_filename
        
        # Cria um clipe de fundo colorido
        background_clip = ColorClip(size=(1080, 1920), color=(25, 25, 112), duration=total_duration) # Cor "Midnight Blue"
        
        # Compõe o vídeo final
        final_clip = CompositeVideoClip([background_clip] + clips)
        
        # Renderiza o arquivo de vídeo
        final_clip.write_videofile(str(final_video_path), fps=24, codec='libx264')
            
        return final_video_path


def create_video_automation_agent(message_bus) -> List[VideoAutomationAgent]:
    """
    Cria o agente de Automação de Vídeo.
    """
    agents = []
    logger.info("🎬 Criando VideoAutomationAgent...")
    try:
        agent = VideoAutomationAgent("video_automation_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando VideoAutomationAgent: {e}", exc_info=True)
    return agents
