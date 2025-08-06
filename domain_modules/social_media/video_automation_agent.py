#!/usr/bin/env python3
"""
Módulo do Agente de Automação de Vídeo - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente automatiza a criação e edição de vídeos para mídias sociais.
Utiliza as bibliotecas MoviePy e Pillow para criar vídeos a partir de
imagens, adicionar áudio e realizar outras manipulações.
"""

import logging
import os
from typing import Any, Dict, List
from pathlib import Path

try:
    from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
    from PIL import Image
    LIBRARIES_AVAILABLE = True
except ImportError:
    LIBRARIES_AVAILABLE = False

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


class VideoAutomationAgent(BaseNetworkAgent):
    """
    Agente especialista que usa ferramentas de software para criar e
    editar vídeos programaticamente.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o VideoAutomationAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "video_creation_from_images",
            "add_background_audio",
            "video_concatenation",
        ])
        
        self.output_dir = Path("./generated_videos")
        self.output_dir.mkdir(exist_ok=True)

        if not LIBRARIES_AVAILABLE:
            self.status = "degraded"
            logger.critical(
                "Bibliotecas 'moviepy' ou 'Pillow' não encontradas. "
                "O VideoAutomationAgent operará em modo degradado."
            )
        
        logger.info(f"🎬 Agente de Automação de Vídeo ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para criação de vídeo."""
        if self.status == "degraded":
            await self.publish_error_response(message, "Dependências necessárias (moviepy, Pillow) não estão instaladas.")
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "create_video_from_images":
            await self.handle_create_video_request(message)

    async def handle_create_video_request(self, message: AgentMessage) -> None:
        """
        Handles the logic for creating a video from a list of images and optional audio.

        This method validates the input, loads images, creates a video clip using MoviePy,
        adds background audio if provided, writes the final video file, and returns the result.
        Robust error handling and logging are provided for diagnostics and production reliability.

        Args:
            message (AgentMessage): The incoming message containing image paths, audio path, and other options.

        Returns:
            None
        """
        image_paths: List[str] = message.content.get("image_paths", [])
        audio_path: str = message.content.get("audio_path")
        duration_per_image: int = message.content.get("duration_per_image", 3)  # segundos
        output_filename: str = message.content.get("output_filename", f"video_{self.timestamp}.mp4")

        if not image_paths:
            logger.warning("[VideoAutomationAgent] Nenhuma imagem fornecida para a criação do vídeo.")
            await self.publish_error_response(message, "Nenhuma imagem fornecida para a criação do vídeo.")
            return

        logger.info(f"[VideoAutomationAgent] Iniciando criação de vídeo '{output_filename}' com {len(image_paths)} imagens.")

        try:
            # Validar e carregar imagens
            valid_images: List[str] = [path for path in image_paths if Path(path).exists() and Path(path).is_file()]
            if not valid_images:
                logger.warning("[VideoAutomationAgent] Nenhuma das imagens fornecidas foi encontrada.")
                await self.publish_error_response(message, "Nenhuma das imagens fornecidas foi encontrada.")
                return

            # Cria o clipe de vídeo a partir da sequência de imagens
            video_clip = ImageSequenceClip(valid_images, durations=[duration_per_image] * len(valid_images))

            # Adiciona o áudio, se fornecido
            if audio_path and Path(audio_path).exists():
                audio_clip = AudioFileClip(audio_path)
                # Garante que o áudio tenha a mesma duração do vídeo
                video_clip = video_clip.set_audio(audio_clip.set_duration(video_clip.duration))

            # Define o caminho de saída
            output_path: Path = self.output_dir / output_filename

            # Escreve o arquivo de vídeo final
            video_clip.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                fps=24,
                logger=None  # Desativa o logger verboso do moviepy
            )

            logger.info(f"[VideoAutomationAgent] Vídeo criado com sucesso em: {output_path}")

            # Responde com sucesso
            response_content: Dict[str, Any] = {
                "status": "completed",
                "video_path": str(output_path),
                "duration": video_clip.duration,
                "num_images": len(valid_images)
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.critical(f"[VideoAutomationAgent] Erro ao criar o vídeo: {e}", exc_info=True)
            await self.publish_error_response(message, f"Ocorreu um erro interno durante a criação do vídeo: {e}")
