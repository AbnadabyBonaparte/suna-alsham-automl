import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const path = request.nextUrl.pathname;
    
    // Define public paths that don't require authentication
    const isPublicPath = path === '/login' || path === '/signup' || path === '/';
    
    // Get the token from cookies - Supabase v2 format
    const supabaseToken = request.cookies.get('sb-vktzdrsigrdnemdshcdp-auth-token')?.value;
    
    // Also check localStorage backup via cookie
    const hasToken = !!supabaseToken;
    
    // Redirect logic
    if (isPublicPath && hasToken && path !== '/') {
        return NextResponse.redirect(new URL('/dashboard', request.url));
    }
    
    if (!isPublicPath && !hasToken) {
        return NextResponse.redirect(new URL('/login', request.url));
    }
    
    return NextResponse.next();
}

export const config = {
    matcher: [
        '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
    ],
};
