import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface AnalyticsData {
  agentsBySquad: { squad: string; count: number; avgEfficiency: number }[];
  requestsByStatus: { status: string; count: number }[];
  efficiencyOverTime: { date: string; efficiency: number }[];
  systemMetrics: {
    totalAgents: number;
    activeAgents: number;
    avgEfficiency: number;
    totalRequests: number;
    uptime: number;
  };
}

interface AnalyticsStore {
  data: AnalyticsData | null;
  loading: boolean;
  error: string | null;
  timeRange: '7d' | '30d' | '90d';
  setData: (data: AnalyticsData) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setTimeRange: (range: '7d' | '30d' | '90d') => void;
}

export const useAnalyticsStore = create<AnalyticsStore>()(
  devtools(
    (set) => ({
      data: null,
      loading: false,
      error: null,
      timeRange: '30d',
      setData: (data) => set({ data }, false, 'analytics/setData'),
      setLoading: (loading) => set({ loading }, false, 'analytics/setLoading'),
      setError: (error) => set({ error }, false, 'analytics/setError'),
      setTimeRange: (timeRange) => set({ timeRange }, false, 'analytics/setTimeRange'),
    }),
    { name: 'AnalyticsStore' }
  )
);
