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

// Define o tipo para a API de Reconhecimento de Voz, que pode ter prefixos
type SpeechRecognitionType = typeof window.SpeechRecognition | typeof window.webkitSpeechRecognition | undefined;
const SpeechRecognition = (window.SpeechRecognition || window.webkitSpeechRecognition) as SpeechRecognitionType;

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
  // Usamos o tipo global SpeechRecognition que foi definido acima
  const recognitionRef = useRef<globalThis.SpeechRecognition | null>(null);
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
    const browserSupported = !!SpeechRecognition && !!window.speechSynthesis;

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
      // Garante que o stream do microfone seja parado
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(track => track.stop());
        mediaStreamRef.current = null;
      }
    };
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // CLEAR ERROR
  // ═══════════════════════════════════════════════════════════════════════════════

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null, micPermissionDenied: false }));
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // TEXT-TO-SPEECH (VOZ J.A.R.V.I.S.)
  // ═══════════════════════════════════════════════════════════════════════════════

  const speak = useCallback((text: string) => {
    if (!synthRef.current || !state.voiceEnabled) {
      // Fallback silencioso
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

      utterance.onerror = () => {
        // Fallback silencioso - não mostrar erro para TTS
        setState(prev => ({ ...prev, isSpeaking: false }));
      };

      synthRef.current.speak(utterance);
    } catch (error) {
      // Fallback silencioso
      setState(prev => ({ ...prev, isSpeaking: false }));
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
    if (!state.browserSupported) {
      // O erro já foi setado na inicialização
      return;
    }

    // Parar TTS se estiver falando
    if (synthRef.current) {
      synthRef.current.cancel();
    }

    // Limpar transcrição anterior
    setState(prev => ({ ...prev, currentTranscript: '', error: null, micPermissionDenied: false }));

    try {
      // 1. Pedir permissão de microfone e obter stream
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      mediaStreamRef.current = stream;

      // 2. Inicializar Speech Recognition
      if (!SpeechRecognition) {
        // Não deveria acontecer se browserSupported for true, mas é um bom fallback
        throw new Error('Speech Recognition API not available.');
      }

      const recognition = new SpeechRecognition();
      recognition.continuous = false; // Não contínuo, para uma única frase
      recognition.interimResults = true; // Resultados parciais para feedback visual
      recognition.lang = 'pt-BR';
      recognitionRef.current = recognition;

      // 3. Configurar Eventos
      recognition.onstart = () => {
        setState(prev => ({ ...prev, isListening: true }));
      };

      recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setState(prev => ({
          ...prev,
          currentTranscript: finalTranscript || interimTranscript,
        }));

        if (finalTranscript) {
          recognition.stop(); // Parar após resultado final
        }
      };

      recognition.onerror = (event) => {
        console.error('[ORION Voice] Recognition Error:', event.error);
        setState(prev => ({ ...prev, isListening: false }));

        if (event.error === 'no-speech' || event.error === 'audio-capture') {
          // Erros recuperáveis
          setState(prev => ({
            ...prev,
            error: {
              type: 'mic-not-found',
              message: 'Não detectei sua voz. Tente novamente.',
              recoverable: true,
            },
          }));
        } else if (event.error === 'network') {
          setState(prev => ({
            ...prev,
            error: {
              type: 'network',
              message: 'Problema de conexão. Verifique sua internet.',
              recoverable: true,
            },
          }));
        } else {
          setState(prev => ({
            ...prev,
            error: {
              type: 'unknown',
              message: `Erro desconhecido: ${event.error}`,
              recoverable: true,
            },
          }));
        }
      };

      recognition.onend = () => {
        setState(prev => ({ ...prev, isListening: false }));
        const finalTranscript = recognitionRef.current?.currentTranscript || state.currentTranscript;

        // Se houver transcrição final, chamar o callback
        if (finalTranscript && onTranscriptCompleteRef.current) {
          onTranscriptCompleteRef.current(finalTranscript);
        }
        
        // Limpar o stream do microfone após o uso
        if (mediaStreamRef.current) {
            mediaStreamRef.current.getTracks().forEach(track => track.stop());
            mediaStreamRef.current = null;
        }
      };

      // 4. Iniciar
      recognition.start();
      setState(prev => ({ ...prev, isListening: true }));

    } catch (error) {
      console.error('[ORION Voice] Microfone Error:', error);
      setState(prev => ({ ...prev, isListening: false }));

      if (error instanceof DOMException && error.name === 'NotAllowedError') {
        // Permissão negada pelo usuário
        setState(prev => ({
          ...prev,
          micPermissionDenied: true,
          error: {
            type: 'mic-denied',
            message: 'Permissão de microfone negada. Por favor, habilite-a nas configurações do seu navegador.',
            recoverable: false,
          },
        }));
      } else {
        // Outros erros de microfone
        setState(prev => ({
          ...prev,
          error: {
            type: 'mic-not-found',
            message: 'Não foi possível acessar o microfone. Verifique se ele está conectado.',
            recoverable: true,
          },
        }));
      }
      
      // Limpar o stream em caso de erro
      if (mediaStreamRef.current) {
          mediaStreamRef.current.getTracks().forEach(track => track.stop());
          mediaStreamRef.current = null;
      }
    }
  }, [state.browserSupported, state.currentTranscript]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // PARAR RECONHECIMENTO DE VOZ
  // ═══════════════════════════════════════════════════════════════════════════════

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setState(prev => ({ ...prev, isListening: false }));
    }
    // Garante que o stream do microfone seja parado
    if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(track => track.stop());
        mediaStreamRef.current = null;
    }
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // GET MEDIA STREAM (Para o Visualizador de Áudio)
  // ═══════════════════════════════════════════════════════════════════════════════

  const getMediaStream = useCallback(() => {
    return mediaStreamRef.current;
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // RETURN
  // ═══════════════════════════════════════════════════════════════════════════════

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
