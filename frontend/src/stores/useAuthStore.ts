import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { User, Session } from '@supabase/supabase-js';

interface AuthStore {
  user: User | null;
  session: Session | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setUser: (user: User | null) => void;
  setSession: (session: Session | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  logout: () => void;
  
  // Computed
  getUserId: () => string | null;
  getUserEmail: () => string | null;
}

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        session: null,
        isAuthenticated: false,
        isLoading: true,
        error: null,
        
        setUser: (user) => set({ 
          user, 
          isAuthenticated: !!user 
        }, false, 'auth/setUser'),
        
        setSession: (session) => set({ 
          session 
        }, false, 'auth/setSession'),
        
        setLoading: (loading) => set({ 
          isLoading: loading 
        }, false, 'auth/setLoading'),
        
        setError: (error) => set({ 
          error 
        }, false, 'auth/setError'),
        
        logout: () => set({ 
          user: null, 
          session: null, 
          isAuthenticated: false 
        }, false, 'auth/logout'),
        
        getUserId: () => get().user?.id ?? null,
        getUserEmail: () => get().user?.email ?? null,
      }),
      {
        name: 'alsham-auth-storage',
        partialize: (state) => ({ 
          user: state.user,
          session: state.session,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    ),
    { name: 'AuthStore' }
  )
);
