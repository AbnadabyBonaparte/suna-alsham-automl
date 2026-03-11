import { useUIStore } from '@/stores/useUIStore';
import { useSoundEngine } from '@/hooks/useSoundEngine';
import type { ThemeId } from '@/types/theme';

export function useTheme() {
  const store = useUIStore();
  const soundEngine = useSoundEngine(store.themeConfig, {
    volume: 0.2,
    enabled: store.soundEnabled,
  });

  return {
    currentTheme: store.currentTheme,
    themeConfig: store.themeConfig,
    setTheme: (theme: ThemeId) => {
      soundEngine.playClick();
      store.setTheme(theme);
    },
    cycleTheme: () => {
      soundEngine.playClick();
      store.cycleTheme();
    },
    isTransitioning: store.isTransitioning,
    soundEnabled: store.soundEnabled,
    setSoundEnabled: store.setSoundEnabled,
    playClick: soundEngine.playClick,
    playHover: soundEngine.playHover,
    toggleAmbient: soundEngine.toggleAmbient,
  };
}
