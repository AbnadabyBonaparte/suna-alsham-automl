import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { User, Session, AuthError } from '@supabase/supabase-js';
import { createClient } from '@/lib/supabase/client';

const FOUNDER_EMAIL = 'casamondestore@gmail.com';

interface UserMetadata {
  founder_access?: boolean;
  subscription_plan?: string;
  subscription_status?: string;
  onboarding_completed?: boolean;
}

interface AuthStore {
  user: User | null;
  session: Session | null;
  metadata: UserMetadata | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  hasFounderAccess: () => boolean;
  hasAccess: () => boolean;
  getUserId: () => string | null;
  getUserEmail: () => string | null;

  setUser: (user: User | null) => void;
  setSession: (session: Session | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;

  signIn: (email: string, password: string) => Promise<{ error: AuthError | null }>;
  signUp: (email: string, password: string) => Promise<{ error: AuthError | null }>;
  signOut: () => Promise<void>;
  refreshMetadata: () => Promise<void>;
  initAuth: () => () => void;
}

async function loadUserMetadata(userId: string): Promise<UserMetadata | null> {
  try {
    const supabase = createClient();
    const { data, error } = await supabase
      .from('profiles')
      .select('subscription_plan, subscription_status, founder_access, onboarding_completed')
      .eq('id', userId)
      .single();

    if (error) {
      console.error('Erro ao carregar metadata:', error);
      return null;
    }

    return data;
  } catch (err) {
    console.error('Erro ao carregar metadata:', err);
    return null;
  }
}

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        session: null,
        metadata: null,
        isAuthenticated: false,
        isLoading: true,
        error: null,

        hasFounderAccess: () => {
          const { user, metadata } = get();
          return user?.email === FOUNDER_EMAIL || metadata?.founder_access === true;
        },

        hasAccess: () => {
          const state = get();
          if (state.hasFounderAccess()) return true;
          const m = state.metadata;
          return (
            (m?.subscription_plan === 'enterprise' && m?.subscription_status === 'active') ||
            m?.subscription_status === 'active'
          );
        },

        getUserId: () => get().user?.id ?? null,
        getUserEmail: () => get().user?.email ?? null,

        setUser: (user) =>
          set({ user, isAuthenticated: !!user }, false, 'auth/setUser'),

        setSession: (session) =>
          set({ session }, false, 'auth/setSession'),

        setLoading: (loading) =>
          set({ isLoading: loading }, false, 'auth/setLoading'),

        setError: (error) =>
          set({ error }, false, 'auth/setError'),

        signIn: async (email, password) => {
          try {
            const supabase = createClient();

            const { error } = await supabase.auth.signInWithPassword({
              email,
              password,
            });

            if (error) {
              return { error };
            }

            window.location.href = '/dashboard';

            return { error: null };
          } catch (err: unknown) {
            const message =
              err instanceof Error ? err.message : 'Erro ao fazer login. Verifique suas credenciais.';
            return {
              error: { message, status: 500 } as AuthError,
            };
          }
        },

        signUp: async (email, password) => {
          try {
            const supabase = createClient();

            const { error } = await supabase.auth.signUp({
              email,
              password,
            });

            if (!error) {
              window.location.href = '/onboarding';
            }

            return { error };
          } catch (err: unknown) {
            const message =
              err instanceof Error ? err.message : 'Erro ao criar conta.';
            return {
              error: { message, status: 500 } as AuthError,
            };
          }
        },

        signOut: async () => {
          try {
            const supabase = createClient();
            await supabase.auth.signOut();
            set(
              {
                user: null,
                session: null,
                metadata: null,
                isAuthenticated: false,
              },
              false,
              'auth/signOut',
            );
            window.location.href = '/login';
          } catch (err) {
            console.error('Erro ao fazer logout:', err);
          }
        },

        refreshMetadata: async () => {
          const { user } = get();
          if (!user) return;
          const metadata = await loadUserMetadata(user.id);
          set({ metadata }, false, 'auth/refreshMetadata');
        },

        initAuth: () => {
          const supabase = createClient();

          const handleAuthChange = async (
            _event: string,
            session: Session | null,
          ) => {
            set(
              {
                session,
                user: session?.user ?? null,
                isAuthenticated: !!session?.user,
              },
              false,
              'auth/authChange',
            );

            if (session?.user) {
              const metadata = await loadUserMetadata(session.user.id);
              set({ metadata, isLoading: false }, false, 'auth/metadataLoaded');
            } else {
              set({ metadata: null, isLoading: false }, false, 'auth/noUser');
            }
          };

          supabase.auth.getSession().then(async ({ data: { session } }) => {
            await handleAuthChange('INITIAL_SESSION', session);
          });

          const {
            data: { subscription },
          } = supabase.auth.onAuthStateChange(handleAuthChange);

          return () => subscription.unsubscribe();
        },
      }),
      {
        name: 'alsham-auth-storage',
        partialize: (state) => ({
          user: state.user,
          session: state.session,
          isAuthenticated: state.isAuthenticated,
        }),
      },
    ),
    { name: 'AuthStore' },
  ),
);
