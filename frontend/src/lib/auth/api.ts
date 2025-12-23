import { cookies } from 'next/headers';
import { createRouteHandlerClient } from '@supabase/ssr';
import type { SupabaseClient } from '@supabase/supabase-js';

export async function getAuthenticatedRouteClient(): Promise<SupabaseClient> {
  const cookieStore = await cookies();
  return createRouteHandlerClient({ cookies: () => cookieStore });
}
