/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SOUND ENGINE HOOK
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/hooks/useSoundEngine.ts
 * 📋 Sistema de áudio para feedback sensorial dos temas
 * ═══════════════════════════════════════════════════════════════
 */

import { useCallback, useRef, useEffect, useState } from 'react';
import { ThemeConfig } from '@/types/theme';

interface SoundEngineOptions {
  volume?: number;
  enabled?: boolean;
}

export function useSoundEngine(themeConfig: ThemeConfig, options: SoundEngineOptions = {}) {
  const { volume = 0.2, enabled = true } = options;
  
  // Refs para manter instâncias de áudio
  const clickAudioRef = useRef<HTMLAudioElement | null>(null);
  const ambientAudioRef = useRef<HTMLAudioElement | null>(null);
  const hoverAudioRef = useRef<HTMLAudioElement | null>(null);
  
  // Estado para controlar se áudio está habilitado
  const [soundEnabled, setSoundEnabled] = useState(enabled);

  // Pré-carregar sons quando o tema mudar
  useEffect(() => {
    if (!soundEnabled) return;

    // Preload click sound
    if (themeConfig.sound.click) {
      clickAudioRef.current = new Audio(themeConfig.sound.click);
      clickAudioRef.current.volume = volume;
      clickAudioRef.current.load();
    }

    // Preload hover sound
    if (themeConfig.sound.hover) {
      hoverAudioRef.current = new Audio(themeConfig.sound.hover);
      hoverAudioRef.current.volume = volume * 0.5; // Hover mais sutil
      hoverAudioRef.current.load();
    }

    // Preload ambient sound (não tocar automaticamente)
    if (themeConfig.sound.ambient) {
      ambientAudioRef.current = new Audio(themeConfig.sound.ambient);
      ambientAudioRef.current.volume = volume * 0.3; // Ambiente ainda mais sutil
      ambientAudioRef.current.loop = true;
      ambientAudioRef.current.load();
    }

    // Cleanup ao desmontar
    return () => {
      clickAudioRef.current = null;
      hoverAudioRef.current = null;
      if (ambientAudioRef.current) {
        ambientAudioRef.current.pause();
        ambientAudioRef.current = null;
      }
    };
  }, [themeConfig, volume, soundEnabled]);

  // Tocar som de click
  const playClick = useCallback(() => {
    if (!soundEnabled || !clickAudioRef.current) return;
    
    try {
      // Reset e tocar
      clickAudioRef.current.currentTime = 0;
      clickAudioRef.current.play().catch(() => {
        // Ignorar erro se usuário não interagiu ainda (autoplay policy)
      });
    } catch (error) {
      // Silenciosamente falhar
    }
  }, [soundEnabled]);

  // Tocar som de hover
  const playHover = useCallback(() => {
    if (!soundEnabled || !hoverAudioRef.current) return;
    
    try {
      hoverAudioRef.current.currentTime = 0;
      hoverAudioRef.current.play().catch(() => {});
    } catch (error) {
      // Silenciosamente falhar
    }
  }, [soundEnabled]);

  // Tocar/pausar som ambiente
  const toggleAmbient = useCallback((play: boolean) => {
    if (!soundEnabled || !ambientAudioRef.current) return;
    
    try {
      if (play) {
        ambientAudioRef.current.play().catch(() => {});
      } else {
        ambientAudioRef.current.pause();
      }
    } catch (error) {
      // Silenciosamente falhar
    }
  }, [soundEnabled]);

  // Parar todos os sons
  const stopAll = useCallback(() => {
    if (clickAudioRef.current) {
      clickAudioRef.current.pause();
      clickAudioRef.current.currentTime = 0;
    }
    if (hoverAudioRef.current) {
      hoverAudioRef.current.pause();
      hoverAudioRef.current.currentTime = 0;
    }
    if (ambientAudioRef.current) {
      ambientAudioRef.current.pause();
      ambientAudioRef.current.currentTime = 0;
    }
  }, []);

  return {
    playClick,
    playHover,
    toggleAmbient,
    stopAll,
    soundEnabled,
    setSoundEnabled,
  };
}
