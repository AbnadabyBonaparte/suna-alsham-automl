// frontend/src/components/backgrounds/RealityBackground.tsx
// Reality Codex - Background Switcher
// Source: ALSHAM_QUANTUM_REALIDADES_VISUAIS_ULTIMATE_v3.md

'use client';

import React from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { QuantumBackground } from './QuantumBackground';
import { AscensionBackground } from './AscensionBackground';

const BACKGROUND_MAP: Record<string, React.ComponentType> = {
  quantum: QuantumBackground,
  ascension: AscensionBackground,
  // Futuros temas serão adicionados aqui:
  // military: MilitaryBackground,
  // neural: NeuralBackground,
  // titanium: TitaniumBackground,
};

export function RealityBackground() {
  const { theme } = useTheme();
  
  const BackgroundComponent = BACKGROUND_MAP[theme] || QuantumBackground;
  
  return <BackgroundComponent />;
}

export default RealityBackground;
