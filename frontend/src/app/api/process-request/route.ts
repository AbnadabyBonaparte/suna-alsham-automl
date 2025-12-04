/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - PROCESS REQUEST API ROUTE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/process-request/route.ts
 * 🎯 Processa requests usando agents e OpenAI API
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseAdmin } from '@/lib/supabase-admin';
import OpenAI from 'openai';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 60;

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    const supabaseAdmin = getSupabaseAdmin();
    const body = await request.json();
    const { request_id } = body;

    if (!request_id) {
      return NextResponse.json(
        { error: 'request_id é obrigatório' },
        { status: 400 }
      );
    }

    console.log(`[PROCESS] Iniciando processamento da request ${request_id}`);

    // 1. Buscar a request no banco
    const { data: requestData, error: requestError } = await supabaseAdmin
      .from('requests')
      .select('*')
      .eq('id', request_id)
      .single();

    if (requestError || !requestData) {
      console.error('[PROCESS] Request não encontrada:', requestError);
      return NextResponse.json(
        { error: 'Request não encontrada' },
        { status: 404 }
      );
    }

    console.log(`[PROCESS] Request encontrada:`, requestData);

    // 2. Selecionar um agent disponível (status='idle')
    const { data: agents, error: agentsError } = await supabaseAdmin
      .from('agents')
      .select('*')
      .eq('status', 'idle')
      .limit(1);

    if (agentsError || !agents || agents.length === 0) {
      console.error('[PROCESS] Nenhum agent disponível:', agentsError);
      return NextResponse.json(
        { error: 'Nenhum agent disponível no momento' },
        { status: 503 }
      );
    }

    const agent = agents[0];
    console.log(`[PROCESS] Agent selecionado: ${agent.name} (${agent.id})`);

    // 3. Atualizar status da request para 'processing'
    await supabaseAdmin
      .from('requests')
      .update({
        status: 'processing',
        updated_at: new Date().toISOString()
      })
      .eq('id', request_id);

    // 4. Atualizar status do agent para 'processing' e current_task
    await supabaseAdmin
      .from('agents')
      .update({
        status: 'processing',
        current_task: requestData.title,
        last_active: new Date().toISOString()
      })
      .eq('id', agent.id);

    console.log(`[PROCESS] Chamando OpenAI API...`);

    // 5. Chamar OpenAI API com o prompt do agent
    try {
      const completion = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [
          {
            role: 'system',
            content: `Você é ${agent.name}, um agent do tipo ${agent.role}. Sua tarefa é processar requests com eficiência e precisão.`
          },
          {
            role: 'user',
            content: `Tarefa: ${requestData.title}\n\nDescrição: ${requestData.description || 'Sem descrição adicional'}\n\nPor favor, processe esta tarefa e forneça uma resposta detalhada.`
          }
        ],
        temperature: 0.7,
        max_tokens: 1000,
      });

      const result = completion.choices[0]?.message?.content || 'Sem resposta';
      console.log(`[PROCESS] OpenAI respondeu com sucesso`);

      // 6. Salvar resultado e atualizar status da request para 'completed'
      await supabaseAdmin
        .from('requests')
        .update({
          status: 'completed',
          updated_at: new Date().toISOString()
        })
        .eq('id', request_id);

      // 7. Atualizar agent para 'idle' e atualizar last_active
      await supabaseAdmin
        .from('agents')
        .update({
          status: 'idle',
          current_task: 'Aguardando próxima tarefa',
          last_active: new Date().toISOString()
        })
        .eq('id', agent.id);

      console.log(`[PROCESS] Request ${request_id} processada com sucesso!`);

      return NextResponse.json({
        success: true,
        request_id,
        agent_id: agent.id,
        agent_name: agent.name,
        result,
        message: 'Request processada com sucesso'
      });

    } catch (openaiError: any) {
      console.error('[PROCESS] Erro ao chamar OpenAI:', openaiError);

      // Reverter status em caso de erro
      await supabaseAdmin
        .from('requests')
        .update({
          status: 'failed',
          updated_at: new Date().toISOString()
        })
        .eq('id', request_id);

      await supabaseAdmin
        .from('agents')
        .update({
          status: 'idle',
          current_task: 'Aguardando próxima tarefa',
          last_active: new Date().toISOString()
        })
        .eq('id', agent.id);

      return NextResponse.json(
        {
          error: 'Erro ao processar com OpenAI',
          details: openaiError.message
        },
        { status: 500 }
      );
    }

  } catch (error: any) {
    console.error('[PROCESS] Erro geral:', error);
    return NextResponse.json(
      {
        error: 'Erro ao processar request',
        details: error.message
      },
      { status: 500 }
    );
  }
}
