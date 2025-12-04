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

    // 1. Buscar todos os agents primeiro
    const { data: agents, error: agentsError } = await supabaseAdmin
      .from('agents')
      .select('id, name, role, efficiency, evolution_count, last_evolved_at, status');

    if (agentsError) {
      console.error('[EVOLUTION:ANALYZE] Erro ao buscar agents:', agentsError);
      return NextResponse.json(
        { error: 'Erro ao buscar agents', details: agentsError.message },
        { status: 500 }
      );
    }

    console.log(`[EVOLUTION:ANALYZE] ${agents?.length || 0} agents encontrados`);

    // 2. Tentar buscar métricas (pode não existir a tabela)
    let metricsData: any[] = [];
    try {
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

      const { data, error } = await supabaseAdmin
        .from('agent_metrics')
        .select('*')
        .gte('created_at', sevenDaysAgo.toISOString());

      if (!error && data) {
        metricsData = data;
      }
    } catch (e) {
      console.log('[EVOLUTION:ANALYZE] Tabela agent_metrics não existe ou está vazia');
    }

    console.log(`[EVOLUTION:ANALYZE] ${metricsData?.length || 0} registros de métricas encontrados`);

    // 3. Agregar métricas por agent (se existirem)
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
          Math.max(1, existing.total_requests + (metric.requests_processed || 0))
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

      // Identificar issues baseado na efficiency do agent
      const issues: string[] = [];
      let recommendation: 'urgent' | 'recommended' | 'stable' = 'stable';

      const efficiency = agent.efficiency || 85;

      if (efficiency < 50) {
        issues.push(`Eficiência muito baixa: ${efficiency}%`);
        recommendation = 'urgent';
      } else if (efficiency < 75) {
        issues.push(`Eficiência abaixo do ideal: ${efficiency}%`);
        recommendation = 'recommended';
      }

      if (agent.status === 'WARNING' || agent.status === 'ERROR') {
        issues.push(`Status: ${agent.status}`);
        if (recommendation !== 'urgent') recommendation = 'recommended';
      }

      if ((agent.evolution_count || 0) === 0) {
        issues.push('Agent nunca foi evoluído');
        if (recommendation === 'stable') recommendation = 'recommended';
      }

      return {
        agent_id: agent.id,
        agent_name: agent.name,
        agent_role: agent.role || 'general',
        total_requests: metrics.total_requests,
        successful_requests: metrics.successful_requests,
        failed_requests: metrics.failed_requests,
        success_rate: parseFloat(success_rate.toFixed(2)),
        avg_processing_time_ms: metrics.avg_processing_time_ms,
        current_efficiency: efficiency,
        evolution_count: agent.evolution_count || 0,
        last_evolved_at: agent.last_evolved_at,
        recommendation,
        issues,
      };
    });

    // 5. Ordenar por urgência e pior performance
    const sortedPerformances = performances.sort((a, b) => {
      const urgencyWeight = { urgent: 3, recommended: 2, stable: 1 };
      if (urgencyWeight[a.recommendation] !== urgencyWeight[b.recommendation]) {
        return urgencyWeight[b.recommendation] - urgencyWeight[a.recommendation];
      }
      return a.current_efficiency - b.current_efficiency;
    });

    // 6. Pegar os 10 candidatos para evolução
    const candidates = sortedPerformances
      .filter(p => p.recommendation !== 'stable')
      .slice(0, 10);

    console.log('[EVOLUTION:ANALYZE] ═══════════════════════════════════════════');
    console.log(`[EVOLUTION:ANALYZE] ${candidates.length} candidatos para evolução identificados`);
    console.log('[EVOLUTION:ANALYZE] ═══════════════════════════════════════════');

    return NextResponse.json({
      success: true,
      total_agents: performances.length,
      candidates_count: candidates.length,
      candidates,
      all_performances: sortedPerformances.slice(0, 50), // Limitar para performance
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
