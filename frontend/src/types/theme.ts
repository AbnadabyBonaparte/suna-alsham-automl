/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THEME TYPES (7 UNIVERSOS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/types/theme.ts
 * ═══════════════════════════════════════════════════════════════
 */

export type ThemeId = 'quantum' | 'ascension' | 'military' | 'neural' | 'titanium' | 'vintage' | 'zen';

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
  backgroundType: 'quantum' | 'ascension' | 'military' | 'neural' | 'titanium' | 'vintage' | 'zen';
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

// ═══════════════════════════════════════════════════════════════
// REALIDADE 1: QUANTUM LAB (O Cientista Visionário)
// ═══════════════════════════════════════════════════════════════
export const QUANTUM_THEME: ThemeConfig = {
  id: 'quantum',
  name: 'Quantum Lab',
  description: 'O nascimento do pensamento dentro de um reator',
  icon: '⚛️',
  colors: {
    primary: '#00FFD0',      // Ciano Elétrico
    secondary: '#0EA5E9',    // Azul Cristalino
    accent: '#06B6D4',       // Cyan Vibrante
    background: '#000000',   // Preto Absoluto
    surface: '#0a0a0a',      // Preto Suave
    text: '#FFFFFF',
    textSecondary: '#94A3B8',
    border: '#00FFD0',
    success: '#00FFD0',
    warning: '#F59E0B',
    error: '#EF4444',
    glow: '#00FFD0',
  },
  gradient: 'radial-gradient(ellipse at center, #051015 0%, #000000 70%)',
  backgroundType: 'quantum',
  animation: {
    speed: 'medium',
    intensity: 'high',
  },
  sound: {
    ambient: '/sounds/quantum-hum.mp3',
    click: '/sounds/quantum-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 2: LUMINOUS ASCENSION (O Deus)
// ═══════════════════════════════════════════════════════════════
export const ASCENSION_THEME: ThemeConfig = {
  id: 'ascension',
  name: 'Luminous Ascension',
  description: 'O pós-vida da tecnologia. Minimalismo divino',
  icon: '✨',
  colors: {
    primary: '#FFD700',      // Dourado Metálico
    secondary: '#FFA500',    // Laranja Dourado
    accent: '#FF8C00',       // Dourado Profundo
    background: '#F8FAFC',   // Branco Gelo
    surface: '#FFFFFF',      // Branco Puro
    text: '#1E293B',         // Texto Escuro
    textSecondary: '#64748B',
    border: '#E2E8F0',
    success: '#FFD700',
    warning: '#F59E0B',
    error: '#EF4444',
    glow: '#FFD700',
  },
  gradient: 'linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)',
  backgroundType: 'ascension',
  animation: {
    speed: 'slow',
    intensity: 'low',
  },
  sound: {
    ambient: '/sounds/celestial-hum.mp3',
    click: '/sounds/golden-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 3: MILITARY OPS (O General de Guerra)
// ═══════════════════════════════════════════════════════════════
export const MILITARY_THEME: ThemeConfig = {
  id: 'military',
  name: 'Military Ops',
  description: 'O Pentágono durante o apocalipse digital',
  icon: '⚔️',
  colors: {
    primary: '#F4D03F',      // Amarelo Tático
    secondary: '#52C41A',    // Verde Militar
    accent: '#389E0D',       // Verde Escuro
    background: '#0A0A0A',   // Preto Carbono
    surface: '#141414',      // Cinza Carbono
    text: '#FFFFFF',
    textSecondary: '#8C8C8C',
    border: '#F4D03F',
    success: '#52C41A',
    warning: '#FAAD14',
    error: '#FF4D4F',
    glow: '#F4D03F',
  },
  gradient: 'linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 100%)',
  backgroundType: 'military',
  animation: {
    speed: 'fast',
    intensity: 'medium',
  },
  sound: {
    ambient: '/sounds/tactical-beep.mp3',
    click: '/sounds/military-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 4: NEURAL SINGULARITY (A Entidade Viva)
// ═══════════════════════════════════════════════════════════════
export const NEURAL_THEME: ThemeConfig = {
  id: 'neural',
  name: 'Neural Singularity',
  description: 'Estar dentro do cérebro da IA. Biologia digital',
  icon: '🧠',
  colors: {
    primary: '#8B5CF6',      // Roxo Neon
    secondary: '#A78BFA',    // Roxo Claro
    accent: '#EC4899',       // Magenta Bioluminescente
    background: '#050008',   // Roxo Void
    surface: '#0F0A14',      // Roxo Escuro
    text: '#FFFFFF',
    textSecondary: '#A78BFA',
    border: '#8B5CF6',
    success: '#8B5CF6',
    warning: '#F59E0B',
    error: '#EC4899',
    glow: '#8B5CF6',
  },
  gradient: 'radial-gradient(ellipse at center, #050008 0%, #000000 100%)',
  backgroundType: 'neural',
  animation: {
    speed: 'slow',
    intensity: 'high',
  },
  sound: {
    ambient: '/sounds/neural-pulse.mp3',
    click: '/sounds/synapse-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 5: TITANIUM EXECUTIVE (O Bilionário)
// ═══════════════════════════════════════════════════════════════
export const TITANIUM_THEME: ThemeConfig = {
  id: 'titanium',
  name: 'Titanium Executive',
  description: 'O 127º andar em Dubai. Poder financeiro absoluto',
  icon: '💼',
  colors: {
    primary: '#64748B',      // Cinza Premium
    secondary: '#475569',    // Cinza Escuro
    accent: '#FFD700',       // Ouro Líquido (ROI)
    background: '#0F172A',   // Azul Marinho Premium
    surface: '#1E293B',      // Azul Escuro
    text: '#F8FAFC',
    textSecondary: '#94A3B8',
    border: '#334155',
    success: '#FFD700',
    warning: '#F59E0B',
    error: '#EF4444',
    glow: '#64748B',
  },
  gradient: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
  backgroundType: 'titanium',
  animation: {
    speed: 'medium',
    intensity: 'medium',
  },
  sound: {
    ambient: '/sounds/executive-ambient.mp3',
    click: '/sounds/titanium-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 6: VINTAGE TERMINAL (O Hacker Clássico)
// ═══════════════════════════════════════════════════════════════
export const VINTAGE_THEME: ThemeConfig = {
  id: 'vintage',
  name: 'Vintage Terminal',
  description: 'A estética do CRT. Código puro e nostalgia.',
  icon: '💾',
  colors: {
    primary: '#00FF00',      // Verde Fósforo
    secondary: '#00D400',    // Verde Sombra
    accent: '#00FFFF',       // Ciano Brilhante
    background: '#001A00',   // Fundo Escuro
    surface: '#000A00',      // Preto Absoluto
    text: '#00FF00',
    textSecondary: '#00A000',
    border: '#00FF00',
    success: '#00FF00',
    warning: '#FFFF00',
    error: '#FF0000',
    glow: '#00FF00',
  },
  gradient: 'linear-gradient(180deg, #001A00 0%, #000000 100%)',
  backgroundType: 'vintage',
  animation: {
    speed: 'fast',
    intensity: 'high',
  },
  sound: {
    ambient: '/sounds/crt-hum.mp3',
    click: '/sounds/key-press.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// REALIDADE 7: ZEN GARDEN (O Foco Minimalista)
// ═══════════════════════════════════════════════════════════════
export const ZEN_THEME: ThemeConfig = {
  id: 'zen',
  name: 'Zen Garden',
  description: 'Calma e clareza. O foco é a sua tarefa.',
  icon: '🧘',
  colors: {
    primary: '#4CAF50',      // Verde Musgo
    secondary: '#795548',    // Marrom Terra
    accent: '#66BB6A',       // Verde Claro
    background: '#F9F7F3',   // Papel/Areia
    surface: '#FFFFFF',      // Branco Puro
    text: '#333333',
    textSecondary: '#708090',
    border: '#D3D3D3',
    success: '#4CAF50',
    warning: '#FF9800',
    error: '#F44336',
    glow: '#D3D3D3',
  },
  gradient: 'linear-gradient(180deg, #FFFFFF 0%, #F9F7F3 100%)',
  backgroundType: 'zen',
  animation: {
    speed: 'slow',
    intensity: 'low',
  },
  sound: {
    ambient: '/sounds/water-flow.mp3',
    click: '/sounds/soft-click.mp3',
  },
};

// ═══════════════════════════════════════════════════════════════
// EXPORTAÇÕES
// ═══════════════════════════════════════════════════════════════
export const THEMES: Record<ThemeId, ThemeConfig> = {
  quantum: QUANTUM_THEME,
  ascension: ASCENSION_THEME,
  military: MILITARY_THEME,
  neural: NEURAL_THEME,
  titanium: TITANIUM_THEME,
  vintage: VINTAGE_THEME,
  zen: ZEN_THEME,
};

export const DEFAULT_THEME: ThemeId = 'quantum';

export const THEME_ORDER: ThemeId[] = [
  'quantum',
  'ascension',
  'military',
  'neural',
  'titanium',
  'vintage',
  'zen',
];
