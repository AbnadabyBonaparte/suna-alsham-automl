/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - GLOBAL KEY LISTENER
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/layout/GlobalKeyListener.tsx
 * 📋 ATALHOS: Alt+Shift+T (trocar tema), Alt+Shift+G (god mode)
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useEffect } from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { useRouter } from 'next/navigation';

export function GlobalKeyListener() {
  const { cycleTheme } = useTheme();
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Alt + Shift + T = Trocar Tema
      if (event.altKey && event.shiftKey && event.key === 'T') {
        event.preventDefault();
        cycleTheme();
        
        // Feedback visual
        const flash = document.createElement('div');
        flash.style.cssText = `
          position: fixed;
          inset: 0;
          background: var(--color-primary);
          opacity: 0.2;
          pointer-events: none;
          z-index: 9999;
          animation: flashTheme 0.3s ease-out;
        `;
        document.body.appendChild(flash);
        setTimeout(() => flash.remove(), 300);
      }

      // Alt + Shift + G = God Mode (Bonaparte)
      if (event.altKey && event.shiftKey && event.key === 'G') {
        event.preventDefault();
        router.push('/bonaparte');
      }

      // Alt + Shift + S = Singularity
      if (event.altKey && event.shiftKey && event.key === 'S') {
        event.preventDefault();
        router.push('/dashboard/singularity');
      }

      // Alt + Shift + H = Home
      if (event.altKey && event.shiftKey && event.key === 'H') {
        event.preventDefault();
        router.push('/dashboard');
      }

      // Esc = Close modals/overlays
      if (event.key === 'Escape') {
        const activeElement = document.activeElement as HTMLElement;
        if (activeElement && activeElement.blur) {
          activeElement.blur();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    // Adicionar estilo de animação
    if (!document.getElementById('flash-theme-style')) {
      const style = document.createElement('style');
      style.id = 'flash-theme-style';
      style.textContent = `
        @keyframes flashTheme {
          0% { opacity: 0.2; }
          50% { opacity: 0.4; }
          100% { opacity: 0; }
        }
      `;
      document.head.appendChild(style);
    }

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [cycleTheme, router]);

  return null;
}
