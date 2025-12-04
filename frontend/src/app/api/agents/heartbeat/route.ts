/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - AGENTS HEARTBEAT API ROUTE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/agents/heartbeat/route.ts
 * 💓 Atualiza last_active de agents idle para mantê-los "vivos"
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseAdmin } from '@/lib/supabase-admin';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    const supabaseAdmin = getSupabaseAdmin();
    console.log('[HEARTBEAT] Atualizando last_active dos agents...');

    // Atualizar last_active de todos os agents com status 'idle'
    const { data: updatedAgents, error } = await supabaseAdmin
      .from('agents')
      .update({
        last_active: new Date().toISOString()
      })
      .eq('status', 'idle')
      .select();

    if (error) {
      console.error('[HEARTBEAT] Erro ao atualizar agents:', error);
      return NextResponse.json(
        { error: 'Erro ao atualizar heartbeat', details: error.message },
        { status: 500 }
      );
    }

    const count = updatedAgents?.length || 0;
    console.log(`[HEARTBEAT] ${count} agents atualizados com sucesso`);

    return NextResponse.json({
      success: true,
      updated_count: count,
      timestamp: new Date().toISOString(),
      message: `${count} agents atualizados`
    });

  } catch (error: any) {
    console.error('[HEARTBEAT] Erro geral:', error);
    return NextResponse.json(
      { error: 'Erro ao processar heartbeat', details: error.message },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const supabaseAdmin = getSupabaseAdmin();
    console.log('[HEARTBEAT] Consultando status dos agents...');

    // Buscar status geral dos agents
    const { data: agents, error } = await supabaseAdmin
      .from('agents')
      .select('id, name, status, last_active')
      .order('last_active', { ascending: false });

    if (error) {
      console.error('[HEARTBEAT] Erro ao buscar agents:', error);
      return NextResponse.json(
        { error: 'Erro ao buscar status dos agents', details: error.message },
        { status: 500 }
      );
    }

    // Calcular estatísticas
    const stats = {
      total: agents?.length || 0,
      idle: agents?.filter(a => a.status === 'idle').length || 0,
      processing: agents?.filter(a => a.status === 'processing').length || 0,
      active: agents?.filter(a => a.status === 'active').length || 0,
      offline: agents?.filter(a => a.status === 'offline').length || 0,
    };

    console.log('[HEARTBEAT] Status dos agents:', stats);

    return NextResponse.json({
      success: true,
      stats,
      agents: agents || [],
      timestamp: new Date().toISOString()
    });

  } catch (error: any) {
    console.error('[HEARTBEAT] Erro geral:', error);
    return NextResponse.json(
      { error: 'Erro ao consultar status', details: error.message },
      { status: 500 }
    );
  }
}
