/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ADMIN HOOK
 * ═══════════════════════════════════════════════════════════════
 * Hook para buscar dados administrativos (usuários)
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

export interface AdminUser {
  id: string;
  username: string | null;
  full_name: string | null;
  avatar_url: string | null;
  created_at: string;
}

export function useAdmin() {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('profiles')
        .select('id, username, full_name, avatar_url, created_at')
        .order('created_at', { ascending: false })
        .limit(50);

      if (fetchError) throw fetchError;

      setUsers((data || []) as AdminUser[]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch users';
      setError(errorMessage);
      console.error('Error fetching admin users:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return {
    users,
    loading,
    error,
    fetchUsers,
    totalUsers: users.length,
    // Não há coluna de presença/status em `profiles`, então não sabemos
    // quem está ativo. Retornamos null (desconhecido) em vez de afirmar
    // que todos os usuários estão ativos.
    activeUsers: null as number | null,
  };
}
