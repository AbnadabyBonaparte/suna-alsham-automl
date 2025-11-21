import { create } from 'zustand';
import { QuantumState, Agent } from '@/types/quantum';
import { fetchAgents } from './api';

// DADOS DE FALLBACK (Caso o Backend esteja dormindo)
const FALLBACK_AGENTS: Agent[] = [
  { id: 'orc-alpha', name: 'ORCHESTRA ALPHA', role: 'CORE', status: 'ACTIVE', efficiency: 99.9, currentTask: 'Sincronizando 5 nós neurais', lastActive: 'Now' },
  { id: 'rev-hunt', name: 'REVENUE HUNTER', role: 'SPECIALIST', status: 'PROCESSING', efficiency: 94.2, currentTask: 'Analisando padrões de compra globais', lastActive: 'Now' },
  { id: 'sec-guard', name: 'SECURITY GUARDIAN', role: 'GUARD', status: 'ACTIVE', efficiency: 100.0, currentTask: 'Varredura de ameaças quânticas', lastActive: 'Now' },
  { id: 'cont-cre', name: 'CONTENT CREATOR', role: 'ANALYST', status: 'IDLE', efficiency: 87.15, currentTask: 'Agregando multicanal', lastActive: '2m ago' },
  { id: 'mark-pred', name: 'MARKET PREDICTOR', role: 'ANALYST', status: 'WARNING', efficiency: 76.1, currentTask: 'Recalculando volatilidade do mercado', lastActive: '1m ago' },
  { id: 'supp-sent', name: 'SUPPORT SENTINEL', role: 'SPECIALIST', status: 'ACTIVE', efficiency: 98.3, currentTask: 'Monitoramento de tickets em tempo real', lastActive: 'Now' },
  { id: 'dev-mast', name: 'DEVOPS MASTER', role: 'CORE', status: 'ACTIVE', efficiency: 98.4, currentTask: 'Otimizando pipeline CI/CD', lastActive: 'Now' },
  { id: 'data-min', name: 'DATA MINER', role: 'ANALYST', status: 'PROCESSING', efficiency: 91.4, currentTask: 'Extração de dados profundos', lastActive: 'Now' },
  { id: 'net-watch', name: 'NETWORK WATCHER', role: 'GUARD', status: 'ACTIVE', efficiency: 100.0, currentTask: 'Ping 2ms - Latência zero', lastActive: 'Now' },
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