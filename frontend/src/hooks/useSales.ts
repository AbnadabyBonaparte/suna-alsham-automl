/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SALES HOOK
 * ═══════════════════════════════════════════════════════════════
 * Custom hook for sales deals data fetching
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useSalesStore, type Deal, type SalesStats } from '@/stores/useSalesStore';
import { useNotificationStore } from '@/stores/useNotificationStore';

export function useSales() {
  const {
    deals,
    stats,
    loading,
    error,
    setDeals,
    setStats,
    setLoading,
    setError
  } = useSalesStore();
  const { addNotification } = useNotificationStore();

  // Fetch deals from Supabase
  const fetchDeals = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('deals')
        .select('*')
        .order('created_at', { ascending: false });

      if (fetchError) throw fetchError;

      const dealsData = (data || []) as Deal[];
      setDeals(dealsData);

      // Calculate stats
      const wonDeals = dealsData.filter(d => d.status === 'closed_won');
      const lostDeals = dealsData.filter(d => d.status === 'closed_lost');
      const inProgressDeals = dealsData.filter(d => d.status === 'negotiation' || d.status === 'lead');

      const totalValue = dealsData.reduce((sum, d) => sum + d.value, 0);
      const wonValue = wonDeals.reduce((sum, d) => sum + d.value, 0);
      const lostValue = lostDeals.reduce((sum, d) => sum + d.value, 0);
      const inProgressValue = inProgressDeals.reduce((sum, d) => sum + d.value, 0);

      const calculatedStats: SalesStats = {
        total_deals: dealsData.length,
        total_value: totalValue,
        won_value: wonValue,
        lost_value: lostValue,
        in_progress_value: inProgressValue,
        conversion_rate: dealsData.length > 0
          ? (wonDeals.length / dealsData.length) * 100
          : 0,
        avg_deal_value: dealsData.length > 0
          ? totalValue / dealsData.length
          : 0,
      };

      setStats(calculatedStats);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch deals';
      setError(errorMessage);
      addNotification({
        type: 'error',
        title: 'Error fetching deals',
        message: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  // Create new deal
  const createDeal = async (deal: Omit<Deal, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      setLoading(true);

      const { data, error: createError } = await supabase
        .from('deals')
        .insert([deal])
        .select()
        .single();

      if (createError) throw createError;

      addNotification({
        type: 'success',
        title: 'Deal created',
        message: 'Deal created successfully',
      });

      await fetchDeals(); // Refresh list
      return data as Deal;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create deal';
      addNotification({
        type: 'error',
        title: 'Error creating deal',
        message: errorMessage,
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Update deal
  const updateDeal = async (id: string, updates: Partial<Deal>) => {
    try {
      setLoading(true);

      const { error: updateError } = await supabase
        .from('deals')
        .update(updates)
        .eq('id', id);

      if (updateError) throw updateError;

      addNotification({
        type: 'success',
        title: 'Deal updated',
        message: 'Deal updated successfully',
      });

      await fetchDeals(); // Refresh list
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update deal';
      addNotification({
        type: 'error',
        title: 'Error updating deal',
        message: errorMessage,
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Auto-fetch on mount
  useEffect(() => {
    fetchDeals();
  }, []);

  return {
    deals,
    stats,
    loading,
    error,
    fetchDeals,
    createDeal,
    updateDeal,
  };
}
