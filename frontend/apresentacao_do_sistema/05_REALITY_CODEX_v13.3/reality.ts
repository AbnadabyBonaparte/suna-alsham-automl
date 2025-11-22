/**
 * Complete Reality Configuration System
 * Based on ALSHAM QUANTUM CÓDICE VISUAL OFICIAL
 */

export type RealityId = 'quantum' | 'military' | 'neural' | 'titanium' | 'ascension';

export type CardShape = 'chamfered' | 'rounded' | 'sharp' | 'organic' | 'neumorphic';

export type HoverEffect = 'glow' | 'scanline' | 'breathing' | 'lift' | 'none';

export type AnimationSpeed = 'fast' | 'normal' | 'slow';

export interface RealityColors {
    bgCore: string;
    bgPanel: string;
    textPrimary: string;
    accent: string;
    accentSecondary?: string;
    border: string;
}

export interface RealityGeometry {
    radius: string;
    borderWidth: string;
    cardShape: CardShape;
}

export interface RealityAssets {
    particles: boolean;
    tacticalGrid: boolean;
    neuralPulse: boolean;
    noiseTexture: boolean;
    volumetricLight: boolean;
    scanlines: boolean;
}

export interface RealityTypography {
    displayFont: string;
    monoFont: string;
    textTransform: 'none' | 'uppercase';
}

export interface RealityEffects {
    backdropBlur: string;
    cardOpacity: number;
    boxShadow: string;
    hoverEffect: HoverEffect;
}

export interface RealityAnimations {
    speed: AnimationSpeed;
    springConfig: {
        stiffness: number;
        damping: number;
    };
}

export interface RealityConfig {
    id: RealityId;
    name: string;
    archetype: string;
    colors: RealityColors;
    geometry: RealityGeometry;
    assets: RealityAssets;
    typography: RealityTypography;
    effects: RealityEffects;
    animations: RealityAnimations;
}

/**
 * Complete Reality Configurations
 */
