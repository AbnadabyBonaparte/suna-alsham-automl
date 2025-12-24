import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  console.log('[MIDDLEWARE] Processando:', request.nextUrl.pathname);

  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => request.cookies.set(name, value));

          supabaseResponse = NextResponse.next({
            request,
          });

          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options),
          );
        },
      },
    },
  );

  // IMPORTANT: Avoid writing any logic between createServerClient and
  // supabase.auth.getUser(). A simple mistake could make it very hard to debug
  // issues with users being randomly logged out.

  const {
    data: { user },
  } = await supabase.auth.getUser();

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
    '/api/stripe/webhook',
    '/api/stripe/checkout',
  ];

  const isPublicRoute = PUBLIC_ROUTES.some((route) =>
    request.nextUrl.pathname === route || request.nextUrl.pathname.startsWith('/api/'),
  );

  // Se é rota pública, deixa passar
  if (isPublicRoute) {
    console.log('[MIDDLEWARE] Rota pública, deixando passar');
    return supabaseResponse;
  }

  // Se é rota de desenvolvimento, deixa passar
  if (request.nextUrl.pathname.startsWith('/dev/')) {
    console.log('[MIDDLEWARE] Rota de desenvolvimento, deixando passar');
    return supabaseResponse;
  }

  // ========================================
  // 1. NÃO AUTENTICADO - REDIRECIONAR PARA LOGIN
  // ========================================
  if (!user) {
    console.log('[MIDDLEWARE] Usuário não autenticado, redirecionando para /login');
    // Se não está em rota pública, redirecionar para login
    if (request.nextUrl.pathname !== '/login') {
      const url = request.nextUrl.clone();
      url.pathname = '/login';
      url.searchParams.set('redirect', request.nextUrl.pathname);
      return NextResponse.redirect(url);
    }
    return supabaseResponse;
  }

  console.log('[MIDDLEWARE] Usuário autenticado:', user.email);

  // ========================================
  // 2. USUÁRIO AUTENTICADO - VERIFICAR ONBOARDING
  // ========================================

  // CRÍTICO: NÃO verificar onboarding durante requisições RSC para evitar loops
  const isRSCRequest = request.nextUrl.searchParams.has('_rsc');
  if (isRSCRequest) {
    console.log('[MIDDLEWARE] Requisição RSC detectada, ignorando verificações');
    return supabaseResponse;
  }

  // Buscar profile do usuário
  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select('onboarding_completed, role, subscription_plan, subscription_status, founder_access')
    .eq('id', user.id)
    .single();

  // Debug logs
  console.log('[MIDDLEWARE] Profile do usuário:', {
    path: request.nextUrl.pathname,
    userId: user.id,
    userEmail: user.email,
    profileExists: !!profile,
    profileError: profileError?.message,
    onboarding_completed: profile?.onboarding_completed,
    role: profile?.role,
  });

  // Se profile não existe, criar automaticamente
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
      console.log('[MIDDLEWARE] Perfil criado, redirecionando para /onboarding');
      const url = request.nextUrl.clone();
      url.pathname = '/onboarding';
      return NextResponse.redirect(url);
    }
  }

  // ========================================
  // 3. VERIFICAR ONBOARDING
  // ========================================

  // Se onboarding NÃO foi completado e não está em /onboarding, redirecionar
  if (profile && profile.onboarding_completed === false && request.nextUrl.pathname !== '/onboarding') {
    console.log('[MIDDLEWARE] Onboarding não completado, redirecionando para /onboarding');
    const url = request.nextUrl.clone();
    url.pathname = '/onboarding';
    return NextResponse.redirect(url);
  }

  // Se onboarding FOI completado e está em /onboarding, redirecionar para dashboard
  if (profile && profile.onboarding_completed === true && request.nextUrl.pathname === '/onboarding') {
    console.log('[MIDDLEWARE] Onboarding completo, redirecionando para /dashboard');
    const url = request.nextUrl.clone();
    url.pathname = '/dashboard';
    return NextResponse.redirect(url);
  }

  // ========================================
  // 4. VERIFICAR PAGAMENTO (para rotas protegidas)
  // ========================================

  const protectedPaths = ['/dashboard', '/settings', '/admin', '/api/quantum', '/api/evolution'];
  const isProtectedPath = protectedPaths.some((path) =>
    request.nextUrl.pathname.startsWith(path),
  );

  if (isProtectedPath && profile) {
    // Verificar se é o dono (acesso total)
    const isOwner = user.email === 'casamondestore@gmail.com';
    if (isOwner) {
      console.log('[MIDDLEWARE] 👑 DONO DETECTADO - ACESSO TOTAL LIBERADO');
      supabaseResponse.headers.set('x-user-authenticated', 'true');
      supabaseResponse.headers.set('x-user-founder', 'true');
      supabaseResponse.headers.set('x-user-email', user.email);
      return supabaseResponse;
    }

    // Verificar founder access
    const hasFounderAccess = profile.founder_access === true;
    if (hasFounderAccess) {
      console.log('[MIDDLEWARE] 🏆 FOUNDER ACCESS - ACESSO TOTAL LIBERADO');
      supabaseResponse.headers.set('x-user-authenticated', 'true');
      supabaseResponse.headers.set('x-user-founder', 'true');
      return supabaseResponse;
    }

    // Verificar subscription
    const hasEnterprisePlan = profile.subscription_plan === 'enterprise';
    const isSubscriptionActive = profile.subscription_status === 'active';

    if (hasEnterprisePlan && isSubscriptionActive) {
      console.log('[MIDDLEWARE] 💎 ENTERPRISE PLAN ATIVO - ACESSO LIBERADO');
      supabaseResponse.headers.set('x-user-authenticated', 'true');
      supabaseResponse.headers.set('x-user-plan', 'enterprise');
      supabaseResponse.headers.set('x-user-paid', 'true');
      return supabaseResponse;
    }

    if (isSubscriptionActive) {
      console.log('[MIDDLEWARE] ✅ SUBSCRIPTION ATIVA - ACESSO LIBERADO');
      supabaseResponse.headers.set('x-user-authenticated', 'true');
      supabaseResponse.headers.set('x-user-plan', profile.subscription_plan || 'free');
      supabaseResponse.headers.set('x-user-paid', 'true');
      return supabaseResponse;
    }

    // Usuário logado mas sem permissões - redireciona para pricing
    console.log(`[MIDDLEWARE] 💰 Acesso negado a ${request.nextUrl.pathname} - usuário não pagou`);
    const url = request.nextUrl.clone();
    url.pathname = '/pricing';
    url.searchParams.set('reason', 'payment_required');
    return NextResponse.redirect(url);
  }

  // ========================================
  // 5. REDIRECIONAR /login se já autenticado
  // ========================================

  if (user && request.nextUrl.pathname === '/login') {
    // Se completou onboarding, ir para dashboard
    if (profile?.onboarding_completed === true) {
      console.log('[MIDDLEWARE] Usuário autenticado e onboarding completo, redirecionando para /dashboard');
      const url = request.nextUrl.clone();
      url.pathname = '/dashboard';
      return NextResponse.redirect(url);
    } else {
      // Se não completou onboarding, ir para onboarding
      console.log('[MIDDLEWARE] Usuário autenticado mas onboarding incompleto, redirecionando para /onboarding');
      const url = request.nextUrl.clone();
      url.pathname = '/onboarding';
      return NextResponse.redirect(url);
    }
  }

  // ========================================
  // 6. DEIXAR PASSAR (para rotas autenticadas)
  // ========================================

  console.log('[MIDDLEWARE] Deixando passar requisição para:', request.nextUrl.pathname);
  return supabaseResponse;
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
