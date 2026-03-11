import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { createServerClient } from '@supabase/ssr';
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

async function createServerSupabaseClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options),
            );
          } catch {
            // Ignora em Server Components
          }
        },
      },
    },
  );
}

function createDefaultProfile(userId: string): DashboardProfile {
  return {
    id: userId,
    username: null,
    full_name: null,
    avatar_url: null,
    subscription_plan: 'free',
    subscription_status: 'inactive',
    founder_access: null,
    created_at: new Date().toISOString(),
  };
}

export async function requireDashboardAccess(): Promise<DashboardAccess> {
  const supabase = await createServerSupabaseClient();

  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  console.log('[AUTH] getUser result:', { userId: user?.id, error: userError?.message });

  if (userError || !user) {
    console.log('[AUTH] No user found, redirecting to login');
    redirect('/login?redirect=/dashboard');
  }

  const { data: profile, error } = await supabase
    .from('profiles')
    .select(
      'id, username, full_name, avatar_url, subscription_plan, subscription_status, founder_access, billing_cycle, subscription_end, created_at, updated_at',
    )
    .eq('id', user.id)
    .single();

  console.log('[AUTH] Profile query:', { profileId: profile?.id, error: error?.message, code: error?.code });

  const finalProfile = profile || createDefaultProfile(user.id);

  const hasFounderAccess = finalProfile.founder_access === true ||
    user.email === 'casamondestore@gmail.com';
  const isEnterprise = finalProfile.subscription_plan === 'enterprise';
  const hasActiveSubscription = finalProfile.subscription_status === 'active';

  const hasAccess =
    hasFounderAccess || (isEnterprise && hasActiveSubscription) || hasActiveSubscription;

  return {
    profile: finalProfile,
    user,
    hasFounderAccess,
    isEnterprise,
    hasAccess,
  };
}
