import { useUIStore } from '@/stores/useUIStore';
import { act } from '@testing-library/react';
import { THEMES, DEFAULT_THEME, THEME_ORDER } from '@/types/theme';

describe('useUIStore', () => {
  beforeEach(() => {
    useUIStore.setState({
      currentTheme: DEFAULT_THEME,
      themeConfig: THEMES[DEFAULT_THEME],
      isTransitioning: false,
      soundEnabled: true,
      sidebarOpen: true,
      reducedMotion: false,
    });
  });

  it('should have correct initial state', () => {
    const state = useUIStore.getState();
    expect(state.currentTheme).toBe(DEFAULT_THEME);
    expect(state.themeConfig).toEqual(THEMES[DEFAULT_THEME]);
    expect(state.isTransitioning).toBe(false);
    expect(state.soundEnabled).toBe(true);
    expect(state.sidebarOpen).toBe(true);
  });

  it('should set theme correctly', () => {
    act(() => {
      useUIStore.getState().setTheme('military');
    });

    const state = useUIStore.getState();
    expect(state.currentTheme).toBe('military');
    expect(state.themeConfig).toEqual(THEMES['military']);
  });

  it('should cycle through themes', () => {
    act(() => {
      useUIStore.getState().setTheme(THEME_ORDER[0]);
    });

    act(() => {
      useUIStore.getState().cycleTheme();
    });

    expect(useUIStore.getState().currentTheme).toBe(THEME_ORDER[1]);
  });

  it('should toggle sidebar', () => {
    expect(useUIStore.getState().sidebarOpen).toBe(true);
    
    act(() => {
      useUIStore.getState().toggleSidebar();
    });
    
    expect(useUIStore.getState().sidebarOpen).toBe(false);
    
    act(() => {
      useUIStore.getState().toggleSidebar();
    });
    
    expect(useUIStore.getState().sidebarOpen).toBe(true);
  });

  it('should toggle sound', () => {
    expect(useUIStore.getState().soundEnabled).toBe(true);
    
    act(() => {
      useUIStore.getState().setSoundEnabled(false);
    });
    
    expect(useUIStore.getState().soundEnabled).toBe(false);
  });

  it('should set reduced motion', () => {
    act(() => {
      useUIStore.getState().setReducedMotion(true);
    });
    
    expect(useUIStore.getState().reducedMotion).toBe(true);
  });

  it('should reject invalid theme ids', () => {
    const prevTheme = useUIStore.getState().currentTheme;
    
    act(() => {
      useUIStore.getState().setTheme('nonexistent' as any);
    });
    
    expect(useUIStore.getState().currentTheme).toBe(prevTheme);
  });
});
