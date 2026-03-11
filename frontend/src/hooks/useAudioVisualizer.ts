/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - AUDIO VISUALIZER HOOK (10/10 EDITION)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/hooks/useAudioVisualizer.ts
 * 🎵 Ondas sonoras + Nível de áudio em tempo real
 * 💎 Visualização premium para o ORION J.A.R.V.I.S.
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useState, useRef, useCallback, useEffect } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface AudioVisualizerState {
  audioLevel: number; // 0-1
  isAnalyzing: boolean;
  frequencyData: number[]; // Para visualização de barras/ondas
}

export interface UseAudioVisualizerReturn {
  state: AudioVisualizerState;
  startAnalysis: (stream: MediaStream) => void;
  stopAnalysis: () => void;
  getPulseScale: () => number;
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export function useAudioVisualizer(): UseAudioVisualizerReturn {
  // ═══ STATE ═══
  const [state, setState] = useState<AudioVisualizerState>({
    audioLevel: 0,
    isAnalyzing: false,
    frequencyData: [],
  });

  // ═══ REFS ═══
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const dataArrayRef = useRef<Uint8Array<ArrayBuffer> | null>(null);

  // ═══════════════════════════════════════════════════════════════════════════════
  // CLEANUP
  // ═══════════════════════════════════════════════════════════════════════════════

  const cleanup = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }

    if (sourceRef.current) {
      sourceRef.current.disconnect();
      sourceRef.current = null;
    }

    if (analyserRef.current) {
      analyserRef.current.disconnect();
      analyserRef.current = null;
    }

    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }

    dataArrayRef.current = null;
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return cleanup;
  }, [cleanup]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // INICIAR ANÁLISE DE ÁUDIO
  // ═══════════════════════════════════════════════════════════════════════════════

  const startAnalysis = useCallback((stream: MediaStream) => {
    if (typeof window === 'undefined') return;

    try {
      // Limpar análise anterior
      cleanup();

      // Criar contexto de áudio
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) {
        console.warn('[Audio Visualizer] AudioContext não suportado');
        return;
      }

      audioContextRef.current = new AudioContextClass();
      analyserRef.current = audioContextRef.current.createAnalyser();

      // Configurar analyser para melhor precisão
      analyserRef.current.fftSize = 256;
      analyserRef.current.smoothingTimeConstant = 0.8;
      analyserRef.current.minDecibels = -90;
      analyserRef.current.maxDecibels = -10;

      // Conectar stream ao analyser
      sourceRef.current = audioContextRef.current.createMediaStreamSource(stream);
      sourceRef.current.connect(analyserRef.current);

      // Criar array para dados de frequência
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);

      setState(prev => ({ ...prev, isAnalyzing: true }));

      // Loop de atualização
      const updateLevel = () => {
        if (!analyserRef.current || !dataArrayRef.current) return;

        analyserRef.current.getByteFrequencyData(dataArrayRef.current);

        // Calcular nível médio (0-1)
        const sum = dataArrayRef.current.reduce((acc, val) => acc + val, 0);
        const average = sum / dataArrayRef.current.length;
        const normalizedLevel = Math.min(average / 255, 1);

        // Pegar primeiros 16 valores para visualização de frequência
        const frequencyData = Array.from(dataArrayRef.current.slice(0, 16)).map(v => v / 255);

        setState(prev => ({
          ...prev,
          audioLevel: normalizedLevel,
          frequencyData,
        }));

        animationFrameRef.current = requestAnimationFrame(updateLevel);
      };

      updateLevel();
      console.log('[Audio Visualizer] Análise iniciada');

    } catch (error) {
      console.error('[Audio Visualizer] Erro ao iniciar análise:', error);
      cleanup();
    }
  }, [cleanup]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // PARAR ANÁLISE
  // ═══════════════════════════════════════════════════════════════════════════════

  const stopAnalysis = useCallback(() => {
    cleanup();
    setState({
      audioLevel: 0,
      isAnalyzing: false,
      frequencyData: [],
    });
    console.log('[Audio Visualizer] Análise parada');
  }, [cleanup]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // CALCULAR ESCALA DE PULSE (para animações)
  // ═══════════════════════════════════════════════════════════════════════════════

  const getPulseScale = useCallback(() => {
    // Retorna um valor entre 1 e 1.3 baseado no nível de áudio
    return 1 + state.audioLevel * 0.3;
  }, [state.audioLevel]);

  return {
    state,
    startAnalysis,
    stopAnalysis,
    getPulseScale,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK AUXILIAR: PULSE ANIMATION
// ═══════════════════════════════════════════════════════════════════════════════

export function useOrionPulse() {
  const [pulseIntensity, setPulseIntensity] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulseIntensity(prev => (prev + 0.1) % (Math.PI * 2));
    }, 50);

    return () => clearInterval(interval);
  }, []);

  const getGlow = useCallback(() => {
    return 0.3 + Math.sin(pulseIntensity) * 0.2;
  }, [pulseIntensity]);

  const getRotation = useCallback(() => {
    return (pulseIntensity * 180) / Math.PI;
  }, [pulseIntensity]);

  const getScale = useCallback(() => {
    return 1 + Math.sin(pulseIntensity) * 0.05;
  }, [pulseIntensity]);

  return {
    pulseIntensity,
    getGlow,
    getRotation,
    getScale,
  };
}

