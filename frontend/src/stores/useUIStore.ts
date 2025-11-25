import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIStore {
  sidebarOpen: boolean;
  currentTheme: string;
  soundEnabled: boolean;
  reducedMotion: boolean;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setTheme: (theme: string) => void;
  toggleSound: () => void;
  setReducedMotion: (reduced: boolean) => void;
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      currentTheme: 'ascension',
      soundEnabled: true,
      reducedMotion: false,
      
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setTheme: (theme) => set({ currentTheme: theme }),
      toggleSound: () => set((state) => ({ soundEnabled: !state.soundEnabled })),
      setReducedMotion: (reduced) => set({ reducedMotion: reduced }),
    }),
    {
      name: 'alsham-ui-storage',
    }
  )
);
