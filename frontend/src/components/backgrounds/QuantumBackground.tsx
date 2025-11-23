// frontend/src/components/backgrounds/QuantumBackground.tsx
// Reality Codex - Quantum Lab Background
// Source: ALSHAM_QUANTUM_REALIDADES_VISUAIS_ULTIMATE_v3.md

'use client';

import React, { useEffect, useRef, useState } from 'react';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import './QuantumBackground.css';

// Configurações de performance
const CONFIG = {
  particleCount: 30,
  canvasParticles: 100,
  connectionDistance: 150,
  mouseInfluence: 100,
};

export function QuantumBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const prefersReducedMotion = useReducedMotion();
  const [useCanvas, setUseCanvas] = useState(false);

  // Detectar se device suporta Canvas performático
  useEffect(() => {
    if (prefersReducedMotion) return;

    const checkPerformance = () => {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl');
      if (!gl) return false;

      if ('getBattery' in navigator) {
        (navigator as any).getBattery().then((battery: any) => {
          if (battery.level < 0.2 && !battery.charging) {
            setUseCanvas(false);
          }
        });
      }

      return true;
    };

    setUseCanvas(checkPerformance());
  }, [prefersReducedMotion]);

  // Canvas particles (enhancement progressivo)
  useEffect(() => {
    if (!useCanvas || !canvasRef.current || prefersReducedMotion) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
      opacity: number;
    }> = [];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const initParticles = () => {
      particles = Array.from({ length: CONFIG.canvasParticles }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1,
        opacity: Math.random() * 0.5 + 0.2,
      }));
    };

    let mouseX = 0;
    let mouseY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach((p, i) => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        const dx = mouseX - p.x;
        const dy = mouseY - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < CONFIG.mouseInfluence) {
          const force = (CONFIG.mouseInfluence - dist) / CONFIG.mouseInfluence;
          p.vx -= (dx / dist) * force * 0.02;
          p.vy -= (dy / dist) * force * 0.02;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 255, 200, ${p.opacity})`;
        ctx.fill();

        particles.slice(i + 1).forEach((p2) => {
          const d = Math.hypot(p.x - p2.x, p.y - p2.y);
          if (d < CONFIG.connectionDistance) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(0, 255, 200, ${0.1 * (1 - d / CONFIG.connectionDistance)})`;
            ctx.stroke();
          }
        });
      });

      animationId = requestAnimationFrame(animate);
    };

    resize();
    initParticles();
    animate();

    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, [useCanvas, prefersReducedMotion]);

  // CSS particles
  const cssParticles = Array.from({ length: CONFIG.particleCount }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    delay: i * 0.3,
    duration: 15 + Math.random() * 10,
    size: Math.random() * 2 + 2,
  }));

  return (
    <div className="quantum-bg" aria-hidden="true">
      {/* Grid base */}
      <div className="quantum-grid" />

      {/* CSS Particles (fallback) */}
      {!useCanvas &&
        cssParticles.map((p) => (
          <div
            key={p.id}
            className="quantum-particle"
            style={{
              left: `${p.x}%`,
              top: `${p.y}%`,
              width: p.size,
              height: p.size,
              ['--delay' as any]: `${p.delay}s`,
              ['--duration' as any]: `${p.duration}s`,
            }}
          />
        ))}

      {/* Canvas particles (enhancement) */}
      {useCanvas && (
        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full"
        />
      )}

      {/* Core glow */}
      <div className="quantum-core-glow" />

      {/* Vignette */}
      <div className="quantum-vignette" />
    </div>
  );
}

export default QuantumBackground;
