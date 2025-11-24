/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THEME CONTEXT PROVIDER (NÍVEL DEUS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/contexts/ThemeContext.tsx
 * 📋 Com Sound Engine + View Transitions API para experiência cinematográfica
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { ThemeId, ThemeConfig, THEMES, DEFAULT_THEME, THEME_ORDER } from '@/types/theme';
import { useSoundEngine } from '@/hooks/useSoundEngine';

interface ThemeContextType {
  currentTheme: ThemeId;
  themeConfig: ThemeConfig;
  setTheme: (theme: ThemeId) => void;
  cycleTheme: () => void;
  isTransitioning: boolean;
  // Sound controls
  playClick: () => void;
  playHover: () => void;
  toggleAmbient: (play: boolean) => void;
  soundEnabled: boolean;
  setSoundEnabled: (enabled: boolean) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const STORAGE_KEY = 'alsham_quantum_theme';
const SOUND_STORAGE_KEY = 'alsham_quantum_sound_enabled';
const TRANSITION_DURATION = 800; // ms

// Type augmentation para View Transitions API
declare global {
  interface Document {
    startViewTransition?: (callback: () => void) => {
      finished: Promise<void>;
      ready: Promise<void>;
      updateCallbackDone: Promise<void>;
    };
  }
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [currentTheme, setCurrentTheme] = useState<ThemeId>(DEFAULT_THEME);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Carregar preferência de som do localStorage
  const [soundEnabled, setSoundEnabledState] = useState(true);

  useEffect(() => {
    const savedSound = localStorage.getItem(SOUND_STORAGE_KEY);
    if (savedSound !== null) {
      setSoundEnabledState(savedSound === 'true');
    }
  }, []);

  // Inicializar Sound Engine
  const soundEngine = useSoundEngine(THEMES[currentTheme], { 
    volume: 0.2,
    enabled: soundEnabled 
  });

  // Função para alterar estado de som e salvar no localStorage
  const setSoundEnabled = useCallback((enabled: boolean) => {
    setSoundEnabledState(enabled);
    localStorage.setItem(SOUND_STORAGE_KEY, enabled.toString());
    soundEngine.setSoundEnabled(enabled);
  }, [soundEngine]);

  // Carregar tema salvo do localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem(STORAGE_KEY) as ThemeId;
    if (savedTheme && THEMES[savedTheme]) {
      setCurrentTheme(savedTheme);
    }
  }, []);

  // Aplicar CSS variables quando o tema mudar
  useEffect(() => {
    const theme = THEMES[currentTheme];
    const root = document.documentElement;

    // Aplicar cores
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value);
    });

    // Aplicar classe do tema
    root.setAttribute('data-theme', currentTheme);
    
    // Aplicar classe de transição
    root.classList.add('theme-transition');
    
    // Salvar no localStorage
    localStorage.setItem(STORAGE_KEY, currentTheme);

    // Remover classe de transição após animação
    const timeout = setTimeout(() => {
      root.classList.remove('theme-transition');
    }, TRANSITION_DURATION);

    return () => clearTimeout(timeout);
  }, [currentTheme]);

  /**
   * ═══════════════════════════════════════════════════════════════
   * 🎬 VIEW TRANSITIONS API - A TRANSIÇÃO CINEMATOGRÁFICA
   * ═══════════════════════════════════════════════════════════════
   */
  const setTheme = useCallback((theme: ThemeId) => {
    if (!THEMES[theme]) return;

    setIsTransitioning(true);

    // Tocar som de click ao trocar tema
    soundEngine.playClick();

    // Verificar se o navegador suporta View Transitions API
    if (typeof document !== 'undefined' && document.startViewTransition) {
      // Usar View Transitions para transição suave e cinematográfica
      document.startViewTransition(() => {
        setCurrentTheme(theme);
      });
    } else {
      // Fallback para navegadores antigos (apenas transição CSS)
      setCurrentTheme(theme);
    }
    
    setTimeout(() => {
      setIsTransitioning(false);
    }, TRANSITION_DURATION);

    // Analytics
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('event', 'theme_change', {
        theme_name: theme,
      });
    }
  }, [soundEngine]);

  const cycleTheme = useCallback(() => {
    const currentIndex = THEME_ORDER.indexOf(currentTheme);
    const nextIndex = (currentIndex + 1) % THEME_ORDER.length;
    setTheme(THEME_ORDER[nextIndex]);
  }, [currentTheme, setTheme]);

  const value: ThemeContextType = {
    currentTheme,
    themeConfig: THEMES[currentTheme],
    setTheme,
    cycleTheme,
    isTransitioning,
    // Sound engine methods
    playClick: soundEngine.playClick,
    playHover: soundEngine.playHover,
    toggleAmbient: soundEngine.toggleAmbient,
    soundEnabled,
    setSoundEnabled,
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
