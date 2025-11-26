/**
 * Hook para gerenciar requests com Zustand + Supabase
 */
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useRequestsStore, Request } from '@/stores';

export function useRequests() {
  const store = useRequestsStore();

  // Buscar requests ao montar
  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      store.setLoading(true);
      
      const { data, error } = await supabase
        .from('requests')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;
      
      store.setRequests(data || []);
    } catch (err: any) {
      console.error('Error fetching requests:', err);
      store.setError(err.message);
    } finally {
      store.setLoading(false);
    }
  };

  const createRequest = async (title: string, description: string, priority: 'low' | 'normal' | 'high' = 'normal') => {
    try {
      store.setLoading(true);
      
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      const { data, error } = await supabase
        .from('requests')
        .insert({
          user_id: user.id,
          title,
          description,
          priority,
          status: 'queued'
        })
        .select()
        .single();

      if (error) throw error;
      
      store.addRequest(data);
      return data;
    } catch (err: any) {
      console.error('Error creating request:', err);
      store.setError(err.message);
      throw err;
    } finally {
      store.setLoading(false);
    }
  };

  const updateRequestStatus = async (id: string, status: Request['status']) => {
    try {
      const { error } = await supabase
        .from('requests')
        .update({ status })
        .eq('id', id);

      if (error) throw error;
      
      store.updateRequest(id, { status });
    } catch (err: any) {
      console.error('Error updating request:', err);
      store.setError(err.message);
    }
  };

  const deleteRequest = async (id: string) => {
    try {
      const { error } = await supabase
        .from('requests')
        .delete()
        .eq('id', id);

      if (error) throw error;
      
      store.deleteRequest(id);
    } catch (err: any) {
      console.error('Error deleting request:', err);
      store.setError(err.message);
    }
  };

  return {
    ...store,
    fetchRequests,
    createRequest,
    updateRequestStatus,
    deleteRequest,
  };
}
