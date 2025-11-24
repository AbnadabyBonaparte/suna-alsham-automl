/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THEME TYPES (9 UNIVERSOS - GLOBAL ELITE)
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
  | 'cobalt' 
  | 'crimson';

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

// ═══════════════════════════════════════════════════════════════
// 1. QUANTUM LAB (O Cientista Visionário)
// ═══════════════════════════════════════════════════════════════
export const QUANTUM_THEME: ThemeConfig = {
  id: 'quantum',
  name: 'Quantum Lab',
  description: 'O nascimento do pensamento dentro de um reator.',
  icon: '⚛️',
  colors: {
    primary: '#00FFD0',
    secondary: '#0EA5E9',
    accent: '#06B6D4',
    background: '#000000',
    surface: '#0a0a0a',
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
  animation: { speed: 'medium', intensity: 'high' },
  sound: { ambient: '/sounds/quantum-hum.mp3', click: '/sounds/quantum-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 2. LUMINOUS ASCENSION (O Deus)
// ═══════════════════════════════════════════════════════════════
export const ASCENSION_THEME: ThemeConfig = {
  id: 'ascension',
  name: 'Luminous Ascension',
  description: 'O pós-vida da tecnologia. Minimalismo divino.',
  icon: '✨',
  colors: {
    primary: '#FFD700',
    secondary: '#FFA500',
    accent: '#FF8C00',
    background: '#F8FAFC',
    surface: '#FFFFFF',
    text: '#1E293B',
    textSecondary: '#64748B',
    border: '#E2E8F0',
    success: '#FFD700',
    warning: '#F59E0B',
    error: '#EF4444',
    glow: '#FFD700',
  },
  gradient: 'linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)',
  backgroundType: 'ascension',
  animation: { speed: 'slow', intensity: 'low' },
  sound: { ambient: '/sounds/celestial-hum.mp3', click: '/sounds/golden-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 3. MILITARY OPS (O General - PENTAGON WAR ROOM)
// ═══════════════════════════════════════════════════════════════
export const MILITARY_THEME: ThemeConfig = {
  id: 'military',
  name: 'Military Ops',
  description: 'War Room do Pentágono. Camuflagem digital e fibra de carbono.',
  icon: '🎯', // Ícone de Sniper
  colors: {
    primary: '#FFD600',      // Amarelo Tático de Alto Contraste (HUD)
    secondary: '#333333',    // Gunmetal Grey
    accent: '#EF4444',       // Vermelho Alerta/Laser
    background: '#050505',   // Preto Fosco Absoluto (Stealth)
    surface: '#111111',      // Textura Fibra de Carbono (Simulada)
    text: '#E5E5E5',         // Branco Gelo Sujo
    textSecondary: '#6B7280', // Cinza Tático
    border: '#404040',       // Aço Escovado Escuro
    success: '#10B981',      // Verde Radar
    warning: '#F59E0B',      // Laranja Perigo
    error: '#DC2626',        // Vermelho Crítico
    glow: '#FFD600',         // Glow Amarelo HUD
  },
  gradient: 'linear-gradient(180deg, #050505 0%, #111111 100%)', // Fundo Stealth
  backgroundType: 'military',
  animation: { speed: 'fast', intensity: 'high' },
  sound: { ambient: '/sounds/radar-sweep.mp3', click: '/sounds/tactical-switch.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 4. NEURAL SINGULARITY (A IA Viva)
// ═══════════════════════════════════════════════════════════════
export const NEURAL_THEME: ThemeConfig = {
  id: 'neural',
  name: 'Neural Singularity',
  description: 'Estar dentro do cérebro da IA. Biologia digital.',
  icon: '🧠',
  colors: {
    primary: '#8B5CF6',
    secondary: '#A78BFA',
    accent: '#EC4899',
    background: '#050008',
    surface: '#0F0A14',
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
  animation: { speed: 'slow', intensity: 'high' },
  sound: { ambient: '/sounds/neural-pulse.mp3', click: '/sounds/synapse-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 5. TITANIUM EXECUTIVE (Dubai 127º Andar)
// ═══════════════════════════════════════════════════════════════
export const TITANIUM_THEME: ThemeConfig = {
  id: 'titanium',
  name: 'Titanium Executive',
  description: 'Dubai Penthouse. Couro Saffiano, Ouro Líquido e Platina.',
  icon: '🤵',
  colors: {
    primary: '#F1F5F9',      // Platina Pura
    secondary: '#1E293B',    // Azul Meia-Noite
    accent: '#D4AF37',       // Ouro Metálico Real (Champagne Gold)
    background: '#020617',   // Azul Marinho Profundo (Deep Navy)
    surface: '#0F172A',      // Couro Azulado
    text: '#F8FAFC',         // Branco Titânio
    textSecondary: '#94A3B8', // Prata Fosco
    border: '#334155',       // Borda Metálica Fina
    success: '#D4AF37',      // Sucesso é Ouro
    warning: '#B45309',      // Bronze
    error: '#991B1B',        // Rubi Escuro
    glow: '#D4AF37',         // Brilho Dourado Sutil
  },
  gradient: 'linear-gradient(135deg, #020617 0%, #0F172A 100%)',
  backgroundType: 'titanium',
  animation: { speed: 'medium', intensity: 'low' },
  sound: { ambient: '/sounds/vault-ambience.mp3', click: '/sounds/heavy-metal-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 6. VINTAGE TERMINAL (Hacker Style)
// ═══════════════════════════════════════════════════════════════
export const VINTAGE_THEME: ThemeConfig = {
  id: 'vintage',
  name: 'Vintage Terminal',
  description: 'A estética do CRT. Código puro e nostalgia.',
  icon: '💾',
  colors: {
    primary: '#00FF00',
    secondary: '#00D400',
    accent: '#00FFFF',
    background: '#001A00',
    surface: '#000A00',
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
  animation: { speed: 'fast', intensity: 'high' },
  sound: { ambient: '/sounds/crt-hum.mp3', click: '/sounds/key-press.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 7. ZEN GARDEN (Minimalismo)
// ═══════════════════════════════════════════════════════════════
export const ZEN_THEME: ThemeConfig = {
  id: 'zen',
  name: 'Zen Garden',
  description: 'Calma e clareza. O foco é a sua tarefa.',
  icon: '🧘',
  colors: {
    primary: '#4CAF50',
    secondary: '#795548',
    accent: '#66BB6A',
    background: '#F9F7F3',
    surface: '#FFFFFF',
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
  animation: { speed: 'slow', intensity: 'low' },
  sound: { ambient: '/sounds/water-flow.mp3', click: '/sounds/soft-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 8. COBALT PRIME (Enterprise Trust)
// ═══════════════════════════════════════════════════════════════
export const COBALT_THEME: ThemeConfig = {
  id: 'cobalt',
  name: 'Cobalt Prime',
  description: 'Estabilidade corporativa. Confiança e dados massivos.',
  icon: '💎',
  colors: {
    primary: '#3B82F6',
    secondary: '#1E40AF',
    accent: '#60A5FA',
    background: '#0B1120',
    surface: '#111827',
    text: '#F9FAFB',
    textSecondary: '#94A3B8',
    border: '#1E3A8A',
    success: '#059669',
    warning: '#F59E0B',
    error: '#DC2626',
    glow: '#3B82F6',
  },
  gradient: 'radial-gradient(circle at top right, #1E3A8A 0%, #0B1120 60%)',
  backgroundType: 'cobalt',
  animation: { speed: 'slow', intensity: 'medium' },
  sound: { ambient: '/sounds/server-room.mp3', click: '/sounds/soft-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 9. CRIMSON VELOCITY (High Performance)
// ═══════════════════════════════════════════════════════════════
export const CRIMSON_THEME: ThemeConfig = {
  id: 'crimson',
  name: 'Crimson Velocity',
  description: 'Alta performance e agressividade. Modo Sport.',
  icon: '🏎️',
  colors: {
    primary: '#EF4444',
    secondary: '#991B1B',
    accent: '#F87171',
    background: '#0F0505',
    surface: '#1C0505',
    text: '#FFFFFF',
    textSecondary: '#FECACA',
    border: '#7F1D1D',
    success: '#10B981',
    warning: '#F59E0B',
    error: '#FF0000',
    glow: '#EF4444',
  },
  gradient: 'linear-gradient(to bottom right, #450a0a 0%, #000000 80%)',
  backgroundType: 'crimson',
  animation: { speed: 'fast', intensity: 'high' },
  sound: { ambient: '/sounds/engine-hum.mp3', click: '/sounds/mechanical-click.mp3' },
};

// ═══════════════════════════════════════════════════════════════
// 10. AGRUPAMENTO FINAL (ORDEM CORRIGIDA)
// ═══════════════════════════════════════════════════════════════
export const THEMES: Record<ThemeId, ThemeConfig> = {
  quantum: QUANTUM_THEME,
  ascension: ASCENSION_THEME,
  military: MILITARY_THEME,
  neural: NEURAL_THEME,
  titanium: TITANIUM_THEME,
  vintage: VINTAGE_THEME,
  zen: ZEN_THEME,
  cobalt: COBALT_THEME,
  crimson: CRIMSON_THEME,
};

export const DEFAULT_THEME: ThemeId = 'quantum';

export const THEME_ORDER: ThemeId[] = [
  'quantum',
  'ascension',
  'military', // O General (Novo)
  'titanium', // O Bilionário (Novo)
  'cobalt',
  'crimson',
  'neural',
  'vintage',
  'zen',
];
