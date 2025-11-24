/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - REALITY BACKGROUND WRAPPER
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/backgrounds/RealityBackground.tsx
 * 📋 Escolhe qual background renderizar baseado no tema atual
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useTheme } from '@/contexts/ThemeContext';
import dynamic from 'next/dynamic';
import { useReducedMotion } from '@/hooks/useReducedMotion';

// Lazy load backgrounds para performance
const QuantumBackground = dynamic(() => import('./QuantumBackground'), {
  ssr: false,
  loading: () => null,
});

const AscensionBackground = dynamic(() => import('./AscensionBackground'), {
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
  const prefersReducedMotion = useReducedMotion(); // Assumindo que você tem este hook para acessibilidade

  // Renderizar background apropriado para cada tema
  switch (themeConfig.backgroundType) {
    case 'quantum':
      return <QuantumBackground />;
    
    case 'ascension':
      return <AscensionBackground />;
    
    case 'military':
      // Military usa background CSS puro (grid hexagonal + scanlines)
      return (
        <div className="fixed inset-0 pointer-events-none z-0">
          <div className="absolute inset-0 bg-[url('/grid-military.svg')] opacity-10" />
          <div className="absolute inset-0 animate-scanline" />
        </div>
      );
    
    case 'neural':
      // Neural usa efeito de neurônios pulsando (similar ao Quantum mas roxo)
      // RECOMENDAÇÃO: Criar um NeuralBackground.tsx dedicado para o 10/10
      return <QuantumBackground color={themeConfig.colors.primary} />;
    
    case 'titanium':
      // Titanium usa textura de couro + ruído
      return (
        <div className="fixed inset-0 pointer-events-none z-0">
          <div className="absolute inset-0 bg-[url('/leather-texture.svg')] opacity-5" />
          <div className="absolute inset-0 bg-noise opacity-10" />
        </div>
      );
      
    case 'vintage':
      // Vintage usa o componente dedicado para CRT
      return <VintageBackground />;
      
    case 'zen':
      // Zen usa o componente dedicado para papel/minimalismo
      return <ZenBackground />;
    
    default:
      return <QuantumBackground />;
  }
}
