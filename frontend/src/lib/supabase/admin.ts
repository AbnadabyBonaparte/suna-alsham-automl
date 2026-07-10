import { createClient, type SupabaseClient } from '@supabase/supabase-js';

/**
 * Cliente Supabase com SERVICE ROLE (admin).
 *
 * ⚠️ SERVER-ONLY. Nunca importe este módulo em componentes client —
 * a service role key ignora RLS e não pode vazar para o browser.
 * Use apenas em route handlers, server actions e cron jobs.
 */
export function createAdminClient(): SupabaseClient {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!url || !serviceRoleKey) {
    throw new Error(
      'Supabase admin client requer NEXT_PUBLIC_SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY.',
    );
  }

  return createClient(url, serviceRoleKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}
