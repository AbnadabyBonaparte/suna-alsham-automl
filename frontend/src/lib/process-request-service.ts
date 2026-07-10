/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - REQUEST PROCESSING SERVICE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/lib/process-request-service.ts
 * 🎯 Lógica reutilizável para processar requests com agents
 * ═══════════════════════════════════════════════════════════════
 */

import { getSupabaseAdmin } from '@/lib/supabase-admin';
import OpenAI from 'openai';

// Lazy initialization do cliente OpenAI
let _openai: OpenAI | null = null;
function getOpenAI(): OpenAI {
  if (!_openai) {
    _openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }
  return _openai;
}

export interface ProcessRequestResult {
  success: boolean;
  request_id: string;
  agent_id?: string;
  agent_name?: string;
  result?: string;
  error?: string;
  details?: string;
}

/**
 * Processa uma única request usando um agent disponível
 * @param request_id - ID da request a ser processada
 * @param agent_id - ID do agent específico (opcional)
 * @param timeout - Timeout em segundos (default: 60)
 * @returns Resultado do processamento
 */
export async function processRequest(
  request_id: string,
  agent_id?: string,
  timeout: number = 60
): Promise<ProcessRequestResult> {
  try {
    console.log(`[PROCESS-SERVICE] Iniciando processamento da request ${request_id}`);
    
    const supabaseAdmin = getSupabaseAdmin();
    const openai = getOpenAI();

    // 1. Buscar a request no banco
    const { data: requestData, error: requestError } = await supabaseAdmin
      .from('requests')
      .select('*')
      .eq('id', request_id)
      .single();

    if (requestError || !requestData) {
      console.error('[PROCESS-SERVICE] Request não encontrada:', requestError);
      return {
        success: false,
        request_id,
        error: 'Request não encontrada',
        details: requestError?.message
      };
    }

    console.log(`[PROCESS-SERVICE] Request encontrada:`, requestData);

    // 2. Selecionar agent (específico ou disponível)
    let agent;
    if (agent_id) {
      // Usar agent específico
      const { data: agentData, error: agentError } = await supabaseAdmin
        .from('agents')
        .select('*')
        .eq('id', agent_id)
        .eq('status', 'idle')
        .single();

      if (agentError || !agentData) {
        console.error('[PROCESS-SERVICE] Agent específico não disponível:', agentError);
        return {
          success: false,
          request_id,
          error: 'Agent específico não disponível',
          details: agentError?.message
        };
      }
      agent = agentData;
    } else {
      // Selecionar agent disponível automaticamente
      const { data: agents, error: agentsError } = await supabaseAdmin
        .from('agents')
        .select('*')
        .eq('status', 'idle')
        .limit(1);

      if (agentsError || !agents || agents.length === 0) {
        console.error('[PROCESS-SERVICE] Nenhum agent disponível:', agentsError);
        return {
          success: false,
          request_id,
          error: 'Nenhum agent disponível',
          details: agentsError?.message
        };
      }
      agent = agents[0];
    }

    console.log(`[PROCESS-SERVICE] Agent selecionado: ${agent.name} (${agent.id})`);

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

    console.log(`[PROCESS-SERVICE] Chamando OpenAI API...`);

    // 5. Chamar OpenAI API com o prompt do agent (com timeout)
    try {
      const completionPromise = openai.chat.completions.create({
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

      // Aplicar timeout
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Timeout ao processar request')), timeout * 1000)
      );

      const completion = (await Promise.race([completionPromise, timeoutPromise])) as {
        choices?: Array<{ message?: { content?: string | null } }>;
      };
      const result = completion.choices?.[0]?.message?.content || 'Sem resposta';
      console.log(`[PROCESS-SERVICE] OpenAI respondeu com sucesso`);

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

      console.log(`[PROCESS-SERVICE] Request ${request_id} processada com sucesso!`);

      return {
        success: true,
        request_id,
        agent_id: agent.id,
        agent_name: agent.name,
        result
      };

    } catch (openaiError: unknown) {
      console.error('[PROCESS-SERVICE] Erro ao chamar OpenAI:', openaiError);

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

      return {
        success: false,
        request_id,
        error: 'Erro ao processar com OpenAI',
        details: openaiError instanceof Error ? openaiError.message : String(openaiError)
      };
    }

  } catch (error: unknown) {
    console.error('[PROCESS-SERVICE] Erro geral:', error);
    return {
      success: false,
      request_id,
      error: 'Erro ao processar request',
      details: error instanceof Error ? error.message : String(error)
    };
  }
}
