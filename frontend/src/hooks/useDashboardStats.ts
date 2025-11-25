/**
 * Hook para buscar estatísticas reais do dashboard
 */
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

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

export function useDashboardStats() {
  const [stats, setStats] = useState<DashboardStats>({
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
  });

  useEffect(() => {
    async function fetchStats() {
      const startTime = performance.now();
      
      try {
        // 1. Agents stats (pegando 40 para o gráfico)
        const { data: agents, error: agentsError } = await supabase
          .from('agents')
          .select('efficiency, status, current_task')
          .limit(40);

        if (agentsError) throw agentsError;

        const totalAgents = agents?.length || 0;
        const activeAgents = agents?.filter(a => a.current_task && a.current_task !== 'Standby mode' && a.current_task !== 'Aguardando comando').length || 0;
        const avgEfficiency = agents?.length
          ? agents.reduce((sum, a) => sum + (a.efficiency || 0), 0) / agents.length
          : 0;
        const agentEfficiencies = agents?.map(a => a.efficiency || 0) || [];

        // Contar total de agents
        const { count: totalAgentsCount } = await supabase
          .from('agents')
          .select('*', { count: 'exact', head: true });

        // 2. Deals count
        const { count: dealsCount } = await supabase
          .from('deals')
          .select('*', { count: 'exact', head: true });

        // 3. Tickets count
        const { count: ticketsCount } = await supabase
          .from('support_tickets')
          .select('*', { count: 'exact', head: true });

        // 4. Posts count
        const { count: postsCount } = await supabase
          .from('social_posts')
          .select('*', { count: 'exact', head: true });

        // Calcular uptime (assumindo sistema stable desde Jan 2025)
        const systemStartDate = new Date("2024-11-20T14:30:00-03:00");
        const now = new Date();
        const totalHours = (now.getTime() - systemStartDate.getTime()) / (1000 * 60 * 60);
        const downtimeHours = 0.5; // Downtime estimado (pode ser buscado de uma tabela depois)
        const uptimePercent = ((totalHours - downtimeHours) / totalHours) * 100;

        const endTime = performance.now();
        const latency = Math.round(endTime - startTime);

        setStats({
          totalAgents: totalAgentsCount || 0,
          avgEfficiency: Math.round(avgEfficiency * 10) / 10,
          activeAgents,
          totalDeals: dealsCount || 0,
          totalTickets: ticketsCount || 0,
          totalPosts: postsCount || 0,
          latencyMs: latency,
          uptimePercent: Math.round(uptimePercent * 100) / 100,
          agentEfficiencies,
          loading: false,
          error: null,
        });
      } catch (err: any) {
        console.error('Error fetching dashboard stats:', err);
        setStats(prev => ({
          ...prev,
          loading: false,
          error: err.message,
        }));
      }
    }

    fetchStats();
  }, []);

  return stats;
}


