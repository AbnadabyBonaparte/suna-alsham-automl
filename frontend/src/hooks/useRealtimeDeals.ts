/**
 * ALSHAM QUANTUM - Realtime Deals Hook
 * Real-time subscription for deals table (sales pipeline)
 */

import { useState, useEffect, useMemo } from 'react';
import { createClient } from '@/lib/supabase/client';
import type { RealtimeChannel } from '@supabase/supabase-js';

export interface Deal {
  id: string;
  title: string;
  client_name: string;
  value: number;
  probability: number;
  status: 'lead' | 'negotiation' | 'closed_won' | 'closed_lost';
  expected_close_date: string;
  stage: 'discovery' | 'qualification' | 'proposal' | 'negotiation' | 'closed';
  contact_email: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

interface UseRealtimeDealsOptions {
  onNewDeal?: (deal: Deal) => void;
  onDealUpdate?: (deal: Deal) => void;
  onDealClosed?: (deal: Deal) => void;
}

export function useRealtimeDeals(options: UseRealtimeDealsOptions = {}) {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const supabase = useMemo(() => createClient(), []);

  useEffect(() => {
    let channel: RealtimeChannel;

    async function setupRealtimeSubscription() {
      try {
        // Initial fetch
        const { data, error: fetchError } = await supabase
          .from('deals')
          .select('*')
          .order('expected_close_date', { ascending: true });

        if (fetchError) {
          throw fetchError;
        }

        setDeals(data || []);
        setLoading(false);

        // Setup realtime subscription
        channel = supabase
          .channel('deals-channel')
          .on(
            'postgres_changes',
            {
              event: '*',
              schema: 'public',
              table: 'deals',
            },
            (payload) => {
              console.log('💰 Deal change detected:', payload);

              if (payload.eventType === 'INSERT') {
                const newDeal = payload.new as Deal;
                setDeals((prev) => [...prev, newDeal]);

                // Call callback if provided
                if (options.onNewDeal) {
                  options.onNewDeal(newDeal);
                }
              } else if (payload.eventType === 'UPDATE') {
                const updatedDeal = payload.new as Deal;
                setDeals((prev) =>
                  prev.map((deal) =>
                    deal.id === updatedDeal.id ? updatedDeal : deal
                  )
                );

                // Check if deal was just closed
                const oldDeal = payload.old as Deal;
                const wasClosed =
                  (updatedDeal.status === 'closed_won' || updatedDeal.status === 'closed_lost') &&
                  oldDeal.status !== updatedDeal.status;

                // Call callbacks
                if (options.onDealUpdate) {
                  options.onDealUpdate(updatedDeal);
                }

                if (wasClosed && options.onDealClosed) {
                  options.onDealClosed(updatedDeal);
                }
              } else if (payload.eventType === 'DELETE') {
                setDeals((prev) =>
                  prev.filter((deal) => deal.id !== payload.old.id)
                );
              }
            }
          )
          .subscribe((status) => {
            console.log('📡 Deals subscription status:', status);
          });

      } catch (err) {
        console.error('❌ Realtime deals error:', err);
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
  }, [supabase, options.onNewDeal, options.onDealUpdate, options.onDealClosed]);

  // Helper to calculate pipeline value by stage
  const getPipelineByStage = () => {
    return deals.reduce((acc, deal) => {
      const stage = deal.stage;
      if (!acc[stage]) {
        acc[stage] = { count: 0, totalValue: 0, weightedValue: 0 };
      }
      acc[stage].count++;
      acc[stage].totalValue += deal.value;
      acc[stage].weightedValue += deal.value * (deal.probability / 100);
      return acc;
    }, {} as Record<string, { count: number; totalValue: number; weightedValue: number }>);
  };

  // Helper to get deals by status
  const getDealsByStatus = (status: Deal['status']) => {
    return deals.filter((deal) => deal.status === status);
  };

  return {
    deals,
    loading,
    error,
    getPipelineByStage,
    getDealsByStatus,
  };
}
