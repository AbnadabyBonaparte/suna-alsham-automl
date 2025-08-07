"""
Video Automation Agent - ALSHAM QUANTUM Native
Agente especializado em automação de criação e edição de vídeos para mídias sociais
Versão: 2.1.0 - Nativa (sem dependências SUNA-ALSHAM)
"""

import asyncio
import logging
import os
import subprocess
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import tempfile
import shutil

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

# Enums e Classes de Dados
class VideoFormat(Enum):
    MP4 = "mp4"
    MOV = "mov"
    AVI = "avi"
    WEBM = "webm"
    MKV = "mkv"

class VideoQuality(Enum):
    LOW = "360p"
    MEDIUM = "720p"
    HIGH = "1080p"
    ULTRA = "1440p"
    ULTRA_4K = "2160p"

class VideoStyle(Enum):
    SLIDESHOW = "slideshow"
    CINEMATIC = "cinematic"
    SOCIAL_MEDIA = "social_media"
    TUTORIAL = "tutorial"
    PROMOTIONAL = "promotional"
    STORY = "story"

class TransitionType(Enum):
    FADE = "fade"
    SLIDE = "slide"
    ZOOM = "zoom"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    NONE = "none"

@dataclass
class VideoAsset:
    asset_id: str
    asset_type: str  # image, video, audio, text
    path: str
    duration: float = 3.0
    start_time: float = 0.0
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoTransition:
    transition_type: TransitionType
    duration: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoProject:
    project_id: str
    title: str
    description: str
    assets: List[VideoAsset]
    transitions: List[VideoTransition] = field(default_factory=list)
    output_settings: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    total_duration: float = 0.0

