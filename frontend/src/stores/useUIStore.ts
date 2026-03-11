import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { ThemeId, ThemeConfig, THEMES, DEFAULT_THEME, THEME_ORDER } from '@/types/theme';

const TRANSITION_DURATION = 800;

declare global {
  interface Document {
    startViewTransition?: (callback: () => void) => {
      finished: Promise<void>;
      ready: Promise<void>;
      updateCallbackDone: Promise<void>;
    };
  }
}

function applyThemeToDOM(themeId: ThemeId): void {
  if (typeof document === 'undefined') return;
  const theme = THEMES[themeId];
  if (!theme) return;

  const root = document.documentElement;

  Object.entries(theme.colors).forEach(([key, value]) => {
    root.style.setProperty(`--color-${key}`, value);
  });

  root.setAttribute('data-theme', themeId);
  root.classList.add('theme-transition');
  setTimeout(() => root.classList.remove('theme-transition'), TRANSITION_DURATION);
}

interface UIStore {
  currentTheme: ThemeId;
  themeConfig: ThemeConfig;
  isTransitioning: boolean;
  soundEnabled: boolean;
  sidebarOpen: boolean;
  reducedMotion: boolean;

  setTheme: (theme: ThemeId) => void;
  cycleTheme: () => void;
  setSoundEnabled: (enabled: boolean) => void;
  toggleSidebar: () => void;
  setReducedMotion: (reduced: boolean) => void;
  applyTheme: () => void;
}

export const useUIStore = create<UIStore>()(
  devtools(
    persist(
      (set, get) => ({
        currentTheme: DEFAULT_THEME,
        themeConfig: THEMES[DEFAULT_THEME],
        isTransitioning: false,
        soundEnabled: true,
        sidebarOpen: true,
        reducedMotion: false,

        setTheme: (theme: ThemeId) => {
          if (!THEMES[theme]) return;

          set({ isTransitioning: true }, false, 'ui/setTheme:start');

          const applyUpdate = () => {
            applyThemeToDOM(theme);
            set(
              { currentTheme: theme, themeConfig: THEMES[theme] },
              false,
              'ui/setTheme:apply',
            );
          };

          if (typeof document !== 'undefined' && document.startViewTransition) {
            document.startViewTransition(applyUpdate);
          } else {
            applyUpdate();
          }

          setTimeout(() => {
            set({ isTransitioning: false }, false, 'ui/setTheme:end');
          }, TRANSITION_DURATION);

          if (typeof window !== 'undefined' && (window as Record<string, unknown>).gtag) {
            (window as Record<string, unknown> & { gtag: (...args: unknown[]) => void }).gtag(
              'event',
              'theme_change',
              { theme_name: theme },
            );
          }
        },

        cycleTheme: () => {
          const { currentTheme } = get();
          const currentIndex = THEME_ORDER.indexOf(currentTheme);
          const nextIndex = (currentIndex + 1) % THEME_ORDER.length;
          get().setTheme(THEME_ORDER[nextIndex]);
        },

        setSoundEnabled: (enabled: boolean) => {
          set({ soundEnabled: enabled }, false, 'ui/setSoundEnabled');
        },

        toggleSidebar: () => {
          set(
            (state) => ({ sidebarOpen: !state.sidebarOpen }),
            false,
            'ui/toggleSidebar',
          );
        },

        setReducedMotion: (reduced: boolean) => {
          set({ reducedMotion: reduced }, false, 'ui/setReducedMotion');
        },

        applyTheme: () => {
          applyThemeToDOM(get().currentTheme);
        },
      }),
      {
        name: 'alsham-ui-storage',
        partialize: (state) => ({
          currentTheme: state.currentTheme,
          soundEnabled: state.soundEnabled,
          sidebarOpen: state.sidebarOpen,
          reducedMotion: state.reducedMotion,
        }),
        onRehydrateStorage: () => (state) => {
          if (state) {
            state.themeConfig = THEMES[state.currentTheme] ?? THEMES[DEFAULT_THEME];
            applyThemeToDOM(state.currentTheme);
          }
        },
      },
    ),
    { name: 'UIStore' },
  ),
);
