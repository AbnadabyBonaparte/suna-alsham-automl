"""
Dashboard de Evolução SUNA-ALSHAM
Apresentação visual e compreensível das melhorias do sistema
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class AgentEvolution:
    """Dados de evolução de um agente"""
    agent_id: str
    agent_name: str
    initial_performance: float
    current_performance: float
    last_cycle_performance: float
    evolution_percentage: float
    improvements: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)

class EvolutionDashboard:
    """Dashboard empresarial para mostrar evolução do sistema"""
    
    def __init__(self):
        self.evolution_data = {}
        self.cycle_number = 0
        self.start_date = datetime.now()
        self.client_metrics = defaultdict(float)
        
    def format_percentage(self, value: float, show_sign: bool = True) -> str:
        """Formata porcentagem com sinal positivo/negativo"""
        sign = "+" if value > 0 and show_sign else ""
        return f"{sign}{value:.1f}%"
    
    def calculate_roi_impact(self, performance_gain: float) -> Dict[str, float]:
        """Calcula impacto no ROI baseado em ganho de performance"""
        # Fórmulas simplificadas mas realistas
        roi_increase = performance_gain * 1.5  # 1.5x multiplicador
        cost_reduction = performance_gain * 0.8  # 80% do ganho vira redução de custo
        efficiency_gain = performance_gain * 2.1  # Eficiência tem maior impacto
        
        return {
            "roi_increase": roi_increase,
            "cost_reduction": cost_reduction,
            "efficiency_gain": efficiency_gain
        }
    
    def generate_executive_summary(self) -> str:
        """Gera resumo executivo para C-level"""
        total_evolution = sum(agent.evolution_percentage for agent in self.evolution_data.values()) / len(self.evolution_data) if self.evolution_data else 0
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║           SUNA-ALSHAM AI - RESUMO EXECUTIVO                  ║
╚══════════════════════════════════════════════════════════════╝

📅 Período: {self.start_date.strftime('%d/%m/%Y')} - {datetime.now().strftime('%d/%m/%Y')}
🔄 Ciclos Completados: {self.cycle_number}
📈 Evolução Média do Sistema: {self.format_percentage(total_evolution)}

💼 IMPACTO NOS NEGÓCIOS:
├─ 📊 ROI: {self.format_percentage(total_evolution * 1.5)}
├─ 💰 Redução de Custos: {self.format_percentage(total_evolution * 0.8)}
├─ ⚡ Eficiência Operacional: {self.format_percentage(total_evolution * 2.1)}
└─ 🎯 Precisão de Decisões: {self.format_percentage(total_evolution * 1.2)}

🏆 TOP 3 AGENTES MAIS EVOLUÍDOS:
"""
        
        # Top 3 agentes
        top_agents = sorted(self.evolution_data.values(), key=lambda x: x.evolution_percentage, reverse=True)[:3]
        for i, agent in enumerate(top_agents, 1):
            summary += f"{i}. {agent.agent_name}: {self.format_percentage(agent.evolution_percentage)}\n"
        
        return summary
    
    def generate_agent_report(self, agent: AgentEvolution) -> str:
        """Gera relatório individual de agente"""
        last_cycle_gain = agent.current_performance - agent.last_cycle_performance
        
        report = f"""
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AGENTE: {agent.agent_name.upper():<47}│
├─────────────────────────────────────────────────────────────┤
│ 📊 MÉTRICAS DE PERFORMANCE:                                 │
│   • Performance Atual: {agent.current_performance:.1f}%                           │
│   • Ganho Último Ciclo: {self.format_percentage(last_cycle_gain):<10}           │
│   • Evolução Total: {self.format_percentage(agent.evolution_percentage):<10}              │
│                                                             │
│ 📈 HISTÓRICO:                                               │
│   • Performance Inicial: {agent.initial_performance:.1f}%                         │
│   • Ciclos de Melhoria: {self.cycle_number}                                │
│   • Taxa de Evolução: {(agent.evolution_percentage / max(1, self.cycle_number)):.2f}%/ciclo    │
│                                                             │
│ ✨ MELHORIAS IMPLEMENTADAS:                                 │
"""
        
        for improvement in agent.improvements[-3:]:  # Últimas 3 melhorias
            report += f"│   • {improvement:<53}│\n"
        
        report += "└─────────────────────────────────────────────────────────────┘"
        
        return report
    
    def generate_visual_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Gera barra de progresso visual"""
        filled = int(width * percentage / 100)
        empty = width - filled
        
        if percentage >= 80:
            color = "🟩"
        elif percentage >= 60:
            color = "🟨"
        else:
            color = "🟥"
        
        bar = f"[{color * filled}{'⬜' * empty}] {percentage:.1f}%"
        return bar
    
    def generate_client_dashboard(self) -> str:
        """Gera dashboard completo para cliente"""
        dashboard = self.generate_executive_summary()
        
        dashboard += "\n\n📊 EVOLUÇÃO POR AGENTE:\n"
        dashboard += "━" * 65 + "\n"
        
        for agent in self.evolution_data.values():
            evolution_bar = self.generate_visual_progress_bar(agent.current_performance)
            dashboard += f"\n{agent.agent_name:<25} {evolution_bar}"
            dashboard += f"\nEvolução: {self.format_percentage(agent.evolution_percentage)} desde instalação\n"
        
        # Métricas de negócio
        dashboard += "\n\n💼 MÉTRICAS DE NEGÓCIO:\n"
        dashboard += "━" * 65 + "\n"
        
        if self.client_metrics:
            for metric, value in self.client_metrics.items():
                dashboard += f"• {metric}: {value}\n"
        
        return dashboard
    
    def update_agent_evolution(self, agent_id: str, performance_data: Dict[str, Any]):
        """Atualiza dados de evolução de um agente"""
        if agent_id not in self.evolution_data:
            # Primeira vez
            self.evolution_data[agent_id] = AgentEvolution(
                agent_id=agent_id,
                agent_name=performance_data.get('name', agent_id),
                initial_performance=performance_data.get('performance', 70.0),
                current_performance=performance_data.get('performance', 70.0),
                last_cycle_performance=performance_data.get('performance', 70.0),
                evolution_percentage=0.0
            )
        else:
            agent = self.evolution_data[agent_id]
            agent.last_cycle_performance = agent.current_performance
            agent.current_performance = performance_data.get('performance', agent.current_performance)
            agent.evolution_percentage = ((agent.current_performance - agent.initial_performance) / agent.initial_performance) * 100
            
            # Adicionar melhorias
            if 'improvements' in performance_data:
                agent.improvements.extend(performance_data['improvements'])
    
    def save_dashboard_state(self, filepath: str = "evolution_dashboard.json"):
        """Salva estado do dashboard"""
        state = {
            "cycle_number": self.cycle_number,
            "start_date": self.start_date.isoformat(),
            "evolution_data": {
                agent_id: {
                    "agent_name": agent.agent_name,
                    "initial_performance": agent.initial_performance,
                    "current_performance": agent.current_performance,
                    "evolution_percentage": agent.evolution_percentage,
                    "improvements": agent.improvements
                }
                for agent_id, agent in self.evolution_data.items()
            },
            "client_metrics": dict(self.client_metrics)
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    async def display_realtime_dashboard(self):
        """Display dashboard em tempo real (para web interface)"""
        while True:
            # Clear screen (em produção, enviaria para WebSocket)
            print("\033[2J\033[H")  # Clear terminal
            
            # Mostrar dashboard
            print(self.generate_client_dashboard())
            
            # Atualizar a cada 30 segundos
            await asyncio.sleep(30)

# Integração com FastAPI para endpoint web
def create_dashboard_endpoints(app):
    """Cria endpoints para dashboard web"""
    dashboard = EvolutionDashboard()
    
    @app.get("/dashboard")
    async def get_dashboard():
        """Retorna dashboard em formato JSON para frontend"""
        return {
            "executive_summary": dashboard.generate_executive_summary(),
            "agents": [
                {
                    "id": agent.agent_id,
                    "name": agent.agent_name,
                    "current_performance": agent.current_performance,
                    "evolution": agent.evolution_percentage,
                    "improvements": agent.improvements[-5:]  # Últimas 5
                }
                for agent in dashboard.evolution_data.values()
            ],
            "business_metrics": dict(dashboard.client_metrics),
            "cycle": dashboard.cycle_number
        }
    
    @app.get("/dashboard/agent/{agent_id}")
    async def get_agent_details(agent_id: str):
        """Retorna detalhes de um agente específico"""
        if agent_id in dashboard.evolution_data:
            agent = dashboard.evolution_data[agent_id]
            return {
                "report": dashboard.generate_agent_report(agent),
                "data": {
                    "name": agent.agent_name,
                    "performance": agent.current_performance,
                    "evolution": agent.evolution_percentage,
                    "history": agent.metrics
                }
            }
        return {"error": "Agent not found"}
    
    return dashboard

# Exemplo de uso
if __name__ == "__main__":
    # Simular evolução
    dashboard = EvolutionDashboard()
    
    # Dados fictícios para demonstração
    agents_data = [
        {"id": "video_creator_001", "name": "VideoCreator AI", "performance": 75.0},
        {"id": "content_analyzer_001", "name": "Content Analyzer", "performance": 82.0},
        {"id": "social_poster_001", "name": "Social Media Bot", "performance": 69.0}
    ]
    
    # Simular 5 ciclos de evolução
    for cycle in range(5):
        dashboard.cycle_number = cycle + 1
        
        for agent in agents_data:
            # Simular melhoria de 2-5% por ciclo
            improvement = 2 + (cycle * 0.8)
            agent["performance"] += improvement
            agent["improvements"] = [f"Otimização algoritmo v{cycle+1}"]
            
            dashboard.update_agent_evolution(agent["id"], agent)
    
    # Mostrar dashboard
    print(dashboard.generate_client_dashboard())
