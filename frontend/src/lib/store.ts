import { create } from 'zustand';
import { Agent, QuantumState, AgentRole, AgentStatus } from '@/types/quantum';
import { fetchAgents } from './api';

// DADOS DE FALLBACK (Caso o Backend esteja dormindo)
const generateMockAgents = () => {
  const roles: AgentRole[] = ['CORE', 'GUARD', 'SPECIALIST', 'ANALYST'];
  const statuses: AgentStatus[] = ['ACTIVE', 'PROCESSING', 'LEARNING', 'WARNING', 'IDLE'];
  const tasks = [
    'Sincronizando nós neurais', 'Analisando padrões de compra', 'Varredura de ameaças',
    'Otimizando pipeline', 'Extração de dados', 'Monitoramento de latência',
    'Recalculando rotas', 'Indexando memória vetorial', 'Aguardando comando'
  ];

  const agents: Agent[] = [
    { id: 'orc-alpha', name: 'ORCHESTRA ALPHA', role: 'CORE', status: 'ACTIVE', efficiency: 99.9, currentTask: 'Sincronizando 57 nós neurais', lastActive: 'Now' },
    { id: 'rev-hunt', name: 'REVENUE HUNTER', role: 'SPECIALIST', status: 'PROCESSING', efficiency: 94.2, currentTask: 'Analisando padrões de compra globais', lastActive: 'Now' },
    { id: 'sec-guard', name: 'SECURITY GUARDIAN', role: 'GUARD', status: 'ACTIVE', efficiency: 100.0, currentTask: 'Varredura de ameaças quânticas', lastActive: 'Now' },
  ];

  for (let i = 4; i <= 57; i++) {
    agents.push({
      id: `agent-${i.toString().padStart(3, '0')}`,
      name: `UNIT-${Math.random().toString(36).substring(7).toUpperCase()}`,
      role: roles[Math.floor(Math.random() * roles.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      efficiency: 70 + Math.random() * 30,
      currentTask: tasks[Math.floor(Math.random() * tasks.length)],
      lastActive: `${Math.floor(Math.random() * 60)}s ago`
    });
  }
  return agents;
};

const FALLBACK_AGENTS: Agent[] = generateMockAgents();

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

  connectToQuantumCore: async () => {
    try {
      const realAgents = await fetchAgents();
      if (realAgents && realAgents.length > 0 && realAgents[0].id !== 'sec-01') { // sec-01 is mock
        set({ agents: realAgents, isLive: true });
        return;
      }
    } catch (e) {
      console.warn("Quantum Core connection failed, switching to simulation.");
    }
    set({ isLive: true }); // Keep live true to allow simulation to run
  },

  simulatePulse: async () => {
    const state = get();
    if (!state.isLive) return;

    // TENTATIVA DE CONEXÃO REAL (Throttle this in real app, but ok for now)
    // Only try real fetch occasionally or if we suspect we are back online? 
    // For now, let's mix real data fetch with simulation to keep it alive.

    try {
      // We can try to fetch real data here, but maybe it's too heavy for every pulse.
      // Let's just simulate for now unless explicitly connected.
      // If we want hybrid, we could check a flag.
    } catch (e) {
      // Silent fail
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
