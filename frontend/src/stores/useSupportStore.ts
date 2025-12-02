/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SUPPORT STORE
 * ═══════════════════════════════════════════════════════════════
 * Enterprise-grade Zustand store for support tickets
 * ═══════════════════════════════════════════════════════════════
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface SupportTicket {
  id: string;
  user_id: string;
  title: string;
  description: string;
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  priority: 'low' | 'normal' | 'high' | 'critical';
  sentiment: number; // 0-100
  assigned_to?: string;
  created_at: string;
  updated_at: string;
}

export interface SupportStats {
  total: number;
  open: number;
  in_progress: number;
  resolved: number;
  closed: number;
  avg_sentiment: number;
  critical_count: number;
}

interface SupportStore {
  tickets: SupportTicket[];
  stats: SupportStats;
  loading: boolean;
  error: string | null;

  setTickets: (tickets: SupportTicket[]) => void;
  setStats: (stats: SupportStats) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  addTicket: (ticket: SupportTicket) => void;
  updateTicket: (id: string, updates: Partial<SupportTicket>) => void;
  removeTicket: (id: string) => void;
}

export const useSupportStore = create<SupportStore>()(
  devtools(
    (set) => ({
      tickets: [],
      stats: {
        total: 0,
        open: 0,
        in_progress: 0,
        resolved: 0,
        closed: 0,
        avg_sentiment: 0,
        critical_count: 0,
      },
      loading: false,
      error: null,

      setTickets: (tickets) =>
        set(
          { tickets },
          false,
          'SET_TICKETS'
        ),

      setStats: (stats) =>
        set(
          { stats },
          false,
          'SET_STATS'
        ),

      setLoading: (loading) =>
        set(
          { loading },
          false,
          'SET_LOADING'
        ),

      setError: (error) =>
        set(
          { error },
          false,
          'SET_ERROR'
        ),

      addTicket: (ticket) =>
        set(
          (state) => ({
            tickets: [...state.tickets, ticket],
          }),
          false,
          'ADD_TICKET'
        ),

      updateTicket: (id, updates) =>
        set(
          (state) => ({
            tickets: state.tickets.map((ticket) =>
              ticket.id === id ? { ...ticket, ...updates } : ticket
            ),
          }),
          false,
          'UPDATE_TICKET'
        ),

      removeTicket: (id) =>
        set(
          (state) => ({
            tickets: state.tickets.filter((ticket) => ticket.id !== id),
          }),
          false,
          'REMOVE_TICKET'
        ),
    }),
    { name: 'SupportStore' }
  )
);
