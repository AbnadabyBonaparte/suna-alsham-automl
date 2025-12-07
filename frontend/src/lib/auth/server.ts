import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { createServerClient, type CookieOptions } from '@supabase/ssr';
import type { User } from '@supabase/supabase-js';

export interface DashboardProfile {
  id: string;
  username: string | null;
  full_name: string | null;
  avatar_url: string | null;
  subscription_plan: string | null;
  subscription_status: string | null;
  founder_access: boolean | null;
  billing_cycle?: 'monthly' | 'yearly' | null;
  subscription_end?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface DashboardAccess {
  profile: DashboardProfile;
  user: User;
  hasFounderAccess: boolean;
  isEnterprise: boolean;
  hasAccess: boolean;
}

function createServerSupabaseClient() {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options });
        },
      },
    },
  );
}

export async function requireDashboardAccess(): Promise<DashboardAccess> {
  const supabase = createServerSupabaseClient();

  const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';

  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session || !session.user) {
    redirect('/login?redirect=/dashboard');
  }

  const user = session.user;

  if (isDevMode) {
    console.log('[AUTH][DEV] session', session);
    console.log('[AUTH][DEV] user.id', user.id);
  }

  const { data: profile, error } = await supabase
    .from('profiles')
    .select(
      'id, username, full_name, avatar_url, subscription_plan, subscription_status, founder_access, billing_cycle, subscription_end, created_at, updated_at',
    )
    .eq('id', user.id)
    .single();

  if (error || !profile) {
    redirect('/onboarding');
  }

  if (isDevMode) {
    console.log('[AUTH][DEV] profile', profile);
  }

  const hasFounderAccess = profile.founder_access === true;
  const isEnterprise = profile.subscription_plan === 'enterprise';
  const hasActiveSubscription = profile.subscription_status === 'active';

  const hasAccess =
    hasFounderAccess || (isEnterprise && hasActiveSubscription) || hasActiveSubscription;

  if (isDevMode) {
    console.log('[AUTH][DEV] hasAccess', hasAccess);
  }

  if (!hasAccess) {
    redirect('/pricing?reason=payment_required');
  }

  return {
    profile,
    user,
    hasFounderAccess,
    isEnterprise,
    hasAccess,
  };
}
