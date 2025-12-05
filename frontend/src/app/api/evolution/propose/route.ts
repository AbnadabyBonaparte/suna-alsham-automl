/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - EVOLUTION PROPOSAL API (with Claude)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/evolution/propose/route.ts
 * 🧠 Usa Claude API para analisar agents e propor melhorias
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseAdmin } from '@/lib/supabase-admin';
import { getAnthropic } from '@/lib/lazy-clients';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 60;

interface ProposalRequest {
  agent_id: string;
}

export async function POST(request: NextRequest) {
  const startTime = Date.now();

  try {
    const supabaseAdmin = getSupabaseAdmin();
    console.log('[EVOLUTION:PROPOSE] ═══════════════════════════════════════════');
    console.log('[EVOLUTION:PROPOSE] Iniciando proposta de evolução com Claude');

    // Validar ANTHROPIC_API_KEY
    if (!process.env.ANTHROPIC_API_KEY) {
      return NextResponse.json(
        { error: 'ANTHROPIC_API_KEY não configurada' },
        { status: 500 }
      );
    }

    // 1. Parse request body
    const body: ProposalRequest = await request.json();
    const { agent_id } = body;

    if (!agent_id) {
      return NextResponse.json(
        { error: 'agent_id é obrigatório' },
        { status: 400 }
      );
    }

    console.log(`[EVOLUTION:PROPOSE] Agent ID: ${agent_id}`);

    // 2. Buscar o agent
    const { data: agent, error: agentError } = await supabaseAdmin
      .from('agents')
      .select('*')
      .eq('id', agent_id)
      .single();

    if (agentError || !agent) {
      console.error('[EVOLUTION:PROPOSE] Agent não encontrado:', agentError);
      return NextResponse.json(
        { error: 'Agent não encontrado', details: agentError?.message },
        { status: 404 }
      );
    }

    console.log(`[EVOLUTION:PROPOSE] Agent encontrado: ${agent.name} (${agent.role})`);

    // 3. Buscar métricas dos últimos 7 dias
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    const { data: metrics } = await supabaseAdmin
      .from('agent_metrics')
      .select('*')
      .eq('agent_id', agent_id)
      .gte('metric_date', sevenDaysAgo.toISOString().split('T')[0]);

    // 4. Buscar requests com falhas recentes
    const { data: failedRequests } = await supabaseAdmin
      .from('requests')
      .select('title, description, error_message, created_at')
      .eq('agent_id', agent_id)
      .eq('status', 'failed')
      .order('created_at', { ascending: false })
      .limit(10);

    // 5. Agregar métricas
    const totalRequests = metrics?.reduce((sum, m) => sum + (m.requests_processed || 0), 0) || 0;
    const totalSuccess = metrics?.reduce((sum, m) => sum + (m.requests_successful || 0), 0) || 0;
    const totalFailed = metrics?.reduce((sum, m) => sum + (m.requests_failed || 0), 0) || 0;
    const successRate = totalRequests > 0 ? (totalSuccess / totalRequests) * 100 : 0;
    const avgProcessingTime = metrics?.length
      ? metrics.reduce((sum, m) => sum + (m.avg_processing_time_ms || 0), 0) / metrics.length
      : 0;

    console.log(`[EVOLUTION:PROPOSE] Métricas - Total: ${totalRequests}, Sucesso: ${totalSuccess}, Falha: ${totalFailed}, Taxa: ${successRate.toFixed(1)}%`);

    // 6. Montar contexto para o Claude
    const currentPrompt = agent.system_prompt || 'You are an AI agent assistant designed to help with CRM tasks.';

    const failedRequestsSummary = (failedRequests || [])
      .map(r => `- "${r.title}": ${r.error_message || 'Sem detalhes do erro'}`)
      .join('\n') || 'Nenhuma falha recente';

    const claudePrompt = `You are an AI expert specializing in optimizing AI agent system prompts for CRM systems.

**AGENT INFORMATION:**
- Name: ${agent.name}
- Role: ${agent.role}
- Current Efficiency: ${agent.efficiency}%
- Evolution Count: ${agent.evolution_count || 0}

**PERFORMANCE METRICS (Last 7 days):**
- Total Requests Processed: ${totalRequests}
- Successful: ${totalSuccess} (${successRate.toFixed(1)}%)
- Failed: ${totalFailed}
- Average Processing Time: ${(avgProcessingTime / 1000).toFixed(2)}s

**CURRENT SYSTEM PROMPT:**
\`\`\`
${currentPrompt}
\`\`\`

**RECENT FAILURES:**
${failedRequestsSummary}

**YOUR TASK:**
Analyze the current system prompt and propose an improved version.

**RESPONSE FORMAT (JSON):**
{
  "weaknesses": ["list of 2-4 specific weaknesses"],
  "improvements": ["list of 2-4 specific improvements"],
  "proposed_prompt": "the complete new system prompt",
  "expected_gain": "estimated improvement percentage (e.g., '10-15%')",
  "confidence": "high|medium|low",
  "reasoning": "brief explanation of the main changes"
}`;

    console.log('[EVOLUTION:PROPOSE] Chamando Claude API...');

    // 7. Chamar Claude API (lazy initialization)
    const anthropic = await getAnthropic();
    
    if (!anthropic) {
      return NextResponse.json(
        { error: 'Claude API não configurada' },
        { status: 500 }
      );
    }

    const message = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 2048,
      temperature: 0.7,
      messages: [
        {
          role: 'user',
          content: claudePrompt,
        },
      ],
    });

    const responseText = message.content[0].type === 'text' ? message.content[0].text : '';
    console.log('[EVOLUTION:PROPOSE] Resposta do Claude recebida');

    // 8. Parse resposta do Claude
    let analysis;
    try {
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        analysis = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('JSON não encontrado na resposta');
      }
    } catch (parseError) {
      console.error('[EVOLUTION:PROPOSE] Erro ao parsear resposta do Claude:', parseError);
      return NextResponse.json(
        { error: 'Erro ao processar resposta do Claude', details: responseText },
        { status: 500 }
      );
    }

    // Validar campos obrigatórios
    if (!analysis.proposed_prompt || !analysis.weaknesses || !analysis.improvements) {
      return NextResponse.json(
        { error: 'Resposta do Claude incompleta', details: analysis },
        { status: 500 }
      );
    }

    console.log('[EVOLUTION:PROPOSE] Análise concluída:', {
      weaknesses: analysis.weaknesses.length,
      improvements: analysis.improvements.length,
      confidence: analysis.confidence,
    });

    // 9. Salvar proposta no banco
    const { data: proposal, error: proposalError } = await supabaseAdmin
      .from('evolution_proposals')
      .insert({
        agent_id,
        current_prompt: currentPrompt,
        proposed_prompt: analysis.proposed_prompt,
        analysis: {
          weaknesses: analysis.weaknesses,
          improvements: analysis.improvements,
          expected_gain: analysis.expected_gain,
          confidence: analysis.confidence,
          reasoning: analysis.reasoning || '',
          metrics: {
            total_requests: totalRequests,
            success_rate: parseFloat(successRate.toFixed(2)),
            avg_processing_time_ms: Math.round(avgProcessingTime),
          },
        },
        status: 'pending',
      })
      .select()
      .single();

    if (proposalError) {
      console.error('[EVOLUTION:PROPOSE] Erro ao salvar proposta:', proposalError);
      return NextResponse.json(
        { error: 'Erro ao salvar proposta', details: proposalError.message },
        { status: 500 }
      );
    }

    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log('[EVOLUTION:PROPOSE] ═══════════════════════════════════════════');
    console.log(`[EVOLUTION:PROPOSE] ✅ Proposta criada com sucesso em ${duration}s`);
    console.log(`[EVOLUTION:PROPOSE] Proposal ID: ${proposal.id}`);
    console.log('[EVOLUTION:PROPOSE] ═══════════════════════════════════════════');

    return NextResponse.json({
      success: true,
      proposal_id: proposal.id,
      agent_id,
      agent_name: agent.name,
      analysis: {
        weaknesses: analysis.weaknesses,
        improvements: analysis.improvements,
        expected_gain: analysis.expected_gain,
        confidence: analysis.confidence,
        reasoning: analysis.reasoning,
      },
      current_prompt: currentPrompt,
      proposed_prompt: analysis.proposed_prompt,
      duration_seconds: parseFloat(duration),
      timestamp: new Date().toISOString(),
    });

  } catch (error: any) {
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    console.error('[EVOLUTION:PROPOSE] ❌ Erro geral:', error);

    return NextResponse.json(
      {
        error: 'Erro ao gerar proposta de evolução',
        details: error.message,
        duration_seconds: parseFloat(duration),
      },
      { status: 500 }
    );
  }
}
