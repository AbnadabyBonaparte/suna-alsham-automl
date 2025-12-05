/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THEME SWITCHER UI (GLOBAL ELITE EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/ui/ThemeSwitcher.tsx
 * 📋 Interface visual cinematográfica para 9 Realidades
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useState } from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { THEMES, THEME_ORDER, ThemeId } from '@/types/theme';
import { 
  Palette, 
  X, 
  Sparkles, 
  Volume2, 
  VolumeX, 
  Atom,           // Quantum
  Sun,            // Ascension
  Crosshair,      // Military
  BrainCircuit,   // Neural
  Gem,            // Titanium
  Terminal,       // Vintage
  Leaf,           // Zen
  Building2,      // Cobalt
  Zap             // Crimson
} from 'lucide-react';

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
    playClick();
  };

  // Helper para renderizar ícones profissionais baseados no ID do tema
  const getThemeIcon = (id: string, color: string) => {
    const iconProps = { 
      className: "w-8 h-8", 
      style: { color: color, filter: `drop-shadow(0 0 8px ${color})` } 
    };

    switch (id) {
      case 'quantum':   return <Atom {...iconProps} />;
      case 'ascension': return <Sun {...iconProps} />;
      case 'military':  return <Crosshair {...iconProps} />;
      case 'neural':    return <BrainCircuit {...iconProps} />;
      case 'titanium':  return <Gem {...iconProps} />;
      case 'vintage':   return <Terminal {...iconProps} />;
      case 'zen':       return <Leaf {...iconProps} />;
      case 'cobalt':    return <Building2 {...iconProps} />;
      case 'crimson':   return <Zap {...iconProps} />;
      default:          return <Sparkles {...iconProps} />;
    }
  };

  return (
    <>
     {/* Floating Button - ORBE DE ENERGIA - Reposicionado para não conflitar com ORION */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 left-6 w-14 h-14 rounded-full flex items-center justify-center transition-all duration-500 hover:scale-110 z-[100] group"
        style={{
          background: `rgba(0,0,0,0.8)`,
          backdropFilter: 'blur(16px)',
          border: '1px solid var(--color-primary)',
          boxShadow: `0 0 15px var(--color-glow), inset 0 0 20px rgba(0,0,0,0.5)`,
        }}
        title="Alterar Realidade (Alt+Shift+T)"
      >
        <div className="absolute inset-0 rounded-full opacity-20 group-hover:opacity-40 transition-opacity bg-[var(--color-primary)] blur-md" />
        <Palette className="w-6 h-6 text-[var(--color-primary)] relative z-10" />
      </button>

      {/* Modal Overlay - CINEMATOGRÁFICO */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/90 backdrop-blur-md z-[200] flex items-center justify-center p-4 animate-fadeIn"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="bg-[#050505] border border-white/10 rounded-3xl p-8 max-w-6xl w-full shadow-2xl animate-slideUp max-h-[95vh] overflow-y-auto relative overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Background Grid Sutil no Modal */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />

            {/* Header */}
            <div className="flex items-center justify-between mb-8 relative z-10">
              <div>
                <h2 className="text-3xl font-bold text-white flex items-center gap-3 tracking-tight">
                  <Sparkles className="w-8 h-8 text-[var(--color-primary)] animate-pulse" />
                  REALITY CODEX
                </h2>
                <p className="text-gray-400 text-sm mt-2 font-mono uppercase tracking-widest">
                  {THEME_ORDER.length} Universos Ativos • Selecione sua Frequência
                </p>
              </div>
              
              <div className="flex items-center gap-3">
                {/* Sound Toggle */}
                <button
                  onClick={handleSoundToggle}
                  className={`p-3 rounded-xl transition-all border ${
                    soundEnabled
                      ? 'bg-[var(--color-primary)]/10 border-[var(--color-primary)] text-[var(--color-primary)]'
                      : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
                  }`}
                >
                  {soundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
                </button>
                
                {/* Close Button */}
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-red-500/20 hover:text-red-400 hover:border-red-500/50 transition-all text-gray-400"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Theme Grid - DESIGN TIPO "CARTAS DE JOGO DE LUXO" */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 relative z-10">
              {THEME_ORDER.map((themeId) => {
                const theme = THEMES[themeId];
                const isActive = currentTheme === themeId;

                return (
                  <button
                    key={themeId}
                    onClick={() => handleThemeSelect(themeId)}
                    disabled={isTransitioning}
                    className={`group relative p-6 rounded-2xl border transition-all duration-500 overflow-hidden text-left flex flex-col h-full ${
                      isActive
                        ? 'border-[var(--color-primary)] bg-[var(--color-primary)]/5 shadow-[0_0_30px_-10px_var(--color-primary)] scale-[1.02]'
                        : 'border-white/5 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.04] hover:translate-y-[-4px]'
                    }`}
                  >
                    {/* Background Gradient Sutil dentro do card */}
                    <div 
                      className="absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-700"
                      style={{ background: theme.gradient }}
                    />

                    <div className="flex items-start justify-between mb-4">
                      {/* Ícone Profundo (Glassmorphism Container) */}
                      <div 
                        className="w-14 h-14 rounded-2xl flex items-center justify-center border border-white/5 shadow-inner"
                        style={{ 
                          background: `linear-gradient(135deg, ${theme.colors.surface} 0%, ${theme.colors.background} 100%)`,
                          boxShadow: isActive ? `0 0 20px ${theme.colors.primary}40` : 'none'
                        }}
                      >
                        {getThemeIcon(themeId, theme.colors.primary)}
                      </div>

                      {/* Indicador de Ativo */}
                      {isActive && (
                        <span 
                          className="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border"
                          style={{ 
                            borderColor: theme.colors.primary, 
                            color: theme.colors.primary,
                            background: `${theme.colors.primary}10`
                          }}
                        >
                          Ativo
                        </span>
                      )}
                    </div>

                    {/* Conteúdo de Texto */}
                    <div>
                      <h3 
                        className="text-lg font-bold mb-2 transition-colors"
                        style={{ color: isActive ? theme.colors.primary : '#FFF' }}
                      >
                        {theme.name}
                      </h3>
                      <p className="text-sm text-gray-500 font-medium leading-relaxed group-hover:text-gray-400 transition-colors">
                        {theme.description}
                      </p>
                    </div>

                    {/* Barra de Cores (DNA do Tema) */}
                    <div className="mt-6 flex items-center gap-2 pt-4 border-t border-white/5">
                      <div className="text-[10px] text-gray-600 font-mono uppercase mr-auto">Paleta</div>
                      <div className="w-6 h-6 rounded-full border border-white/10" style={{ background: theme.colors.primary }} />
                      <div className="w-6 h-6 rounded-full border border-white/10" style={{ background: theme.colors.secondary }} />
                      <div className="w-6 h-6 rounded-full border border-white/10" style={{ background: theme.colors.background }} />
                    </div>
                  </button>
                );
              })}
            </div>
            
            {/* Footer */}
            <div className="mt-8 text-center">
                <p className="text-xs text-gray-600 font-mono">
                    ALSHAM QUANTUM v13.3 • REALITY ENGINE ACTIVE
                </p>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(40px) scale(0.95); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .animate-fadeIn { animation: fadeIn 0.3s ease-out forwards; }
        .animate-slideUp { animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
      `}</style>
    </>
  );
}
