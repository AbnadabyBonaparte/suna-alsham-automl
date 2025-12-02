/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SALES STORE
 * ═══════════════════════════════════════════════════════════════
 * Enterprise-grade Zustand store for sales deals
 * ═══════════════════════════════════════════════════════════════
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface Deal {
  id: string;
  user_id: string;
  client_name: string;
  value: number;
  status: 'lead' | 'negotiation' | 'closed_won' | 'closed_lost';
  probability: number; // 0-100
  expected_close_date?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface SalesStats {
  total_deals: number;
  total_value: number;
  won_value: number;
  lost_value: number;
  in_progress_value: number;
  conversion_rate: number;
  avg_deal_value: number;
}

interface SalesStore {
  deals: Deal[];
  stats: SalesStats;
  loading: boolean;
  error: string | null;

  setDeals: (deals: Deal[]) => void;
  setStats: (stats: SalesStats) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  addDeal: (deal: Deal) => void;
  updateDeal: (id: string, updates: Partial<Deal>) => void;
  removeDeal: (id: string) => void;
}

export const useSalesStore = create<SalesStore>()(
  devtools(
    (set) => ({
      deals: [],
      stats: {
        total_deals: 0,
        total_value: 0,
        won_value: 0,
        lost_value: 0,
        in_progress_value: 0,
        conversion_rate: 0,
        avg_deal_value: 0,
      },
      loading: false,
      error: null,

      setDeals: (deals) =>
        set(
          { deals },
          false,
          'SET_DEALS'
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

      addDeal: (deal) =>
        set(
          (state) => ({
            deals: [...state.deals, deal],
          }),
          false,
          'ADD_DEAL'
        ),

      updateDeal: (id, updates) =>
        set(
          (state) => ({
            deals: state.deals.map((deal) =>
              deal.id === id ? { ...deal, ...updates } : deal
            ),
          }),
          false,
          'UPDATE_DEAL'
        ),

      removeDeal: (id) =>
        set(
          (state) => ({
            deals: state.deals.filter((deal) => deal.id !== id),
          }),
          false,
          'REMOVE_DEAL'
        ),
    }),
    { name: 'SalesStore' }
  )
);
