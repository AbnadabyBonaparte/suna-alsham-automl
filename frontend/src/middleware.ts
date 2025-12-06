/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - MIDDLEWARE DE PROTEÇÃO (SSR + SUPABASE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/middleware.ts
 * 🔐 Proteção de rotas com verificação de pagamento
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
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
const PAID_ROUTES = ['/dashboard'];

export async function middleware(req: NextRequest) {
  const url = req.nextUrl;
  const { pathname } = url;

  // Resposta base já carregando os headers da request
  const res = NextResponse.next({
    request: {
      headers: req.headers,
    },
  });

  // ========================================
  // MODO DESENVOLVIMENTO - BYPASS TOTAL
  // ========================================
  const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
  if (isDevMode) {
    console.log('🛠️ DEV MODE: Bypass de autenticação ativado');
    return res;
  }

  // ========================================
  // 1. ROTAS PÚBLICAS / API - LIBERA
  // ========================================
  const isApiRoute = pathname.startsWith('/api/');
  const isPublicRoute = PUBLIC_ROUTES.includes(pathname);

  if (isApiRoute || isPublicRoute) {
    return res;
  }

  // ========================================
  // ROTAS DE DESENVOLVIMENTO - LIBERA
  // ========================================
  if (pathname.startsWith('/dev/')) {
    console.log('🛠️ DEV ROUTE: Acesso liberado para rota de desenvolvimento');
    return res;
  }

  // ========================================
  // 2. CONFIG SUPABASE (SSR CLIENT)
// ========================================
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    console.warn('⚠️ Supabase não configurado no middleware');
    return res;
  }

  const supabase = createServerClient(supabaseUrl, supabaseAnonKey, {
    cookies: {
      getAll() {
        return req.cookies.getAll();
      },
      setAll(cookies) {
        cookies.forEach(({ name, value, options }) => {
          res.cookies.set(name, value, options);
        });
      },
    },
  });

  const {
    data: { user },
  } = await supabase.auth.getUser();

  // ========================================
  // 3. ROTAS DE DASHBOARD - VERIFICAÇÃO COMPLETA
  // ========================================
  if (pathname.startsWith('/dashboard')) {
    // Se não tem usuário logado → login
    if (!user) {
      console.log(`🔒 Acesso negado a ${pathname} - não autenticado`);
      const redirectUrl = new URL('/login', req.url);
      redirectUrl.searchParams.set('redirect', pathname);
      return NextResponse.redirect(redirectUrl);
    }

    const userId = user.id;
    const userEmail = user.email ?? '';

    // ========================================
    // 4. DONO SEMPRE TEM ACESSO
    // ========================================
    if (userEmail === 'casamondestore@gmail.com') {
      console.log('👑 DONO DETECTADO - ACESSO TOTAL LIBERADO');
      res.headers.set('x-user-authenticated', 'true');
      res.headers.set('x-user-founder', 'true');
      res.headers.set('x-user-email', userEmail);
      return res;
    }

    // Buscar dados do usuário na tabela profiles
    const { data: userData, error: userError } = await supabase
      .from('profiles')
      .select('subscription_plan, subscription_status, founder_access')
      .eq('id', userId)
      .single();

    if (userError) {
      console.error('Erro ao buscar dados do usuário:', userError);
      const redirectUrl = new URL('/pricing', req.url);
      return NextResponse.redirect(redirectUrl);
    }

    // ========================================
    // 5. VERIFICAÇÃO DE PERMISSÕES
    // ========================================
    const hasFounderAccess = userData?.founder_access === true;
    const hasEnterprisePlan = userData?.subscription_plan === 'enterprise';
    const isSubscriptionActive = userData?.subscription_status === 'active';

    if (hasFounderAccess) {
      console.log('🏆 FOUNDER ACCESS - ACESSO TOTAL LIBERADO');
      res.headers.set('x-user-authenticated', 'true');
      res.headers.set('x-user-founder', 'true');
      res.headers.set(
        'x-user-plan',
        userData?.subscription_plan || 'free',
      );
      return res;
    }

    if (hasEnterprisePlan && isSubscriptionActive) {
      console.log('💎 ENTERPRISE PLAN ATIVO - ACESSO LIBERADO');
      res.headers.set('x-user-authenticated', 'true');
      res.headers.set('x-user-plan', 'enterprise');
      res.headers.set('x-user-paid', 'true');
      return res;
    }

    if (isSubscriptionActive) {
      console.log('✅ SUBSCRIPTION ATIVA - ACESSO LIBERADO');
      res.headers.set('x-user-authenticated', 'true');
      res.headers.set(
        'x-user-plan',
        userData?.subscription_plan || 'free',
      );
      res.headers.set('x-user-paid', 'true');
      return res;
    }

    console.log(
      `💰 Acesso negado a ${pathname} - usuário não pagou (ID: ${userId})`,
    );
    const redirectUrl = new URL('/pricing', req.url);
    redirectUrl.searchParams.set('reason', 'payment_required');
    return NextResponse.redirect(redirectUrl);
  }

  // ========================================
  // 6. OUTRAS ROTAS - DEIXA PASSAR
  // ========================================
  return res;
}

export const config = {
  matcher: [
    // Match all request paths exceto estáticos e assets públicos
    '/((?!_next/static|_next/image|favicon.ico|public|.*\\..*|sounds|images).*)',
  ],
};
