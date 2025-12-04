/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - CREATE REQUEST API ROUTE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/requests/create/route.ts
 * 📝 API para criar novas requests de usuários
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { supabaseAdmin } from '@/lib/supabase-admin';

export async function POST(request: NextRequest) {
  try {
    // 1. Validar autenticação do usuário
    const cookieStore = cookies();
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            return cookieStore.get(name)?.value;
          },
          set(name: string, value: string, options: any) {
            cookieStore.set({ name, value, ...options });
          },
          remove(name: string, options: any) {
            cookieStore.set({ name, value: '', ...options });
          },
        },
      }
    );

    const { data: { user }, error: authError } = await supabase.auth.getUser();

    if (authError || !user) {
      console.error('[CREATE-REQUEST] Usuário não autenticado:', authError);
      return NextResponse.json(
        { error: 'Não autenticado' },
        { status: 401 }
      );
    }

    console.log(`[CREATE-REQUEST] Usuário autenticado: ${user.id}`);

    // 2. Validar e extrair dados do body
    const body = await request.json();
    const { title, description, priority, agent_id } = body;

    if (!title || typeof title !== 'string' || title.trim().length === 0) {
      return NextResponse.json(
        { error: 'Título é obrigatório' },
        { status: 400 }
      );
    }

    // Validar priority
    const validPriorities = ['low', 'normal', 'high', 'urgent'];
    const requestPriority = priority && validPriorities.includes(priority) ? priority : 'normal';

    console.log(`[CREATE-REQUEST] Criando request: "${title}" com prioridade ${requestPriority}`);

    // 3. Se agent_id foi fornecido, validar que existe
    if (agent_id) {
      const { data: agent, error: agentError } = await supabaseAdmin
        .from('agents')
        .select('id, name, status')
        .eq('id', agent_id)
        .single();

      if (agentError || !agent) {
        console.error('[CREATE-REQUEST] Agent não encontrado:', agentError);
        return NextResponse.json(
          { error: 'Agent especificado não encontrado' },
          { status: 404 }
        );
      }

      console.log(`[CREATE-REQUEST] Agent selecionado: ${agent.name}`);
    }

    // 4. Criar a request no banco de dados
    const { data: newRequest, error: insertError } = await supabaseAdmin
      .from('requests')
      .insert({
        user_id: user.id,
        title: title.trim(),
        description: description?.trim() || null,
        priority: requestPriority,
        status: 'queued',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .select()
      .single();

    if (insertError || !newRequest) {
      console.error('[CREATE-REQUEST] Erro ao inserir request:', insertError);
      return NextResponse.json(
        { error: 'Erro ao criar request', details: insertError?.message },
        { status: 500 }
      );
    }

    console.log(`[CREATE-REQUEST] ✅ Request criada com sucesso: ${newRequest.id}`);

    // 5. Retornar a request criada
    return NextResponse.json({
      success: true,
      request: newRequest,
      message: 'Request criada com sucesso! Será processada em breve...'
    }, { status: 201 });

  } catch (error: any) {
    console.error('[CREATE-REQUEST] Erro geral:', error);
    return NextResponse.json(
      { error: 'Erro ao criar request', details: error.message },
      { status: 500 }
    );
  }
}

// Endpoint GET para buscar requests do usuário autenticado
export async function GET(request: NextRequest) {
  try {
    // 1. Validar autenticação
    const cookieStore = cookies();
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            return cookieStore.get(name)?.value;
          },
          set(name: string, value: string, options: any) {
            cookieStore.set({ name, value, ...options });
          },
          remove(name: string, options: any) {
            cookieStore.set({ name, value: '', ...options });
          },
        },
      }
    );

    const { data: { user }, error: authError } = await supabase.auth.getUser();

    if (authError || !user) {
      return NextResponse.json(
        { error: 'Não autenticado' },
        { status: 401 }
      );
    }

    // 2. Buscar requests do usuário
    const { data: requests, error: fetchError } = await supabaseAdmin
      .from('requests')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (fetchError) {
      console.error('[CREATE-REQUEST] Erro ao buscar requests:', fetchError);
      return NextResponse.json(
        { error: 'Erro ao buscar requests', details: fetchError.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      requests: requests || [],
      count: requests?.length || 0
    });

  } catch (error: any) {
    console.error('[CREATE-REQUEST] Erro geral:', error);
    return NextResponse.json(
      { error: 'Erro ao buscar requests', details: error.message },
      { status: 500 }
    );
  }
}
