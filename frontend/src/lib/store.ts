import { create } from 'zustand';
import { QuantumState, Agent } from '@/types/quantum';
import { fetchAgents } from './api';

// DADOS DE FALLBACK (Caso o Backend esteja dormindo)
const FALLBACK_AGENTS: Agent[] = [
  { id: 'sec-01', name: 'SECURITY-GUARDIAN', role: 'GUARD', status: 'PROCESSING', efficiency: 99.9, currentTask: 'Varredura Ativa', lastActive: 'Now' },
  { id: 'web-01', name: 'WEB-SEARCH-OMEGA', role: 'SPECIALIST', status: 'IDLE', efficiency: 94.1, currentTask: 'Aguardando', lastActive: '2s ago' },
  { id: 'cor-v3', name: 'CORE-AGENT-V3', role: 'CORE', status: 'LEARNING', efficiency: 97.5, currentTask: 'Otimização', lastActive: 'Now' },
];

export const useQuantumStore = create<QuantumState>((set, get) => ({
  agents: FALLBACK_AGENTS,
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

  simulatePulse: async () => {
    const state = get();
    if (!state.isLive) return;

    // TENTATIVA DE CONEXÃO REAL
    try {
        const realAgents = await fetchAgents();
        if (realAgents && realAgents.length > 0) {
            set({ agents: realAgents });
            return; // Se conseguiu dados reais, para a simulação
        }
    } catch (e) {
        // Falha silenciosa, mantém simulação
    }

    // SIMULAÇÃO (FALLBACK)
    const loadFluctuation = Math.random() > 0.5 ? 0.5 : -0.5;
    const newLoad = Math.min(100, Math.max(10, state.metrics.systemLoad + loadFluctuation));

    const newAgents = state.agents.map(agent => {
        if (Math.random() > 0.7) {
            return {
                ...agent,
                efficiency: Math.min(100, Math.max(70, agent.efficiency + (Math.random() - 0.5) * 2))
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
