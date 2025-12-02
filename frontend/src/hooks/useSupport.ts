/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SUPPORT HOOK
 * ═══════════════════════════════════════════════════════════════
 * Custom hook for support tickets data fetching
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useSupportStore, type SupportTicket, type SupportStats } from '@/stores/useSupportStore';
import { useNotificationStore } from '@/stores/useNotificationStore';

export function useSupport() {
  const {
    tickets,
    stats,
    loading,
    error,
    setTickets,
    setStats,
    setLoading,
    setError
  } = useSupportStore();
  const { addNotification } = useNotificationStore();

  // Fetch tickets from Supabase
  const fetchTickets = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('support_tickets')
        .select('*')
        .order('created_at', { ascending: false });

      if (fetchError) throw fetchError;

      const ticketsData = (data || []) as SupportTicket[];
      setTickets(ticketsData);

      // Calculate stats
      const calculatedStats: SupportStats = {
        total: ticketsData.length,
        open: ticketsData.filter(t => t.status === 'open').length,
        in_progress: ticketsData.filter(t => t.status === 'in_progress').length,
        resolved: ticketsData.filter(t => t.status === 'resolved').length,
        closed: ticketsData.filter(t => t.status === 'closed').length,
        avg_sentiment: ticketsData.length > 0
          ? ticketsData.reduce((sum, t) => sum + t.sentiment, 0) / ticketsData.length
          : 0,
        critical_count: ticketsData.filter(t => t.priority === 'critical').length,
      };

      setStats(calculatedStats);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch support tickets';
      setError(errorMessage);
      addNotification({
        type: 'error',
        title: 'Error fetching tickets',
        message: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  // Create new ticket
  const createTicket = async (ticket: Omit<SupportTicket, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      setLoading(true);

      const { data, error: createError } = await supabase
        .from('support_tickets')
        .insert([ticket])
        .select()
        .single();

      if (createError) throw createError;

      addNotification({
        type: 'success',
        title: 'Ticket created',
        message: 'Support ticket created successfully',
      });

      await fetchTickets(); // Refresh list
      return data as SupportTicket;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create ticket';
      addNotification({
        type: 'error',
        title: 'Error creating ticket',
        message: errorMessage,
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Update ticket
  const updateTicket = async (id: string, updates: Partial<SupportTicket>) => {
    try {
      setLoading(true);

      const { error: updateError } = await supabase
        .from('support_tickets')
        .update(updates)
        .eq('id', id);

      if (updateError) throw updateError;

      addNotification({
        type: 'success',
        title: 'Ticket updated',
        message: 'Support ticket updated successfully',
      });

      await fetchTickets(); // Refresh list
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update ticket';
      addNotification({
        type: 'error',
        title: 'Error updating ticket',
        message: errorMessage,
      });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Auto-fetch on mount
  useEffect(() => {
    fetchTickets();
  }, []);

  return {
    tickets,
    stats,
    loading,
    error,
    fetchTickets,
    createTicket,
    updateTicket,
  };
}
