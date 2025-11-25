import { create } from 'zustand';

interface DashboardStats {
  totalAgents: number;
  avgEfficiency: number;
  activeAgents: number;
  totalDeals: number;
  totalTickets: number;
  totalPosts: number;
  latencyMs: number;
  uptimePercent: number;
  agentEfficiencies: number[];
  loading: boolean;
  error: string | null;
}

interface DashboardStore extends DashboardStats {
  setStats: (stats: Partial<DashboardStats>) => void;
  refreshStats: () => Promise<void>;
}

export const useDashboardStore = create<DashboardStore>((set) => ({
  totalAgents: 0,
  avgEfficiency: 0,
  activeAgents: 0,
  totalDeals: 0,
  totalTickets: 0,
  totalPosts: 0,
  latencyMs: 0,
  uptimePercent: 0,
  agentEfficiencies: [],
  loading: true,
  error: null,
  
  setStats: (stats) => set(stats),
  
  refreshStats: async () => {
    // Hook irá popular isso
    set({ loading: true });
  },
}));
