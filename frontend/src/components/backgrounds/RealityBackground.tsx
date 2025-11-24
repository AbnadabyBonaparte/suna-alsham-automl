/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - REALITY BACKGROUND ORCHESTRATOR (9 UNIVERSOS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/backgrounds/RealityBackground.tsx
 * 📋 Escolhe qual background renderizar baseado no tema atual da Global Elite.
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useTheme } from '@/contexts/ThemeContext';
import dynamic from 'next/dynamic';

// Lazy load backgrounds para performance máxima
const QuantumBackground = dynamic(() => import('./QuantumBackground'), {
  ssr: false,
  loading: () => null,
});

const AscensionBackground = dynamic(() => import('./AscensionBackground'), {
  ssr: false,
  loading: () => null,
});

const MilitaryBackground = dynamic(() => import('./MilitaryBackground'), {
  ssr: false,
  loading: () => null,
});

const TitaniumBackground = dynamic(() => import('./TitaniumBackground'), {
  ssr: false,
  loading: () => null,
});

const VintageBackground = dynamic(() => import('./VintageBackground'), {
  ssr: false,
  loading: () => null,
});

const ZenBackground = dynamic(() => import('./ZenBackground'), {
  ssr: false,
  loading: () => null,
});

export default function RealityBackground() {
  const { currentTheme, themeConfig } = useTheme();

  // O switch case decide qual componente renderizar
  // Para temas baseados em partículas (Neural, Cobalt, Crimson), reutilizamos o QuantumBackground
  
  switch (currentTheme) {
    // 1. QUANTUM (Ciano Padrão)
    case 'quantum':
      return <QuantumBackground color="#00FFD0" />;
    
    // 2. ASCENSION (Divino)
    case 'ascension':
      return <AscensionBackground />;
    
    // 3. MILITARY (Night Vision Radar)
    case 'military':
      return <MilitaryBackground />;
    
    // 4. NEURAL (Roxo Vivo)
    case 'neural':
      return <QuantumBackground color="#8B5CF6" />;
    
    // 5. TITANIUM (Dubai Night)
    case 'titanium':
      return <TitaniumBackground />;
      
    // 6. VINTAGE (CRT Hacker)
    case 'vintage':
      return <VintageBackground />;
      
    // 7. ZEN (Minimalista)
    case 'zen':
      return <ZenBackground />;

    // 8. COBALT (Azul Enterprise) - Reutiliza Quantum
    case 'cobalt':
      return <QuantumBackground color="#3B82F6" />;

    // 9. CRIMSON (Vermelho Performance) - Reutiliza Quantum
    case 'crimson':
      return <QuantumBackground color="#EF4444" />;
    
    // Fallback de segurança
    default:
      return <QuantumBackground color="#00FFD0" />;
  }
}
