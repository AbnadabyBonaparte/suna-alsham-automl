// frontend/src/components/ui/ThemeSwitcher.tsx
// Reality Codex - Theme Switcher Component
// Source: ALSHAM_QUANTUM_REALIDADES_VISUAIS_ULTIMATE_v3.md

'use client';

import React, { useState } from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { THEMES, getEnabledThemes } from '@/types/theme';
import { trackThemeChange, trackThemeSwitcherOpen } from '@/lib/analytics';

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  
  const enabledThemes = getEnabledThemes();
  const currentTheme = THEMES[theme];

  const handleOpen = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      trackThemeSwitcherOpen();
    }
  };

  const handleThemeSelect = (themeId: string) => {
    const selectedTheme = THEMES[themeId as keyof typeof THEMES];
    setTheme(themeId as any);
    trackThemeChange(themeId, selectedTheme.name);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      {/* Trigger Button */}
      <button
        onClick={handleOpen}
        className="flex items-center gap-2 px-3 py-2 rounded-lg transition-all duration-300"
        style={{
          background: 'var(--button-bg)',
          border: '1px solid var(--border)',
          color: 'var(--text-primary)',
        }}
        aria-label="Trocar tema"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <span className="text-lg">{currentTheme.icon}</span>
        <span className="text-sm font-medium hidden sm:inline">
          {currentTheme.name}
        </span>
        <svg
          className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Menu */}
          <div
            className="absolute right-0 mt-2 w-64 rounded-xl overflow-hidden z-50"
            style={{
              background: 'var(--dropdown-bg)',
              border: '1px solid var(--border)',
              boxShadow: 'var(--shadow-lg)',
              backdropFilter: 'var(--backdrop-blur)',
            }}
            role="listbox"
            aria-label="Selecionar tema"
          >
            <div className="p-2">
              <div 
                className="px-3 py-2 text-xs font-semibold uppercase tracking-wider"
                style={{ color: 'var(--text-muted)' }}
              >
                Realidades Visuais
              </div>
              
              {enabledThemes.map((t) => (
                <button
                  key={t.id}
                  onClick={() => handleThemeSelect(t.id)}
                  className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200 ${
                    theme === t.id ? 'ring-2' : ''
                  }`}
                  style={{
                    background: theme === t.id ? 'var(--accent-subtle)' : 'transparent',
                    ringColor: theme === t.id ? 'var(--accent)' : 'transparent',
                  }}
                  role="option"
                  aria-selected={theme === t.id}
                >
                  <span className="text-2xl">{t.icon}</span>
                  <div className="flex-1 text-left">
                    <div 
                      className="font-medium"
                      style={{ color: 'var(--text-primary)' }}
                    >
                      {t.name}
                    </div>
                    <div 
                      className="text-xs"
                      style={{ color: 'var(--text-muted)' }}
                    >
                      {t.description}
                    </div>
                  </div>
                  {theme === t.id && (
                    <svg 
                      className="w-5 h-5" 
                      fill="currentColor" 
                      viewBox="0 0 20 20"
                      style={{ color: 'var(--accent)' }}
                    >
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              ))}
            </div>
            
            {/* Keyboard hint */}
            <div 
              className="px-4 py-2 text-xs border-t"
              style={{ 
                color: 'var(--text-muted)',
                borderColor: 'var(--border-subtle)',
                background: 'var(--bg-panel)',
              }}
            >
              <kbd className="px-1 rounded" style={{ background: 'var(--bg-elevated)' }}>Alt</kbd>
              {' + '}
              <kbd className="px-1 rounded" style={{ background: 'var(--bg-elevated)' }}>Shift</kbd>
              {' + '}
              <kbd className="px-1 rounded" style={{ background: 'var(--bg-elevated)' }}>T</kbd>
              {' para alternar'}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default ThemeSwitcher;
