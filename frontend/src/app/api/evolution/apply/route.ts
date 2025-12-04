/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - EVOLUTION APPLY API
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/evolution/apply/route.ts
 * ✅ Aplica evoluções aprovadas aos agents
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseAdmin } from '@/lib/supabase-admin';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 60;

interface ApplyRequest {
  proposal_id: string;
  action: 'approve' | 'reject';
}

export async function POST(request: NextRequest) {
  const startTime = Date.now();

  try {
    const supabaseAdmin = getSupabaseAdmin();
    console.log('[EVOLUTION:APPLY] ═══════════════════════════════════════════');
    console.log('[EVOLUTION:APPLY] Processando ação de evolução');

    // 1. Parse request body
    const body: ApplyRequest = await request.json();
    const { proposal_id, action } = body;

    if (!proposal_id || !action) {
      return NextResponse.json(
        { error: 'proposal_id e action são obrigatórios' },
        { status: 400 }
      );
    }

    if (action !== 'approve' && action !== 'reject') {
      return NextResponse.json(
        { error: 'action deve ser "approve" ou "reject"' },
        { status: 400 }
      );
    }

    console.log(`[EVOLUTION:APPLY] Proposal ID: ${proposal_id}, Action: ${action}`);

    // 2. Buscar a proposta
    const { data: proposal, error: proposalError } = await supabaseAdmin
      .from('evolution_proposals')
      .select('*')
      .eq('id', proposal_id)
      .single();

    if (proposalError || !proposal) {
      console.error('[EVOLUTION:APPLY] Proposta não encontrada:', proposalError);
      return NextResponse.json(
        { error: 'Proposta não encontrada', details: proposalError?.message },
        { status: 404 }
      );
    }

    // Validar status da proposta
    if (proposal.status !== 'pending' && proposal.status !== 'approved') {
      return NextResponse.json(
        { error: `Proposta já foi processada (status: ${proposal.status})` },
        { status: 400 }
      );
    }

    console.log(`[EVOLUTION:APPLY] Proposta encontrada para agent: ${proposal.agent_id}`);

    // 3. REJEITAR proposta
    if (action === 'reject') {
      const { error: updateError } = await supabaseAdmin
        .from('evolution_proposals')
        .update({
          status: 'rejected',
          updated_at: new Date().toISOString(),
        })
        .eq('id', proposal_id);

      if (updateError) {
        console.error('[EVOLUTION:APPLY] Erro ao rejeitar proposta:', updateError);
        return NextResponse.json(
          { error: 'Erro ao rejeitar proposta', details: updateError.message },
          { status: 500 }
        );
      }

      console.log('[EVOLUTION:APPLY] ❌ Proposta rejeitada');

      return NextResponse.json({
        success: true,
        action: 'rejected',
        proposal_id,
        message: 'Proposta rejeitada com sucesso',
        timestamp: new Date().toISOString(),
      });
    }

    // 4. APROVAR e APLICAR proposta
    console.log('[EVOLUTION:APPLY] Aplicando evolução ao agent...');

    // Buscar o agent primeiro para obter o evolution_count atual
    const { data: currentAgent, error: fetchAgentError } = await supabaseAdmin
      .from('agents')
      .select('evolution_count')
      .eq('id', proposal.agent_id)
      .single();

    if (fetchAgentError || !currentAgent) {
      console.error('[EVOLUTION:APPLY] Erro ao buscar agent:', fetchAgentError);
      return NextResponse.json(
        { error: 'Erro ao buscar agent', details: fetchAgentError?.message },
        { status: 500 }
      );
    }

    const newEvolutionCount = (currentAgent.evolution_count || 0) + 1;

    // Atualizar o agent com o novo prompt
    const { data: updatedAgent, error: agentError } = await supabaseAdmin
      .from('agents')
      .update({
        system_prompt: proposal.proposed_prompt,
        evolution_count: newEvolutionCount,
        last_evolved_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      })
      .eq('id', proposal.agent_id)
      .select()
      .single();

    if (agentError) {
      console.error('[EVOLUTION:APPLY] Erro ao atualizar agent:', agentError);
      return NextResponse.json(
        { error: 'Erro ao aplicar evolução ao agent', details: agentError.message },
        { status: 500 }
      );
    }

    // Marcar proposta como merged
    const { error: mergeError } = await supabaseAdmin
      .from('evolution_proposals')
      .update({
        status: 'merged',
        updated_at: new Date().toISOString(),
      })
      .eq('id', proposal_id);

    if (mergeError) {
      console.error('[EVOLUTION:APPLY] Erro ao marcar proposta como merged:', mergeError);
      // Não é crítico, continuar...
    }

    // Criar log da evolução
    await supabaseAdmin.from('agent_logs').insert({
      agent_id: proposal.agent_id,
      event_type: 'metric_update',
      message: `Agent evoluído via proposta ${proposal_id}. Evolution count: ${updatedAgent.evolution_count}`,
      metadata: {
        proposal_id,
        evolution_count: updatedAgent.evolution_count,
        previous_prompt_length: proposal.current_prompt?.length || 0,
        new_prompt_length: proposal.proposed_prompt?.length || 0,
        expected_gain: proposal.analysis?.expected_gain || 'unknown',
      },
    });

    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log('[EVOLUTION:APPLY] ═══════════════════════════════════════════');
    console.log(`[EVOLUTION:APPLY] ✅ Evolução aplicada com sucesso em ${duration}s`);
    console.log(`[EVOLUTION:APPLY] Agent: ${proposal.agent_id}, Evolution Count: ${updatedAgent.evolution_count}`);
    console.log('[EVOLUTION:APPLY] ═══════════════════════════════════════════');

    return NextResponse.json({
      success: true,
      action: 'merged',
      proposal_id,
      agent_id: proposal.agent_id,
      evolution_count: updatedAgent.evolution_count,
      last_evolved_at: updatedAgent.last_evolved_at,
      message: 'Evolução aplicada com sucesso! O agent foi atualizado.',
      duration_seconds: parseFloat(duration),
      timestamp: new Date().toISOString(),
    });

  } catch (error: any) {
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    console.error('[EVOLUTION:APPLY] ❌ Erro geral:', error);

    return NextResponse.json(
      {
        error: 'Erro ao processar ação de evolução',
        details: error.message,
        duration_seconds: parseFloat(duration),
      },
      { status: 500 }
    );
  }
}

// Endpoint GET para buscar histórico de evoluções
export async function GET(request: NextRequest) {
  try {
    const supabaseAdmin = getSupabaseAdmin();
    const { searchParams } = new URL(request.url);
    const agent_id = searchParams.get('agent_id');
    const status = searchParams.get('status');

    console.log('[EVOLUTION:APPLY] Buscando histórico de evoluções');

    let query = supabaseAdmin
      .from('evolution_proposals')
      .select(`
        *,
        agents:agent_id (id, name, role)
      `)
      .order('created_at', { ascending: false });

    if (agent_id) {
      query = query.eq('agent_id', agent_id);
    }

    if (status) {
      query = query.eq('status', status);
    }

    const { data: proposals, error } = await query;

    if (error) {
      console.error('[EVOLUTION:APPLY] Erro ao buscar histórico:', error);
      return NextResponse.json(
        { error: 'Erro ao buscar histórico de evoluções', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      count: proposals?.length || 0,
      proposals: proposals || [],
      timestamp: new Date().toISOString(),
    });

  } catch (error: any) {
    console.error('[EVOLUTION:APPLY] Erro ao buscar histórico:', error);
    return NextResponse.json(
      { error: 'Erro ao buscar histórico', details: error.message },
      { status: 500 }
    );
  }
}
