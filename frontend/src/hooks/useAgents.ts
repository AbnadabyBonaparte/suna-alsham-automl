/**
 * Hook para gerenciar agents com Zustand store
 */
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useAgentsStore } from '@/stores/useAgentsStore';

export function useAgents() {
  const store = useAgentsStore();

  useEffect(() => {
    async function fetchAgents() {
      // Só buscar se store estiver vazia
      if (store.agents.length > 0) return;

      try {
        store.setLoading(true);
        
        const { data, error } = await supabase
          .from('agents')
          .select('*')
          .order('created_at', { ascending: true });

        if (error) {
          console.error('Error fetching agents:', error);
          store.setError(error.message);
        } else if (data && data.length > 0) {
          // Normalizar dados
          const normalizedData = data.map((agent: any) => ({
            ...agent,
            currentTask: agent.current_task || 'Aguardando comando',
          }));
          store.setAgents(normalizedData);
        }
      } catch (err: any) {
        console.error('Failed to fetch agents:', err);
        store.setError(err.message);
      } finally {
        store.setLoading(false);
      }
    }

    fetchAgents();
  }, []);

  return store;
}
