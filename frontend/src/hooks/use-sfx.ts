"use client";

import { useCallback } from 'react';

export function useSfx() {
  const play = useCallback((sound: 'click' | 'hover' | 'alert' | 'ambient') => {
    if (typeof window === 'undefined') return; // Proteção Server-Side

    try {
      // Tenta tocar o som da pasta public/sounds
      const audio = new Audio(`/sounds/${sound}.mp3`);
      audio.volume = 0.4; // Volume agradável (não muito alto)
      
      const playPromise = audio.play();
      
      if (playPromise !== undefined) {
        playPromise.catch((error) => {
          // Ignora erros de "user didn't interact yet" comuns em browsers
          // console.warn("Audio playback prevented:", error);
        });
      }
    } catch (e) {
      // Falha silenciosa para não quebrar a UI
    }
  }, []);

  return { play };
}
