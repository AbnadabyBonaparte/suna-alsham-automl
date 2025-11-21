"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface Theme {
  name: string;
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  particles: string;
  textPrimary: string;
  textSecondary: string;
  cardBg: string;
  cardBorder: string;
}

export const themes: Record<string, Theme> = {
  quantumVoid: {
    name: "Quantum Void",
    primary: "#6C3483",
    secondary: "#9c27b0",
    accent: "#F4D03F",
    background: "linear-gradient(135deg, #020C1B 0%, #1a0033 50%, #330066 100%)",
    particles: "#9c27b0",
    textPrimary: "#FFFFFF",
    textSecondary: "#B8B8D1",
    cardBg: "rgba(108, 52, 131, 0.1)",
    cardBorder: "rgba(156, 39, 176, 0.3)"
  },
  luxuryGlass: {
    name: "Luxury Glass",
    primary: "#F4D03F",
    secondary: "#2ECC71",
    accent: "#6C3483",
    background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
    particles: "#F4D03F",
    textPrimary: "#FFFFFF",
    textSecondary: "#E8E8E8",
    cardBg: "rgba(244, 208, 63, 0.05)",
    cardBorder: "rgba(244, 208, 63, 0.3)"
  },
  neuralTwilight: {
    name: "Neural Twilight",
    primary: "#1F618D",
    secondary: "#3f51b5",
    accent: "#2196f3",
    background: "linear-gradient(135deg, #1a237e 0%, #283593 50%, #3f51b5 100%)",
    particles: "#2196f3",
    textPrimary: "#FFFFFF",
    textSecondary: "#C5CAE9",
    cardBg: "rgba(33, 150, 243, 0.1)",
    cardBorder: "rgba(63, 81, 181, 0.3)"
  },
  cyberAurora: {
    name: "Cyber Aurora",
    primary: "#2ECC71",
    secondary: "#00f5ff",
    accent: "#1de9b6",
    background: "linear-gradient(135deg, #004d40 0%, #00695c 50%, #00796b 100%)",
    particles: "#00f5ff",
    textPrimary: "#FFFFFF",
    textSecondary: "#B2DFDB",
    cardBg: "rgba(0, 245, 255, 0.1)",
    cardBorder: "rgba(29, 233, 182, 0.3)"
  },
  transcendentalLight: {
    name: "Transcendental Light",
    primary: "#6C3483",
    secondary: "#1F618D",
    accent: "#F4D03F",
    background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%, #667eea 100%)",
    particles: "#667eea",
    textPrimary: "#1a1a2e",
    textSecondary: "#4a5568",
    cardBg: "rgba(255, 255, 255, 0.6)",
    cardBorder: "rgba(102, 126, 234, 0.3)"
  }
};

interface ThemeContextType {
  currentTheme: string;
  theme: Theme;
  setTheme: (themeName: string) => void;
  availableThemes: string[];
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [currentTheme, setCurrentTheme] = useState<string>('quantumVoid');

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('suna-theme');
    if (savedTheme && themes[savedTheme]) {
      setCurrentTheme(savedTheme);
    }
  }, []);

  // Apply theme to document
  useEffect(() => {
    const theme = themes[currentTheme];
    const root = document.documentElement;

    // Apply CSS variables
    root.style.setProperty('--theme-primary', theme.primary);
    root.style.setProperty('--theme-secondary', theme.secondary);
    root.style.setProperty('--theme-accent', theme.accent);
    root.style.setProperty('--theme-particles', theme.particles);
    root.style.setProperty('--theme-text-primary', theme.textPrimary);
    root.style.setProperty('--theme-text-secondary', theme.textSecondary);
    root.style.setProperty('--theme-card-bg', theme.cardBg);
    root.style.setProperty('--theme-card-border', theme.cardBorder);

    // Apply background gradient
    document.body.style.background = theme.background;
    document.body.style.backgroundAttachment = 'fixed';

    // Save to localStorage
    localStorage.setItem('suna-theme', currentTheme);
  }, [currentTheme]);

  const setTheme = (themeName: string) => {
    if (themes[themeName]) {
      setCurrentTheme(themeName);
    }
  };

  const value: ThemeContextType = {
    currentTheme,
    theme: themes[currentTheme],
    setTheme,
    availableThemes: Object.keys(themes)
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