class VideoAutomationAgent(BaseNetworkAgent):
    """
    Agente de Automação de Vídeo Avançado
    
    Responsabilidades:
    - Criação de vídeos a partir de imagens, áudios e textos
    - Edição automatizada com transições e efeitos
    - Otimização para diferentes plataformas sociais
    - Renderização em múltiplos formatos e qualidades
    - Templates pré-configurados para casos comuns
    """
    
    def __init__(self, agent_id: str = "video_automation_agent", config: Dict[str, Any] = None):
        super().__init__(agent_id, config)
        
        # Configuração de diretórios
        self.workspace_dir = Path(config.get('workspace_dir', './video_workspace'))
        self.output_dir = self.workspace_dir / 'output'
        self.temp_dir = self.workspace_dir / 'temp'
        self.templates_dir = self.workspace_dir / 'templates'
        
        # Criar diretórios necessários
        for directory in [self.workspace_dir, self.output_dir, self.temp_dir, self.templates_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Configurações de vídeo
        self.default_fps = config.get('default_fps', 30)
        self.default_quality = VideoQuality(config.get('default_quality', 'HIGH'))
        self.default_format = VideoFormat(config.get('default_format', 'MP4'))
        
        # Cache de projetos ativos
        self.active_projects: Dict[str, VideoProject] = {}
        self.rendering_queue: List[str] = []
        self.completed_projects: Dict[str, Dict[str, Any]] = {}
        
        # Configuração de ferramentas
        self.ffmpeg_available = self._check_ffmpeg()
        self.imagemagick_available = self._check_imagemagick()
        
        # Templates pré-configurados
        self._initialize_templates()
        
        self.logger.info("🎬 Video Automation Agent inicializado com sucesso")
        self.status = "active"

    def _check_ffmpeg(self) -> bool:
        """Verifica se FFmpeg está disponível"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.logger.info("✅ FFmpeg encontrado e funcional")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        self.logger.warning("⚠️ FFmpeg não encontrado. Funcionalidades limitadas.")
        return False

    def _check_imagemagick(self) -> bool:
        """Verifica se ImageMagick está disponível"""
        try:
            result = subprocess.run(['convert', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.logger.info("✅ ImageMagick encontrado e funcional")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        self.logger.warning("⚠️ ImageMagick não encontrado. Funcionalidades de imagem limitadas.")
        return False

    def _initialize_templates(self):
        """Inicializa templates pré-configurados"""
        self.video_templates = {
            'social_media_post': {
                'aspect_ratio': '1:1',
                'duration_per_asset': 3.0,
                'transition_duration': 0.5,
                'max_duration': 60.0,
                'style': VideoStyle.SOCIAL_MEDIA,
                'format': VideoFormat.MP4,
                'quality': VideoQuality.HIGH
            },
            'instagram_story': {
                'aspect_ratio': '9:16',
                'duration_per_asset': 2.5,
                'transition_duration': 0.3,
                'max_duration': 15.0,
                'style': VideoStyle.STORY,
                'format': VideoFormat.MP4,
                'quality': VideoQuality.HIGH
            },
            'promotional_video': {
                'aspect_ratio': '16:9',
                'duration_per_asset': 4.0,
                'transition_duration': 1.0,
                'max_duration': 120.0,
                'style': VideoStyle.PROMOTIONAL,
                'format': VideoFormat.MP4,
                'quality': VideoQuality.ULTRA
            },
            'slideshow': {
                'aspect_ratio': '16:9',
                'duration_per_asset': 5.0,
                'transition_duration': 1.5,
                'max_duration': 300.0,
                'style': VideoStyle.SLIDESHOW,
                'format': VideoFormat.MP4,
                'quality': VideoQuality.HIGH
            }
        }

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de automação de vídeo"""
        try:
            self.logger.info(f"🎬 Processando requisição: {request.get('action', 'unknown')}")
            
            action = request.get('action', '')
            
            if action == 'create_video':
                return await self._create_video(request)
            elif action == 'create_slideshow':
                return await self._create_slideshow(request)
            elif action == 'add_audio_to_video':
                return await self._add_audio_to_video(request)
            elif action == 'merge_videos':
                return await self._merge_videos(request)
            elif action == 'extract_frames':
                return await self._extract_frames(request)
            elif action == 'apply_effects':
                return await self._apply_effects(request)
            elif action == 'optimize_for_platform':
                return await self._optimize_for_platform(request)
            elif action == 'get_project_status':
                return await self._get_project_status(request.get('project_id'))
            elif action == 'list_templates':
                return await self._list_templates()
            else:
                return await self._handle_unknown_action(action, request)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no processamento: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _create_video(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um vídeo a partir de assets fornecidos"""
        try:
            # Validar entrada
            assets_data = request.get('assets', [])
            if not assets_data:
                return {
                    'success': False,
                    'error': 'Nenhum asset fornecido',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Criar projeto
            project = self._create_project(request)
            
            # Processar assets
            processed_assets = await self._process_assets(project, assets_data)
            
            if not processed_assets:
                return {
                    'success': False,
                    'error': 'Nenhum asset válido encontrado',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Gerar vídeo
            result = await self._render_video(project)
            
            if result['success']:
                self.completed_projects[project.project_id] = result
                if project.project_id in self.active_projects:
                    del self.active_projects[project.project_id]
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na criação do vídeo: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _create_slideshow(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um slideshow a partir de imagens"""
        try:
            images = request.get('images', [])
            if not images:
                return {
                    'success': False,
                    'error': 'Nenhuma imagem fornecida',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Configurar projeto como slideshow
            slideshow_request = {
                **request,
                'template': 'slideshow',
                'assets': [
                    {
                        'type': 'image',
                        'path': img,
                        'duration': request.get('duration_per_image', 3.0)
                    }
                    for img in images
                ]
            }
            
            if request.get('background_audio'):
                slideshow_request['assets'].append({
                    'type': 'audio',
                    'path': request['background_audio'],
                    'duration': -1  # Audio completo
                })
            
            return await self._create_video(slideshow_request)
            
        except Exception as e:
            self.logger.error(f"❌ Erro na criação do slideshow: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _add_audio_to_video(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona áudio a um vídeo existente"""
        try:
            video_path = request.get('video_path')
            audio_path = request.get('audio_path')
            
            if not video_path or not audio_path:
                return {
                    'success': False,
                    'error': 'Caminho do vídeo e áudio são obrigatórios',
                    'timestamp': datetime.now().isoformat()
                }
            
            if not self.ffmpeg_available:
                return {
                    'success': False,
                    'error': 'FFmpeg não disponível para processamento de áudio',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Validar arquivos
            if not Path(video_path).exists() or not Path(audio_path).exists():
                return {
                    'success': False,
                    'error': 'Arquivo de vídeo ou áudio não encontrado',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Gerar nome de saída
            output_name = request.get('output_name', f'video_with_audio_{uuid.uuid4().hex[:8]}.mp4')
            output_path = self.output_dir / output_name
            
            # Comando FFmpeg para adicionar áudio
            cmd = [
                'ffmpeg', '-y',  # Sobrescrever se existir
                '-i', str(video_path),
                '-i', str(audio_path),
                '-c:v', 'copy',  # Não recodificar vídeo
                '-c:a', 'aac',   # Codec de áudio
                '-shortest',     # Usar duração do mais curto
                str(output_path)
            ]
            
            # Executar comando
            result = await self._run_ffmpeg_command(cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'output_path': str(output_path),
                    'message': 'Áudio adicionado com sucesso',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao adicionar áudio: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _merge_videos(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Mescla múltiplos vídeos em um só"""
        try:
            video_paths = request.get('video_paths', [])
            if len(video_paths) < 2:
                return {
                    'success': False,
                    'error': 'Pelo menos 2 vídeos são necessários para mesclagem',
                    'timestamp': datetime.now().isoformat()
                }
            
            if not self.ffmpeg_available:
                return {
                    'success': False,
                    'error': 'FFmpeg não disponível',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Validar todos os arquivos
            for video_path in video_paths:
                if not Path(video_path).exists():
                    return {
                        'success': False,
                        'error': f'Arquivo não encontrado: {video_path}',
                        'timestamp': datetime.now().isoformat()
                    }
            
            # Criar arquivo de lista temporário
            temp_list_file = self.temp_dir / f'merge_list_{uuid.uuid4().hex[:8]}.txt'
            
            with open(temp_list_file, 'w') as f:
                for video_path in video_paths:
                    f.write(f"file '{os.path.abspath(video_path)}'\n")
            
            # Gerar nome de saída
            output_name = request.get('output_name', f'merged_video_{uuid.uuid4().hex[:8]}.mp4')
            output_path = self.output_dir / output_name
            
            # Comando FFmpeg para merge
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(temp_list_file),
                '-c', 'copy',
                str(output_path)
            ]
            
            result = await self._run_ffmpeg_command(cmd)
            
            # Limpar arquivo temporário
            temp_list_file.unlink(missing_ok=True)
            
            if result['success']:
                return {
                    'success': True,
                    'output_path': str(output_path),
                    'merged_videos': len(video_paths),
                    'message': 'Vídeos mesclados com sucesso',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na mesclagem: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _extract_frames(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai frames de um vídeo"""
        try:
            video_path = request.get('video_path')
            if not video_path or not Path(video_path).exists():
                return {
                    'success': False,
                    'error': 'Caminho do vídeo inválido',
                    'timestamp': datetime.now().isoformat()
                }
            
            if not self.ffmpeg_available:
                return {
                    'success': False,
                    'error': 'FFmpeg não disponível',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Configurações de extração
            fps = request.get('fps', 1)  # 1 frame por segundo por padrão
            output_format = request.get('format', 'jpg')
            
            # Criar diretório para frames
            frames_dir = self.output_dir / f'frames_{uuid.uuid4().hex[:8]}'
            frames_dir.mkdir(exist_ok=True)
            
            # Comando FFmpeg para extração
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_path),
                '-vf', f'fps={fps}',
                '-q:v', '2',  # Alta qualidade
                str(frames_dir / f'frame_%04d.{output_format}')
            ]
            
            result = await self._run_ffmpeg_command(cmd)
            
            if result['success']:
                # Listar frames extraídos
                frame_files = list(frames_dir.glob(f'*.{output_format}'))
                
                return {
                    'success': True,
                    'frames_dir': str(frames_dir),
                    'frame_count': len(frame_files),
                    'frame_files': [str(f) for f in frame_files],
                    'message': f'{len(frame_files)} frames extraídos',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na extração de frames: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _optimize_for_platform(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Otimiza vídeo para plataforma específica"""
        try:
            video_path = request.get('video_path')
            platform = request.get('platform', 'instagram').lower()
            
            if not video_path or not Path(video_path).exists():
                return {
                    'success': False,
                    'error': 'Caminho do vídeo inválido',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Configurações por plataforma
            platform_specs = self._get_platform_specifications(platform)
            
            if not platform_specs:
                return {
                    'success': False,
                    'error': f'Plataforma não suportada: {platform}',
                    'available_platforms': list(self._get_supported_platforms()),
                    'timestamp': datetime.now().isoformat()
                }
            
            # Gerar nome otimizado
            output_name = request.get('output_name', 
                                   f'optimized_{platform}_{uuid.uuid4().hex[:8]}.mp4')
            output_path = self.output_dir / output_name
            
            # Construir comando FFmpeg
            cmd = self._build_optimization_command(video_path, output_path, platform_specs)
            
            result = await self._run_ffmpeg_command(cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'output_path': str(output_path),
                    'platform': platform,
                    'specifications': platform_specs,
                    'message': f'Vídeo otimizado para {platform}',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na otimização: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _create_project(self, request: Dict[str, Any]) -> VideoProject:
        """Cria um novo projeto de vídeo"""
        project_id = str(uuid.uuid4())
        
        # Aplicar template se especificado
        template_name = request.get('template', 'social_media_post')
        template = self.video_templates.get(template_name, self.video_templates['social_media_post'])
        
        # Configurações de saída
        output_settings = {
            'format': request.get('format', template['format']),
            'quality': request.get('quality', template['quality']),
            'fps': request.get('fps', self.default_fps),
            'aspect_ratio': request.get('aspect_ratio', template['aspect_ratio']),
            'max_duration': request.get('max_duration', template['max_duration'])
        }
        
        project = VideoProject(
            project_id=project_id,
            title=request.get('title', f'Video Project {datetime.now().strftime("%Y%m%d_%H%M%S")}'),
            description=request.get('description', ''),
            assets=[],
            output_settings=output_settings,
            metadata={
                'template': template_name,
                'client_id': request.get('client_id'),
                'platform_target': request.get('platform_target'),
                'style': template.get('style', VideoStyle.SOCIAL_MEDIA)
            }
        )
        
        self.active_projects[project_id] = project
        return project

    async def _process_assets(self, project: VideoProject, assets_data: List[Dict[str, Any]]) -> List[VideoAsset]:
        """Processa e valida assets do projeto"""
        processed_assets = []
        
        for i, asset_data in enumerate(assets_data):
            try:
                asset = await self._process_single_asset(asset_data, i)
                if asset:
                    processed_assets.append(asset)
                    project.total_duration += asset.duration
            except Exception as e:
                self.logger.warning(f"⚠️ Erro no processamento do asset {i}: {e}")
                continue
        
        project.assets = processed_assets
        return processed_assets

    async def _process_single_asset(self, asset_data: Dict[str, Any], index: int) -> Optional[VideoAsset]:
        """Processa um asset individual"""
        asset_type = asset_data.get('type', '').lower()
        asset_path = asset_data.get('path', '')
        
        if not asset_path or not Path(asset_path).exists():
            self.logger.warning(f"⚠️ Asset não encontrado: {asset_path}")
            return None
        
        asset_id = f"asset_{index}_{uuid.uuid4().hex[:8]}"
        
        # Configurar duração baseada no tipo
        if asset_type == 'image':
            duration = asset_data.get('duration', 3.0)
        elif asset_type == 'video':
            duration = await self._get_video_duration(asset_path)
        elif asset_type == 'audio':
            duration = await self._get_audio_duration(asset_path)
        else:
            duration = asset_data.get('duration', 3.0)
        
        return VideoAsset(
            asset_id=asset_id,
            asset_type=asset_type,
            path=asset_path,
            duration=duration,
            start_time=asset_data.get('start_time', 0.0),
            properties=asset_data.get('properties', {})
        )

    async def _render_video(self, project: VideoProject) -> Dict[str, Any]:
        """Renderiza o projeto de vídeo final"""
        try:
            if not self.ffmpeg_available:
                return await self._render_video_fallback(project)
            
            output_name = f"{project.title.replace(' ', '_')}_{project.project_id[:8]}.{project.output_settings['format'].value}"
            output_path = self.output_dir / output_name
            
            # Construir comando FFmpeg complexo
            cmd = await self._build_render_command(project, output_path)
            
            self.logger.info(f"🎬 Iniciando renderização: {output_path}")
            
            result = await self._run_ffmpeg_command(cmd, timeout=300)  # 5 minutos timeout
            
            if result['success']:
                # Calcular métricas do vídeo final
                video_info = await self._get_video_info(output_path)
                
                return {
                    'success': True,
                    'project_id': project.project_id,
                    'output_path': str(output_path),
                    'video_info': video_info,
                    'assets_used': len(project.assets),
                    'total_duration': project.total_duration,
                    'render_time': result.get('execution_time', 0),
                    'message': 'Vídeo renderizado com sucesso',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na renderização: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _build_render_command(self, project: VideoProject, output_path: Path) -> List[str]:
        """Constrói comando FFmpeg para renderização"""
        cmd = ['ffmpeg', '-y']  # Sobrescrever se existir
        
        # Adicionar inputs
        input_files = []
        for asset in project.assets:
            cmd.extend(['-i', asset.path])
            input_files.append(asset.path)
        
        # Configurar filtros complexos
        filter_complex = await self._build_filter_complex(project)
        
        if filter_complex:
            cmd.extend(['-filter_complex', filter_complex])
        
        # Configurações de codificação
        cmd.extend([
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-r', str(project.output_settings['fps']),
            str(output_path)
        ])
        
        return cmd

    async def _build_filter_complex(self, project: VideoProject) -> str:
        """Constrói filtro complexo para FFmpeg"""
        filters = []
        
        # Processar cada asset
        for i, asset in enumerate(project.assets):
            if asset.asset_type == 'image':
                # Configurar imagem com duração
                filters.append(f"[{i}:v]loop=loop=-1:size=1:start=0,setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={project.output_settings['fps']},trim=duration={asset.duration}[img{i}]")
        
        # Concatenar todos os clipes de vídeo
        video_inputs = []
        audio_inputs = []
        
        for i, asset in enumerate(project.assets):
            if asset.asset_type == 'image':
                video_inputs.append(f"img{i}")
            elif asset.asset_type == 'video':
                video_inputs.append(f"{i}:v")
                audio_inputs.append(f"{i}:a")
        
        # Concatenar vídeos
        if video_inputs:
            concat_filter = ''.join(f'[{inp}]' for inp in video_inputs)
            concat_filter += f'concat=n={len(video_inputs)}:v=1:a=0[outv]'
            filters.append(concat_filter)
        
        # Concatenar áudios se existirem
        if audio_inputs:
            audio_concat = ''.join(f'[{inp}]' for inp in audio_inputs)
            audio_concat += f'concat=n={len(audio_inputs)}:v=0:a=1[outa]'
            filters.append(audio_concat)
        
        return ';'.join(filters) if filters else ''

    async def _run_ffmpeg_command(self, cmd: List[str], timeout: int = 120) -> Dict[str, Any]:
        """Executa comando FFmpeg de forma assíncrona"""
        try:
            start_time = datetime.now()
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=timeout
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            if process.returncode == 0:
                self.logger.info(f"✅ Comando FFmpeg executado com sucesso em {execution_time:.2f}s")
                return {
                    'success': True,
                    'execution_time': execution_time,
                    'stdout': stdout.decode('utf-8', errors='ignore'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                error_msg = stderr.decode('utf-8', errors='ignore')
                self.logger.error(f"❌ Erro no FFmpeg: {error_msg}")
                return {
                    'success': False,
                    'error': f'FFmpeg error: {error_msg}',
                    'returncode': process.returncode,
                    'timestamp': datetime.now().isoformat()
                }
                
        except asyncio.TimeoutError:
            return {
                'success': False,
                'error': f'Timeout após {timeout} segundos',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _get_video_duration(self, video_path: str) -> float:
        """Obtém duração de um vídeo"""
        if not self.ffmpeg_available:
            return 10.0  # Valor padrão
        
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', str(video_path)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await process.communicate()
            
            if process.returncode == 0:
                info = json.loads(stdout.decode())
                return float(info['format']['duration'])
        except:
            pass
        
        return 10.0  # Valor padrão em caso de erro

    async def _get_audio_duration(self, audio_path: str) -> float:
        """Obtém duração de um áudio"""
        return await self._get_video_duration(audio_path)

    async def _get_video_info(self, video_path: Path) -> Dict[str, Any]:
        """Obtém informações detalhadas de um vídeo"""
        if not self.ffmpeg_available:
            return {'error': 'FFmpeg não disponível'}
        
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', str(video_path)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, _ = await process.communicate()
            
            if process.returncode == 0:
                return json.loads(stdout.decode())
        except:
            pass
        
        return {'error': 'Não foi possível obter informações do vídeo'}

    def _get_platform_specifications(self, platform: str) -> Optional[Dict[str, Any]]:
        """Retorna especificações para plataforma específica"""
        specs = {
            'instagram': {
                'max_duration': 60,
                'aspect_ratios': ['1:1', '4:5', '9:16'],
                'max_file_size': '100MB',
                'recommended_resolution': '1080x1080',
                'fps': 30,
                'video_codec': 'h264',
                'audio_codec': 'aac'
            },
            'tiktok': {
                'max_duration': 180,
                'aspect_ratios': ['9:16'],
                'max_file_size': '287.6MB',
                'recommended_resolution': '1080x1920',
                'fps': 30,
                'video_codec': 'h264',
                'audio_codec': 'aac'
            },
            'youtube': {
                'max_duration': 43200,  # 12 horas
                'aspect_ratios': ['16:9'],
                'max_file_size': '256GB',
                'recommended_resolution': '1920x1080',
                'fps': 60,
                'video_codec': 'h264',
                'audio_codec': 'aac'
            },
            'facebook': {
                'max_duration': 240,
                'aspect_ratios': ['16:9', '1:1', '4:5'],
                'max_file_size': '10GB',
                'recommended_resolution': '1920x1080',
                'fps': 30,
                'video_codec': 'h264',
                'audio_codec': 'aac'
            }
        }
        
        return specs.get(platform.lower())

    def _get_supported_platforms(self) -> List[str]:
        """Retorna lista de plataformas suportadas"""
        return ['instagram', 'tiktok', 'youtube', 'facebook', 'twitter', 'linkedin']

    def _build_optimization_command(self, input_path: str, output_path: Path, specs: Dict[str, Any]) -> List[str]:
        """Constrói comando de otimização para plataforma"""
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_path),
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-maxrate', '8M',
            '-bufsize', '16M',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-r', str(specs.get('fps', 30)),
            '-movflags', '+faststart',
            str(output_path)
        ]
        
        # Adicionar filtros de resolução se especificado
        if 'recommended_resolution' in specs:
            width, height = specs['recommended_resolution'].split('x')
            cmd.extend(['-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2'])
        
        return cmd

    async def _render_video_fallback(self, project: VideoProject) -> Dict[str, Any]:
        """Renderização alternativa quando FFmpeg não está disponível"""
        self.logger.warning("🔧 Usando renderização alternativa (sem FFmpeg)")
        
        # Simulação de renderização
        await asyncio.sleep(2)  # Simular processamento
        
        return {
            'success': False,
            'error': 'FFmpeg não disponível. Renderização completa indisponível.',
            'suggestion': 'Instale FFmpeg para funcionalidade completa',
            'assets_processed': len(project.assets),
            'timestamp': datetime.now().isoformat()
        }

    async def _get_project_status(self, project_id: str) -> Dict[str, Any]:
        """Retorna status de um projeto"""
        if project_id in self.active_projects:
            project = self.active_projects[project_id]
            return {
                'success': True,
                'project': {
                    'project_id': project.project_id,
                    'title': project.title,
                    'status': 'active',
                    'progress': 50.0,  # Simulado
                    'assets_count': len(project.assets),
                    'total_duration': project.total_duration,
                    'created_at': project.created_at.isoformat()
                },
                'timestamp': datetime.now().isoformat()
            }
        elif project_id in self.completed_projects:
            return {
                'success': True,
                'project': self.completed_projects[project_id],
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': False,
                'error': 'Projeto não encontrado',
                'timestamp': datetime.now().isoformat()
            }

    async def _list_templates(self) -> Dict[str, Any]:
        """Lista templates disponíveis"""
        return {
            'success': True,
            'templates': self.video_templates,
            'total_templates': len(self.video_templates),
            'timestamp': datetime.now().isoformat()
        }

    async def _apply_effects(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica efeitos a um vídeo"""
        # Implementação futura de efeitos avançados
        return {
            'success': False,
            'error': 'Funcionalidade de efeitos em desenvolvimento',
            'timestamp': datetime.now().isoformat()
        }

    async def _handle_unknown_action(self, action: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Trata ações não reconhecidas"""
        return {
            'success': False,
            'error': f'Ação não reconhecida: {action}',
            'available_actions': [
                'create_video',
                'create_slideshow',
                'add_audio_to_video',
                'merge_videos',
                'extract_frames',
                'optimize_for_platform',
                'get_project_status',
                'list_templates'
            ],
            'timestamp': datetime.now().isoformat()
        }

def create_agents(config: Dict[str, Any] = None) -> Dict[str, BaseNetworkAgent]:
    """
    Factory function para criar instâncias dos agentes de vídeo
    
    Returns:
        Dict[str, BaseNetworkAgent]: Dicionário com instâncias dos agentes
    """
    config = config or {}
    
    agents = {
        'video_automation': VideoAutomationAgent(
            agent_id="video_automation_agent",
            config=config.get('video_automation', {})
        )
    }
    
    # Log da criação
    logger = logging.getLogger("ALSHAM.VideoAutomation")
    logger.info(f"🎬 Video Automation Agent criado - Total: {len(agents)} agentes")
    
    return agents

# Export para compatibilidade
__all__ = [
    'VideoAutomationAgent',
    'BaseNetworkAgent',
    'create_agents',
    'VideoFormat',
    'VideoQuality', 
    'VideoStyle',
    'TransitionType',
    'VideoAsset',
    'VideoTransition',
    'VideoProject'
]

if __name__ == "__main__":
    # Test básico
    import asyncio
    
    async def test_video_agent():
        agent = VideoAutomationAgent()
        
        # Test slideshow creation
        slideshow_request = {
            'action': 'create_slideshow',
            'title': 'Test Slideshow',
            'images': [
                '/path/to/image1.jpg',
                '/path/to/image2.jpg', 
                '/path/to/image3.jpg'
            ],
            'duration_per_image': 3.0,
            'template': 'slideshow'
        }
        
        result = await agent.process_request(slideshow_request)
        print(f"✅ Resultado do slideshow: {result}")
        
        # Test template listing
        templates = await agent.process_request({'action': 'list_templates'})
        print(f"📋 Templates disponíveis: {len(templates['templates'])}")
    
    asyncio.run(test_video_agent())
