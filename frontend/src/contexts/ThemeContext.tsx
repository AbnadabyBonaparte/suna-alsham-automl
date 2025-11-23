// frontend/src/contexts/ThemeContext.tsx
// Reality Codex - Theme Context Provider

'use client';

import React, { 
  createContext, 
  useContext, 
  useState, 
  useEffect, 
  useCallback,
  ReactNode 
} from 'react';
import { ThemeId, THEMES, DEFAULT_THEME, getEnabledThemes } from '@/types/theme';

interface ThemeContextType {
  theme: ThemeId;
  setTheme: (theme: ThemeId) => void;
  toggleTheme: () => void;
  availableThemes: typeof THEMES;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const STORAGE_KEY = 'alsham-quantum-theme';

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<ThemeId>(DEFAULT_THEME);
  const [mounted, setMounted] = useState(false);
  
  // Load theme from localStorage
  useEffect(() => {
    setMounted(true);
    
    try {
      const savedTheme = localStorage.getItem(STORAGE_KEY) as ThemeId | null;
      if (savedTheme && THEMES[savedTheme]?.enabled) {
        setThemeState(savedTheme);
        document.documentElement.setAttribute('data-theme', savedTheme);
      } else {
        document.documentElement.setAttribute('data-theme', DEFAULT_THEME);
      }
    } catch (e) {
      console.warn('Failed to load theme from localStorage:', e);
    }
  }, []);
  
  // Save theme to localStorage and update DOM
  const setTheme = useCallback((newTheme: ThemeId) => {
    if (!THEMES[newTheme]?.enabled) return;
    
    setThemeState(newTheme);
    localStorage.setItem(STORAGE_KEY, newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  }, []);
  
  // Toggle between enabled themes
  const toggleTheme = useCallback(() => {
    const enabledThemes = getEnabledThemes();
    const currentIndex = enabledThemes.findIndex(t => t.id === theme);
    const nextIndex = (currentIndex + 1) % enabledThemes.length;
    setTheme(enabledThemes[nextIndex].id);
  }, [theme, setTheme]);
  
  // Keyboard shortcuts
  useEffect(() => {
    const handleKeydown = (e: KeyboardEvent) => {
      // Alt+Shift+T = Toggle
      if (e.altKey && e.shiftKey && e.key.toLowerCase() === 't') {
        e.preventDefault();
        toggleTheme();
        return;
      }
      
      // Alt+1-5 = Specific theme
      if (e.altKey && !e.shiftKey && !e.ctrlKey) {
        const num = parseInt(e.key);
        if (num >= 1 && num <= 5) {
          const themeIds: ThemeId[] = ['quantum', 'ascension', 'military', 'neural', 'titanium'];
          const targetTheme = themeIds[num - 1];
          
          if (THEMES[targetTheme]?.enabled) {
            e.preventDefault();
            setTheme(targetTheme);
          }
        }
      }
    };
    
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  }, [toggleTheme, setTheme]);
  
  // Prevent flash of wrong theme
  if (!mounted) {
    return null;
  }
  
  return (
    <ThemeContext.Provider 
      value={{ 
        theme, 
        setTheme, 
        toggleTheme, 
        availableThemes: THEMES 
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
