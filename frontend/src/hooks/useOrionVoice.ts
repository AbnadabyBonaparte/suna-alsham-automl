/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION VOICE HOOK (10/10 EDITION)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/hooks/useOrionVoice.ts
 * 🎤 Toda lógica de voz: TTS (Text-to-Speech) + Speech Recognition
 * 💎 Tratamento de erros elegante + Fallbacks silenciosos
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useState, useRef, useCallback, useEffect } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface VoiceState {
  isListening: boolean;
  isSpeaking: boolean;
  voiceEnabled: boolean;
  micPermissionDenied: boolean;
  browserSupported: boolean;
  voicesLoaded: boolean;
  currentTranscript: string;
  error: VoiceError | null;
}

export interface VoiceError {
  type: 'mic-denied' | 'mic-not-found' | 'browser-unsupported' | 'network' | 'tts-failed' | 'unknown';
  message: string;
  recoverable: boolean;
}

export interface UseOrionVoiceReturn {
  state: VoiceState;
  startListening: () => Promise<void>;
  stopListening: () => void;
  speak: (text: string) => void;
  cancelSpeech: () => void;
  toggleVoice: () => void;
  clearError: () => void;
  getMediaStream: () => MediaStream | null;
}

// ═══════════════════════════════════════════════════════════════════════════════
// WEB SPEECH API TYPES
// ═══════════════════════════════════════════════════════════════════════════════

interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message?: string;
}

