import os

# 1. ARQUIVO .ENV.LOCAL (Configurações)
env_content = """
# CONEXÃO COM O CÉREBRO (PYTHON/FASTAPI)
NEXT_PUBLIC_API_URL=https://suna-alsham-automl-production.up.railway.app

# CONEXÃO COM A MEMÓRIA (SUPABASE)
NEXT_PUBLIC_SUPABASE_URL=https://sua-url-supabase.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-chave-anonima

# CONFIGURAÇÕES DO SISTEMA
NEXT_PUBLIC_SYSTEM_VERSION=v11.0
NEXT_PUBLIC_ENV=production
"""

# 2. ARQUIVO API.TS (Ponte de Dados)
api_ts_content = """
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchSystemStatus() {
  try {
    // Tenta buscar do backend real
    const res = await fetch(`${API_URL}/api/system/status`, { next: { revalidate: 10 } });
    if (!res.ok) throw new Error('Falha na conexão neural');
    return res.json();
  } catch (error) {
    console.warn("⚠️ Backend Offline. Usando dados de fallback holográficos.");
    return null; // Retorna null para a UI saber que deve usar fallback
  }
}

export async function fetchAgents() {
  try {
    const res = await fetch(`${API_URL}/api/agents`, { next: { revalidate: 5 } });
    if (!res.ok) throw new Error('Falha ao listar agentes');
    return res.json();
  } catch (error) {
    return [];
  }
}
"""

# 3. ARQUIVO STORE.TS (Cérebro Híbrido)
store_ts_content = """
import { create } from 'zustand';
import { QuantumState, Agent } from '@/types/quantum';
import { fetchAgents } from './api';

// DADOS DE FALLBACK (Caso o Backend esteja dormindo)
const FALLBACK_AGENTS: Agent[] = [
  { id: 'sec-01', name: 'SECURITY-GUARDIAN', role: 'GUARD', status: 'PROCESSING', efficiency: 99.9, currentTask: 'Varredura Ativa', lastActive: 'Now' },
  { id: 'web-01', name: 'WEB-SEARCH-OMEGA', role: 'SPECIALIST', status: 'IDLE', efficiency: 94.1, currentTask: 'Aguardando', lastActive: '2s ago' },
  { id: 'cor-v3', name: 'CORE-AGENT-V3', role: 'CORE', status: 'LEARNING', efficiency: 97.5, currentTask: 'Otimização', lastActive: 'Now' },
  { id: 'db-01', name: 'DATABASE-MASTER', role: 'CORE', status: 'PROCESSING', efficiency: 99.8, currentTask: 'Sharding de Dados', lastActive: 'Now' },
  { id: 'viz-01', name: 'VISUALIZATION-AI', role: 'ANALYST', status: 'IDLE', efficiency: 100, currentTask: 'Renderizando Gráficos', lastActive: '1m ago' },
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
"""

# FUNÇÃO PARA ESCREVER
def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Arquivo RECRIADO: {path}")
    except Exception as e:
        print(f"❌ Erro em {path}: {e}")

print("🛠️ Iniciando reparo da camada de conexão...")
write_file(".env.local", env_content)
write_file("src/lib/api.ts", api_ts_content)
write_file("src/lib/store.ts", store_ts_content)
print("🏁 Reparo concluído.")
