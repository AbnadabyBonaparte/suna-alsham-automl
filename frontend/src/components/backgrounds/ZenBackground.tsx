/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ZEN GARDEN BACKGROUND
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/backgrounds/ZenBackground.tsx
 * 📋 Fundo minimalista com textura de papel e sombras suaves.
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React from 'react';

export function ZenBackground() {
  return (
    <div 
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden"
      style={{ background: 'var(--color-background)' }}
      aria-hidden="true"
    >
      {/* 1. Textura de Papel/Areia (Zen Paper Texture) */}
      <div className="zen-paper-texture" />
      
      {/* 2. Sombra suave no centro (para dar profundidade) */}
      <div 
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] h-[80%] rounded-full"
        style={{
          boxShadow: '0 0 100px 50px rgba(0, 0, 0, 0.05) inset',
          pointerEvents: 'none',
          opacity: 0.5,
        }}
      />
      
      {/* 3. Gradiente sutil para simular luz natural */}
      <div 
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(circle at 50% 10%, rgba(255, 255, 255, 0.5) 0%, transparent 30%)',
          pointerEvents: 'none',
          opacity: 0.3,
        }}
      />
    </div>
  );
}

export default ZenBackground;
