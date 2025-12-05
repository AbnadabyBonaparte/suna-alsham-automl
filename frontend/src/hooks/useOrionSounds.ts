/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION SOUNDS HOOK (10/10 EDITION)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/hooks/useOrionSounds.ts
 * 🔊 Sons premium estilo Iron Man / J.A.R.V.I.S.
 * 💎 Ativação, listening, response, error, success
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useCallback, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export type SoundType = 'activate' | 'listening' | 'response' | 'error' | 'click' | 'success' | 'wakeup';

export interface UseOrionSoundsReturn {
  playSound: (type: SoundType) => void;
  isSupported: boolean;
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export function useOrionSounds(): UseOrionSoundsReturn {
  const audioContextRef = useRef<AudioContext | null>(null);

  // ═══════════════════════════════════════════════════════════════════════════════
  // GET/CREATE AUDIO CONTEXT
  // ═══════════════════════════════════════════════════════════════════════════════

  const getAudioContext = useCallback((): AudioContext | null => {
    if (typeof window === 'undefined') return null;

    try {
      if (!audioContextRef.current || audioContextRef.current.state === 'closed') {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
          audioContextRef.current = new AudioContextClass();
        }
      }

      // Resume se estiver suspenso
      if (audioContextRef.current?.state === 'suspended') {
        audioContextRef.current.resume();
      }

      return audioContextRef.current;
    } catch {
      return null;
    }
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // PLAY SOUND
  // ═══════════════════════════════════════════════════════════════════════════════

  const playSound = useCallback((type: SoundType) => {
    const audioContext = getAudioContext();
    if (!audioContext) return;

    try {
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      const now = audioContext.currentTime;

      switch (type) {
        // ═══ ATIVAÇÃO ESTILO IRON MAN ═══
        case 'activate':
          oscillator.type = 'sine';
          oscillator.frequency.setValueAtTime(523.25, now); // C5
          oscillator.frequency.exponentialRampToValueAtTime(783.99, now + 0.1); // G5
          oscillator.frequency.exponentialRampToValueAtTime(1046.50, now + 0.2); // C6
          oscillator.frequency.exponentialRampToValueAtTime(1318.51, now + 0.3); // E6
          gainNode.gain.setValueAtTime(0.12, now);
          gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
          oscillator.start(now);
          oscillator.stop(now + 0.5);
          break;

        // ═══ WAKEUP - "ACORDAR" QUANDO DIZ "ORION" ═══
        case 'wakeup':
          oscillator.type = 'sine';
          // Acorde majestoso ascendente
          oscillator.frequency.setValueAtTime(261.63, now); // C4
          oscillator.frequency.exponentialRampToValueAtTime(329.63, now + 0.08); // E4
          oscillator.frequency.exponentialRampToValueAtTime(392.00, now + 0.16); // G4
          oscillator.frequency.exponentialRampToValueAtTime(523.25, now + 0.24); // C5
          oscillator.frequency.exponentialRampToValueAtTime(659.25, now + 0.32); // E5
          gainNode.gain.setValueAtTime(0.1, now);
          gainNode.gain.setValueAtTime(0.12, now + 0.16);
          gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
          oscillator.start(now);
          oscillator.stop(now + 0.5);
          break;

        // ═══ ESCUTANDO ═══
        case 'listening':
          oscillator.type = 'sine';
          oscillator.frequency.setValueAtTime(880, now);
          oscillator.frequency.exponentialRampToValueAtTime(1100, now + 0.1);
          gainNode.gain.setValueAtTime(0.08, now);
          gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          oscillator.start(now);
          oscillator.stop(now + 0.2);
          break;

        // ═══ RESPOSTA ELEGANTE ═══
        case 'response':
          oscillator.type = 'sine';
          oscillator.frequency.setValueAtTime(659.25, now); // E5
          oscillator.frequency.exponentialRampToValueAtTime(783.99, now + 0.1); // G5
          oscillator.frequency.exponentialRampToValueAtTime(880, now + 0.2); // A5
          gainNode.gain.setValueAtTime(0.08, now);
          gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
          oscillator.start(now);
          oscillator.stop(now + 0.3);
          break;

        // ═══ CLICK MINIMALISTA ═══
        case 'click':
          oscillator.type = 'sine';
          oscillator.frequency.setValueAtTime(1200, now);
          gainNode.gain.setValueAtTime(0.04, now);
          gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
          oscillator.start(now);
          oscillator.stop(now + 0.05);
          break;

        // ═══ SUCESSO ═══
        case 'success':
          oscillator.type = 'sine';
          oscillator.frequency.setValueAtTime(523.25, now); // C5
          oscillator.frequency.exponentialRampToValueAtTime(659.25, now + 0.1); // E5
          oscillator.frequency.exponentialRampToValueAtTime(783.99, now + 0.2); // G5
          oscillator.frequency.exponentialRampToValueAtTime(1046.50, now + 0.3); // C6
          gainNode.gain.setValueAtTime(0.1, now);
          gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
          oscillator.start(now);
          oscillator.stop(now + 0.4);
          break;

        // ═══ ERRO GRAVE ═══
        case 'error':
          oscillator.type = 'sawtooth';
          oscillator.frequency.setValueAtTime(200, now);
          oscillator.frequency.exponentialRampToValueAtTime(100, now + 0.3);
          gainNode.gain.setValueAtTime(0.08, now);
          gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
          oscillator.start(now);
          oscillator.stop(now + 0.4);
          break;
      }
    } catch (error) {
      // Fallback silencioso - não quebrar a UX por causa de som
      console.log('[ORION Sounds] Audio not available:', error);
    }
  }, [getAudioContext]);

  // Verificar se é suportado
  const isSupported = typeof window !== 'undefined' && 
    !!(window.AudioContext || window.webkitAudioContext);

  return {
    playSound,
    isSupported,
  };
}

