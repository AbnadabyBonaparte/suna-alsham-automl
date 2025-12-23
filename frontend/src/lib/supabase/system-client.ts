import { createClient, type SupabaseClient } from '@supabase/supabase-js';

export function getSystemJobClient(): SupabaseClient {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const systemJwt = process.env.SUPABASE_SYSTEM_JWT;

  if (!supabaseUrl || !anonKey || !systemJwt) {
    throw new Error('Supabase system job configuration missing');
  }

  return createClient(supabaseUrl, anonKey, {
    global: {
      headers: {
        Authorization: `Bearer ${systemJwt}`,
      },
    },
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });
}
