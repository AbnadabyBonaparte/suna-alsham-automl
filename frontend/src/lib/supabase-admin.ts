import { createClient, SupabaseClient } from '@supabase/supabase-js';

// Lazy initialization - só cria o cliente quando for realmente usado
let _supabaseAdmin: SupabaseClient | null = null;

// Função getter para criar o cliente apenas em runtime (não durante o build)
export function getSupabaseAdmin(): SupabaseClient {
  if (_supabaseAdmin) {
    return _supabaseAdmin;
  }

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!supabaseUrl || !supabaseServiceRoleKey) {
    throw new Error('Missing Supabase environment variables for admin client');
  }

  _supabaseAdmin = createClient(supabaseUrl, supabaseServiceRoleKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  });

  return _supabaseAdmin;
}

// Export para retrocompatibilidade - usa getter lazy
// NOTA: Se você importar supabaseAdmin diretamente, ele será undefined durante o build
// Use getSupabaseAdmin() para garantir que funcione corretamente
export const supabaseAdmin = {
  get client() {
    return getSupabaseAdmin();
  }
};
