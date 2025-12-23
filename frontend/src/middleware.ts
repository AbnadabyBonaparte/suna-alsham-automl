import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
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

  // Force refresh of auth state
  await supabase.auth.getUser();

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
    const { data: profile } = await supabase
      .from('profiles')
      .select('onboarding_completed')
      .eq('id', user.id)
      .single();

    // Se não completou onboarding, redirecionar para onboarding
    if (profile && !profile.onboarding_completed && request.nextUrl.pathname !== '/onboarding') {
      const url = request.nextUrl.clone();
      url.pathname = '/onboarding';
      return NextResponse.redirect(url);
    }
  }

  // Se autenticado e completou onboarding, mas está em /onboarding → dashboard
  if (user && request.nextUrl.pathname === '/onboarding') {
    const { data: profile } = await supabase
      .from('profiles')
      .select('onboarding_completed')
      .eq('id', user.id)
      .single();

    if (profile?.onboarding_completed) {
      const url = request.nextUrl.clone();
      url.pathname = '/dashboard';
      return NextResponse.redirect(url);
    }
  }

  // Se autenticado e está em /login, redirecionar baseado no onboarding
  if (user && request.nextUrl.pathname === '/login') {
    const { data: profile } = await supabase
      .from('profiles')
      .select('onboarding_completed')
      .eq('id', user.id)
      .single();

    const redirectTo = request.nextUrl.searchParams.get('redirect') || '/dashboard';
    const url = request.nextUrl.clone();

    // Se não completou onboarding, ir para onboarding
    if (profile && !profile.onboarding_completed) {
      url.pathname = '/onboarding';
    } else {
      url.pathname = redirectTo;
    }

    url.searchParams.delete('redirect');
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
