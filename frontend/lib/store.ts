import { create } from 'zustand';
import { QuantumState, Agent } from '@/types/quantum';

const INITIAL_AGENTS: Agent[] = [
  { id: '1', name: 'ALSHAM-CORE-01', role: 'CORE', status: 'PROCESSING', efficiency: 98.5, currentTask: 'Otimizando ROI', lastActive: 'Now' },
  { id: '2', name: 'GUARDIAN-X', role: 'GUARD', status: 'IDLE', efficiency: 100, currentTask: 'Monitoramento de Rede', lastActive: '2m ago' },
  { id: '3', name: 'MARKET-SEER', role: 'SPECIALIST', status: 'LEARNING', efficiency: 92.1, currentTask: 'Análise de Tendência', lastActive: '5s ago' },
  { id: '4', name: 'NEXUS-LINK', role: 'ANALYST', status: 'PROCESSING', efficiency: 95.4, currentTask: 'Indexação de Dados', lastActive: 'Now' },
];

export const useQuantumStore = create<QuantumState>((set, get) => ({
  agents: INITIAL_AGENTS,
  metrics: {
    roi: 2847,
    savings: 4.7,
    activeAgents: 57,
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

    const loadFluctuation = Math.random() > 0.5 ? 1 : -1;
    const newLoad = Math.min(100, Math.max(10, state.metrics.systemLoad + loadFluctuation));

    const newAgents = state.agents.map(agent => {
        if (Math.random() > 0.7) {
            return {
                ...agent,
                efficiency: Math.min(100, Math.max(80, agent.efficiency + (Math.random() - 0.5))),
                status: Math.random() > 0.9 ? 'LEARNING' : agent.status
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
