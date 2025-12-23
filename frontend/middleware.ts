import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { createMiddlewareClient } from '@supabase/ssr';

const PUBLIC_API_PREFIXES = ['/api/stripe'];
const SYSTEM_JOB_ROUTES = ['/api/evolution/daily', '/api/agents/heartbeat', '/api/queue/process'];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (!pathname.startsWith('/api/')) {
    return NextResponse.next();
  }

  if (PUBLIC_API_PREFIXES.some(prefix => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  if (SYSTEM_JOB_ROUTES.some(prefix => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  const response = NextResponse.next();
  const supabase = createMiddlewareClient({ req: request, res: response });
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    return NextResponse.json({ error: 'Autenticação requerida' }, { status: 401 });
  }

  return response;
}

export const config = {
  matcher: ['/api/:path*'],
};
