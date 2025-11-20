'use client';

import { useCallback } from 'react';

// Mapeamento simples de sons
const SOUNDS = {
  click: '/sounds/click_mechanical.mp3',
  hover: '/sounds/hover_hum.mp3',
  success: '/sounds/success_chime.mp3',
  alert: '/sounds/alert_error.mp3',
  boot: '/sounds/boot_sequence.mp3',
};

export function useSFX() {
  const play = useCallback((type: keyof typeof SOUNDS) => {
    try {
      const audio = new Audio(SOUNDS[type]);
      audio.volume = 0.3; 
      audio.play().catch(() => {
        // Ignora erros se o arquivo nao existir
      });
    } catch (err) {
      console.warn('Audio playback failed', err);
    }
  }, []);

  return { play };
}
