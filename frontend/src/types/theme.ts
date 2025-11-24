/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THEME TYPES (9 UNIVERSOS - GLOBAL ELITE EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/types/theme.ts
 * ═══════════════════════════════════════════════════════════════
 */

export type ThemeId = 
  | 'quantum' 
  | 'ascension' 
  | 'military' 
  | 'neural' 
  | 'titanium' 
  | 'vintage' 
  | 'zen' 
  | 'cobalt'   // NOVO: Enterprise Trust
  | 'crimson'; // NOVO: High Performance

export interface ThemeColors {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  success: string;
  warning: string;
  error: string;
  glow: string;
}

export interface ThemeConfig {
  id: ThemeId;
  name: string;
  description: string;
  icon: string;
  colors: ThemeColors;
  gradient: string;
  backgroundType: ThemeId;
  animation: {
    speed: 'slow' | 'medium' | 'fast';
    intensity: 'low' | 'medium' | 'high';
  };
  sound: {
    ambient?: string;
    click?: string;
    hover?: string;
  };
}

// ... [MANTENHA OS TEMAS: QUANTUM, ASCENSION, MILITARY, NEURAL, VINTAGE, ZEN AQUI] ...
// (Vou focar apenas nas alterações e novidades abaixo)

// ═══════════════════════════════════════════════════════════════
// REALIDADE 5: TITANIUM EXECUTIVE (Refinado - Estilo Apple/SpaceX)
// ═══════════════════════════════════════════════════════════════
export const TITANIUM_THEME: ThemeConfig = {
  id: 'titanium',
  name: 'Titanium Executive',
  description: 'Minimalismo industrial. O luxo do grafite e metal.',
  icon: '🛡️', // Ícone atualizado
  colors: {
    primary: '#E5E7EB',      // Cinza Platina (Apple Silver)
    secondary: '#9CA3AF',    // Cinza Médio
    accent: '#FFFFFF',       // Branco Absoluto
    background: '#111111',   // Preto Fosco (Não mais azulado)
    surface: '#1C1C1E',      // Grafite Profundo (iOS Dark Mode)
    text: '#F3F4F6',
    textSecondary: '#9CA3AF',
    border: '#374151',
    success: '#10B981',      // Verde Stock Market
    warning: '#F59E0B',
    error: '#EF4444',
    glow: '#E5E7EB',
  },
  gradient: 'linear-gradient(145deg, #111111 0%, #1C1C1E 100%)',
  backgroundType: 'titanium',
  animation: {
    speed: 'medium',
    intensity: 'low', // Mais sóbrio
  },
  sound: {
    ambient: '/sounds/executive-ambient.mp3',
    click: '/sounds/titanium-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 8: COBALT PRIME (Estilo Microsoft/IBM/Enterprise)
// ═══════════════════════════════════════════════════════════════
export const COBALT_THEME: ThemeConfig = {
  id: 'cobalt',
  name: 'Cobalt Prime',
  description: 'Estabilidade corporativa. Confiança e dados massivos.',
  icon: '💎',
  colors: {
    primary: '#3B82F6',      // Azul IBM/Chase
    secondary: '#1E40AF',    // Azul Profundo
    accent: '#60A5FA',       // Azul Claro
    background: '#0B1120',   // Navy Dark Mode
    surface: '#111827',      // Cool Gray Dark
    text: '#F9FAFB',
    textSecondary: '#94A3B8',
    border: '#1E3A8A',
    success: '#059669',
    warning: '#F59E0B',
    error: '#DC2626',
    glow: '#3B82F6',
  },
  gradient: 'radial-gradient(circle at top right, #1E3A8A 0%, #0B1120 60%)',
  backgroundType: 'cobalt', // Requereria criar esse tipo ou usar 'quantum' com cor azul
  animation: {
    speed: 'slow',
    intensity: 'medium',
  },
  sound: {
    ambient: '/sounds/server-room.mp3',
    click: '/sounds/soft-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 9: CRIMSON VELOCITY (Estilo Tesla/Netflix/Gamer)
// ═══════════════════════════════════════════════════════════════
export const CRIMSON_THEME: ThemeConfig = {
  id: 'crimson',
  name: 'Crimson Velocity',
  description: 'Alta performance e agressividade. Modo Sport.',
  icon: '🏎️',
  colors: {
    primary: '#EF4444',      // Vermelho Performance
    secondary: '#991B1B',    // Vermelho Sangue
    accent: '#F87171',       // Vermelho Laser
    background: '#0F0505',   // Quase Preto com toque vermelho
    surface: '#1C0505',      // Carbono Avermelhado
    text: '#FFFFFF',
    textSecondary: '#FECACA',
    border: '#7F1D1D',
    success: '#10B981',
    warning: '#F59E0B',
    error: '#FF0000',        // Vermelho Puro
    glow: '#EF4444',
  },
  gradient: 'linear-gradient(to bottom right, #450a0a 0%, #000000 80%)',
  backgroundType: 'crimson', // Requereria criar esse tipo ou usar 'military'
  animation: {
    speed: 'fast',
    intensity: 'high',
  },
  sound: {
    ambient: '/sounds/engine-hum.mp3',
    click: '/sounds/mechanical-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// EXPORTAÇÕES ATUALIZADAS
// ═══════════════════════════════════════════════════════════════
export const THEMES: Record<ThemeId, ThemeConfig> = {
  quantum: QUANTUM_THEME,     // O Visionário
  ascension: ASCENSION_THEME, // O Divino
  military: MILITARY_THEME,   // O Tático
  neural: NEURAL_THEME,       // A IA Viva
  titanium: TITANIUM_THEME,   // O Executivo (Apple Style)
  vintage: VINTAGE_THEME,     // O Hacker
  zen: ZEN_THEME,             // O Equilíbrio
  cobalt: COBALT_THEME,       // A Corporação (Microsoft Style)
  crimson: CRIMSON_THEME,     // A Performance (Tesla Style)
};

export const DEFAULT_THEME: ThemeId = 'quantum';

export const THEME_ORDER: ThemeId[] = [
  'quantum',
  'ascension',
  'cobalt',    // Inserido para balancear
  'military',
  'crimson',   // Inserido para impacto
  'neural',
  'titanium',
  'vintage',
  'zen',
];
