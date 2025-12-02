/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - LOADING STATE STORE
 * ═══════════════════════════════════════════════════════════════
 * Global loading state management with Zustand + DevTools
 * ═══════════════════════════════════════════════════════════════
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface LoadingState {
  [key: string]: boolean;
}

interface LoadingStore {
  loadingStates: LoadingState;
  isLoading: (key: string) => boolean;
  setLoading: (key: string, loading: boolean) => void;
  clearLoading: (key: string) => void;
  clearAll: () => void;
}

export const useLoadingStore = create<LoadingStore>()(
  devtools(
    (set, get) => ({
      loadingStates: {},

      isLoading: (key) => get().loadingStates[key] ?? false,

      setLoading: (key, loading) =>
        set(
          (state) => ({
            loadingStates: {
              ...state.loadingStates,
              [key]: loading,
            },
          }),
          false,
          `SET_LOADING_${key.toUpperCase()}`
        ),

      clearLoading: (key) =>
        set(
          (state) => {
            const newState = { ...state.loadingStates };
            delete newState[key];
            return { loadingStates: newState };
          },
          false,
          `CLEAR_LOADING_${key.toUpperCase()}`
        ),

      clearAll: () =>
        set(
          { loadingStates: {} },
          false,
          'CLEAR_ALL_LOADING'
        ),
    }),
    { name: 'LoadingStore' }
  )
);
