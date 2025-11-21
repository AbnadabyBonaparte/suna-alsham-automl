import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    // Get the pathname
    const path = request.nextUrl.pathname;

    // Define public paths that don't require authentication
    const isPublicPath = path === '/login' || path === '/signup' || path === '/';

    // Get the token from cookies (Supabase stores it as 'sb-access-token')
    const token = request.cookies.get('sb-access-token')?.value || '';

    // Redirect logic
    if (isPublicPath && token && path !== '/') {
        // If user is logged in and tries to access login/signup, redirect to dashboard
        return NextResponse.redirect(new URL('/dashboard', request.url));
    }

    if (!isPublicPath && !token) {
        // If user is not logged in and tries to access protected route, redirect to login
        return NextResponse.redirect(new URL('/login', request.url));
    }

    return NextResponse.next();
}

// Configure which routes use this middleware
export const config = {
    matcher: [
        /*
         * Match all request paths except:
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         * - public folder
         */
        '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
    ],
};
