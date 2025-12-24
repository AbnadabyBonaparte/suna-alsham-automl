import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function updateSession(request: NextRequest) {
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
    return supabaseResponse;
  }

  // Se é rota de desenvolvimento, deixa passar
  if (request.nextUrl.pathname.startsWith('/dev/')) {
    return supabaseResponse;
  }

  // ========================================
  // 1. NÃO AUTENTICADO - REDIRECIONAR PARA LOGIN
  // ========================================
  if (!user) {
    // Se não está em rota pública, redirecionar para login
    if (request.nextUrl.pathname !== '/login') {
      const url = request.nextUrl.clone();
      url.pathname = '/login';
      url.searchParams.set('redirect', request.nextUrl.pathname);
      return NextResponse.redirect(url);
    }
    return supabaseResponse;
  }

  // ========================================
  // 2. USUÁRIO AUTENTICADO - VERIFICAR ONBOARDING
  // ========================================

  // CRÍTICO: NÃO verificar onboarding durante requisições RSC para evitar loops
  const isRSCRequest = request.nextUrl.searchParams.has('_rsc');
  if (isRSCRequest) {
    console.log('[PROXY] Requisição RSC detectada, ignorando verificações de onboarding/pagamento');
    return supabaseResponse;
  }

  // Buscar profile do usuário
  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select('onboarding_completed, role, subscription_plan, subscription_status, founder_access')
    .eq('id', user.id)
    .single();

  // Debug logs
  console.log('[PROXY] Verificando autenticação e onboarding:', {
    path: request.nextUrl.pathname,
    userId: user.id,
    userEmail: user.email,
    profileExists: !!profile,
    profileError: profileError?.message,
    onboarding_completed: profile?.onboarding_completed,
    role: profile?.role,
    subscription_status: profile?.subscription_status,
  });

  // Se profile não existe, criar automaticamente
  if (profileError && profileError.code === 'PGRST116') {
    console.log('[PROXY] Perfil não existe, criando automaticamente...');
    const { error: insertError } = await supabase
      .from('profiles')
      .insert({
        id: user.id,
        username: user.email?.split('@')[0] || 'user',
        onboarding_completed: false,
      });

    if (!insertError) {
      console.log('[PROXY] Perfil criado, redirecionando para onboarding');
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
    console.log('[PROXY] Onboarding não completado, redirecionando para /onboarding');
    const url = request.nextUrl.clone();
    url.pathname = '/onboarding';
    return NextResponse.redirect(url);
  }

  // Se onboarding FOI completado e está em /onboarding, redirecionar para dashboard
  if (profile && profile.onboarding_completed === true && request.nextUrl.pathname === '/onboarding') {
    console.log('[PROXY] Onboarding completo, redirecionando para /dashboard');
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
      console.log('[PROXY] 👑 DONO DETECTADO - ACESSO TOTAL LIBERADO');
      return supabaseResponse;
    }

    // Verificar founder access
    const hasFounderAccess = profile.founder_access === true;
    if (hasFounderAccess) {
      console.log('[PROXY] 🏆 FOUNDER ACCESS - ACESSO TOTAL LIBERADO');
      return supabaseResponse;
    }

    // Verificar subscription
    const hasEnterprisePlan = profile.subscription_plan === 'enterprise';
    const isSubscriptionActive = profile.subscription_status === 'active';

    if (hasEnterprisePlan && isSubscriptionActive) {
      console.log('[PROXY] 💎 ENTERPRISE PLAN ATIVO - ACESSO LIBERADO');
      return supabaseResponse;
    }

    if (isSubscriptionActive) {
      console.log('[PROXY] ✅ SUBSCRIPTION ATIVA - ACESSO LIBERADO');
      return supabaseResponse;
    }

    // Usuário logado mas sem permissões - redireciona para pricing
    console.log(`[PROXY] 💰 Acesso negado a ${request.nextUrl.pathname} - usuário não pagou`);
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
      console.log('[PROXY] Usuário autenticado e onboarding completo, redirecionando para /dashboard');
      const url = request.nextUrl.clone();
      url.pathname = '/dashboard';
      return NextResponse.redirect(url);
    } else {
      // Se não completou onboarding, ir para onboarding
      console.log('[PROXY] Usuário autenticado mas onboarding incompleto, redirecionando para /onboarding');
      const url = request.nextUrl.clone();
      url.pathname = '/onboarding';
      return NextResponse.redirect(url);
    }
  }

  // IMPORTANT: You *must* return the supabaseResponse object as it is. If you're
  // creating a new response object with NextResponse.next() make sure to:
  // 1. Pass the request in it, like so:
  //    const myNewResponse = NextResponse.next({ request })
  // 2. Copy over the cookies, like so:
  //    myNewResponse.cookies.setAll(supabaseResponse.cookies.getAll())
  // 3. Change the myNewResponse object to fit your needs, but avoid changing
  //    the cookies!
  // 4. Finally:
  //    return myNewResponse
  // If this is not done, you may be causing the browser and server to go out
  // of sync and terminate the user's session prematurely!

  return supabaseResponse;
}