export const REALITY_CONFIGS: Record<RealityId, RealityConfig> = {
    quantum: {
        id: 'quantum',
        name: 'QUANTUM LAB',
        archetype: 'The Visionary Scientist',
        colors: {
            bgCore: '#000000',
            bgPanel: 'rgba(0, 255, 200, 0.03)',
            textPrimary: '#00FFC8',
            accent: '#00FFC8',
            accentSecondary: '#00D4AA',
            border: 'rgba(0, 255, 200, 0.2)',
        },
        geometry: {
            radius: '12px',
            borderWidth: '1px',
            cardShape: 'chamfered',
        },
        assets: {
            particles: true,
            tacticalGrid: false,
            neuralPulse: false,
            noiseTexture: false,
            volumetricLight: false,
            scanlines: false,
        },
        typography: {
            displayFont: 'var(--font-orbitron)',
            monoFont: 'var(--font-ibm-plex-mono)',
            textTransform: 'none',
        },
        effects: {
            backdropBlur: 'blur(12px)',
            cardOpacity: 0.1,
            boxShadow: '0 0 20px rgba(0, 255, 200, 0.15)',
            hoverEffect: 'glow',
        },
        animations: {
            speed: 'normal',
            springConfig: { stiffness: 300, damping: 25 },
        },
    },

    military: {
        id: 'military',
        name: 'MILITARY OPS',
        archetype: 'The General',
        colors: {
            bgCore: '#0A0E1A',
            bgPanel: 'rgba(20, 30, 50, 0.9)',
            textPrimary: '#F4D03F',
            accent: '#F4D03F',
            accentSecondary: '#FF3333',
            border: 'rgba(244, 208, 63, 0.3)',
        },
        geometry: {
            radius: '0px',
            borderWidth: '2px',
            cardShape: 'sharp',
        },
        assets: {
            particles: false,
            tacticalGrid: true,
            neuralPulse: false,
            noiseTexture: false,
            volumetricLight: false,
            scanlines: true,
        },
        typography: {
            displayFont: 'var(--font-ibm-plex-mono)',
            monoFont: 'var(--font-ibm-plex-mono)',
            textTransform: 'uppercase',
        },
        effects: {
            backdropBlur: 'none',
            cardOpacity: 1,
            boxShadow: 'none',
            hoverEffect: 'scanline',
        },
        animations: {
            speed: 'fast',
            springConfig: { stiffness: 500, damping: 30 },
        },
    },

    neural: {
        id: 'neural',
        name: 'NEURAL SINGULARITY',
        archetype: 'The Living Entity',
        colors: {
            bgCore: '#050008',
            bgPanel: 'rgba(40, 0, 60, 0.2)',
            textPrimary: '#D022FF',
            accent: '#D022FF',
            accentSecondary: '#22CCFF',
            border: 'rgba(208, 34, 255, 0.3)',
        },
        geometry: {
            radius: '30px',
            borderWidth: '1px',
            cardShape: 'organic',
        },
        assets: {
            particles: false,
            tacticalGrid: false,
            neuralPulse: true,
            noiseTexture: false,
            volumetricLight: false,
            scanlines: false,
        },
        typography: {
            displayFont: 'var(--font-orbitron)',
            monoFont: 'var(--font-ibm-plex-mono)',
            textTransform: 'none',
        },
        effects: {
            backdropBlur: 'blur(16px)',
            cardOpacity: 0.15,
            boxShadow: '0 0 35px rgba(208, 34, 255, 0.25)',
            hoverEffect: 'breathing',
        },
        animations: {
            speed: 'slow',
            springConfig: { stiffness: 150, damping: 20 },
        },
    },

    titanium: {
        id: 'titanium',
        name: 'TITANIUM EXECUTIVE',
        archetype: 'The Billionaire',
        colors: {
            bgCore: '#0F172A',
            bgPanel: 'rgba(255, 255, 255, 0.03)',
            textPrimary: '#F8FAFC',
            accent: '#38BDF8',
            accentSecondary: '#D97706',
            border: 'rgba(255, 255, 255, 0.08)',
        },
        geometry: {
            radius: '8px',
            borderWidth: '0.5px',
            cardShape: 'rounded',
        },
        assets: {
            particles: false,
            tacticalGrid: false,
            neuralPulse: false,
            noiseTexture: true,
            volumetricLight: false,
            scanlines: false,
        },
        typography: {
            displayFont: 'var(--font-inter)',
            monoFont: 'var(--font-ibm-plex-mono)',
            textTransform: 'none',
        },
        effects: {
            backdropBlur: 'blur(20px)',
            cardOpacity: 0.05,
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.4)',
            hoverEffect: 'lift',
        },
        animations: {
            speed: 'fast',
            springConfig: { stiffness: 400, damping: 28 },
        },
    },

    ascension: {
        id: 'ascension',
        name: 'LUMINOUS ASCENSION',
        archetype: 'The God',
        colors: {
            bgCore: '#F8FAFC',
            bgPanel: 'rgba(255, 255, 255, 0.6)',
            textPrimary: '#475569',
            accent: '#D97706',
            accentSecondary: '#F59E0B',
            border: 'rgba(217, 119, 6, 0.2)',
        },
        geometry: {
            radius: '16px',
            borderWidth: '0px',
            cardShape: 'neumorphic',
        },
        assets: {
            particles: false,
            tacticalGrid: false,
            neuralPulse: false,
            noiseTexture: false,
            volumetricLight: true,
            scanlines: false,
        },
        typography: {
            displayFont: 'var(--font-cinzel)',
            monoFont: 'var(--font-inter)',
            textTransform: 'none',
        },
        effects: {
            backdropBlur: 'none',
            cardOpacity: 1,
            boxShadow: '8px 8px 16px rgba(0, 0, 0, 0.1), -8px -8px 16px rgba(255, 255, 255, 0.9)',
            hoverEffect: 'lift',
        },
        animations: {
            speed: 'slow',
            springConfig: { stiffness: 200, damping: 22 },
        },
    },
};
