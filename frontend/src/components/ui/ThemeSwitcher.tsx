/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THEME SWITCHER UI (7 UNIVERSOS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/ui/ThemeSwitcher.tsx
 * 📋 Interface visual para escolher entre 7 realidades + controle de som
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useState } from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { THEMES, THEME_ORDER } from '@/types/theme';
import { Palette, X, Sparkles, Volume2, VolumeX } from 'lucide-react';

export function ThemeSwitcher() {
  const { 
    currentTheme, 
    setTheme, 
    isTransitioning,
    soundEnabled,
    setSoundEnabled,
    playClick,
  } = useTheme();
  
  const [isOpen, setIsOpen] = useState(false);

  const handleThemeSelect = (themeId: string) => {
    setTheme(themeId as any);
    setTimeout(() => setIsOpen(false), 300);
  };

  const handleSoundToggle = () => {
    setSoundEnabled(!soundEnabled);
    playClick(); // Feedback imediato
  };

  return (
    <>
     {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-primary to-accent backdrop-blur-xl border-2 border-primary shadow-2xl shadow-primary/20 flex items-center justify-center transition-all hover:scale-110 hover:shadow-primary/40 z-[100]"
        title="Trocar Realidade Visual (Alt+Shift+T)"
        aria-label="Abrir seletor de temas"
      >
        <Palette className="w-6 h-6 text-white drop-shadow-lg" />
      </button>

      {/* Modal Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-[200] flex items-center justify-center p-4 animate-fadeIn"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="bg-surface border border-border rounded-2xl p-6 max-w-5xl w-full shadow-2xl animate-slideUp max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-6 h-6 text-primary" />
                  Escolha Sua Realidade
                </h2>
                <p className="text-textSecondary text-sm mt-1">
                  7 universos visuais únicos • Experiência cinematográfica
                </p>
              </div>
              <div className="flex items-center gap-2">
                {/* Sound Toggle */}
                <button
                  onClick={handleSoundToggle}
                  className={`p-2 rounded-lg transition-colors ${
                    soundEnabled
                      ? 'bg-primary/20 text-primary hover:bg-primary/30'
                      : 'bg-white/5 text-textSecondary hover:bg-white/10'
                  }`}
                  title={soundEnabled ? 'Desativar sons' : 'Ativar sons'}
                >
                  {soundEnabled ? (
                    <Volume2 className="w-5 h-5" />
                  ) : (
                    <VolumeX className="w-5 h-5" />
                  )}
                </button>
                
                {/* Close Button */}
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 hover:bg-white/5 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5 text-textSecondary" />
                </button>
              </div>
            </div>

            {/* Theme Grid - 7 temas */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {THEME_ORDER.map((themeId) => {
                const theme = THEMES[themeId];
                const isActive = currentTheme === themeId;

                return (
                  <button
                    key={themeId}
                    onClick={() => handleThemeSelect(themeId)}
                    disabled={isTransitioning}
                    className={`group relative p-5 rounded-xl border-2 transition-all duration-300 ${
                      isActive
                        ? 'border-primary bg-primary/10 shadow-lg shadow-primary/20 scale-105'
                        : 'border-border hover:border-primary/50 hover:bg-white/5 hover:scale-102'
                    }`}
                  >
                    {/* Active Indicator */}
                    {isActive && (
                      <div className="absolute top-3 right-3 w-3 h-3 bg-primary rounded-full animate-pulse" />
                    )}

                    {/* Icon */}
                    <div className="text-4xl mb-3">{theme.icon}</div>

                    {/* Title */}
                    <h3 className={`text-base font-bold mb-1 ${
                      isActive ? 'text-white' : 'text-textSecondary group-hover:text-white'
                    }`}>
                      {theme.name}
                    </h3>

                    {/* Description */}
                    <p className="text-xs text-textSecondary mb-4 line-clamp-2 h-8">
                      {theme.description}
                    </p>

                    {/* Color Preview */}
                    <div className="flex gap-2 mb-3">
                      <div
                        className="flex-1 h-6 rounded shadow-inner"
                        style={{ backgroundColor: theme.colors.primary }}
                      />
                      <div
                        className="flex-1 h-6 rounded shadow-inner"
                        style={{ backgroundColor: theme.colors.secondary }}
                      />
                      <div
                        className="flex-1 h-6 rounded shadow-inner"
                        style={{ backgroundColor: theme.colors.accent }}
                      />
                    </div>

                    {/* Gradient Preview */}
                    <div
                      className="w-full h-2 rounded-full"
                      style={{ background: theme.gradient }}
                    />

                    {/* Hover Glow Effect */}
                    <div className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                      <div
                        className="absolute inset-0 rounded-xl"
                        style={{
                          background: `radial-gradient(circle at center, ${theme.colors.primary}15 0%, transparent 70%)`,
                        }}
                      />
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Keyboard Shortcut Hint */}
            <div className="mt-6 pt-4 border-t border-border flex items-center justify-center gap-2 text-sm text-textSecondary">
              <kbd className="px-2 py-1 bg-black/30 rounded border border-border font-mono text-xs">
                Alt
              </kbd>
              <span>+</span>
              <kbd className="px-2 py-1 bg-black/30 rounded border border-border font-mono text-xs">
                Shift
              </kbd>
              <span>+</span>
              <kbd className="px-2 py-1 bg-black/30 rounded border border-border font-mono text-xs">
                T
              </kbd>
              <span className="ml-2">para ciclar entre temas</span>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.2s ease-out;
        }

        .animate-slideUp {
          animation: slideUp 0.3s ease-out;
        }
      `}</style>
    </>
  );
}
