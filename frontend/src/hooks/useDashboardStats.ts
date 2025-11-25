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
    loading: true,
    error: null,
  });

  useEffect(() => {
    async function fetchStats() {
      try {
        // 1. Agents stats
        const { data: agents, error: agentsError } = await supabase
          .from('agents')
          .select('efficiency, status');

        if (agentsError) throw agentsError;

        const totalAgents = agents?.length || 0;
        const activeAgents = agents?.filter(a => a.current_task && a.current_task !== 'Standby mode' && a.current_task !== 'Aguardando comando').length || 0;
        const avgEfficiency = agents?.length
          ? agents.reduce((sum, a) => sum + (a.efficiency || 0), 0) / agents.length
          : 0;

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

        setStats({
          totalAgents,
          avgEfficiency: Math.round(avgEfficiency * 10) / 10,
          activeAgents,
          totalDeals: dealsCount || 0,
          totalTickets: ticketsCount || 0,
          totalPosts: postsCount || 0,
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


