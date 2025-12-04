/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - EVOLUTION ANALYSIS API
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/evolution/analyze/route.ts
 * 🔍 Analisa performance dos agents e identifica candidatos para evolução
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseAdmin } from '@/lib/supabase-admin';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 60;

interface AgentPerformance {
  agent_id: string;
  agent_name: string;
  agent_role: string;
  total_requests: number;
  successful_requests: number;
  failed_requests: number;
  success_rate: number;
  avg_processing_time_ms: number;
  current_efficiency: number;
  evolution_count: number;
  last_evolved_at: string | null;
  recommendation: 'urgent' | 'recommended' | 'stable';
  issues: string[];
}

export async function GET(request: NextRequest) {
  try {
    const supabaseAdmin = getSupabaseAdmin();
    console.log('[EVOLUTION:ANALYZE] ═══════════════════════════════════════════');
    console.log('[EVOLUTION:ANALYZE] Iniciando análise de performance dos agents');

    // 1. Buscar métricas dos últimos 7 dias
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    const { data: metricsData, error: metricsError } = await supabaseAdmin
      .from('agent_metrics')
      .select('*')
      .gte('metric_date', sevenDaysAgo.toISOString().split('T')[0]);

    if (metricsError) {
      console.error('[EVOLUTION:ANALYZE] Erro ao buscar métricas:', metricsError);
      return NextResponse.json(
        { error: 'Erro ao buscar métricas dos agents', details: metricsError.message },
        { status: 500 }
      );
    }

    // 2. Buscar todos os agents
    const { data: agents, error: agentsError } = await supabaseAdmin
      .from('agents')
      .select('id, name, role, efficiency, evolution_count, last_evolved_at');

    if (agentsError) {
      console.error('[EVOLUTION:ANALYZE] Erro ao buscar agents:', agentsError);
      return NextResponse.json(
        { error: 'Erro ao buscar agents', details: agentsError.message },
        { status: 500 }
      );
    }

    console.log(`[EVOLUTION:ANALYZE] ${agents?.length || 0} agents encontrados`);
    console.log(`[EVOLUTION:ANALYZE] ${metricsData?.length || 0} registros de métricas encontrados`);

    // 3. Agregar métricas por agent
    const agentMetricsMap = new Map<string, {
      total_requests: number;
      successful_requests: number;
      failed_requests: number;
      avg_processing_time_ms: number;
    }>();

    metricsData?.forEach((metric) => {
      const existing = agentMetricsMap.get(metric.agent_id) || {
        total_requests: 0,
        successful_requests: 0,
        failed_requests: 0,
        avg_processing_time_ms: 0,
      };

      agentMetricsMap.set(metric.agent_id, {
        total_requests: existing.total_requests + (metric.requests_processed || 0),
        successful_requests: existing.successful_requests + (metric.requests_successful || 0),
        failed_requests: existing.failed_requests + (metric.requests_failed || 0),
        avg_processing_time_ms: Math.round(
          (existing.avg_processing_time_ms * existing.total_requests +
            (metric.avg_processing_time_ms || 0) * (metric.requests_processed || 0)) /
          (existing.total_requests + (metric.requests_processed || 0))
        ),
      });
    });

    // 4. Calcular performance de cada agent
    const performances: AgentPerformance[] = (agents || []).map((agent) => {
      const metrics = agentMetricsMap.get(agent.id) || {
        total_requests: 0,
        successful_requests: 0,
        failed_requests: 0,
        avg_processing_time_ms: 0,
      };

      const success_rate = metrics.total_requests > 0
        ? (metrics.successful_requests / metrics.total_requests) * 100
        : 100; // Sem dados = assume 100% (novo agent)

      // Identificar issues
      const issues: string[] = [];
      let recommendation: 'urgent' | 'recommended' | 'stable' = 'stable';

      if (metrics.total_requests === 0) {
        issues.push('Nenhuma request processada nos últimos 7 dias');
        recommendation = 'recommended';
      }

      if (success_rate < 50) {
        issues.push(`Taxa de sucesso muito baixa: ${success_rate.toFixed(1)}%`);
        recommendation = 'urgent';
      } else if (success_rate < 75) {
        issues.push(`Taxa de sucesso abaixo do ideal: ${success_rate.toFixed(1)}%`);
        recommendation = 'recommended';
      }

      if (metrics.avg_processing_time_ms > 30000) {
        issues.push(`Tempo de processamento alto: ${(metrics.avg_processing_time_ms / 1000).toFixed(1)}s`);
        if (recommendation !== 'urgent') recommendation = 'recommended';
      }

      if (agent.efficiency < 80) {
        issues.push(`Eficiência do agent baixa: ${agent.efficiency}%`);
        if (recommendation !== 'urgent') recommendation = 'recommended';
      }

      if (agent.evolution_count === 0 && metrics.total_requests > 10) {
        issues.push('Agent nunca foi evoluído apesar de ter experiência');
        if (recommendation === 'stable') recommendation = 'recommended';
      }

      return {
        agent_id: agent.id,
        agent_name: agent.name,
        agent_role: agent.role,
        total_requests: metrics.total_requests,
        successful_requests: metrics.successful_requests,
        failed_requests: metrics.failed_requests,
        success_rate: parseFloat(success_rate.toFixed(2)),
        avg_processing_time_ms: metrics.avg_processing_time_ms,
        current_efficiency: agent.efficiency,
        evolution_count: agent.evolution_count || 0,
        last_evolved_at: agent.last_evolved_at,
        recommendation,
        issues,
      };
    });

    // 5. Ordenar por urgência e pior performance
    const sortedPerformances = performances.sort((a, b) => {
      // Priorizar por urgência
      const urgencyWeight = { urgent: 3, recommended: 2, stable: 1 };
      if (urgencyWeight[a.recommendation] !== urgencyWeight[b.recommendation]) {
        return urgencyWeight[b.recommendation] - urgencyWeight[a.recommendation];
      }

      // Depois por success_rate (menor primeiro)
      return a.success_rate - b.success_rate;
    });

    // 6. Pegar os 5 piores (candidatos para evolução)
    const candidates = sortedPerformances
      .filter(p => p.recommendation !== 'stable')
      .slice(0, 5);

    console.log('[EVOLUTION:ANALYZE] ═══════════════════════════════════════════');
    console.log(`[EVOLUTION:ANALYZE] ${candidates.length} candidatos para evolução identificados`);
    console.log('[EVOLUTION:ANALYZE] Candidatos:', candidates.map(c => `${c.agent_name} (${c.recommendation})`).join(', '));
    console.log('[EVOLUTION:ANALYZE] ═══════════════════════════════════════════');

    return NextResponse.json({
      success: true,
      total_agents: performances.length,
      candidates_count: candidates.length,
      candidates,
      all_performances: sortedPerformances,
      analysis_period_days: 7,
      timestamp: new Date().toISOString(),
    });

  } catch (error: any) {
    console.error('[EVOLUTION:ANALYZE] ❌ Erro geral:', error);
    return NextResponse.json(
      { error: 'Erro ao analisar performance dos agents', details: error.message },
      { status: 500 }
    );
  }
}
