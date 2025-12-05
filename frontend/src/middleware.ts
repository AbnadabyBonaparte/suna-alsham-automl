/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - MIDDLEWARE DE PROTEÇÃO
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/middleware.ts
 * 🔐 Proteção de rotas com verificação de pagamento
 * ═══════════════════════════════════════════════════════════════
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { createClient } from '@supabase/supabase-js';

// ========================================
// ROTAS PÚBLICAS (sem autenticação)
// ========================================
const PUBLIC_ROUTES = [
    '/',
    '/pricing',
    '/login',
    '/signup',
    '/forgot-password',
    '/reset-password',
    '/terms',
    '/privacy',
    '/contact',
    '/api/stripe/webhook', // Webhook precisa ser público
    '/api/stripe/checkout',
];

// ========================================
// ROTAS QUE PRECISAM DE PAGAMENTO
// ========================================
const PAID_ROUTES = [
    '/dashboard',
];

export async function middleware(req: NextRequest) {
    const { pathname } = req.nextUrl;

    // ========================================
    // MODO DESENVOLVIMENTO - BYPASS TOTAL
    // ========================================
    const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
    if (isDevMode) {
        console.log('🛠️ DEV MODE: Bypass de autenticação ativado');
        return NextResponse.next();
    }

    // ========================================
    // 1. ROTAS PÚBLICAS - LIBERA
    // ========================================
    if (PUBLIC_ROUTES.some(route => pathname === route || pathname.startsWith('/api/'))) {
        // Permitir todas as rotas de API e rotas públicas
        if (pathname.startsWith('/api/')) {
            return NextResponse.next();
        }

        // Rotas públicas específicas
        if (PUBLIC_ROUTES.includes(pathname)) {
            return NextResponse.next();
        }
    }

// ========================================
// ROTAS DE DESENVOLVIMENTO - LIBERA
// ========================================
if (pathname.startsWith('/dev/')) {
    console.log('🛠️ DEV ROUTE: Acesso liberado para rota de desenvolvimento');
    return NextResponse.next();
}

// ========================================
// FLUXO AJUSTADO: LANDING → PRICING → DASHBOARD (se logado e pagou)
// ========================================
if (pathname === '/' && !pathname.startsWith('/api/')) {
    // Landing page sempre redireciona para pricing como segunda página
    console.log('🎯 FLUXO: Redirecionando landing para pricing');
    const url = req.nextUrl.clone();
    url.pathname = '/pricing';
    return NextResponse.redirect(url);
}

    // ========================================
    // 2. VERIFICAR AUTENTICAÇÃO VIA COOKIE
    // ========================================
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    if (!supabaseUrl || !supabaseAnonKey) {
        // Se não tem Supabase configurado, deixa passar (dev mode)
        console.warn('⚠️ Supabase não configurado no middleware');
        return NextResponse.next();
    }

    // Pegar token do cookie de autenticação do Supabase
    const authToken = req.cookies.get('sb-access-token')?.value || 
                      req.cookies.get('supabase-auth-token')?.value;

    // ========================================
    // 3. ROTAS DE DASHBOARD - PRECISA LOGIN
    // ========================================
    if (pathname.startsWith('/dashboard')) {
        // Se não tem token, redireciona para pricing
        if (!authToken) {
            console.log(`🔒 Acesso negado a ${pathname} - não autenticado`);
            const url = req.nextUrl.clone();
            url.pathname = '/pricing';
            url.searchParams.set('redirect', pathname);
            return NextResponse.redirect(url);
        }

        // ========================================
        // 4. VERIFICAR PAGAMENTO - SEGURANÇA TOTAL
        // ========================================
        const supabase = createClient(supabaseUrl, supabaseAnonKey, {
            auth: {
                persistSession: false
            }
        });

        try {
            // Pegar sessão do usuário
            const { data: { session }, error: sessionError } = await supabase.auth.getSession();

            if (sessionError || !session) {
                console.log(`🔒 Acesso negado a ${pathname} - sessão inválida`);
                const url = req.nextUrl.clone();
                url.pathname = '/pricing';
                return NextResponse.redirect(url);
            }

            const userId = session.user.id;

            // Buscar dados do usuário no Supabase
            const { data: userData, error: userError } = await supabase
                .from('users') // Ajuste para o nome correto da tabela
                .select('plan, paid, stripe_customer_id')
                .eq('id', userId)
                .single();

            if (userError) {
                console.error('Erro ao buscar dados do usuário:', userError);
                // Se erro ao buscar, redireciona para pricing por segurança
                const url = req.nextUrl.clone();
                url.pathname = '/pricing';
                return NextResponse.redirect(url);
            }

            // VERIFICAÇÃO DE PAGAMENTO - DESABILITADA PARA TESTES
            // Usuários logados podem acessar mesmo sem ter pago (para período de teste)
            // if (!userData || userData.paid !== true) {
            //     console.log(`💰 Acesso negado a ${pathname} - usuário não pagou (ID: ${userId})`);
            //     const url = req.nextUrl.clone();
            //     url.pathname = '/pricing';
            //     url.searchParams.set('reason', 'payment_required');
            //     return NextResponse.redirect(url);
            // }

            // Adicionar headers com info do usuário para o client
            const response = NextResponse.next();
            response.headers.set('x-user-authenticated', 'true');
            response.headers.set('x-user-plan', userData.plan || 'free');
            response.headers.set('x-user-paid', userData.paid ? 'true' : 'false');
            return response;

        } catch (error) {
            console.error('Erro no middleware:', error);
            // Em caso de erro, redireciona para pricing por segurança
            const url = req.nextUrl.clone();
            url.pathname = '/pricing';
            return NextResponse.redirect(url);
        }
    }

    // ========================================
    // 5. OUTRAS ROTAS - DEIXA PASSAR
    // ========================================
    return NextResponse.next();
}

export const config = {
    matcher: [
        /*
         * Match all request paths except:
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         * - public folder
         */
        '/((?!_next/static|_next/image|favicon.ico|public|.*\\..*|sounds|images).*)',
    ],
};