interface SpeechRecognitionResult {
  isFinal: boolean;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  maxAlternatives: number;
  onstart: ((this: SpeechRecognition, ev: Event) => void) | null;
  onend: ((this: SpeechRecognition, ev: Event) => void) | null;
  onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => void) | null;
  onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => void) | null;
  start(): void;
  stop(): void;
  abort(): void;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
    webkitAudioContext: typeof AudioContext;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export function useOrionVoice(
  onTranscriptComplete?: (transcript: string) => void
): UseOrionVoiceReturn {
  // ═══ STATE ═══
  const [state, setState] = useState<VoiceState>({
    isListening: false,
    isSpeaking: false,
    voiceEnabled: true,
    micPermissionDenied: false,
    browserSupported: false,
    voicesLoaded: false,
    currentTranscript: '',
    error: null,
  });

  // ═══ REFS ═══
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const onTranscriptCompleteRef = useRef(onTranscriptComplete);

  // Manter ref atualizada
  useEffect(() => {
    onTranscriptCompleteRef.current = onTranscriptComplete;
  }, [onTranscriptComplete]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // INICIALIZAÇÃO
  // ═══════════════════════════════════════════════════════════════════════════════

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Verificar suporte do navegador
    const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
    const browserSupported = !!SpeechRecognitionAPI && !!window.speechSynthesis;

    setState(prev => ({ ...prev, browserSupported }));

    if (!browserSupported) {
      console.warn('[ORION Voice] Navegador não suporta Web Speech API');
      setState(prev => ({
        ...prev,
        error: {
          type: 'browser-unsupported',
          message: 'Seu navegador não suporta reconhecimento de voz. Use Chrome, Edge ou Safari.',
          recoverable: false,
        },
      }));
      return;
    }

    // Inicializar síntese de voz
    synthRef.current = window.speechSynthesis;

    const loadVoices = () => {
      const voices = synthRef.current?.getVoices();
      if (voices && voices.length > 0) {
        setState(prev => ({ ...prev, voicesLoaded: true }));
        console.log('[ORION Voice] Vozes carregadas:', voices.length);
      }
    };

    loadVoices();
    if (synthRef.current) {
      synthRef.current.onvoiceschanged = loadVoices;
    }

    // Cleanup
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
      if (synthRef.current) {
        synthRef.current.cancel();
      }
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // CLEAR ERROR
  // ═══════════════════════════════════════════════════════════════════════════════

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // TEXT-TO-SPEECH (VOZ J.A.R.V.I.S.)
  // ═══════════════════════════════════════════════════════════════════════════════

  const speak = useCallback((text: string) => {
    if (!synthRef.current || !state.voiceEnabled) {
      console.log('[ORION Voice] TTS desabilitado ou indisponível');
      return;
    }

    try {
      // Cancelar fala anterior
      synthRef.current.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-BR';
      utterance.rate = 0.92; // Velocidade elegante
      utterance.pitch = 0.75; // Voz grave J.A.R.V.I.S.
      utterance.volume = 1.0;

      // Encontrar melhor voz masculina brasileira
      const voices = synthRef.current.getVoices();
      const voicePriorities = [
        'Google português do Brasil',
        'Microsoft Daniel',
        'Daniel',
        'Luciano',
        'pt-BR-Wavenet-B',
        'pt-BR-Standard-B',
      ];

      let selectedVoice = voices.find(v =>
        voicePriorities.some(prio => v.name.toLowerCase().includes(prio.toLowerCase()))
      );

      if (!selectedVoice) {
        selectedVoice = voices.find(v => v.lang.includes('pt-BR'));
      }
      if (!selectedVoice) {
        selectedVoice = voices.find(v => v.lang.includes('pt'));
      }
      if (!selectedVoice && voices.length > 0) {
        selectedVoice = voices[0];
      }

      if (selectedVoice) {
        utterance.voice = selectedVoice;
      }

      utterance.onstart = () => {
        setState(prev => ({ ...prev, isSpeaking: true }));
      };

      utterance.onend = () => {
        setState(prev => ({ ...prev, isSpeaking: false }));
      };

      utterance.onerror = (event) => {
        console.error('[ORION Voice] TTS error:', event);
        setState(prev => ({
          ...prev,
          isSpeaking: false,
          // Fallback silencioso - não mostrar erro para TTS
        }));
      };

      synthRef.current.speak(utterance);
    } catch (error) {
      console.error('[ORION Voice] TTS exception:', error);
      setState(prev => ({ ...prev, isSpeaking: false }));
      // Fallback silencioso
    }
  }, [state.voiceEnabled]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // CANCELAR FALA
  // ═══════════════════════════════════════════════════════════════════════════════

  const cancelSpeech = useCallback(() => {
    if (synthRef.current) {
      synthRef.current.cancel();
      setState(prev => ({ ...prev, isSpeaking: false }));
    }
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // TOGGLE VOICE
  // ═══════════════════════════════════════════════════════════════════════════════

  const toggleVoice = useCallback(() => {
    setState(prev => {
      if (prev.voiceEnabled && synthRef.current) {
        synthRef.current.cancel();
      }
      return { ...prev, voiceEnabled: !prev.voiceEnabled };
    });
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // INICIAR RECONHECIMENTO DE VOZ
  // ═══════════════════════════════════════════════════════════════════════════════

  const startListening = useCallback(async () => {
    console.log('[ORION Voice] Iniciando reconhecimento...');

    // Verificar suporte
    if (!state.browserSupported) {
      setState(prev => ({
        ...prev,
        error: {
          type: 'browser-unsupported',
          message: 'Seu navegador não suporta reconhecimento de voz. Use Chrome, Edge ou Safari.',
          recoverable: false,
        },
      }));
      return;
    }

    const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;

    // Parar TTS se estiver falando
    if (synthRef.current) {
      synthRef.current.cancel();
    }

    try {
      // Pedir permissão de microfone
      console.log('[ORION Voice] Solicitando permissão de microfone...');
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      console.log('[ORION Voice] Permissão concedida!');
      mediaStreamRef.current = stream;

      // Criar instância do reconhecimento
      const recognition = new SpeechRecognitionAPI();
      recognition.lang = 'pt-BR';
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.maxAlternatives = 3;

      recognition.onstart = () => {
        console.log('[ORION Voice] Reconhecimento iniciado');
        setState(prev => ({
          ...prev,
          isListening: true,
          micPermissionDenied: false,
          error: null,
          currentTranscript: '',
        }));
      };

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i];
          const transcript = result[0].transcript;

          if (result.isFinal) {
            finalTranscript += transcript;
            console.log('[ORION Voice] Final:', transcript, 'Confiança:', result[0].confidence);
          } else {
            interimTranscript += transcript;
          }
        }

        const currentText = finalTranscript || interimTranscript;
        setState(prev => ({ ...prev, currentTranscript: currentText }));

        if (finalTranscript && onTranscriptCompleteRef.current) {
          setTimeout(() => {
            onTranscriptCompleteRef.current?.(finalTranscript.trim());
            setState(prev => ({ ...prev, currentTranscript: '' }));
          }, 300);
        }
      };

      recognition.onend = () => {
        console.log('[ORION Voice] Reconhecimento finalizado');
        setState(prev => ({ ...prev, isListening: false }));

        // Limpar stream
        if (mediaStreamRef.current) {
          mediaStreamRef.current.getTracks().forEach(track => track.stop());
          mediaStreamRef.current = null;
        }
      };

      recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('[ORION Voice] Erro:', event.error);

        let error: VoiceError | null = null;

        switch (event.error) {
          case 'not-allowed':
          case 'permission-denied':
            error = {
              type: 'mic-denied',
              message: 'Permissão de microfone negada. Clique no cadeado na barra de endereços para permitir.',
              recoverable: true,
            };
            setState(prev => ({ ...prev, micPermissionDenied: true }));
            break;
          case 'no-speech':
            // Não é um erro real, usuário só não falou
            console.log('[ORION Voice] Nenhuma fala detectada');
            break;
          case 'network':
            error = {
              type: 'network',
              message: 'Erro de rede. Verifique sua conexão com a internet.',
              recoverable: true,
            };
            break;
          case 'aborted':
            // Usuário cancelou, não mostrar erro
            break;
          default:
            error = {
              type: 'unknown',
              message: `Erro no reconhecimento: ${event.error}`,
              recoverable: true,
            };
        }

        setState(prev => ({
          ...prev,
          isListening: false,
          error: error,
        }));

        // Limpar stream
        if (mediaStreamRef.current) {
          mediaStreamRef.current.getTracks().forEach(track => track.stop());
          mediaStreamRef.current = null;
        }
      };

      recognitionRef.current = recognition;
      recognition.start();

    } catch (error: unknown) {
      console.error('[ORION Voice] Erro ao acessar microfone:', error);

      const err = error as Error & { name?: string };
      let voiceError: VoiceError;

      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        voiceError = {
          type: 'mic-denied',
          message: 'Acesso ao microfone bloqueado. Clique no cadeado na barra de endereços para permitir.',
          recoverable: true,
        };
        setState(prev => ({ ...prev, micPermissionDenied: true }));
      } else if (err.name === 'NotFoundError') {
        voiceError = {
          type: 'mic-not-found',
          message: 'Nenhum microfone encontrado. Conecte um microfone e tente novamente.',
          recoverable: true,
        };
      } else {
        voiceError = {
          type: 'unknown',
          message: err.message || 'Erro desconhecido ao acessar microfone.',
          recoverable: true,
        };
      }

      setState(prev => ({
        ...prev,
        isListening: false,
        error: voiceError,
      }));

      // Limpar stream se existir
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(track => track.stop());
        mediaStreamRef.current = null;
      }
    }
  }, [state.browserSupported]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // PARAR RECONHECIMENTO
  // ═══════════════════════════════════════════════════════════════════════════════

  const stopListening = useCallback(() => {
    console.log('[ORION Voice] Parando reconhecimento...');

    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      mediaStreamRef.current = null;
    }

    setState(prev => ({ ...prev, isListening: false }));
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // GET MEDIA STREAM (para visualização de áudio)
  // ═══════════════════════════════════════════════════════════════════════════════

  const getMediaStream = useCallback(() => {
    return mediaStreamRef.current;
  }, []);

  return {
    state,
    startListening,
    stopListening,
    speak,
    cancelSpeech,
    toggleVoice,
    clearError,
    getMediaStream,
  };
}
