import os

code = r"""'use client';

import { useCallback } from 'react';

export function useSfx() {
  const play = useCallback((sound: 'click' | 'hover' | 'alert' | 'ambient') => {
    if (typeof window === 'undefined') return; // Proteção Server-Side

    try {
      const audio = new Audio(`/sounds/${sound}.mp3`);
      audio.volume = 0.4;
      
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch(() => {
          // Ignora erros de interação do navegador
        });
      }
    } catch (e) {
      // Silêncio em caso de erro
    }
  }, []);

  return { play };
}
"""

with open("src/hooks/use-sfx.ts", "w") as f:
    f.write(code)

print("✅ Hook de Som (use-sfx.ts) restaurado com integridade.")
