/**
 * ALSHAM QUANTUM - Realtime Agents Hook
 * Real-time subscription for agents table
 */

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import type { RealtimeChannel } from '@supabase/supabase-js';

export interface Agent {
  id: string;
  name: string;
  role: string;
  status: string;
  efficiency: number;
  current_task: string;
  last_active: string;
  created_at: string;
  updated_at: string;
}

export function useRealtimeAgents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let channel: RealtimeChannel;

    async function setupRealtimeSubscription() {
      try {
        // Initial fetch
        const { data, error: fetchError } = await supabase
          .from('agents')
          .select('*')
          .order('name', { ascending: true });

        if (fetchError) {
          throw fetchError;
        }

        setAgents(data || []);
        setLoading(false);

        // Setup realtime subscription
        channel = supabase
          .channel('agents-channel')
          .on(
            'postgres_changes',
            {
              event: '*', // Listen to all events (INSERT, UPDATE, DELETE)
              schema: 'public',
              table: 'agents',
            },
            (payload) => {
              console.log('🔄 Agent change detected:', payload);

              if (payload.eventType === 'INSERT') {
                setAgents((prev) => [...prev, payload.new as Agent]);
              } else if (payload.eventType === 'UPDATE') {
                setAgents((prev) =>
                  prev.map((agent) =>
                    agent.id === payload.new.id ? (payload.new as Agent) : agent
                  )
                );
              } else if (payload.eventType === 'DELETE') {
                setAgents((prev) =>
                  prev.filter((agent) => agent.id !== payload.old.id)
                );
              }
            }
          )
          .subscribe((status) => {
            console.log('📡 Agents subscription status:', status);
          });

      } catch (err) {
        console.error('❌ Realtime agents error:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
        setLoading(false);
      }
    }

    setupRealtimeSubscription();

    // Cleanup subscription on unmount
    return () => {
      if (channel) {
        supabase.removeChannel(channel);
      }
    };
  }, []);

  return { agents, loading, error };
}
