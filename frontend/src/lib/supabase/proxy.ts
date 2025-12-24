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

  const protectedPaths = ['/dashboard', '/settings', '/admin', '/api/quantum', '/api/evolution'];
  const isProtectedPath = protectedPaths.some((path) =>
    request.nextUrl.pathname.startsWith(path),
  );

  // Se não autenticado e tentando acessar rota protegida → login
  if (!user && isProtectedPath) {
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('redirect', request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }

  // Se autenticado, verificar onboarding antes de acessar dashboard
  if (user && isProtectedPath) {
    // Buscar profile para verificar se completou onboarding
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('onboarding_completed, role')
      .eq('id', user.id)
      .single();

    // Debug logs (sempre logar para debug em produção também)
    console.log('[PROXY] Verificando onboarding:', {
      path: request.nextUrl.pathname,
      userId: user.id,
      profileExists: !!profile,
      profileError: profileError?.message,
      onboarding_completed: profile?.onboarding_completed,
      role: profile?.role,
    });

    // Se profile não existe, criar automaticamente e redirecionar para onboarding
    if (profileError && profileError.code === 'PGRST116') {
      console.log('[PROXY] Perfil não existe, criando automaticamente...');
      // Tentar criar perfil básico
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
      } else {
        console.error('[PROXY] Erro ao criar perfil:', insertError);
        // Se não conseguir criar, permitir acesso (evita bloquear usuário)
      }
    }

    // Se profile existe mas onboarding não foi completado, redirecionar
    if (!profileError && profile && profile.onboarding_completed === false && request.nextUrl.pathname !== '/onboarding') {
      console.log('[PROXY] Onboarding não completado, redirecionando para /onboarding');
      const url = request.nextUrl.clone();
      url.pathname = '/onboarding';
      return NextResponse.redirect(url);
    }
    
    // Se onboarding_completed é true ou null/undefined, permitir acesso
    // (null/undefined pode acontecer durante criação de perfil)
  }

  // Se autenticado e completou onboarding, mas está em /onboarding → dashboard
  // IMPORTANTE: Só redireciona se realmente completou, evita loops
  if (user && request.nextUrl.pathname === '/onboarding') {
    // Verificar se há um header indicando que está salvando (evita race condition)
    const isSaving = request.headers.get('x-onboarding-saving') === 'true';
    if (isSaving) {
      console.log('[PROXY] Salvamento de onboarding em progresso, ignorando redirect');
      return supabaseResponse;
    }

    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('onboarding_completed, role')
      .eq('id', user.id)
      .single();

    // Debug logs
    console.log('[PROXY] Verificando onboarding em /onboarding:', {
      userId: user.id,
      profileExists: !!profile,
      profileError: profileError?.message,
      onboarding_completed: profile?.onboarding_completed,
      role: profile?.role,
    });

    // Só redireciona se o onboarding foi realmente completado
    // E se não está em processo de salvamento
    if (!profileError && profile && profile.onboarding_completed === true) {
      console.log('[PROXY] Onboarding completo, redirecionando para /dashboard');
      const url = request.nextUrl.clone();
      url.pathname = '/dashboard';
      return NextResponse.redirect(url);
    } else if (profileError) {
      console.log('[PROXY] Erro ao buscar perfil em /onboarding:', profileError.message);
      // Se houver erro, não redireciona (permite usuário completar onboarding)
    }
  }

  // Se autenticado e está em /login, redirecionar baseado no onboarding
  // IMPORTANTE: Não redirecionar durante processo de login (evita loops)
  if (user && request.nextUrl.pathname === '/login') {
    // Verificar se é uma requisição de login (POST) - não redirecionar nesse caso
    if (request.method === 'POST') {
      console.log('[PROXY] Requisição POST em /login, ignorando redirect');
      return supabaseResponse;
    }

    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('onboarding_completed, role')
      .eq('id', user.id)
      .single();

    console.log('[PROXY] Verificando onboarding em /login:', {
      userId: user.id,
      profileExists: !!profile,
      profileError: profileError?.message,
      onboarding_completed: profile?.onboarding_completed,
    });

    const redirectTo = request.nextUrl.searchParams.get('redirect') || '/dashboard';
    const url = request.nextUrl.clone();

    // Se não completou onboarding, ir para onboarding
    if (!profileError && profile && profile.onboarding_completed === false) {
      console.log('[PROXY] Onboarding pendente, redirecionando para /onboarding');
      url.pathname = '/onboarding';
    } else {
      console.log(`[PROXY] Onboarding completo ou perfil não encontrado, redirecionando para ${redirectTo}`);
      url.pathname = redirectTo;
    }

    url.searchParams.delete('redirect');
    return NextResponse.redirect(url);
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

