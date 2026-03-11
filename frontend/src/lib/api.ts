import { supabase } from './supabase';
import { Agent } from '@/types/quantum';

export async function fetchAgents(): Promise<Agent[]> {
  try {
    const { data, error } = await supabase
      .from('agents')
      .select('*')
      .order('name', { ascending: true });

    if (error) throw error;

    if (!data || data.length === 0) return [];

    return data.map((a: Record<string, unknown>) => ({
      id: a.id as string,
      name: (a.name as string) || 'Unknown Unit',
      role: (a.role as string) || 'SPECIALIST',
      status: (a.status as string) || 'IDLE',
      efficiency: (a.efficiency as number) || 0,
      currentTask: (a.current_task as string) || 'Aguardando comando',
      lastActive: new Date().toLocaleTimeString(),
    }));
  } catch (error) {
    console.error('fetchAgents failed:', error);
    return [];
  }
}

export async function fetchSystemStatus() {
  try {
    const { data, error } = await supabase
      .from('system_metrics')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (error) throw error;

    const { count: agentCount } = await supabase
      .from('agents')
      .select('*', { count: 'exact', head: true })
      .eq('status', 'PROCESSING');

    return {
      uptime: data?.uptime ?? '0%',
      active_agents: agentCount ?? 0,
      health: data?.health ?? 'UNKNOWN',
    };
  } catch (error) {
    console.error('fetchSystemStatus failed:', error);
    return {
      uptime: '0%',
      active_agents: 0,
      health: 'UNKNOWN',
    };
  }
}
