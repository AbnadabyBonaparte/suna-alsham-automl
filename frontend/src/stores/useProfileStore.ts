/**
 * Profile Store - Zustand State Management
 * Manages user profile data with enterprise patterns
 */
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface Profile {
  id: string;
  username: string | null;
  full_name: string | null;
  avatar_url: string | null;
  created_at?: string;
  updated_at?: string;
}

interface ProfileStore {
  profile: Profile | null;
  loading: boolean;
  error: string | null;

  // Actions
  setProfile: (profile: Profile | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updateProfile: (updates: Partial<Profile>) => void;
  clearProfile: () => void;
}

export const useProfileStore = create<ProfileStore>()(
  devtools(
    (set) => ({
      profile: null,
      loading: false,
      error: null,

      setProfile: (profile) => set({ profile, error: null }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),

      updateProfile: (updates) =>
        set((state) => ({
          profile: state.profile ? { ...state.profile, ...updates } : null,
        })),

      clearProfile: () => set({ profile: null, error: null, loading: false }),
    }),
    { name: 'ProfileStore' }
  )
);
