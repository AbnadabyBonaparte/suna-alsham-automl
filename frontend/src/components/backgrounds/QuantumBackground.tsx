/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - QUANTUM LAB BACKGROUND (MULTI-COLOR CORE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/backgrounds/QuantumBackground.tsx
 * 📋 Partículas quânticas flutuando em Canvas HTML5.
 * 📋 Suporta cores dinâmicas para reutilização em Neural/Cobalt/Crimson.
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React, { useEffect, useRef } from 'react';

interface QuantumBackgroundProps {
  color?: string; // Cor primária das partículas (Hex)
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
  pulsePhase: number;
}

export default function QuantumBackground({ color = '#00FFD0' }: QuantumBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Função para converter HEX para RGB
    const hexToRgb = (hex: string) => {
      // Remove o # se existir
      hex = hex.replace(/^#/, '');
      
      // Expande short hex (ex: '03F' -> '0033FF')
      if (hex.length === 3) {
        hex = hex.split('').map(char => char + char).join('');
      }

      const bigint = parseInt(hex, 16);
      const r = (bigint >> 16) & 255;
      const g = (bigint >> 8) & 255;
      const b = bigint & 255;

      return { r, g, b };
    };

    const rgb = hexToRgb(color);

    // Configurar tamanho do canvas
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Criar partículas (Quantidade baseada no tamanho da tela)
    const particleCount = Math.min(Math.floor((window.innerWidth * window.innerHeight) / 15000), 100);
    
    particlesRef.current = Array.from({ length: particleCount }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      radius: Math.random() * 2 + 1,
      opacity: Math.random() * 0.5 + 0.3,
      pulsePhase: Math.random() * Math.PI * 2,
    }));

    // Animação Loop
    const animate = () => {
      if (!ctx || !canvas) return;

      // Limpar canvas com rastro suave (trail effect)
      ctx.fillStyle = `rgba(0, 0, 0, 0.1)`; // Aumentei um pouco a opacidade para limpar mais rápido
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const particles = particlesRef.current;

      // Desenhar conexões entre partículas próximas
      ctx.lineWidth = 0.5;

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          // Conexão apenas se estiver perto (150px)
          if (distance < 150) {
            const opacity = (1 - distance / 150) * 0.2;
            ctx.beginPath();
            ctx.strokeStyle = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${opacity})`;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }

      // Desenhar e atualizar partículas
      particles.forEach((particle) => {
        // Atualizar posição
        particle.x += particle.vx;
        particle.y += particle.vy;

        // Efeito de pulso (brilho oscilante)
        particle.pulsePhase += 0.05;
        const pulseOpacity = Math.sin(particle.pulsePhase) * 0.2 + particle.opacity;

        // Wrap around nas bordas (teletransporte estilo Pac-Man)
        if (particle.x < 0) particle.x = canvas.width;
        if (particle.x > canvas.width) particle.x = 0;
        if (particle.y < 0) particle.y = canvas.height;
        if (particle.y > canvas.height) particle.y = 0;

        // Desenhar Glow da Partícula
        const gradient = ctx.createRadialGradient(
          particle.x,
          particle.y,
          0,
          particle.x,
          particle.y,
          particle.radius * 4 // Glow maior
        );
        gradient.addColorStop(0, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${pulseOpacity})`);
        gradient.addColorStop(0.4, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${pulseOpacity * 0.3})`);
        gradient.addColorStop(1, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0)`);

        ctx.beginPath();
        ctx.fillStyle = gradient;
        ctx.arc(particle.x, particle.y, particle.radius * 4, 0, Math.PI * 2);
        ctx.fill();

        // Desenhar Núcleo Sólido (Branco brilhante)
        ctx.beginPath();
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.min(pulseOpacity + 0.2, 1)})`;
        ctx.arc(particle.x, particle.y, particle.radius * 0.6, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animate();

    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [color]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      // Gradiente de fundo sutil para dar profundidade, mas permitindo que a cor de fundo do CSS brilhe
      style={{ 
        background: 'transparent',
      }}
      aria-hidden="true"
    />
  );
}
