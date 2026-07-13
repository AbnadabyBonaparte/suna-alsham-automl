import { create } from 'zustand';
import { QuantumState } from '@/types/quantum';
import { fetchAgents } from './api';

// DATA HONESTY (Lei Suprema): zero dados fake.
// Estado inicial vazio/zerado — só é preenchido com dados REAIS do Supabase.
export const useQuantumStore = create<QuantumState>((set, get) => ({
  agents: [],
  metrics: {
    roi: 0,
    savings: 0,
    activeAgents: 0,
    systemLoad: 0,
    quantumStability: 0,
  },
  isLive: false,

  toggleLiveMode: () => set((state) => ({ isLive: !state.isLive })),

  updateMetrics: (newMetrics) => set((state) => ({ metrics: { ...state.metrics, ...newMetrics } })),

  updateAgent: (id, data) =>
    set((state) => ({
      agents: state.agents.map((agent) => (agent.id === id ? { ...agent, ...data } : agent)),
    })),

  // Sincroniza SOMENTE dados reais. Sem agentes reais, o estado permanece
  // vazio (empty state honesto) — nunca métricas inventadas.
  syncAgents: async () => {
    try {
      const realAgents = await fetchAgents();
      set({
        agents: realAgents,
        isLive: realAgents.length > 0,
        metrics: {
          ...get().metrics,
          activeAgents: realAgents.filter((a) => a.status === 'PROCESSING').length,
        },
      });
    } catch {
      // Falha ao buscar: mantém estado vazio e honesto, sem simular nada.
      set({ agents: [], isLive: false });
    }
  },
}));
