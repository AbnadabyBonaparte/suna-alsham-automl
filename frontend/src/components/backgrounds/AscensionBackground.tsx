/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - LUMINOUS ASCENSION BACKGROUND
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/backgrounds/AscensionBackground.tsx
 * 📋 God rays dourados com partículas de luz flutuando
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React, { useEffect, useRef } from 'react';

interface LightParticle {
  x: number;
  y: number;
  vy: number;
  opacity: number;
  radius: number;
}

export function AscensionBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<LightParticle[]>([]);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Criar partículas de luz
    const particleCount = 50;
    particlesRef.current = Array.from({ length: particleCount }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vy: Math.random() * -0.5 - 0.2, // Subindo
      opacity: Math.random() * 0.6 + 0.2,
      radius: Math.random() * 3 + 1,
    }));

    const animate = () => {
      if (!ctx || !canvas) return;

      // Limpar com fade suave
      ctx.fillStyle = 'rgba(248, 250, 252, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const particles = particlesRef.current;

      particles.forEach((particle) => {
        // Atualizar posição
        particle.y += particle.vy;

        // Reset partícula quando sair da tela
        if (particle.y < -10) {
          particle.y = canvas.height + 10;
          particle.x = Math.random() * canvas.width;
        }

        // Desenhar partícula com glow dourado
        const gradient = ctx.createRadialGradient(
          particle.x,
          particle.y,
          0,
          particle.x,
          particle.y,
          particle.radius * 4
        );
        gradient.addColorStop(0, `rgba(255, 215, 0, ${particle.opacity})`);
        gradient.addColorStop(0.5, `rgba(255, 165, 0, ${particle.opacity * 0.5})`);
        gradient.addColorStop(1, 'rgba(255, 215, 0, 0)');

        ctx.beginPath();
        ctx.fillStyle = gradient;
        ctx.arc(particle.x, particle.y, particle.radius * 4, 0, Math.PI * 2);
        ctx.fill();

        // Núcleo branco brilhante
        ctx.beginPath();
        ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity * 0.8})`;
        ctx.arc(particle.x, particle.y, particle.radius * 0.8, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  return (
    <>
      {/* Background base com gradiente */}
      <div
        className="fixed inset-0 pointer-events-none z-0"
        style={{
          background: 'linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)',
        }}
        aria-hidden="true"
      />

      {/* God Rays (Raios divinos) */}
      <div
        className="fixed inset-0 pointer-events-none z-0"
        style={{
          background: `
            radial-gradient(ellipse at 50% 0%, rgba(255, 215, 0, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 20% 20%, rgba(255, 215, 0, 0.08) 0%, transparent 40%),
            radial-gradient(ellipse at 80% 30%, rgba(255, 215, 0, 0.08) 0%, transparent 40%)
          `,
          opacity: 0.6,
        }}
        aria-hidden="true"
      />

      {/* Canvas com partículas */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 pointer-events-none z-0"
        aria-hidden="true"
      />
    </>
  );
}

export default AscensionBackground;
