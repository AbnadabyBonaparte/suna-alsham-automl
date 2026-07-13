/**
 * Hook para buscar estatísticas reais do dashboard
 * Integrado com Zustand store
 */
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useDashboardStore } from '@/stores/useDashboardStore';

export function useDashboardStats() {
  const store = useDashboardStore();

  useEffect(() => {
    async function fetchStats() {
      const startTime = performance.now();

      try {
        store.setStats({ loading: true, error: null });

        // 1. Agents stats
        const { data: agents, error: agentsError } = await supabase
          .from('agents')
          .select('efficiency, status, current_task')
          .limit(40);

        if (agentsError) throw agentsError;

        const avgEfficiency = agents?.length
          ? agents.reduce(
              (sum: number, a: { efficiency?: number }) => sum + (a.efficiency || 0),
              0,
            ) / agents.length
          : 0;
        const agentEfficiencies =
          agents?.map((a: { efficiency?: number }) => a.efficiency || 0) || [];

        const { count: totalAgentsCount } = await supabase
          .from('agents')
          .select('*', { count: 'exact', head: true });

        // "Ativo" = operacional (não em falha). Enum real: IDLE|PROCESSING|LEARNING|WARNING|ERROR
        const { count: activeAgentsCount } = await supabase
          .from('agents')
          .select('*', { count: 'exact', head: true })
          .in('status', ['IDLE', 'PROCESSING', 'LEARNING']);

        const { count: dealsCount } = await supabase
          .from('deals')
          .select('*', { count: 'exact', head: true });

        const { count: ticketsCount } = await supabase
          .from('support_tickets')
          .select('*', { count: 'exact', head: true });

        const { count: postsCount } = await supabase
          .from('social_posts')
          .select('*', { count: 'exact', head: true });

        const endTime = performance.now();
        const latency = Math.round(endTime - startTime);

        store.setStats({
          totalAgents: totalAgentsCount || 0,
          avgEfficiency: Math.round(avgEfficiency * 10) / 10,
          activeAgents: activeAgentsCount || 0,
          totalDeals: dealsCount || 0,
          totalTickets: ticketsCount || 0,
          totalPosts: postsCount || 0,
          latencyMs: latency,
          // Sem fonte real de uptime (não há monitor de disponibilidade).
          // Não inventamos "99,x%" a partir de data/downtime hardcoded.
          uptimePercent: null,
          agentEfficiencies,
          loading: false,
          error: null,
        });
      } catch (err: any) {
        console.error('Error fetching dashboard stats:', err);
        store.setStats({
          loading: false,
          error: err.message,
        });
      }
    }

    fetchStats();
  }, []);

  return store;
}
