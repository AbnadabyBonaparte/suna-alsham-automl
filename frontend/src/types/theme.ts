// frontend/src/types/theme.ts
// Reality Codex - Theme Type Definitions

export type ThemeId = 'quantum' | 'military' | 'neural' | 'titanium' | 'ascension';

export interface ThemeConfig {
  id: ThemeId;
  name: string;
  description: string;
  icon: string;
  shortcut: string;
  enabled: boolean;
  category: 'dark' | 'light';
  audience: string[];
}

export const THEMES: Record<ThemeId, ThemeConfig> = {
  quantum: {
    id: 'quantum',
    name: 'Quantum Lab',
    description: 'Laboratório científico futurista com partículas ciano',
    icon: '🔬',
    shortcut: 'Alt+1',
    enabled: true,
    category: 'dark',
    audience: ['Cientistas', 'Desenvolvedores', 'Pesquisadores'],
  },
  ascension: {
    id: 'ascension',
    name: 'Luminous Ascension',
    description: 'Aurora inspiradora com raios dourados',
    icon: '✨',
    shortcut: 'Alt+2',
    enabled: true,
    category: 'light',
    audience: ['Criativos', 'Designers', 'Educadores'],
  },
  military: {
    id: 'military',
    name: 'Military Ops',
    description: 'Centro de comando tático com grid hexagonal',
    icon: '⚔️',
    shortcut: 'Alt+3',
    enabled: false,
    category: 'dark',
    audience: ['Executivos', 'Gestores', 'Estrategistas'],
  },
  neural: {
    id: 'neural',
    name: 'Neural Singularity',
    description: 'Mente da IA com neurônios pulsantes',
    icon: '🧠',
    shortcut: 'Alt+4',
    enabled: false,
    category: 'dark',
    audience: ['Visionários', 'Futuristas', 'Artistas'],
  },
  titanium: {
    id: 'titanium',
    name: 'Titanium Executive',
    description: 'Suite executiva com elegância discreta',
    icon: '💎',
    shortcut: 'Alt+5',
    enabled: false,
    category: 'dark',
    audience: ['Executivos C-level', 'Investidores', 'Advogados'],
  },
};

export const getEnabledThemes = (): ThemeConfig[] => {
  return Object.values(THEMES).filter(theme => theme.enabled);
};

export const getThemeById = (id: ThemeId): ThemeConfig | undefined => {
  return THEMES[id];
};

export const DEFAULT_THEME: ThemeId = 'quantum';
