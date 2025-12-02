/**
 * Hook para gerenciar profile com Zustand + Supabase
 * Usa .maybeSingle() e cria perfil automaticamente se não existir
 */
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useProfileStore, Profile } from '@/stores';

export function useProfile() {
  const store = useProfileStore();

  // Buscar profile ao montar
  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      store.setLoading(true);

      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        store.setProfile(null);
        return;
      }

      // Usar .maybeSingle() em vez de .single()
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.id)
        .maybeSingle();

      if (error) throw error;

      // Se o perfil não existe, criar automaticamente
      if (!data) {
        await createProfile(user.id);
        return;
      }

      store.setProfile(data);
    } catch (err: any) {
      console.error('Error fetching profile:', err);
      store.setError(err.message);
    } finally {
      store.setLoading(false);
    }
  };

  const createProfile = async (userId: string) => {
    try {
      store.setLoading(true);

      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      // Criar perfil com dados básicos do auth
      const { data, error } = await supabase
        .from('profiles')
        .insert({
          id: userId,
          username: user.email?.split('@')[0] || 'user',
          full_name: user.user_metadata?.full_name || null,
          avatar_url: user.user_metadata?.avatar_url || null,
        })
        .select()
        .maybeSingle();

      if (error) throw error;

      if (data) {
        store.setProfile(data);
      }
    } catch (err: any) {
      console.error('Error creating profile:', err);
      store.setError(err.message);
    } finally {
      store.setLoading(false);
    }
  };

  const updateProfile = async (updates: Partial<Profile>) => {
    try {
      store.setLoading(true);

      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      const { data, error } = await supabase
        .from('profiles')
        .update(updates)
        .eq('id', user.id)
        .select()
        .maybeSingle();

      if (error) throw error;

      if (data) {
        store.setProfile(data);
      }
    } catch (err: any) {
      console.error('Error updating profile:', err);
      store.setError(err.message);
      throw err;
    } finally {
      store.setLoading(false);
    }
  };

  return {
    ...store,
    fetchProfile,
    updateProfile,
  };
}
