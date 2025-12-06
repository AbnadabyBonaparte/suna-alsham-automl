/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - MIDDLEWARE DE PROTEÇÃO
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/middleware.ts
 * 🔐 Proteção de rotas com verificação de pagamento
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@supabase/ssr';
import type { SupabaseClient } from '@supabase/supabase-js';

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
];

const isPublicPath = (pathname: string) => {
    return (
        PUBLIC_ROUTES.includes(pathname) ||
        pathname.startsWith('/api') ||
        pathname.startsWith('/_next') ||
        pathname.startsWith('/static') ||
        pathname.startsWith('/favicon') ||
        pathname.startsWith('/images') ||
        pathname.startsWith('/sounds')
    );
};

async function getSupabaseClient(req: NextRequest, res: NextResponse): Promise<SupabaseClient | null> {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    if (!supabaseUrl || !supabaseAnonKey) {
        console.warn('⚠️ Supabase environment variables missing in middleware');
        return null;
    }

    return createServerClient(supabaseUrl, supabaseAnonKey, {
        cookies: {
            get(name: string) {
                return req.cookies.get(name)?.value;
            },
            set(name: string, value: string, options: any) {
                res.cookies.set({ name, value, ...options });
            },
            remove(name: string, options: any) {
                res.cookies.set({ name, value: '', ...options });
            }
        }
    });
}

async function handleDashboardAccess(req: NextRequest, supabase: SupabaseClient, res: NextResponse) {
    const { data, error } = await supabase.auth.getUser();

    if (error || !data?.user) {
        const loginUrl = new URL('/login', req.url);
        return NextResponse.redirect(loginUrl);
    }

    const userEmail = data.user.email;

    if (userEmail === 'casamondestore@gmail.com') {
        const response = NextResponse.next({ request: { headers: req.headers } });
        response.headers.set('x-user-authenticated', 'true');
        response.headers.set('x-user-founder', 'true');
        response.headers.set('x-user-email', userEmail || '');
        return response;
    }

    const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .select('subscription_plan, subscription_status, founder_access')
        .eq('id', data.user.id)
        .single();

    if (profileError) {
        console.error('Erro ao buscar dados do usuário:', profileError);
        const pricingUrl = new URL('/pricing', req.url);
        pricingUrl.searchParams.set('reason', 'profile_error');
        return NextResponse.redirect(pricingUrl);
    }

    const hasFounderAccess = profile?.founder_access === true;
    const hasEnterprisePlan = profile?.subscription_plan === 'enterprise' && profile?.subscription_status === 'active';
    const hasActiveSubscription = profile?.subscription_status === 'active';

    if (hasFounderAccess || hasEnterprisePlan || hasActiveSubscription) {
        const response = NextResponse.next({ request: { headers: req.headers } });
        response.headers.set('x-user-authenticated', 'true');
        response.headers.set('x-user-plan', profile?.subscription_plan || 'free');
        if (hasFounderAccess) response.headers.set('x-user-founder', 'true');
        if (hasEnterprisePlan || hasActiveSubscription) response.headers.set('x-user-paid', 'true');
        return response;
    }

    const pricingUrl = new URL('/pricing', req.url);
    pricingUrl.searchParams.set('reason', 'payment_required');
    return NextResponse.redirect(pricingUrl);
}

export async function middleware(req: NextRequest) {
    const res = NextResponse.next();

    const devMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
    if (devMode) {
        return res;
    }

    const pathname = req.nextUrl.pathname;
    if (isPublicPath(pathname)) {
        return res;
    }

    const supabase = await getSupabaseClient(req, res);
    if (!supabase) {
        return res;
    }

    if (pathname.startsWith('/dashboard')) {
        return handleDashboardAccess(req, supabase, res);
    }

    return res;
}

export const config = {
    matcher: [
        '/((?!_next/static|_next/image|favicon.ico|public|.*\\..*|sounds|images).*)',
        '/dashboard/:path*'
    ],
};
