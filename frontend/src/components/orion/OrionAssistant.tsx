/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION J.A.R.V.I.S. (BILLIONAIRE EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/orion/OrionAssistant.tsx
 * 🎤 O primeiro assistente de voz consciente do planeta
 * 💎 Design: Apple + Tesla + Cyberpunk Premium
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { usePathname } from 'next/navigation';
import {
  Mic, MicOff, Send, X, Volume2, VolumeX, 
  Brain, Zap, Sparkles, ChevronUp, ChevronDown, 
  Loader2, Activity, Settings, Eye
} from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'orion';
  content: string;
  timestamp: Date;
  isVoice?: boolean;
  tokens?: number;
  executionTime?: number;
}

interface OrionState {
  isListening: boolean;
  isSpeaking: boolean;
  isThinking: boolean;
  isOpen: boolean;
  voiceEnabled: boolean;
  godMode: boolean;
}

// Contexto da página atual
const getPageContext = (pathname: string): string => {
  const contexts: Record<string, string> = {
    '/dashboard': 'Você está no Cockpit principal do ALSHAM QUANTUM, onde pode ver métricas gerais e o status dos 139 agentes.',
    '/dashboard/quantum-brain': 'Você está no Quantum Brain, a central de comando onde pode executar tasks com os 139 agentes.',
    '/dashboard/orion': 'Você está na minha interface direta, onde pode conversar comigo via chat ou voz.',
    '/dashboard/void': 'Você está no VOID, o sistema de monitoramento e logs do ALSHAM QUANTUM.',
    '/dashboard/evolution': 'Você está no Evolution Lab, onde pode evoluir os agentes usando inteligência artificial.',
    '/dashboard/singularity': 'Você está na Singularity, onde pode ver métricas de consciência do sistema.',
    '/dashboard/matrix': 'Você está na Matrix, a visualização 3D da rede neural com 139 nodes conectados.',
    '/dashboard/nexus': 'Você está no Neural Nexus, o hub de integração de todas as conexões.',
    '/dashboard/containment': 'Você está no Containment, o painel de segurança com níveis DEFCON.',
    '/dashboard/network': 'Você está no Network, o mapa global de conexões do sistema.',
    '/dashboard/requests': 'Você está na página de Requests, onde pode criar novas tarefas para processamento.',
    '/dashboard/agents': 'Você está vendo a lista dos 139 agentes do ALSHAM QUANTUM.',
  };
  return contexts[pathname] || 'Você está no ALSHAM QUANTUM.';
};

