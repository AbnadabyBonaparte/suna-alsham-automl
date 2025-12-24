/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - MIDDLEWARE CONSOLIDADO
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/middleware.ts
 * 🔐 Middleware unificado: Autenticação + Onboarding + Pagamento
 * ═══════════════════════════════════════════════════════════════
 * 
 * CONSOLIDAÇÃO: Este middleware unifica a lógica de:
 * - middleware.ts (legacy) - Verificação de pagamento
 * - proxy.ts (novo) - Verificação de onboarding
 * 
 * ORDEM DETERMINÍSTICA:
 * 1. Rotas Públicas → Libera
 * 2. Autenticação → Verifica login
 * 3. RSC Check → Ignora requisições RSC
 * 4. Onboarding → Verifica onboarding_completed
 * 5. Pagamento → Verifica subscription
 * 6. Acesso → Permite acesso
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
// ROTAS PROTEGIDAS (precisam de autenticação)
// ========================================
const PROTECTED_PATHS = [
    '/dashboard',
    '/settings',
    '/admin',
    '/api/quantum',
    '/api/evolution',
];

export async function middleware(req: NextRequest) {
    const { pathname } = req.nextUrl;

    // ========================================
    // 1. MODO DESENVOLVIMENTO - BYPASS TOTAL
    // ========================================
    const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
    if (isDevMode) {
        console.log('🛠️ DEV MODE: Bypass de autenticação ativado');
        return NextResponse.next();
    }

    // ========================================
    // 2. ROTAS PÚBLICAS - LIBERA IMEDIATAMENTE
    // ========================================
    // IMPORTANTE: /onboarding é tratada depois, precisa de verificação de auth
    if (PUBLIC_ROUTES.some(route => pathname === route || pathname.startsWith('/api/'))) {
        // Permitir todas as rotas de API e rotas públicas
        if (pathname.startsWith('/api/')) {
            console.log(`[MIDDLEWARE] Rota de API liberada: ${pathname}`);
            return NextResponse.next();
        }

        // Rotas públicas específicas
        if (PUBLIC_ROUTES.includes(pathname)) {
            console.log(`[MIDDLEWARE] Rota pública liberada: ${pathname}`);
            return NextResponse.next();
        }
    }

    // ========================================
    // 3. ROTAS DE DESENVOLVIMENTO - LIBERA
    // ========================================
    if (pathname.startsWith('/dev/')) {
        console.log('🛠️ DEV ROUTE: Acesso liberado para rota de desenvolvimento');
        return NextResponse.next();
    }

    // ========================================
    // 4. VERIFICAR AUTENTICAÇÃO VIA COOKIE
    // ========================================
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    console.log('[MIDDLEWARE] Verificando variáveis de ambiente:', {
        pathname,
        hasSupabaseUrl: !!supabaseUrl,
        hasSupabaseAnonKey: !!supabaseAnonKey,
        supabaseUrlLength: supabaseUrl?.length || 0,
        supabaseAnonKeyLength: supabaseAnonKey?.length || 0,
    });

    if (!supabaseUrl || !supabaseAnonKey) {
        console.error('⚠️ CRÍTICO: Supabase não configurado no middleware!', {
            supabaseUrl: supabaseUrl || 'UNDEFINED',
            supabaseAnonKey: supabaseAnonKey ? 'DEFINED' : 'UNDEFINED',
        });
        // Se não tem Supabase configurado, deixa passar mas loga erro
        return NextResponse.next();
    }

    // Criar resposta base
    let response = NextResponse.next({
        request: {
            headers: req.headers,
        },
    });

    // Criar cliente Supabase SSR com cookies
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

    // Obter usuário autenticado
    const { data: { user }, error: userError } = await supabase.auth.getUser();

    // Verificar se é rota protegida
    const isProtectedPath = PROTECTED_PATHS.some((path) =>
        pathname.startsWith(path)
    );

    // ========================================
    // 5. SE NÃO AUTENTICADO E ROTA PROTEGIDA → LOGIN
    // ========================================
    if (!user && isProtectedPath) {
        console.log(`🔒 Acesso negado a ${pathname} - usuário não autenticado`);
        const url = req.nextUrl.clone();
        url.pathname = '/login';
        url.searchParams.set('redirect', pathname);
        return NextResponse.redirect(url);
    }

    // Se não autenticado e não é rota protegida, deixa passar
    if (!user) {
        return response;
    }

    // ========================================
    // 6. CRÍTICO: VERIFICAR RSC ANTES DE QUALQUER OUTRA VERIFICAÇÃO
    // ========================================
    const isRSCRequest = req.nextUrl.searchParams.has('_rsc');
    if (isRSCRequest) {
        console.log('[MIDDLEWARE] Requisição RSC detectada, ignorando verificações para evitar loop');
        return response;
    }

    // ========================================
    // 7. BUSCAR PROFILE DO USUÁRIO
    // ========================================
    const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .select('onboarding_completed, subscription_plan, subscription_status, founder_access, role')
        .eq('id', user.id)
        .single();

    // Debug logs
    console.log('[MIDDLEWARE] Verificando acesso:', {
        path: pathname,
        userId: user.id,
        userEmail: user.email,
        profileExists: !!profile,
        profileError: profileError?.message,
        onboarding_completed: profile?.onboarding_completed,
        subscription_status: profile?.subscription_status,
        subscription_plan: profile?.subscription_plan,
        founder_access: profile?.founder_access,
    });

    // ========================================
    // 8. VERIFICAÇÃO ESPECIAL - DONO SEMPRE TEM ACESSO
    // ========================================
    if (user.email === 'casamondestore@gmail.com') {
        console.log('👑 DONO DETECTADO - ACESSO TOTAL LIBERADO');
        response.headers.set('x-user-authenticated', 'true');
        response.headers.set('x-user-founder', 'true');
        response.headers.set('x-user-email', user.email);
        return response;
    }

    // ========================================
    // 9. CRIAR PERFIL SE NÃO EXISTIR
    // ========================================
    if (profileError && profileError.code === 'PGRST116') {
        console.log('[MIDDLEWARE] Perfil não existe, criando automaticamente...');
        const { error: insertError } = await supabase
            .from('profiles')
            .insert({
                id: user.id,
                username: user.email?.split('@')[0] || 'user',
                onboarding_completed: false,
            });

        if (!insertError) {
            console.log('[MIDDLEWARE] Perfil criado, redirecionando para onboarding');
            const url = req.nextUrl.clone();
            url.pathname = '/onboarding';
            return NextResponse.redirect(url);
        } else {
            console.error('[MIDDLEWARE] Erro ao criar perfil:', insertError);
            // Se não conseguir criar, permite acesso (evita bloquear usuário)
        }
    }

    // ========================================
    // 10. VERIFICAÇÃO DE ONBOARDING
    // ========================================
    
    // Se está em /onboarding e já completou → redirecionar para dashboard
    if (pathname === '/onboarding') {
        console.log('[MIDDLEWARE] Processando rota /onboarding:', {
            userId: user?.id,
            userEmail: user?.email,
            profileExists: !!profile,
            profileError: profileError?.message,
            onboarding_completed: profile?.onboarding_completed,
        });

        // Verificar se há um header indicando que está salvando (evita race condition)
        const isSaving = req.headers.get('x-onboarding-saving') === 'true';
        if (isSaving) {
            console.log('[MIDDLEWARE] Salvamento de onboarding em progresso, ignorando redirect');
            return response;
        }

        if (!profileError && profile && profile.onboarding_completed === true) {
            console.log('[MIDDLEWARE] ✅ Onboarding completo detectado! Redirecionando de /onboarding para /dashboard');
            const url = req.nextUrl.clone();
            url.pathname = '/dashboard';
            return NextResponse.redirect(url);
        }
        
        // Se onboarding não completo, permite ficar em /onboarding
        console.log('[MIDDLEWARE] Onboarding não completo ou perfil não encontrado, permitindo acesso a /onboarding');
        return response;
    }

    // Se está em /login e já completou onboarding → redirecionar baseado no onboarding
    if (pathname === '/login') {
        // Verificar se é uma requisição de login (POST) - não redirecionar nesse caso
        if (req.method === 'POST') {
            console.log('[MIDDLEWARE] Requisição POST em /login, ignorando redirect');
            return response;
        }

        const redirectTo = req.nextUrl.searchParams.get('redirect') || '/dashboard';
        const url = req.nextUrl.clone();

        // Se não completou onboarding, ir para onboarding
        if (!profileError && profile && profile.onboarding_completed === false) {
            console.log('[MIDDLEWARE] Onboarding pendente, redirecionando para /onboarding');
            url.pathname = '/onboarding';
        } else {
            console.log(`[MIDDLEWARE] Onboarding completo ou perfil não encontrado, redirecionando para ${redirectTo}`);
            url.pathname = redirectTo;
        }

        url.searchParams.delete('redirect');
        return NextResponse.redirect(url);
    }

    // Se está tentando acessar rota protegida e onboarding não completo → redirecionar para onboarding
    if (isProtectedPath && !profileError && profile && profile.onboarding_completed === false) {
        console.log('[MIDDLEWARE] Onboarding não completado, redirecionando para /onboarding');
        const url = req.nextUrl.clone();
        url.pathname = '/onboarding';
        return NextResponse.redirect(url);
    }

    // ========================================
    // 11. VERIFICAÇÃO DE PAGAMENTO (apenas para rotas protegidas)
    // ========================================
    if (isProtectedPath) {
        // Se perfil não existe ou erro ao buscar
        if (profileError && profileError.code !== 'PGRST116') {
            console.error('[MIDDLEWARE] Erro ao buscar dados do usuário:', profileError);
            const url = req.nextUrl.clone();
            url.pathname = '/pricing';
            return NextResponse.redirect(url);
        }

        // Verificar permissões de pagamento
        const hasFounderAccess = profile?.founder_access === true;
        const hasEnterprisePlan = profile?.subscription_plan === 'enterprise';
        const isSubscriptionActive = profile?.subscription_status === 'active';

        if (hasFounderAccess) {
            console.log('🏆 FOUNDER ACCESS - ACESSO TOTAL LIBERADO');
            response.headers.set('x-user-authenticated', 'true');
            response.headers.set('x-user-founder', 'true');
            response.headers.set('x-user-plan', profile?.subscription_plan || 'free');
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
            response.headers.set('x-user-plan', profile?.subscription_plan || 'free');
            response.headers.set('x-user-paid', 'true');
            return response;
        }

        // Usuário logado mas sem permissões - redireciona para pricing
        console.log(`💰 Acesso negado a ${pathname} - usuário não pagou (ID: ${user.id})`);
        const url = req.nextUrl.clone();
        url.pathname = '/pricing';
        url.searchParams.set('reason', 'payment_required');
        return NextResponse.redirect(url);
    }

    // ========================================
    // 12. OUTRAS ROTAS - DEIXA PASSAR
    // ========================================
    return response;
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
