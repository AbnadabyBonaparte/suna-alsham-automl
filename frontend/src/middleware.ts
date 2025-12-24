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
import { createServerClient } from '@supabase/ssr';

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
    // 2. VERIFICAR AUTENTICAÇÃO VIA COOKIE
    // ========================================
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    if (!supabaseUrl || !supabaseAnonKey) {
        // Se não tem Supabase configurado, deixa passar (dev mode)
        console.warn('⚠️ Supabase não configurado no middleware');
        return NextResponse.next();
    }

    // ========================================
    // 3. ROTAS DE DASHBOARD - VERIFICAÇÃO COMPLETA
    // ========================================
    if (pathname.startsWith('/dashboard')) {
        // ========================================
        // 4. CRIAR CLIENTE SUPABASE SSR COM COOKIES
        // ========================================
        let response = NextResponse.next({
            request: {
                headers: req.headers,
            },
        });

        const supabase = createServerClient(supabaseUrl, supabaseAnonKey, {
            cookies: {
                getAll() {
                    return req.cookies.getAll();
                },
                setAll(cookiesToSet) {
                    cookiesToSet.forEach(({ name, value, options }) => {
                        response.cookies.set(name, value, options);
                    });
                },
            },
        });

        try {
            // Pegar sessão do usuário usando cookies
            const { data: { session }, error: sessionError } = await supabase.auth.getSession();

            if (sessionError || !session) {
                console.log(`🔒 Acesso negado a ${pathname} - sessão inválida`, sessionError);
                const url = req.nextUrl.clone();
                url.pathname = '/login';
                url.searchParams.set('redirect', pathname);
                return NextResponse.redirect(url);
            }

            const userId = session.user.id;
            const userEmail = session.user.email;

            // ========================================
            // 5. VERIFICAÇÃO ESPECIAL - DONO SEMPRE TEM ACESSO
            // ========================================
            if (userEmail === 'casamondestore@gmail.com') {
                console.log('👑 DONO DETECTADO - ACESSO TOTAL LIBERADO');
                response.headers.set('x-user-authenticated', 'true');
                response.headers.set('x-user-founder', 'true');
                response.headers.set('x-user-email', userEmail);
                return response;
            }

            // Buscar dados do usuário no Supabase (profiles table)
            const { data: userData, error: userError } = await supabase
                .from('profiles')
                .select('subscription_plan, subscription_status, founder_access')
                .eq('id', userId)
                .single();

            if (userError) {
                console.error('Erro ao buscar dados do usuário:', userError);
                // Se erro ao buscar, redireciona para pricing por segurança
                const url = req.nextUrl.clone();
                url.pathname = '/pricing';
                return NextResponse.redirect(url);
            }

            // ========================================
            // 6. VERIFICAÇÃO DE PERMISSÕES
            // ========================================
            const hasFounderAccess = userData?.founder_access === true;
            const hasEnterprisePlan = userData?.subscription_plan === 'enterprise';
            const isSubscriptionActive = userData?.subscription_status === 'active';

            if (hasFounderAccess) {
                console.log('🏆 FOUNDER ACCESS - ACESSO TOTAL LIBERADO');
                response.headers.set('x-user-authenticated', 'true');
                response.headers.set('x-user-founder', 'true');
                response.headers.set('x-user-plan', userData?.subscription_plan || 'free');
                return response;
            }

            if (hasEnterprisePlan && isSubscriptionActive) {
                console.log('💎 ENTERPRISE PLAN ATIVO - ACESSO LIBERADO');
                response.headers.set('x-user-authenticated', 'true');
                response.headers.set('x-user-plan', 'enterprise');
                response.headers.set('x-user-paid', 'true');
                return response;
            }

            if (isSubscriptionActive) {
                console.log('✅ SUBSCRIPTION ATIVA - ACESSO LIBERADO');
                response.headers.set('x-user-authenticated', 'true');
                response.headers.set('x-user-plan', userData?.subscription_plan || 'free');
                response.headers.set('x-user-paid', 'true');
                return response;
            }

            // Usuário logado mas sem permissões - redireciona para pricing
            console.log(`💰 Acesso negado a ${pathname} - usuário não pagou (ID: ${userId})`);
            const url = req.nextUrl.clone();
            url.pathname = '/pricing';
            url.searchParams.set('reason', 'payment_required');
            return NextResponse.redirect(url);

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
