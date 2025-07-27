#!/usr/bin/env python3
"""
Visualization Agent - Criação de dashboards e gráficos avançados
Sistema de visualização completo para SUNA-ALSHAM
"""

import logging
import asyncio
import json
import base64
import io
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class ChartType(Enum):
    """Tipos de gráficos suportados"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    BOX_PLOT = "box_plot"
    AREA = "area"
    GAUGE = "gauge"
    TREEMAP = "treemap"
    SANKEY = "sankey"
    NETWORK_GRAPH = "network_graph"
    TIME_SERIES = "time_series"
    REAL_TIME = "real_time"

class DashboardTheme(Enum):
    """Temas de dashboard"""
    DARK = "dark"
    LIGHT = "light"
    CORPORATE = "corporate"
    TECH = "tech"
    MINIMAL = "minimal"
    COLORFUL = "colorful"

@dataclass
class ChartConfig:
    """Configuração de gráfico"""
    chart_id: str
    chart_type: ChartType
    title: str
    data_source: str
    x_axis: str
    y_axis: str
    color_scheme: str = "viridis"
    interactive: bool = True
    real_time: bool = False
    refresh_interval: int = 30  # segundos
    filters: Dict[str, Any] = field(default_factory=dict)
    styling: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Dashboard:
    """Dashboard completo"""
    dashboard_id: str
    title: str
    description: str
    theme: DashboardTheme
    charts: List[ChartConfig]
    layout: Dict[str, Any]
    auto_refresh: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class VisualizationRequest:
    """Requisição de visualização"""
    request_id: str
    request_type: str  # chart, dashboard, report
    data: Dict[str, Any]
    config: Dict[str, Any]
    requester_id: str
    priority: Priority
    timestamp: datetime = field(default_factory=datetime.now)

class VisualizationAgent(BaseNetworkAgent):
    """Agente especializado em criação de visualizações e dashboards"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'chart_generation',
            'dashboard_creation',
            'real_time_visualization',
            'interactive_plots',
            'data_analysis',
            'report_generation',
            'trend_visualization',
            'performance_dashboards',
            'network_visualization',
            'custom_themes'
        ]
        self.status = 'active'
        
        # Estado do agente
        self.visualization_queue = asyncio.Queue()
        self.active_dashboards = {}  # dashboard_id -> Dashboard
        self.chart_cache = {}  # chart_id -> cached chart
        self.data_sources = {}  # source_id -> data connection
        self.real_time_streams = {}  # stream_id -> stream config
        
        # Configurações
        self.default_theme = DashboardTheme.TECH
        self.chart_cache_ttl = 300  # 5 minutos
        self.max_data_points = 10000
        self.auto_save_interval = 60  # segundos
        
        # Templates pré-definidos
        self.dashboard_templates = self._load_dashboard_templates()
        self.chart_templates = self._load_chart_templates()
        self.color_palettes = self._load_color_palettes()
        
        # Métricas
        self.visualization_metrics = {
            'charts_created': 0,
            'dashboards_created': 0,
            'real_time_updates': 0,
            'data_points_processed': 0,
            'export_requests': 0
        }
        
        # Tasks de background
        self._processing_task = None
        self._real_time_task = None
        self._cleanup_task = None
        
        # Configurar matplotlib e seaborn
        self._setup_visualization_environment()
        
        logger.info(f"📊 {self.agent_id} inicializado com capacidades avançadas de visualização")
    
    def _setup_visualization_environment(self):
        """Configura ambiente de visualização"""
        # Matplotlib
        plt.style.use('dark_background')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        
        # Seaborn
        sns.set_palette("viridis")
        sns.set_context("notebook", font_scale=1.1)
    
    def _load_dashboard_templates(self) -> Dict[str, Dict[str, Any]]:
        """Carrega templates de dashboard pré-definidos"""
        return {
            'system_overview': {
                'title': 'SUNA-ALSHAM System Overview',
                'description': 'Visão geral completa do sistema',
                'charts': [
                    {'type': ChartType.GAUGE, 'title': 'System Health', 'position': (0, 0)},
                    {'type': ChartType.LINE, 'title': 'Agent Activity', 'position': (0, 1)},
                    {'type': ChartType.PIE, 'title': 'Agent Distribution', 'position': (1, 0)},
                    {'type': ChartType.HEATMAP, 'title': 'Message Flow', 'position': (1, 1)}
                ]
            },
            'performance_dashboard': {
                'title': 'Performance Analytics',
                'description': 'Métricas de performance em tempo real',
                'charts': [
                    {'type': ChartType.TIME_SERIES, 'title': 'CPU Usage', 'position': (0, 0)},
                    {'type': ChartType.TIME_SERIES, 'title': 'Memory Usage', 'position': (0, 1)},
                    {'type': ChartType.BAR, 'title': 'Top Processes', 'position': (1, 0)},
                    {'type': ChartType.AREA, 'title': 'Network I/O', 'position': (1, 1)}
                ]
            },
            'agent_network': {
                'title': 'Agent Network Visualization',
                'description': 'Rede de comunicação entre agentes',
                'charts': [
                    {'type': ChartType.NETWORK_GRAPH, 'title': 'Agent Network', 'position': (0, 0, 2, 2)},
                    {'type': ChartType.SANKEY, 'title': 'Message Flow', 'position': (2, 0)},
                    {'type': ChartType.BAR, 'title': 'Message Volume', 'position': (2, 1)}
                ]
            },
            'evolution_tracking': {
                'title': 'Evolution & Learning Dashboard',
                'description': 'Acompanhamento da evolução do sistema',
                'charts': [
                    {'type': ChartType.LINE, 'title': 'Learning Progress', 'position': (0, 0)},
                    {'type': ChartType.SCATTER, 'title': 'Performance vs Complexity', 'position': (0, 1)},
                    {'type': ChartType.TREEMAP, 'title': 'Code Quality Metrics', 'position': (1, 0)},
                    {'type': ChartType.BOX_PLOT, 'title': 'Optimization Results', 'position': (1, 1)}
                ]
            }
        }
    
    def _load_chart_templates(self) -> Dict[str, Dict[str, Any]]:
        """Carrega templates de gráficos"""
        return {
            'agent_performance': {
                'type': ChartType.LINE,
                'config': {
                    'x_axis': 'timestamp',
                    'y_axis': 'performance_score',
                    'color_by': 'agent_id',
                    'title': 'Agent Performance Over Time'
                }
            },
            'system_health_gauge': {
                'type': ChartType.GAUGE,
                'config': {
                    'value_field': 'health_score',
                    'min_value': 0,
                    'max_value': 100,
                    'thresholds': [30, 70, 90],
                    'colors': ['red', 'yellow', 'green', 'blue']
                }
            },
            'message_heatmap': {
                'type': ChartType.HEATMAP,
                'config': {
                    'x_axis': 'hour',
                    'y_axis': 'agent_type',
                    'value': 'message_count',
                    'color_scale': 'Blues'
                }
            }
        }
    
    def _load_color_palettes(self) -> Dict[str, List[str]]:
        """Carrega paletas de cores"""
        return {
            'tech': ['#00ff88', '#00ccff', '#ff6b6b', '#ffd93d', '#ff9f43'],
            'corporate': ['#3742fa', '#2ed573', '#ff4757', '#ffa502', '#747d8c'],
            'viridis': ['#440154', '#3b528b', '#21908c', '#5dc863', '#fde725'],
            'plasma': ['#0d0887', '#6a00a8', '#b12a90', '#e16462', '#fca636'],
            'cyberpunk': ['#00ff41', '#ff073a', '#00b4d8', '#ffd60a', '#e63946']
        }
    
    async def start_visualization_service(self):
        """Inicia serviços de visualização"""
        if not self._processing_task:
            self._processing_task = asyncio.create_task(self._processing_loop())
            self._real_time_task = asyncio.create_task(self._real_time_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info(f"📊 {self.agent_id} iniciou serviços de visualização")
    
    async def stop_visualization_service(self):
        """Para serviços de visualização"""
        tasks = [self._processing_task, self._real_time_task, self._cleanup_task]
        for task in tasks:
            if task:
                task.cancel()
        
        self._processing_task = None
        self._real_time_task = None
        self._cleanup_task = None
        
        logger.info(f"🛑 {self.agent_id} parou serviços de visualização")
    
    async def _processing_loop(self):
        """Loop principal de processamento"""
        while True:
            try:
                if not self.visualization_queue.empty():
                    request = await self.visualization_queue.get()
                    await self._process_visualization_request(request)
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de processamento: {e}")
    
    async def _real_time_loop(self):
        """Loop para atualizações em tempo real"""
        while True:
            try:
                # Atualizar dashboards em tempo real
                for dashboard_id, dashboard in self.active_dashboards.items():
                    if dashboard.auto_refresh:
                        await self._update_real_time_dashboard(dashboard)
                
                await asyncio.sleep(5)  # Atualizar a cada 5 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop real-time: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza"""
        while True:
            try:
                # Limpar cache expirado
                current_time = datetime.now()
                expired_charts = []
                
                for chart_id, (chart_data, timestamp) in self.chart_cache.items():
                    if (current_time - timestamp).seconds > self.chart_cache_ttl:
                        expired_charts.append(chart_id)
                
                for chart_id in expired_charts:
                    del self.chart_cache[chart_id]
                
                await asyncio.sleep(self.auto_save_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no cleanup: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'create_chart':
                result = await self.create_chart(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'create_dashboard':
                result = await self.create_dashboard(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'update_real_time':
                result = await self.update_real_time_data(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'export_visualization':
                result = await self.export_visualization(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_dashboard':
                result = await self.get_dashboard(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de dados
            notification_type = message.content.get('notification_type')
            
            if notification_type == 'performance_data':
                await self._handle_performance_data(message.content)
            elif notification_type == 'agent_status':
                await self._handle_agent_status(message.content)
            elif notification_type == 'system_metrics':
                await self._handle_system_metrics(message.content)
    
    async def create_chart(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um gráfico"""
        try:
            chart_type = ChartType(request_data.get('chart_type', 'line'))
            data = request_data.get('data', [])
            config = request_data.get('config', {})
            
            logger.info(f"📊 Criando gráfico {chart_type.value}")
            
            # Validar dados
            if not data:
                return {'status': 'error', 'message': 'Dados não fornecidos'}
            
            # Criar gráfico baseado no tipo
            chart_result = None
            
            if chart_type == ChartType.LINE:
                chart_result = await self._create_line_chart(data, config)
            elif chart_type == ChartType.BAR:
                chart_result = await self._create_bar_chart(data, config)
            elif chart_type == ChartType.PIE:
                chart_result = await self._create_pie_chart(data, config)
            elif chart_type == ChartType.SCATTER:
                chart_result = await self._create_scatter_chart(data, config)
            elif chart_type == ChartType.HEATMAP:
                chart_result = await self._create_heatmap(data, config)
            elif chart_type == ChartType.GAUGE:
                chart_result = await self._create_gauge_chart(data, config)
            elif chart_type == ChartType.TIME_SERIES:
                chart_result = await self._create_time_series(data, config)
            elif chart_type == ChartType.NETWORK_GRAPH:
                chart_result = await self._create_network_graph(data, config)
            else:
                return {'status': 'error', 'message': f'Tipo de gráfico {chart_type.value} não suportado'}
            
            if chart_result:
                chart_id = f"chart_{len(self.chart_cache)}"
                self.chart_cache[chart_id] = (chart_result, datetime.now())
                self.visualization_metrics['charts_created'] += 1
                
                return {
                    'status': 'completed',
                    'chart_id': chart_id,
                    'chart_type': chart_type.value,
                    'chart_data': chart_result,
                    'config_used': config
                }
            else:
                return {'status': 'error', 'message': 'Falha na criação do gráfico'}
                
        except Exception as e:
            logger.error(f"❌ Erro criando gráfico: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _create_line_chart(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria gráfico de linha"""
        try:
            df = pd.DataFrame(data)
            
            # Configurações
            x_col = config.get('x_axis', df.columns[0])
            y_col = config.get('y_axis', df.columns[1] if len(df.columns) > 1 else df.columns[0])
            title = config.get('title', 'Line Chart')
            color_by = config.get('color_by')
            
            # Criar gráfico com Plotly
            if color_by and color_by in df.columns:
                fig = px.line(df, x=x_col, y=y_col, color=color_by, title=title)
            else:
                fig = px.line(df, x=x_col, y=y_col, title=title)
            
            # Aplicar tema
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            # Converter para JSON
            chart_json = fig.to_json()
            
            return {
                'type': 'plotly',
                'data': chart_json,
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando line chart: {e}")
            return None
    
    async def _create_bar_chart(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria gráfico de barras"""
        try:
            df = pd.DataFrame(data)
            
            x_col = config.get('x_axis', df.columns[0])
            y_col = config.get('y_axis', df.columns[1] if len(df.columns) > 1 else df.columns[0])
            title = config.get('title', 'Bar Chart')
            
            fig = px.bar(df, x=x_col, y=y_col, title=title)
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando bar chart: {e}")
            return None
    
    async def _create_pie_chart(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria gráfico de pizza"""
        try:
            df = pd.DataFrame(data)
            
            names_col = config.get('names', df.columns[0])
            values_col = config.get('values', df.columns[1] if len(df.columns) > 1 else df.columns[0])
            title = config.get('title', 'Pie Chart')
            
            fig = px.pie(df, names=names_col, values=values_col, title=title)
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando pie chart: {e}")
            return None
    
    async def _create_gauge_chart(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria gráfico gauge (medidor)"""
        try:
            value = data[0].get('value', 0) if data else 0
            title = config.get('title', 'Gauge Chart')
            min_val = config.get('min', 0)
            max_val = config.get('max', 100)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': title},
                delta={'reference': config.get('reference', max_val * 0.8)},
                gauge={'axis': {'range': [None, max_val]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, max_val * 0.3], 'color': "lightgray"},
                           {'range': [max_val * 0.3, max_val * 0.7], 'color': "gray"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': max_val * 0.9}}))
            
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando gauge chart: {e}")
            return None
    
    async def _create_heatmap(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria heatmap"""
        try:
            df = pd.DataFrame(data)
            
            # Preparar dados para heatmap
            if 'pivot' in config:
                pivot_config = config['pivot']
                df = df.pivot_table(
                    index=pivot_config.get('index'),
                    columns=pivot_config.get('columns'),
                    values=pivot_config.get('values'),
                    aggfunc=pivot_config.get('aggfunc', 'mean')
                )
            
            title = config.get('title', 'Heatmap')
            
            fig = px.imshow(df, title=title)
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando heatmap: {e}")
            return None
    
    async def _create_time_series(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria série temporal"""
        try:
            df = pd.DataFrame(data)
            
            # Converter coluna de tempo
            time_col = config.get('time_column', 'timestamp')
            if time_col in df.columns:
                df[time_col] = pd.to_datetime(df[time_col])
            
            value_col = config.get('value_column', 'value')
            title = config.get('title', 'Time Series')
            
            fig = px.line(df, x=time_col, y=value_col, title=title)
            
            # Configurações específicas de time series
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1h", step="hour", stepmode="backward"),
                        dict(count=6, label="6h", step="hour", stepmode="backward"),
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando time series: {e}")
            return None
    
    async def _create_network_graph(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria gráfico de rede"""
        try:
            # Extrair nós e arestas
            nodes = data.get('nodes', []) if isinstance(data, dict) else []
            edges = data.get('edges', []) if isinstance(data, dict) else []
            
            if not nodes:
                return None
            
            # Criar gráfico de rede com Plotly
            node_trace = go.Scatter(
                x=[node.get('x', 0) for node in nodes],
                y=[node.get('y', 0) for node in nodes],
                mode='markers+text',
                text=[node.get('name', '') for node in nodes],
                textposition="middle center",
                marker=dict(
                    size=[node.get('size', 10) for node in nodes],
                    color=[node.get('color', 'blue') for node in nodes]
                ),
                name="Agents"
            )
            
            edge_traces = []
            for edge in edges:
                edge_trace = go.Scatter(
                    x=[edge.get('x0'), edge.get('x1'), None],
                    y=[edge.get('y0'), edge.get('y1'), None],
                    mode='lines',
                    line=dict(width=edge.get('width', 1), color=edge.get('color', 'gray')),
                    showlegend=False
                )
                edge_traces.append(edge_trace)
            
            fig = go.Figure(data=[node_trace] + edge_traces)
            fig.update_layout(
                title=config.get('title', 'Network Graph'),
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Agent Network Visualization",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando network graph: {e}")
            return None
    
    async def _create_scatter_chart(self, data: List[Dict], config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria gráfico de dispersão"""
        try:
            df = pd.DataFrame(data)
            
            x_col = config.get('x_axis', df.columns[0])
            y_col = config.get('y_axis', df.columns[1] if len(df.columns) > 1 else df.columns[0])
            title = config.get('title', 'Scatter Plot')
            color_by = config.get('color_by')
            size_by = config.get('size_by')
            
            fig = px.scatter(
                df, x=x_col, y=y_col, 
                color=color_by if color_by and color_by in df.columns else None,
                size=size_by if size_by and size_by in df.columns else None,
                title=title
            )
            
            self._apply_theme(fig, config.get('theme', 'tech'))
            
            return {
                'type': 'plotly',
                'data': fig.to_json(),
                'config': config
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando scatter chart: {e}")
            return None
    
    def _apply_theme(self, fig, theme_name: str):
        """Aplica tema ao gráfico"""
        themes = {
            'tech': {
                'template': 'plotly_dark',
                'color_palette': self.color_palettes['tech']
            },
            'corporate': {
                'template': 'plotly_white',
                'color_palette': self.color_palettes['corporate']
            },
            'dark': {
                'template': 'plotly_dark',
                'color_palette': self.color_palettes['cyberpunk']
            }
        }
        
        theme = themes.get(theme_name, themes['tech'])
        
        fig.update_layout(
            template=theme['template'],
            colorway=theme['color_palette']
        )
    
    async def create_dashboard(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria dashboard completo"""
        try:
            template_name = request_data.get('template', 'system_overview')
            title = request_data.get('title', 'Custom Dashboard')
            theme = DashboardTheme(request_data.get('theme', 'tech'))
            
            logger.info(f"📊 Criando dashboard: {title}")
            
            # Usar template ou configuração customizada
            if template_name in self.dashboard_templates:
                template = self.dashboard_templates[template_name]
                charts_config = template['charts']
            else:
                charts_config = request_data.get('charts', [])
            
            # Criar dashboard
            dashboard_id = f"dashboard_{len(self.active_dashboards)}"
            
            dashboard = Dashboard(
                dashboard_id=dashboard_id,
                title=title,
                description=request_data.get('description', ''),
                theme=theme,
                charts=[],
                layout=request_data.get('layout', {'grid': True, 'columns': 2})
            )
            
            # Criar gráficos do dashboard
            created_charts = []
            for chart_config in charts_config:
                # Simular dados se não fornecidos
                chart_data = chart_config.get('data', self._generate_sample_data(chart_config['type']))
                
                chart_result = await self.create_chart({
                    'chart_type': chart_config['type'].value,
                    'data': chart_data,
                    'config': chart_config
                })
                
                if chart_result['status'] == 'completed':
                    created_charts.append(chart_result)
            
            dashboard.charts = created_charts
            self.active_dashboards[dashboard_id] = dashboard
            self.visualization_metrics['dashboards_created'] += 1
            
            return {
                'status': 'completed',
                'dashboard_id': dashboard_id,
                'title': title,
                'charts_created': len(created_charts),
                'dashboard_url': f"/dashboard/{dashboard_id}",
                'auto_refresh': dashboard.auto_refresh
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando dashboard: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_sample_data(self, chart_type: ChartType) -> List[Dict[str, Any]]:
        """Gera dados de exemplo para demonstração"""
        if chart_type == ChartType.LINE or chart_type == ChartType.TIME_SERIES:
            return [
                {'timestamp': datetime.now() - timedelta(minutes=i*5), 'value': 50 + i*2 + np.random.randint(-10, 10)}
                for i in range(20)
            ]
        elif chart_type == ChartType.BAR:
            return [
                {'category': f'Agent {i}', 'value': np.random.randint(10, 100)}
                for i in range(1, 8)
            ]
        elif chart_type == ChartType.PIE:
            return [
                {'name': 'Core Agents', 'value': 5},
                {'name': 'Specialized Agents', 'value': 8},
                {'name': 'System Agents', 'value': 3},
                {'name': 'Service Agents', 'value': 4}
            ]
        elif chart_type == ChartType.GAUGE:
            return [{'value': np.random.randint(60, 95)}]
        else:
            return [
                {'x': i, 'y': np.random.randint(1, 100)}
                for i in range(1, 21)
            ]
    
    async def update_real_time_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza dados em tempo real"""
        try:
            chart_id = request_data.get('chart_id')
            new_data = request_data.get('data', [])
            
            if chart_id in self.chart_cache:
                # Atualizar dados do gráfico
                chart_data, timestamp = self.chart_cache[chart_id]
                
                # Implementar lógica de atualização baseada no tipo
                # Por ora, substituir dados completamente
                updated_chart = await self._update_chart_data(chart_data, new_data)
                
                self.chart_cache[chart_id] = (updated_chart, datetime.now())
                self.visualization_metrics['real_time_updates'] += 1
                
                return {
                    'status': 'completed',
                    'chart_id': chart_id,
                    'updated_at': datetime.now().isoformat(),
                    'data_points': len(new_data)
                }
            else:
                return {'status': 'error', 'message': 'Chart not found'}
                
        except Exception as e:
            logger.error(f"❌ Erro atualizando dados real-time: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _update_chart_data(self, chart_data: Dict[str, Any], new_data: List[Dict]) -> Dict[str, Any]:
        """Atualiza dados de um gráfico"""
        # Implementação simplificada - em produção seria mais sofisticada
        chart_data['last_updated'] = datetime.now().isoformat()
        chart_data['data_points'] = len(new_data)
        return chart_data
    
    async def _update_real_time_dashboard(self, dashboard: Dashboard):
        """Atualiza dashboard em tempo real"""
        try:
            # Solicitar dados atualizados do sistema
            for chart in dashboard.charts:
                # Simular atualização com novos dados
                if chart.get('chart_type') in ['time_series', 'line', 'gauge']:
                    # Solicitar dados atualizados
                    await self._request_fresh_data(chart['chart_id'])
                    
        except Exception as e:
            logger.error(f"❌ Erro atualizando dashboard real-time: {e}")
    
    async def _request_fresh_data(self, chart_id: str):
        """Solicita dados frescos para um gráfico"""
        # Enviar requisição para outros agentes
        data_request = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="performance_monitor_001",
            message_type=MessageType.REQUEST,
            priority=Priority.LOW,
            content={
                'request_type': 'get_current_metrics',
                'chart_id': chart_id
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(data_request)
    
    async def export_visualization(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Exporta visualização"""
        try:
            export_type = request_data.get('format', 'png')  # png, pdf, html, json
            chart_id = request_data.get('chart_id')
            dashboard_id = request_data.get('dashboard_id')
            
            if chart_id and chart_id in self.chart_cache:
                # Exportar gráfico individual
                chart_data, _ = self.chart_cache[chart_id]
                export_result = await self._export_chart(chart_data, export_type)
                
            elif dashboard_id and dashboard_id in self.active_dashboards:
                # Exportar dashboard completo
                dashboard = self.active_dashboards[dashboard_id]
                export_result = await self._export_dashboard(dashboard, export_type)
                
            else:
                return {'status': 'error', 'message': 'Visualization not found'}
            
            self.visualization_metrics['export_requests'] += 1
            
            return {
                'status': 'completed',
                'format': export_type,
                'export_data': export_result,
                'exported_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro exportando visualização: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _export_chart(self, chart_data: Dict[str, Any], format_type: str) -> str:
        """Exporta gráfico individual"""
        if format_type == 'json':
            return json.dumps(chart_data, indent=2)
        elif format_type == 'html':
            return f"<div>Chart HTML Export: {chart_data.get('type', 'unknown')}</div>"
        else:
            return f"Binary export for {format_type} format"
    
    async def _export_dashboard(self, dashboard: Dashboard, format_type: str) -> str:
        """Exporta dashboard completo"""
        if format_type == 'json':
            return json.dumps({
                'dashboard_id': dashboard.dashboard_id,
                'title': dashboard.title,
                'charts_count': len(dashboard.charts),
                'theme': dashboard.theme.value,
                'exported_at': datetime.now().isoformat()
            }, indent=2)
        else:
            return f"Dashboard export for {format_type} format"
    
    async def get_dashboard(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna dashboard"""
        try:
            dashboard_id = request_data.get('dashboard_id')
            
            if dashboard_id in self.active_dashboards:
                dashboard = self.active_dashboards[dashboard_id]
                
                return {
                    'status': 'completed',
                    'dashboard': {
                        'id': dashboard.dashboard_id,
                        'title': dashboard.title,
                        'description': dashboard.description,
                        'theme': dashboard.theme.value,
                        'charts_count': len(dashboard.charts),
                        'auto_refresh': dashboard.auto_refresh,
                        'created_at': dashboard.created_at.isoformat(),
                        'last_updated': dashboard.last_updated.isoformat()
                    }
                }
            else:
                return {'status': 'error', 'message': 'Dashboard not found'}
                
        except Exception as e:
            logger.error(f"❌ Erro obtendo dashboard: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_performance_data(self, data: Dict[str, Any]):
        """Trata dados de performance recebidos"""
        # Atualizar dashboards de performance automaticamente
        for dashboard_id, dashboard in self.active_dashboards.items():
            if 'performance' in dashboard.title.lower():
                await self._update_real_time_dashboard(dashboard)
    
    async def _handle_agent_status(self, data: Dict[str, Any]):
        """Trata status de agentes"""
        # Atualizar visualizações de rede de agentes
        agent_id = data.get('agent_id')
        status = data.get('status')
        
        # Atualizar dashboards de agentes
        for dashboard_id, dashboard in self.active_dashboards.items():
            if 'agent' in dashboard.title.lower() or 'network' in dashboard.title.lower():
                await self._update_real_time_dashboard(dashboard)
    
    async def _handle_system_metrics(self, data: Dict[str, Any]):
        """Trata métricas do sistema"""
        # Atualizar dashboards de sistema
        for dashboard_id, dashboard in self.active_dashboards.items():
            if 'system' in dashboard.title.lower() or 'overview' in dashboard.title.lower():
                await self._update_real_time_dashboard(dashboard)
    
    async def _process_visualization_request(self, request: VisualizationRequest):
        """Processa requisição de visualização da fila"""
        try:
            if request.request_type == 'chart':
                await self.create_chart(request.data)
            elif request.request_type == 'dashboard':
                await self.create_dashboard(request.data)
            elif request.request_type == 'export':
                await self.export_visualization(request.data)
                
        except Exception as e:
            logger.error(f"❌ Erro processando requisição: {e}")
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

# Importações necessárias
from uuid import uuid4

def create_visualization_agent(message_bus, num_instances=1) -> List[VisualizationAgent]:
    """
    Cria agente de visualização
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de visualização
    """
    agents = []
    
    try:
        logger.info("📊 Criando VisualizationAgent para dashboards avançados...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "visualization_001"
        
        if agent_id not in existing_agents:
            try:
                agent = VisualizationAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de visualização
                asyncio.create_task(agent.start_visualization_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com visualização avançada")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de visualização criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando VisualizationAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []

# FastAPI Integration
def create_visualization_endpoints(app):
    """Cria endpoints FastAPI para visualizações"""
    
    @app.get("/dashboard/{dashboard_id}")
    async def get_dashboard_endpoint(dashboard_id: str):
        """Endpoint para acessar dashboard"""
        # Integração com o agente seria aqui
        return {
            "dashboard_id": dashboard_id,
            "status": "active",
            "charts": [],
            "real_time": True
        }
    
    @app.get("/chart/{chart_id}")
    async def get_chart_endpoint(chart_id: str):
        """Endpoint para acessar gráfico"""
        return {
            "chart_id": chart_id,
            "type": "line",
            "data": {}
        }
    
    @app.post("/visualization/create")
    async def create_visualization_endpoint(request: dict):
        """Endpoint para criar visualização"""
        return {
            "status": "created",
            "visualization_id": "viz_001"
        }

if __name__ == "__main__":
    # Teste básico
    print("🚀 VisualizationAgent - Sistema de Dashboards Avançados")
    print("📊 Capacidades: Gráficos interativos, dashboards real-time, temas customizados")
    print("🎨 Suporte: Plotly, Matplotlib, Seaborn, templates predefinidos")
    print("⚡ Real-time: Atualizações automáticas, streaming de dados")
