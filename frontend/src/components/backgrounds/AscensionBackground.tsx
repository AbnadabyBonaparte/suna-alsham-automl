// frontend/src/components/backgrounds/AscensionBackground.tsx
// Reality Codex - Luminous Ascension Background
// Source: ALSHAM_QUANTUM_REALIDADES_VISUAIS_ULTIMATE_v3.md

'use client';

import React from 'react';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import './AscensionBackground.css';

export function AscensionBackground() {
  const prefersReducedMotion = useReducedMotion();

  // God Rays configuration
  const rays = Array.from({ length: 7 }, (_, i) => ({
    id: i,
    left: 10 + i * 15,
    width: 50 + i * 20,
    duration: 8 + i,
    delay: i * 0.5,
  }));

  // Golden particles configuration
  const particles = Array.from({ length: 25 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    delay: Math.random() * 5,
    duration: 8 + Math.random() * 4,
    size: Math.random() * 4 + 2,
  }));

  return (
    <div className="ascension-bg" aria-hidden="true">
      {/* Subtle grid */}
      <div className="ascension-grid" />

      {/* God Rays */}
      {!prefersReducedMotion && (
        <div className="absolute inset-0">
          {rays.map((ray) => (
            <div
              key={ray.id}
              className="ascension-ray"
              style={{
                left: `${ray.left}%`,
                width: `${ray.width}px`,
                ['--duration' as any]: `${ray.duration}s`,
                ['--delay' as any]: `${ray.delay}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Golden particles */}
      {!prefersReducedMotion && (
        <div className="absolute inset-0 overflow-hidden">
          {particles.map((p) => (
            <div
              key={p.id}
              className="ascension-particle"
              style={{
                left: `${p.x}%`,
                width: p.size,
                height: p.size,
                ['--duration' as any]: `${p.duration}s`,
                ['--delay' as any]: `${p.delay}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Central glow */}
      <div className="ascension-glow" />

      {/* Soft vignette */}
      <div className="ascension-vignette" />
    </div>
  );
}

export default AscensionBackground;
