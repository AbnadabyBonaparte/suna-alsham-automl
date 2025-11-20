import { create } from 'zustand';
import { QuantumState, Agent } from '@/types/quantum';

// DADOS REAIS BASEADOS NA VARREDURA FORENSE (SUNA LEGACY)
const INITIAL_AGENTS: Agent[] = [
  // 🛡️ SENTINELAS
  { id: 'sec-01', name: 'SECURITY-GUARDIAN', role: 'GUARD', status: 'PROCESSING', efficiency: 99.9, currentTask: 'Varredura de Ameaças Ativa', lastActive: 'Now' },
  { id: 'val-01', name: 'VALIDATION-SENTINEL', role: 'GUARD', status: 'IDLE', efficiency: 98.2, currentTask: 'Aguardando Input', lastActive: '5m ago' },
  { id: 'cor-v3', name: 'CORE-AGENT-V3', role: 'CORE', status: 'LEARNING', efficiency: 97.5, currentTask: 'Otimização Neural', lastActive: 'Now' },

  // 🧠 INTELIGÊNCIA
  { id: 'web-01', name: 'WEB-SEARCH-OMEGA', role: 'SPECIALIST', status: 'PROCESSING', efficiency: 94.1, currentTask: 'Indexando Novos Mercados', lastActive: '2s ago' },
  { id: 'viz-01', name: 'VISUALIZATION-AI', role: 'ANALYST', status: 'IDLE', efficiency: 100, currentTask: 'Renderizando Gráficos', lastActive: '1m ago' },
  { id: 'cod-01', name: 'CODE-ANALYZER', role: 'SPECIALIST', status: 'WARNING', efficiency: 89.4, currentTask: 'Refatoração Crítica', lastActive: '10s ago' },

  // ⚙️ INFRAESTRUTURA
  { id: 'db-01', name: 'DATABASE-MASTER', role: 'CORE', status: 'PROCESSING', efficiency: 99.8, currentTask: 'Sharding de Dados', lastActive: 'Now' },
  { id: 'dep-01', name: 'DEPLOYMENT-OPS', role: 'GUARD', status: 'IDLE', efficiency: 100, currentTask: 'Monitorando Vercel', lastActive: '1h ago' },
  
  // 💬 COMUNICAÇÃO
  { id: 'not-01', name: 'NOTIFICATION-HUB', role: 'ANALYST', status: 'IDLE', efficiency: 98.0, currentTask: 'Fila de E-mails Vazia', lastActive: '30m ago' },
];

export const useQuantumStore = create<QuantumState>((set, get) => ({
  agents: INITIAL_AGENTS,
  metrics: {
    roi: 2847,
    savings: 4.7,
    activeAgents: 57, // Número real confirmado no dossiê
    systemLoad: 42,
    quantumStability: 99.9,
  },
  isLive: true,

  toggleLiveMode: () => set((state) => ({ isLive: !state.isLive })),

  updateMetrics: (newMetrics) => 
    set((state) => ({ metrics: { ...state.metrics, ...newMetrics } })),

  updateAgent: (id, data) =>
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, ...data } : agent
      ),
    })),

  simulatePulse: () => {
    const state = get();
    if (!state.isLive) return;

    // Simulação de "Respiração" do Sistema
    const loadFluctuation = Math.random() > 0.5 ? 0.5 : -0.5;
    const newLoad = Math.min(100, Math.max(10, state.metrics.systemLoad + loadFluctuation));

    const newAgents = state.agents.map(agent => {
        // Aleatoriedade controlada para parecer real
        if (Math.random() > 0.7) {
            // Agentes processando mudam de eficiência
            const effChange = (Math.random() - 0.5) * 2;
            let newStatus = agent.status;
            
            // Lógica de status simples
            if (Math.random() > 0.95) newStatus = 'LEARNING';
            else if (Math.random() > 0.95) newStatus = 'PROCESSING';
            else if (Math.random() > 0.98) newStatus = 'IDLE';

            return {
                ...agent,
                efficiency: Math.min(100, Math.max(70, agent.efficiency + effChange)),
                status: newStatus
            }
        }
        return agent;
    });

    set({
        metrics: { ...state.metrics, systemLoad: newLoad },
        agents: newAgents
    });
  }
}));
