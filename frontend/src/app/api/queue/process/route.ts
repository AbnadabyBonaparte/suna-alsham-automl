/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - QUEUE PROCESSING API ROUTE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/queue/process/route.ts
 * 🔄 Processa automaticamente a fila de requests pendentes
 * 💫 Chamado por CRON do Vercel a cada 2 minutos
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { processRequest } from '@/lib/process-request-service';
import { getSystemJobClient } from '@/lib/supabase/system-client';
import { z } from 'zod';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA (OBRIGATÓRIO!)
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 300; // 5 minutos para processar múltiplas requests

const CronHeaderSchema = z.object({
  authorization: z.string().regex(/^Bearer .+$/),
});

function assertCronAuthorization(request: NextRequest) {
  const headers = CronHeaderSchema.safeParse({
    authorization: request.headers.get('authorization') || '',
  });

  const expectedSecret = process.env.INTERNAL_CRON_SECRET;

  if (!expectedSecret) {
    throw new Error('INTERNAL_CRON_SECRET não configurado');
  }

  if (!headers.success || headers.data.authorization !== `Bearer ${expectedSecret}`) {
    return false;
  }

  return true;
}

export async function POST(request: NextRequest) {
  const startTime = Date.now();

  try {
    if (!assertCronAuthorization(request)) {
      return NextResponse.json({ error: 'Acesso não autorizado' }, { status: 401 });
    }

    const supabaseAdmin = getSystemJobClient();
    
    console.log('[QUEUE] ═══════════════════════════════════════════');
    console.log('[QUEUE] Iniciando processamento automático da fila');
    console.log('[QUEUE] ═══════════════════════════════════════════');

    // 1. Buscar requests pendentes (status='queued'), até 5 por vez
    const { data: pendingRequests, error: fetchError } = await supabaseAdmin
      .from('requests')
      .select('*')
      .eq('status', 'queued')
      .order('created_at', { ascending: true }) // FIFO - primeiro a entrar, primeiro a sair
      .limit(5);

    if (fetchError) {
      console.error('[QUEUE] Erro ao buscar requests:', fetchError);
      return NextResponse.json(
        { error: 'Erro ao buscar requests da fila', details: fetchError.message },
        { status: 500 }
      );
    }

    if (!pendingRequests || pendingRequests.length === 0) {
      console.log('[QUEUE] Nenhuma request pendente na fila');
      return NextResponse.json({
        success: true,
        processed: 0,
        message: 'Nenhuma request pendente',
        timestamp: new Date().toISOString()
      });
    }

    console.log(`[QUEUE] ${pendingRequests.length} requests encontradas na fila`);
    console.log('[QUEUE] IDs:', pendingRequests.map(r => r.id).join(', '));

    // 2. Processar todas as requests em paralelo (Promise.all)
    console.log('[QUEUE] Iniciando processamento em paralelo...');

    const processingPromises = pendingRequests.map(async (req) => {
      try {
        console.log(`[QUEUE] Processando request ${req.id}: "${req.title}"`);
        const result = await processRequest(req.id, undefined, 60);

        if (result.success) {
          console.log(`[QUEUE] ✅ Request ${req.id} processada com sucesso`);
        } else {
          console.error(`[QUEUE] ❌ Falha ao processar request ${req.id}:`, result.error);
        }

        return result;
      } catch (error: any) {
        console.error(`[QUEUE] ❌ Exceção ao processar request ${req.id}:`, error);
        return {
          success: false,
          request_id: req.id,
          error: 'Exceção durante processamento',
          details: error.message
        };
      }
    });

    // Aguardar todas as requests processarem
    const results = await Promise.all(processingPromises);

    // 3. Calcular estatísticas
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);

    console.log('[QUEUE] ═══════════════════════════════════════════');
    console.log(`[QUEUE] ✅ Processadas com sucesso: ${successful}`);
    console.log(`[QUEUE] ❌ Falharam: ${failed}`);
    console.log(`[QUEUE] ⏱️  Tempo total: ${duration}s`);
    console.log('[QUEUE] ═══════════════════════════════════════════');

    // 4. Retornar resultado
    return NextResponse.json({
      success: true,
      processed: results.length,
      successful,
      failed,
      duration_seconds: parseFloat(duration),
      results: results.map(r => ({
        request_id: r.request_id,
        success: r.success,
        agent_name: r.agent_name,
        error: r.error
      })),
      timestamp: new Date().toISOString()
    });

  } catch (error: any) {
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    console.error('[QUEUE] ❌ Erro geral no processamento da fila:', error);

    return NextResponse.json(
      {
        error: 'Erro ao processar fila',
        details: error.message,
        duration_seconds: parseFloat(duration),
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

// Endpoint GET para verificar status da fila
export async function GET(request: NextRequest) {
  try {
    const supabaseAdmin = getSupabaseAdmin();
    
    // Buscar estatísticas da fila
    const { data: queuedRequests, error: queuedError } = await supabaseAdmin
      .from('requests')
      .select('id, title, priority, created_at')
      .eq('status', 'queued')
      .order('created_at', { ascending: true });

    const { data: processingRequests, error: processingError } = await supabaseAdmin
      .from('requests')
      .select('id, title, priority, created_at')
      .eq('status', 'processing')
      .order('created_at', { ascending: true });

    if (queuedError || processingError) {
      return NextResponse.json(
        { error: 'Erro ao buscar status da fila' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      queue_size: queuedRequests?.length || 0,
      processing_count: processingRequests?.length || 0,
      queued_requests: queuedRequests || [],
      processing_requests: processingRequests || [],
      timestamp: new Date().toISOString()
    });

  } catch (error: any) {
    console.error('[QUEUE] Erro ao consultar status:', error);
    return NextResponse.json(
      { error: 'Erro ao consultar status da fila', details: error.message },
      { status: 500 }
    );
  }
}
