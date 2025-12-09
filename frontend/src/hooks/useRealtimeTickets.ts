/**
 * ALSHAM QUANTUM - Realtime Support Tickets Hook
 * Real-time subscription for support_tickets table
 */

import { useState, useEffect, useMemo } from 'react';
import { createClient } from '@/lib/supabase/client';
import type { RealtimeChannel } from '@supabase/supabase-js';

export interface SupportTicket {
  id: string;
  title: string;
  description: string;
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  priority: 'low' | 'normal' | 'high' | 'critical';
  category: string;
  assigned_to: string | null;
  created_by: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

interface UseRealtimeTicketsOptions {
  onNewTicket?: (ticket: SupportTicket) => void;
  onTicketUpdate?: (ticket: SupportTicket) => void;
}

export function useRealtimeTickets(options: UseRealtimeTicketsOptions = {}) {
  const [tickets, setTickets] = useState<SupportTicket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const supabase = useMemo(() => createClient(), []);

  useEffect(() => {
    let channel: RealtimeChannel;

    async function setupRealtimeSubscription() {
      try {
        // Initial fetch
        const { data, error: fetchError } = await supabase
          .from('support_tickets')
          .select('*')
          .order('created_at', { ascending: false });

        if (fetchError) {
          throw fetchError;
        }

        setTickets(data || []);
        setLoading(false);

        // Setup realtime subscription
        channel = supabase
          .channel('support-tickets-channel')
          .on(
            'postgres_changes',
            {
              event: '*',
              schema: 'public',
              table: 'support_tickets',
            },
            (payload) => {
              console.log('🎫 Ticket change detected:', payload);

              if (payload.eventType === 'INSERT') {
                const newTicket = payload.new as SupportTicket;
                setTickets((prev) => [newTicket, ...prev]);

                // Call callback if provided
                if (options.onNewTicket) {
                  options.onNewTicket(newTicket);
                }
              } else if (payload.eventType === 'UPDATE') {
                const updatedTicket = payload.new as SupportTicket;
                setTickets((prev) =>
                  prev.map((ticket) =>
                    ticket.id === updatedTicket.id ? updatedTicket : ticket
                  )
                );

                // Call callback if provided
                if (options.onTicketUpdate) {
                  options.onTicketUpdate(updatedTicket);
                }
              } else if (payload.eventType === 'DELETE') {
                setTickets((prev) =>
                  prev.filter((ticket) => ticket.id !== payload.old.id)
                );
              }
            }
          )
          .subscribe((status) => {
            console.log('📡 Support tickets subscription status:', status);
          });

      } catch (err) {
        console.error('❌ Realtime tickets error:', err);
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
  }, [supabase, options.onNewTicket, options.onTicketUpdate]);

  return { tickets, loading, error };
}
