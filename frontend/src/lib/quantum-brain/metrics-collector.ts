// ═══════════════════════════════════════════════════════════════
// COLETOR DE MÉTRICAS - 100% DADOS REAIS (DATA HONESTY!)
// SERVER-ONLY
// ═══════════════════════════════════════════════════════════════

import { createAdminClient } from '@/lib/supabase/admin';
import {
  QuantumBrainState,
  RoleStats,
  RealTimeMetrics,
  AgentRole,
  ROLE_TO_SQUAD,
  SQUAD_COLORS,
  ACTIVE_STATUSES,
  isActiveStatus,
} from './types';

export async function getBrainState(): Promise<QuantumBrainState> {
  const supabase = createAdminClient();

  // 1. Buscar estado do cérebro
  const { data: state } = await supabase
    .from('quantum_brain_state')
    .select('*')
    .single();

  if (!state) {
    throw new Error('Brain state not found. Run initialization SQL first.');
  }

  // 2. Calcular métricas em tempo real dos agents REAIS
  const { data: agents } = await supabase
    .from('agents')
    .select('status, efficiency');

  const totalAgents = agents?.length || 0;
  const activeAgents = agents?.filter(a => isActiveStatus(a.status)).length || 0;
  const avgEfficiency = agents && agents.length > 0
    ? agents.reduce((sum, a) => sum + (a.efficiency || 0), 0) / agents.length
    : 0;

  // 3. Contar fila (requests com status='queued')
  const { count: queueSize } = await supabase
    .from('requests')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'queued');

  // 4. Calcular success rate de quantum_tasks
  const { count: totalTasks } = await supabase
    .from('quantum_tasks')
    .select('*', { count: 'exact', head: true });

  const { count: completedTasks } = await supabase
    .from('quantum_tasks')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'completed');

  const successRate = totalTasks && totalTasks > 0
    ? (completedTasks || 0) / totalTasks
    : 0;

  // 5. Média de tempo de resposta
  const { data: recentTasks } = await supabase
    .from('quantum_tasks')
    .select('execution_time_ms')
    .eq('status', 'completed')
    .order('completed_at', { ascending: false })
    .limit(100);

  const avgResponseTime = recentTasks && recentTasks.length > 0
    ? recentTasks.reduce((sum, t) => sum + (t.execution_time_ms || 0), 0) / recentTasks.length
    : 0;

  // 6. Calcular uptime
  const uptimeStart = new Date(state.uptime_started_at);
  const uptimeSeconds = Math.floor((Date.now() - uptimeStart.getTime()) / 1000);

  return {
    ...state,
    total_agents: totalAgents,
    active_agents: activeAgents,
    average_efficiency: avgEfficiency,
    tasks_in_queue: queueSize || 0,
    success_rate: successRate,
    average_response_time_ms: avgResponseTime,
    uptime_seconds: uptimeSeconds,
  };
}

export async function getRoleStats(): Promise<RoleStats[]> {
  const supabase = createAdminClient();

  const { data: agents } = await supabase
    .from('agents')
    .select('role, status, efficiency');

  if (!agents) return [];

  const today = new Date().toISOString().split('T')[0];
  const { data: todayTasks } = await supabase
    .from('quantum_tasks')
    .select('agent_id')
    .gte('created_at', `${today}T00:00:00`)
    .eq('status', 'completed');

  const tasksByAgent = new Map<string, number>();
  todayTasks?.forEach(t => {
    tasksByAgent.set(t.agent_id, (tasksByAgent.get(t.agent_id) || 0) + 1);
  });

  const roleMap = new Map<AgentRole, { total: number; active: number; effSum: number; tasks: number }>();

  agents.forEach(agent => {
    const role = agent.role as AgentRole;
    const current = roleMap.get(role) || { total: 0, active: 0, effSum: 0, tasks: 0 };
    current.total++;
    if (isActiveStatus(agent.status)) current.active++;
    current.effSum += agent.efficiency || 0;
    roleMap.set(role, current);
  });

  const roles: AgentRole[] = ['CORE', 'GUARD', 'ANALYST', 'SPECIALIST'];

  return roles.map(role => {
    const stats = roleMap.get(role) || { total: 0, active: 0, effSum: 0, tasks: 0 };
    const squad = ROLE_TO_SQUAD[role];

    return {
      role,
      squad,
      color: SQUAD_COLORS[squad],
      total_agents: stats.total,
      active_agents: stats.active,
      average_efficiency: stats.total > 0 ? stats.effSum / stats.total : 0,
      tasks_today: stats.tasks,
    };
  });
}

export async function getRealTimeMetrics(): Promise<RealTimeMetrics> {
  const supabase = createAdminClient();

  const oneMinuteAgo = new Date(Date.now() - 60000).toISOString();
  const { count: tasksLastMinute } = await supabase
    .from('quantum_tasks')
    .select('*', { count: 'exact', head: true })
    .gte('created_at', oneMinuteAgo);

  const { count: activeAgents } = await supabase
    .from('agents')
    .select('*', { count: 'exact', head: true })
    .in('status', ACTIVE_STATUSES);

  const { count: queueSize } = await supabase
    .from('requests')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'queued');

  const { data: recentTasks } = await supabase
    .from('quantum_tasks')
    .select('execution_time_ms')
    .eq('status', 'completed')
    .order('completed_at', { ascending: false })
    .limit(50);

  const avgLatency = recentTasks && recentTasks.length > 0
    ? recentTasks.reduce((sum, t) => sum + (t.execution_time_ms || 0), 0) / recentTasks.length
    : 0;

  const { data: lastTasks } = await supabase
    .from('quantum_tasks')
    .select('status')
    .order('created_at', { ascending: false })
    .limit(100);

  const errorCount = lastTasks?.filter(t => t.status === 'failed').length || 0;
  const errorRate = lastTasks && lastTasks.length > 0 ? errorCount / lastTasks.length : 0;

  const { data: topAgents } = await supabase
    .from('agents')
    .select('id, name, efficiency')
    .in('status', ACTIVE_STATUSES)
    .order('efficiency', { ascending: false })
    .limit(5);

  return {
    timestamp: new Date().toISOString(),
    tasks_per_minute: tasksLastMinute || 0,
    active_agents: activeAgents || 0,
    queue_size: queueSize || 0,
    average_latency_ms: avgLatency,
    error_rate: errorRate,
    top_agents: topAgents || [],
  };
}

export async function getRecentTasks(limit: number = 10) {
  const supabase = createAdminClient();

  const { data } = await supabase
    .from('quantum_tasks')
    .select(`
      id,
      agent_id,
      status,
      execution_time_ms,
      tokens_used,
      cost_usd,
      created_at,
      completed_at
    `)
    .order('created_at', { ascending: false })
    .limit(limit);

  if (data && data.length > 0) {
    const agentIds = [...new Set(data.map(t => t.agent_id))];
    const { data: agents } = await supabase
      .from('agents')
      .select('id, name, role')
      .in('id', agentIds);

    const agentMap = new Map(agents?.map(a => [a.id, a]) || []);

    return data.map(task => ({
      ...task,
      agent_name: agentMap.get(task.agent_id)?.name || 'Unknown',
      agent_role: agentMap.get(task.agent_id)?.role || 'SPECIALIST',
    }));
  }

  return data || [];
}
