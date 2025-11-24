/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - VINTAGE TERMINAL BACKGROUND
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/backgrounds/VintageBackground.tsx
 * 📋 Simula a tela de um terminal CRT com scanlines e ruído.
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React from 'react';

export function VintageBackground() {
  return (
    <div 
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden"
      style={{ background: 'var(--color-background)' }}
      aria-hidden="true"
    >
      {/* 1. CRT Noise (Ruído Estático) */}
      <div className="vintage-noise" />
      
      {/* 2. Scanlines (Linhas de Varredura) */}
      <div className="vintage-scanlines" />
      
      {/* 3. Vinheta (Escurecimento nas bordas) */}
      <div 
        className="absolute inset-0"
        style={{
          boxShadow: 'inset 0 0 100px rgba(0, 0, 0, 0.8)',
          pointerEvents: 'none',
        }}
      />
      
      {/* 4. Efeito de Curvatura (Opcional, para telas mais antigas) */}
      <div 
        className="absolute inset-0"
        style={{
          borderRadius: '50%',
          boxShadow: '0 0 100px rgba(0, 0, 0, 0.8) inset',
          transform: 'scale(1.1)',
          pointerEvents: 'none',
          opacity: 0.2,
        }}
      />
    </div>
  );
}

export default VintageBackground;