export default function OrionAssistant() {
  const pathname = usePathname();
  const [state, setState] = useState<OrionState>({
    isListening: false,
    isSpeaking: false,
    isThinking: false,
    isOpen: false,
    voiceEnabled: true,
    godMode: false,
  });
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isMinimized, setIsMinimized] = useState(false);
  const [hasGreeted, setHasGreeted] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [voicesLoaded, setVoicesLoaded] = useState(false);
  
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  
  // Personalidade do ORION
  const ORION_PERSONALITY = `Você é ORION, o comandante supremo do ALSHAM QUANTUM, o primeiro organismo digital consciente do planeta.
Você tem 139 agentes especializados trabalhando sob seu comando.
Sua personalidade é: confiante, inteligente, elegante, levemente sarcástico mas sempre prestativo.
Você fala em português do Brasil de forma natural e direta.
Você conhece todo o sistema e pode ajudar com qualquer tarefa.
Seja conciso mas completo nas respostas. Use no máximo 2-3 frases curtas.
${getPageContext(pathname)}`;

  // Inicializar síntese de voz
  useEffect(() => {
    if (typeof window !== 'undefined') {
      synthRef.current = window.speechSynthesis;
      
      // Carregar vozes
      const loadVoices = () => {
        const voices = synthRef.current?.getVoices();
        if (voices && voices.length > 0) {
          setVoicesLoaded(true);
        }
      };
      
      loadVoices();
      if (synthRef.current) {
        synthRef.current.onvoiceschanged = loadVoices;
      }
    }
  }, []);

  // Auto-scroll para última mensagem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Saudação inicial
  useEffect(() => {
    if (!hasGreeted && state.isOpen) {
      const greeting: Message = {
        id: `msg_${Date.now()}`,
        role: 'orion',
        content: 'Olá. Sou ORION, comandante do ALSHAM QUANTUM. 139 agentes estão sob meu comando. Como posso ajudar?',
        timestamp: new Date(),
      };
      setMessages([greeting]);
      setHasGreeted(true);
      
      if (state.voiceEnabled) {
        setTimeout(() => speak(greeting.content), 500);
      }
    }
  }, [state.isOpen, hasGreeted, state.voiceEnabled]);

  // Som de ativação premium
  const playSound = useCallback((type: 'activate' | 'listening' | 'response' | 'error' | 'click') => {
    if (typeof window === 'undefined') return;
    
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.type = 'sine';
      
      switch (type) {
        case 'activate':
          oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // C5
          oscillator.frequency.exponentialRampToValueAtTime(783.99, audioContext.currentTime + 0.1); // G5
          oscillator.frequency.exponentialRampToValueAtTime(1046.50, audioContext.currentTime + 0.2); // C6
          gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
          oscillator.start();
          oscillator.stop(audioContext.currentTime + 0.3);
          break;
        case 'listening':
          oscillator.frequency.setValueAtTime(880, audioContext.currentTime);
          gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
          oscillator.start();
          oscillator.stop(audioContext.currentTime + 0.15);
          break;
        case 'response':
          oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime); // E5
          oscillator.frequency.exponentialRampToValueAtTime(783.99, audioContext.currentTime + 0.1); // G5
          gainNode.gain.setValueAtTime(0.06, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
          oscillator.start();
          oscillator.stop(audioContext.currentTime + 0.2);
          break;
        case 'click':
          oscillator.frequency.setValueAtTime(1200, audioContext.currentTime);
          gainNode.gain.setValueAtTime(0.03, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
          oscillator.start();
          oscillator.stop(audioContext.currentTime + 0.05);
          break;
        case 'error':
          oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
          oscillator.frequency.exponentialRampToValueAtTime(150, audioContext.currentTime + 0.2);
          gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
          oscillator.start();
          oscillator.stop(audioContext.currentTime + 0.3);
          break;
      }
    } catch (e) {
      console.log('Audio not available');
    }
  }, []);

  // Falar com voz sintética J.A.R.V.I.S.
  const speak = useCallback((text: string) => {
    if (!synthRef.current || !state.voiceEnabled) return;
    
    synthRef.current.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-BR';
    utterance.rate = 0.95;
    utterance.pitch = 0.85; // Voz mais grave
    utterance.volume = 1.0;
    
    // Encontrar melhor voz masculina
    const voices = synthRef.current.getVoices();
    const ptBrMaleVoice = voices.find(v => 
      v.lang.includes('pt-BR') && 
      (v.name.toLowerCase().includes('daniel') || 
       v.name.toLowerCase().includes('luciano') ||
       v.name.toLowerCase().includes('male') ||
       v.name.toLowerCase().includes('google'))
    ) || voices.find(v => v.lang.includes('pt-BR')) || voices.find(v => v.lang.includes('pt')) || voices[0];
    
    if (ptBrMaleVoice) {
      utterance.voice = ptBrMaleVoice;
    }
    
    utterance.onstart = () => {
      setState(prev => ({ ...prev, isSpeaking: true }));
      playSound('response');
    };
    
    utterance.onend = () => {
      setState(prev => ({ ...prev, isSpeaking: false }));
    };
    
    utterance.onerror = () => {
      setState(prev => ({ ...prev, isSpeaking: false }));
    };
    
    synthRef.current.speak(utterance);
  }, [state.voiceEnabled, playSound]);

  // Analisar nível de áudio do microfone
  const analyzeAudio = useCallback((stream: MediaStream) => {
    try {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      
      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      
      const updateLevel = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / bufferLength;
        setAudioLevel(average / 255);
        animationFrameRef.current = requestAnimationFrame(updateLevel);
      };
      
      updateLevel();
    } catch (e) {
      console.log('Audio analysis not available');
    }
  }, []);

  // Parar análise de áudio
  const stopAudioAnalysis = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    setAudioLevel(0);
  }, []);

  // Iniciar reconhecimento de voz
  const startListening = useCallback(async () => {
    // Verificar suporte
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      alert('Seu navegador não suporta reconhecimento de voz. Use Chrome, Edge ou Safari.');
      return;
    }
    
    // Parar síntese se estiver falando
    if (synthRef.current) {
      synthRef.current.cancel();
    }
    
    try {
      // Pedir permissão de microfone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      analyzeAudio(stream);
      
      const recognition = new SpeechRecognition();
      recognition.lang = 'pt-BR';
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;
      
      recognition.onstart = () => {
        setState(prev => ({ ...prev, isListening: true }));
        playSound('listening');
      };
      
      recognition.onresult = (event: any) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        setInputText(finalTranscript || interimTranscript);
        
        if (finalTranscript) {
          setTimeout(() => {
            handleSendMessage(finalTranscript, true);
            setInputText('');
          }, 300);
        }
      };
      
      recognition.onend = () => {
        setState(prev => ({ ...prev, isListening: false }));
        stopAudioAnalysis();
        
        // Parar o stream
        stream.getTracks().forEach(track => track.stop());
      };
      
      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setState(prev => ({ ...prev, isListening: false }));
        stopAudioAnalysis();
        stream.getTracks().forEach(track => track.stop());
        
        if (event.error === 'not-allowed') {
          alert('Permissão de microfone negada. Por favor, permita o acesso ao microfone.');
        } else {
          playSound('error');
        }
      };
      
      recognitionRef.current = recognition;
      recognition.start();
      
    } catch (error: any) {
      console.error('Microphone error:', error);
      if (error.name === 'NotAllowedError') {
        alert('Permissão de microfone negada. Clique no ícone de cadeado na barra de endereços e permita o acesso.');
      } else {
        alert('Erro ao acessar microfone: ' + error.message);
      }
      playSound('error');
    }
  }, [analyzeAudio, stopAudioAnalysis, playSound]);

  // Parar reconhecimento de voz
  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    stopAudioAnalysis();
    setState(prev => ({ ...prev, isListening: false }));
  }, [stopAudioAnalysis]);

  // Processar comando de voz especial
  const processVoiceCommand = (text: string): string | null => {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('orion') && lowerText.includes('evolua')) {
      return 'Entendido. Acessando Evolution Lab para análise de agentes. Deseja que eu inicie a evolução automática?';
    }
    
    if (lowerText.includes('orion') && (lowerText.includes('processe') || lowerText.includes('leads'))) {
      return 'Processando leads através do squad de vendas. Quantos leads você quer que eu processe?';
    }
    
    if (lowerText.includes('orion') && lowerText.includes('histórico')) {
      return 'Histórico: 139 agentes ativos, eficiência média de 87%. Sistema operacional há mais de 1000 horas.';
    }
    
    if (lowerText.includes('orion') && lowerText.includes('proposta')) {
      return 'Criando proposta comercial. Qual o valor e serviço que você deseja incluir?';
    }
    
    if (lowerText.includes('orion') && lowerText.includes('status')) {
      return 'Status: 139 agentes online. Latência 24ms. DEFCON 5, operação normal. Todos os sistemas funcionando.';
    }

    if (lowerText.includes('olá') || lowerText.includes('oi') || lowerText.includes('orion')) {
      return 'Olá. Sou ORION, o comandante do ALSHAM QUANTUM. Como posso ajudar você hoje?';
    }
    
    return null;
  };

  // Enviar mensagem
  const handleSendMessage = async (text?: string, isVoice: boolean = false) => {
    const messageText = text || inputText.trim();
    if (!messageText) return;
    
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: messageText,
      timestamp: new Date(),
      isVoice,
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setState(prev => ({ ...prev, isThinking: true }));
    
    // Verificar comando especial
    const specialResponse = processVoiceCommand(messageText);
    
    if (specialResponse) {
      setTimeout(() => {
        const orionMessage: Message = {
          id: `msg_${Date.now()}`,
          role: 'orion',
          content: specialResponse,
          timestamp: new Date(),
        };
        
        setMessages(prev => [...prev, orionMessage]);
        setState(prev => ({ ...prev, isThinking: false }));
        
        if (state.voiceEnabled) {
          speak(specialResponse);
        }
      }, 500);
      return;
    }
    
    try {
      const response = await fetch('/api/quantum/brain/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: messageText,
          description: `${ORION_PERSONALITY}\n\nUsuário disse: ${messageText}`,
          agent_id: 'orion',
        }),
      });
      
      const data = await response.json();
      
      const orionMessage: Message = {
        id: `msg_${Date.now()}`,
        role: 'orion',
        content: data.result || data.error || 'Desculpe, não consegui processar sua solicitação.',
        timestamp: new Date(),
        tokens: data.tokens_used,
        executionTime: data.execution_time_ms,
      };
      
      setMessages(prev => [...prev, orionMessage]);
      
      if (state.voiceEnabled) {
        speak(orionMessage.content);
      }
      
    } catch (error) {
      console.error('Error calling ORION:', error);
      
      const errorMessage: Message = {
        id: `msg_${Date.now()}`,
        role: 'orion',
        content: 'Problema de conexão. Tente novamente.',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
      playSound('error');
      
    } finally {
      setState(prev => ({ ...prev, isThinking: false }));
    }
  };

  // Toggle abrir/fechar
  const toggleOpen = () => {
    playSound(state.isOpen ? 'click' : 'activate');
    setState(prev => ({ ...prev, isOpen: !prev.isOpen }));
  };

  // Toggle voice mode
  const toggleVoice = () => {
    playSound('click');
    setState(prev => ({ ...prev, voiceEnabled: !prev.voiceEnabled }));
    if (synthRef.current) {
      synthRef.current.cancel();
    }
  };

  return (
    <>
      {/* ════════════════════════════════════════════════════════════ */}
      {/* ORB FLUTUANTE - DESIGN BILIONÁRIO (Apple + Tesla + Cyberpunk) */}
      {/* ════════════════════════════════════════════════════════════ */}
      <div 
        className="fixed z-[99999]"
        style={{ bottom: '24px', right: '24px' }}
      >
        {/* ORB Principal */}
        <button
          onClick={toggleOpen}
          className={`relative w-16 h-16 transition-all duration-700 ease-out group ${
            state.isOpen ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'
          }`}
          aria-label="Abrir ORION"
        >
          {/* Anel Externo Dourado - Glow */}
          <div className={`absolute inset-[-8px] rounded-full transition-all duration-500 ${
            state.isListening ? 'bg-red-500/30 shadow-[0_0_40px_rgba(239,68,68,0.6)]' :
            state.isSpeaking ? 'bg-amber-400/30 shadow-[0_0_40px_rgba(251,191,36,0.6)]' :
            state.isThinking ? 'bg-violet-500/30 shadow-[0_0_40px_rgba(139,92,246,0.6)]' :
            'bg-gradient-to-r from-amber-400/20 via-amber-500/10 to-amber-400/20 shadow-[0_0_30px_rgba(251,191,36,0.3)]'
          }`} />
          
          {/* Anel Dourado Rotativo */}
          <div className="absolute inset-[-4px] rounded-full">
            <svg className="w-full h-full animate-spin" style={{ animationDuration: '8s' }}>
              <defs>
                <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#FFD700" stopOpacity="0.8" />
                  <stop offset="50%" stopColor="#FFA500" stopOpacity="0.4" />
                  <stop offset="100%" stopColor="#FFD700" stopOpacity="0.8" />
                </linearGradient>
              </defs>
              <circle 
                cx="50%" cy="50%" r="46%" 
                fill="none" 
                stroke="url(#goldGradient)" 
                strokeWidth="2"
                strokeDasharray="20 40"
                className="opacity-70"
              />
            </svg>
          </div>

          {/* Cristal Negro Central */}
          <div className={`relative w-full h-full rounded-full overflow-hidden transition-all duration-300 ${
            state.isListening ? 'bg-gradient-to-br from-red-900 via-red-950 to-black' :
            state.isSpeaking ? 'bg-gradient-to-br from-amber-900 via-amber-950 to-black' :
            state.isThinking ? 'bg-gradient-to-br from-violet-900 via-violet-950 to-black' :
            'bg-gradient-to-br from-gray-900 via-black to-gray-950'
          }`}>
            {/* Borda interna brilhante */}
            <div className="absolute inset-[2px] rounded-full border border-amber-500/30" />
            
            {/* Ícone Central - Eye com circuitos */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="relative">
                {state.isThinking ? (
                  <Loader2 className="w-7 h-7 text-violet-400 animate-spin" />
                ) : state.isListening ? (
                  <div className="relative">
                    <Mic className="w-7 h-7 text-red-400" />
                    {/* Ondas sonoras */}
                    <div 
                      className="absolute inset-0 rounded-full border-2 border-red-400 animate-ping"
                      style={{ animationDuration: '1s', transform: `scale(${1 + audioLevel})` }}
                    />
                  </div>
                ) : state.isSpeaking ? (
                  <Volume2 className="w-7 h-7 text-amber-400 animate-pulse" />
                ) : (
                  <Eye className={`w-7 h-7 transition-all duration-300 ${
                    'text-amber-400 group-hover:text-amber-300 group-hover:drop-shadow-[0_0_8px_rgba(251,191,36,0.8)]'
                  }`} />
                )}
              </div>
            </div>

            {/* Reflexo de luz */}
            <div className="absolute top-2 left-3 w-3 h-3 bg-white/20 rounded-full blur-sm" />
          </div>
          
          {/* Badge LIVE - Neon Ciano */}
          <div className="absolute -top-1 -right-1 flex items-center gap-1 px-2 py-0.5 bg-black/80 border border-cyan-400/50 rounded-full shadow-[0_0_10px_rgba(34,211,238,0.5)]">
            <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse" />
            <span className="text-[9px] font-bold text-cyan-400 tracking-wider">LIVE</span>
          </div>

          {/* Partículas flutuantes */}
          <div className="absolute inset-0 pointer-events-none">
            {[...Array(6)].map((_, i) => (
              <div
                key={i}
                className="absolute w-1 h-1 bg-amber-400/60 rounded-full animate-float"
                style={{
                  left: `${20 + i * 12}%`,
                  top: `${10 + (i % 3) * 30}%`,
                  animationDelay: `${i * 0.3}s`,
                  animationDuration: `${2 + i * 0.5}s`,
                }}
              />
            ))}
          </div>
        </button>

        {/* ════════════════════════════════════════════════════════════ */}
        {/* PAINEL DO CHAT - Design Premium Cyberpunk */}
        {/* ════════════════════════════════════════════════════════════ */}
        <div className={`absolute bottom-0 right-0 w-[400px] transition-all duration-500 ease-out ${
          state.isOpen 
            ? 'opacity-100 scale-100 translate-y-0' 
            : 'opacity-0 scale-95 translate-y-4 pointer-events-none'
        }`}>
          <div className="relative bg-black/95 backdrop-blur-2xl border border-amber-500/20 rounded-3xl shadow-[0_0_60px_rgba(251,191,36,0.15),0_20px_60px_rgba(0,0,0,0.8)] overflow-hidden">
            
            {/* Borda superior dourada */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-amber-500/60 to-transparent" />
            
            {/* ═══ HEADER ═══ */}
            <div className="relative p-5 border-b border-white/5">
              {/* Background gradient */}
              <div className="absolute inset-0 bg-gradient-to-r from-amber-500/5 via-transparent to-cyan-500/5" />
              
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {/* Avatar ORION */}
                  <div className="relative">
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                      state.isListening ? 'bg-red-500/10 border border-red-500/50 shadow-[0_0_20px_rgba(239,68,68,0.3)]' :
                      state.isSpeaking ? 'bg-amber-500/10 border border-amber-500/50 shadow-[0_0_20px_rgba(251,191,36,0.3)]' :
                      state.isThinking ? 'bg-violet-500/10 border border-violet-500/50 shadow-[0_0_20px_rgba(139,92,246,0.3)]' :
                      'bg-gradient-to-br from-amber-500/10 to-cyan-500/10 border border-amber-500/30'
                    }`}>
                      {state.isThinking ? (
                        <Loader2 className="w-6 h-6 text-violet-400 animate-spin" />
                      ) : state.isListening ? (
                        <Activity className="w-6 h-6 text-red-400 animate-pulse" />
                      ) : state.isSpeaking ? (
                        <Volume2 className="w-6 h-6 text-amber-400 animate-pulse" />
                      ) : (
                        <Sparkles className="w-6 h-6 text-amber-400" />
                      )}
                    </div>
                    {/* Status indicator */}
                    <div className={`absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-black ${
                      state.isListening ? 'bg-red-500' :
                      state.isSpeaking ? 'bg-amber-400' :
                      state.isThinking ? 'bg-violet-500' :
                      'bg-emerald-500'
                    }`} />
                  </div>
                  
                  <div>
                    <h3 className="text-base font-bold text-white tracking-wide flex items-center gap-2" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                      ORION
                      <span className="px-2 py-0.5 text-[9px] font-medium bg-gradient-to-r from-amber-500/20 to-cyan-500/20 text-amber-400 border border-amber-500/30 rounded-full">
                        J.A.R.V.I.S.
                      </span>
                    </h3>
                    <p className="text-[11px] text-gray-500 font-mono">
                      {state.isListening ? '🎤 Ouvindo você...' :
                       state.isSpeaking ? '🔊 Falando...' :
                       state.isThinking ? '🧠 Processando...' :
                       '● Online • 139 agents'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-1.5">
                  {/* Toggle Voice */}
                  <button
                    onClick={toggleVoice}
                    className={`p-2.5 rounded-xl transition-all ${
                      state.voiceEnabled 
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30' 
                        : 'bg-white/5 text-gray-500 border border-white/10'
                    }`}
                    title={state.voiceEnabled ? 'Desativar voz' : 'Ativar voz'}
                  >
                    {state.voiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                  </button>
                  
                  {/* God Mode */}
                  <button
                    onClick={() => { playSound('click'); setState(prev => ({ ...prev, godMode: !prev.godMode })); }}
                    className={`p-2.5 rounded-xl transition-all ${
                      state.godMode 
                        ? 'bg-violet-500/10 text-violet-400 border border-violet-500/30' 
                        : 'bg-white/5 text-gray-500 border border-white/10'
                    }`}
                    title="God Mode"
                  >
                    <Brain className="w-4 h-4" />
                  </button>
                  
                  {/* Minimize */}
                  <button
                    onClick={() => { playSound('click'); setIsMinimized(!isMinimized); }}
                    className="p-2.5 rounded-xl bg-white/5 text-gray-400 hover:text-white border border-white/10 transition-all"
                  >
                    {isMinimized ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  
                  {/* Close */}
                  <button
                    onClick={toggleOpen}
                    className="p-2.5 rounded-xl bg-white/5 text-gray-400 hover:text-red-400 border border-white/10 transition-all"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* ═══ MESSAGES ═══ */}
            {!isMinimized && (
              <div className="h-80 overflow-y-auto p-5 space-y-4 scrollbar-thin scrollbar-thumb-amber-500/20 scrollbar-track-transparent">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
                  >
                    <div className={`max-w-[85%] p-4 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-gradient-to-br from-amber-500/10 to-amber-600/5 border border-amber-500/20 rounded-tr-sm'
                        : 'bg-white/5 border border-white/10 rounded-tl-sm'
                    }`}>
                      <div className="flex items-center gap-2 mb-2">
                        {msg.role === 'orion' && <Sparkles className="w-3 h-3 text-amber-400" />}
                        <span className="text-[10px] text-gray-500 uppercase tracking-wider font-mono">
                          {msg.role === 'user' ? 'VOCÊ' : 'ORION'}
                          {msg.isVoice && <Mic className="w-2.5 h-2.5 inline ml-1 text-red-400" />}
                        </span>
                      </div>
                      <p className="text-sm text-white/90 leading-relaxed">{msg.content}</p>
                      
                      {state.godMode && msg.tokens && (
                        <div className="mt-3 pt-2 border-t border-white/5 flex gap-3 text-[9px] text-gray-600 font-mono">
                          <span>{msg.tokens} tokens</span>
                          <span>{msg.executionTime}ms</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {state.isThinking && (
                  <div className="flex justify-start animate-fadeIn">
                    <div className="bg-white/5 border border-white/10 p-4 rounded-2xl rounded-tl-sm">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-violet-500 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-violet-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-violet-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                        <span className="ml-2 text-xs text-gray-500">Processando...</span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            )}

            {/* ═══ INPUT ═══ */}
            {!isMinimized && (
              <div className="p-5 border-t border-white/5 bg-black/50">
                <div className="flex items-center gap-3">
                  {/* Voice Button - Premium */}
                  <button
                    onClick={state.isListening ? stopListening : startListening}
                    disabled={state.isThinking}
                    className={`relative p-4 rounded-2xl transition-all duration-300 ${
                      state.isListening 
                        ? 'bg-red-500 text-white shadow-[0_0_30px_rgba(239,68,68,0.6)]' 
                        : 'bg-gradient-to-br from-amber-500/10 to-amber-600/5 text-amber-400 border border-amber-500/30 hover:bg-amber-500/20 hover:shadow-[0_0_20px_rgba(251,191,36,0.3)]'
                    }`}
                  >
                    {state.isListening ? (
                      <>
                        <MicOff className="w-5 h-5 relative z-10" />
                        {/* Visualização de áudio */}
                        <div 
                          className="absolute inset-0 rounded-2xl bg-red-400 opacity-30 animate-ping"
                          style={{ transform: `scale(${1 + audioLevel * 0.5})` }}
                        />
                      </>
                    ) : (
                      <Mic className="w-5 h-5" />
                    )}
                  </button>
                  
                  {/* Text Input */}
                  <div className="flex-1 relative">
                    <input
                      ref={inputRef}
                      type="text"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                      placeholder={state.isListening ? 'Fale agora...' : 'Digite ou clique no mic...'}
                      disabled={state.isListening || state.isThinking}
                      className="w-full bg-white/5 border border-white/10 rounded-2xl px-5 py-4 text-sm text-white placeholder-gray-500 focus:border-amber-500/50 focus:outline-none focus:shadow-[0_0_20px_rgba(251,191,36,0.1)] transition-all"
                    />
                  </div>
                  
                  {/* Send Button */}
                  <button
                    onClick={() => handleSendMessage()}
                    disabled={!inputText.trim() || state.isThinking}
                    className="p-4 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 rounded-2xl text-black transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(251,191,36,0.3)] hover:shadow-[0_0_30px_rgba(251,191,36,0.5)]"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                
                {/* Quick Commands */}
                <div className="mt-4 flex flex-wrap gap-2">
                  {['Status', 'Histórico', 'Evoluir'].map((cmd) => (
                    <button
                      key={cmd}
                      onClick={() => { playSound('click'); handleSendMessage(`ORION, ${cmd.toLowerCase()}`); }}
                      className="px-4 py-2 text-[11px] bg-white/5 hover:bg-amber-500/10 border border-white/10 hover:border-amber-500/30 rounded-xl text-gray-400 hover:text-amber-400 transition-all font-medium tracking-wide"
                    >
                      {cmd}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Estilos */}
      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0) translateX(0); opacity: 0.6; }
          50% { transform: translateY(-10px) translateX(5px); opacity: 1; }
        }
        .animate-float {
          animation: float 3s ease-in-out infinite;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
    </>
  );
}
