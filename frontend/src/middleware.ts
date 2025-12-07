/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - MIDDLEWARE DE PROTEÇÃO (VERSÃO SIMPLIFICADA)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/middleware.ts
 * 🔐 Proteção básica de rotas baseada em cookie de sessão Supabase
 *    (sem chamar Supabase no edge, para evitar loop de login)
 * ═══════════════════════════════════════════════════════════════
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// ========================================
// ROTAS PÚBLICAS (sem autenticação)
// ========================================
const PUBLIC_ROUTES = [
  '/',
  '/pricing',
  '/login',
  '/signup',
  '/onboarding',
  '/auth/callback',
  '/forgot-password',
  '/reset-password',
  '/terms',
  '/privacy',
  '/contact',
];

const PUBLIC_PREFIXES = [
  '/dev/',
  '/api/',
];

// ========================================
// ROTAS PROTEGIDAS (precisam estar logado)
// ========================================
const PROTECTED_PREFIXES = ['/dashboard'];

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // ========================================
  // 0. BYPASS EM DEV / ROTAS DE SISTEMA
  // ========================================
  const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
  if (isDevMode) {
    console.log('🛠️ DEV MODE: middleware bypass');
    return NextResponse.next();
  }

  // Rotas internas do Next, arquivos estáticos, etc.
  if (
    pathname.startsWith('/_next') ||
    pathname.match(/\.(?:svg|png|jpg|jpeg|gif|webp|ico|css|js|mp3)$/)
  ) {
    return NextResponse.next();
  }

  // ========================================
  // 1. ROTAS PÚBLICAS - LIBERA
  // ========================================
  const isExplicitPublicRoute = PUBLIC_ROUTES.includes(pathname);
  const isPublicPrefix = PUBLIC_PREFIXES.some((prefix) => pathname.startsWith(prefix));
  if (isExplicitPublicRoute || isPublicPrefix) {
    return NextResponse.next();
  }

  // ========================================
  // 2. VERIFICAR SE É ROTA PROTEGIDA
  // ========================================
  const isProtected = PROTECTED_PREFIXES.some((prefix) =>
    pathname.startsWith(prefix),
  );

  if (!isProtected) {
    // Qualquer rota que não seja das protegidas passa direto
    return NextResponse.next();
  }

  // ========================================
  // 3. CHECAR SE EXISTE COOKIE DE AUTENTICAÇÃO SUPABASE
  // ========================================
  // Obs.: checagem fina de permissão (plano/status) ocorre no server
  // via `requireDashboardAccess`; aqui validamos apenas presença do cookie
  // para evitar loops de login no edge.
  const cookies = req.cookies.getAll();

  // Cookies do Supabase seguem o padrão: sb-<project-ref>-auth-token
  const hasSupabaseAuthCookie = cookies.some((cookie) =>
    cookie.name.startsWith('sb-') && cookie.name.endsWith('-auth-token'),
  );

  if (!hasSupabaseAuthCookie) {
    console.log(`🔒 Acesso negado a ${pathname} - sem cookie Supabase`);

    const url = req.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('redirect', pathname);
    return NextResponse.redirect(url);
  }

  // Usuário tem cookie supabase: consideramos autenticado
  const res = NextResponse.next();
  res.headers.set('x-user-authenticated', 'true');
  return res;
}

export const config = {
  matcher: [
    /*
     * Match all request paths exceto:
     * - _next/static (arquivos estáticos)
     * - _next/image (otimização de imagem)
     * - favicon.ico (favicon)
     * - qualquer arquivo com extensão (.*\..*)
     */
    '/((?!_next/static|_next/image|favicon.ico|public|.*\\..*|sounds|images).*)',
  ],
};
