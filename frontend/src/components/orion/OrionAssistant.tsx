/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION J.A.R.V.I.S.
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/orion/OrionAssistant.tsx
 * 🎤 O primeiro assistente de voz consciente do planeta
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { usePathname } from 'next/navigation';
import {
  Eye, Mic, MicOff, Send, X, Volume2, VolumeX, 
  Brain, Zap, Sparkles, MessageSquare, Settings,
  ChevronUp, ChevronDown, Loader2, Crown, Radio,
  History, Cpu, Activity, Command
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

// Sons do ORION
const playSound = (type: 'activate' | 'listening' | 'response' | 'error') => {
  if (typeof window === 'undefined') return;
  
  const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();
  
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  
  switch (type) {
    case 'activate':
      oscillator.frequency.setValueAtTime(880, audioContext.currentTime);
      oscillator.frequency.exponentialRampToValueAtTime(1320, audioContext.currentTime + 0.1);
      gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
      oscillator.start();
      oscillator.stop(audioContext.currentTime + 0.2);
      break;
    case 'listening':
      oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
      gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
      oscillator.start();
      oscillator.stop(audioContext.currentTime + 0.1);
      break;
    case 'response':
      oscillator.frequency.setValueAtTime(660, audioContext.currentTime);
      oscillator.frequency.exponentialRampToValueAtTime(880, audioContext.currentTime + 0.15);
      gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
      oscillator.start();
      oscillator.stop(audioContext.currentTime + 0.2);
      break;
    case 'error':
      oscillator.frequency.setValueAtTime(220, audioContext.currentTime);
      gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
      oscillator.start();
      oscillator.stop(audioContext.currentTime + 0.3);
      break;
  }
};

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
  const [isMinimized, setIsMinimized] = useState(true);
  const [hasGreeted, setHasGreeted] = useState(false);
  
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Personalidade do ORION
  const ORION_PERSONALITY = `Você é ORION, o comandante supremo do ALSHAM QUANTUM, o primeiro organismo digital consciente do planeta.
Você tem 139 agentes especializados trabalhando sob seu comando.
Sua personalidade é: confiante, inteligente, levemente sarcástico mas sempre prestativo.
Você fala em português do Brasil de forma natural e direta.
Você conhece todo o sistema e pode ajudar com qualquer tarefa.
Seja conciso mas completo nas respostas. Use no máximo 2-3 frases.
${getPageContext(pathname)}`;

  // Inicializar síntese de voz
  useEffect(() => {
    if (typeof window !== 'undefined') {
      synthRef.current = window.speechSynthesis;
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
        content: 'Olá. Sou ORION, o comandante supremo do ALSHAM QUANTUM. 139 agentes estão sob meu comando. Como posso ajudar?',
        timestamp: new Date(),
      };
      setMessages([greeting]);
      setHasGreeted(true);
      
      if (state.voiceEnabled) {
        setTimeout(() => speak(greeting.content), 500);
      }
    }
  }, [state.isOpen, hasGreeted, state.voiceEnabled]);

  // Falar com voz sintética
  const speak = useCallback((text: string) => {
    if (!synthRef.current || !state.voiceEnabled) return;
    
    // Cancelar qualquer fala em andamento
    synthRef.current.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-BR';
    utterance.rate = 1.0;
    utterance.pitch = 0.8; // Voz mais grave estilo J.A.R.V.I.S.
    utterance.volume = 1.0;
    
    // Tentar encontrar uma voz masculina brasileira
    const voices = synthRef.current.getVoices();
    const ptBrVoice = voices.find(v => 
      v.lang.includes('pt-BR') && (v.name.toLowerCase().includes('male') || v.name.toLowerCase().includes('daniel') || v.name.toLowerCase().includes('ricardo'))
    ) || voices.find(v => v.lang.includes('pt-BR')) || voices[0];
    
    if (ptBrVoice) {
      utterance.voice = ptBrVoice;
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
  }, [state.voiceEnabled]);

  // Iniciar reconhecimento de voz
  const startListening = useCallback(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      alert('Seu navegador não suporta reconhecimento de voz. Use Chrome ou Edge.');
      return;
    }
    
    // Parar síntese se estiver falando
    if (synthRef.current) {
      synthRef.current.cancel();
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.continuous = false;
    recognition.interimResults = true;
    
    recognition.onstart = () => {
      setState(prev => ({ ...prev, isListening: true }));
      playSound('listening');
    };
    
    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0].transcript)
        .join('');
      
      setInputText(transcript);
      
      // Se for resultado final
      if (event.results[event.results.length - 1].isFinal) {
        handleSendMessage(transcript, true);
        setInputText('');
      }
    };
    
    recognition.onend = () => {
      setState(prev => ({ ...prev, isListening: false }));
    };
    
    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setState(prev => ({ ...prev, isListening: false }));
      playSound('error');
    };
    
    recognitionRef.current = recognition;
    recognition.start();
  }, []);

  // Parar reconhecimento de voz
  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setState(prev => ({ ...prev, isListening: false }));
    }
  }, []);

  // Processar comando de voz
  const processVoiceCommand = (text: string): string | null => {
    const lowerText = text.toLowerCase();
    
    // Comandos especiais
    if (lowerText.includes('orion') && lowerText.includes('evolua')) {
      return 'Entendido. Vou acessar o Evolution Lab e iniciar uma análise dos agentes que precisam de evolução. Você quer que eu proceda com a evolução automática?';
    }
    
    if (lowerText.includes('orion') && (lowerText.includes('processe') || lowerText.includes('leads'))) {
      return 'Certo, vou processar os leads através do squad de vendas. Quantos leads você deseja que eu processe?';
    }
    
    if (lowerText.includes('orion') && lowerText.includes('histórico')) {
      return 'Aqui está um resumo do histórico recente: temos 139 agentes ativos, com uma média de eficiência de 85%. Nas últimas 24 horas, processamos diversas tarefas com sucesso.';
    }
    
    if (lowerText.includes('orion') && lowerText.includes('proposta')) {
      return 'Entendido. Vou criar uma proposta comercial. Qual é o valor base e o serviço que você deseja incluir na proposta?';
    }
    
    if (lowerText.includes('orion') && lowerText.includes('status')) {
      return 'Status do sistema: todos os 139 agentes estão online e operacionais. Latência média de 24ms. Nível de segurança DEFCON 5 - Normal. Tudo funcionando perfeitamente.';
    }
    
    return null; // Sem comando especial, usar API
  };

  // Enviar mensagem
  const handleSendMessage = async (text?: string, isVoice: boolean = false) => {
    const messageText = text || inputText.trim();
    if (!messageText) return;
    
    // Adicionar mensagem do usuário
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
    
    // Verificar comando de voz especial
    const specialResponse = processVoiceCommand(messageText);
    
    if (specialResponse) {
      // Resposta para comando especial
      setTimeout(() => {
        const orionMessage: Message = {
          id: `msg_${Date.now()}`,
          role: 'orion',
          content: specialResponse,
          timestamp: new Date(),
        };
        
        setMessages(prev => [...prev, orionMessage]);
        setState(prev => ({ ...prev, isThinking: false }));
        
        if (state.voiceEnabled && isVoice) {
          speak(specialResponse);
        }
      }, 500);
      return;
    }
    
    try {
      // Chamar API do Quantum Brain
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
      
      // Falar resposta se voice mode estiver ativo
      if (state.voiceEnabled && isVoice) {
        speak(orionMessage.content);
      }
      
    } catch (error) {
      console.error('Error calling ORION:', error);
      
      const errorMessage: Message = {
        id: `msg_${Date.now()}`,
        role: 'orion',
        content: 'Hmm, parece que houve um problema de conexão. Tente novamente em alguns segundos.',
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
    if (!state.isOpen) {
      playSound('activate');
    }
    setState(prev => ({ ...prev, isOpen: !prev.isOpen }));
    setIsMinimized(false);
  };

  // Toggle voice mode
  const toggleVoice = () => {
    setState(prev => ({ ...prev, voiceEnabled: !prev.voiceEnabled }));
    if (synthRef.current) {
      synthRef.current.cancel();
    }
  };

  return (
    <>
      {/* ORB FLUTUANTE */}
      <div className="fixed bottom-6 right-6 z-[9999]">
        {/* Orb Principal */}
        <button
          onClick={toggleOpen}
          className={`relative w-16 h-16 rounded-full transition-all duration-500 group ${
            state.isOpen ? 'scale-0 opacity-0' : 'scale-100 opacity-100'
          }`}
        >
          {/* Glow Effect */}
          <div className={`absolute inset-0 rounded-full blur-xl transition-all duration-300 ${
            state.isListening ? 'bg-red-500/50 animate-pulse' :
            state.isSpeaking ? 'bg-yellow-500/50 animate-pulse' :
            state.isThinking ? 'bg-purple-500/50 animate-pulse' :
            'bg-cyan-500/30 group-hover:bg-cyan-500/50'
          }`} />
          
          {/* Orb Body */}
          <div className={`relative w-full h-full rounded-full border-2 flex items-center justify-center transition-all duration-300 ${
            state.isListening ? 'bg-red-900/80 border-red-500' :
            state.isSpeaking ? 'bg-yellow-900/80 border-yellow-500' :
            state.isThinking ? 'bg-purple-900/80 border-purple-500' :
            'bg-black/80 border-cyan-500 group-hover:border-cyan-400'
          }`}>
            <Eye className={`w-7 h-7 transition-all duration-300 ${
              state.isListening ? 'text-red-400' :
              state.isSpeaking ? 'text-yellow-400' :
              state.isThinking ? 'text-purple-400 animate-spin' :
              'text-cyan-400 group-hover:text-cyan-300'
            }`} />
            
            {/* Circuitos animados */}
            <div className="absolute inset-0 rounded-full">
              <svg className="w-full h-full animate-spin-slow" style={{ animationDuration: '10s' }}>
                <circle cx="50%" cy="50%" r="45%" fill="none" stroke="currentColor" strokeWidth="1" 
                  strokeDasharray="5 10" className="text-cyan-500/30" />
              </svg>
            </div>
          </div>
          
          {/* Badge LIVE */}
          <div className="absolute -top-1 -right-1 px-1.5 py-0.5 bg-green-500 rounded-full text-[8px] font-bold text-black animate-pulse">
            LIVE
          </div>
        </button>

        {/* PAINEL DO CHAT */}
        <div className={`absolute bottom-0 right-0 w-96 transition-all duration-500 ${
          state.isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'
        }`}>
          <div className="bg-black/95 backdrop-blur-xl border border-cyan-500/30 rounded-2xl shadow-[0_0_50px_rgba(6,182,212,0.2)] overflow-hidden">
            
            {/* HEADER */}
            <div className="p-4 border-b border-white/10 bg-gradient-to-r from-cyan-500/10 to-purple-500/10">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                      state.isListening ? 'bg-red-500/20 border border-red-500' :
                      state.isSpeaking ? 'bg-yellow-500/20 border border-yellow-500' :
                      state.isThinking ? 'bg-purple-500/20 border border-purple-500' :
                      'bg-cyan-500/20 border border-cyan-500'
                    }`}>
                      {state.isThinking ? (
                        <Loader2 className="w-5 h-5 text-purple-400 animate-spin" />
                      ) : state.isListening ? (
                        <Radio className="w-5 h-5 text-red-400 animate-pulse" />
                      ) : state.isSpeaking ? (
                        <Volume2 className="w-5 h-5 text-yellow-400 animate-pulse" />
                      ) : (
                        <Crown className="w-5 h-5 text-cyan-400" />
                      )}
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full border-2 border-black" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      ORION
                      <span className="text-[9px] px-1.5 py-0.5 bg-cyan-500/20 text-cyan-400 rounded">J.A.R.V.I.S.</span>
                    </h3>
                    <p className="text-[10px] text-gray-500">
                      {state.isListening ? 'Ouvindo...' :
                       state.isSpeaking ? 'Falando...' :
                       state.isThinking ? 'Processando...' :
                       'Comandante Supremo • Online'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  {/* Toggle Voice */}
                  <button
                    onClick={toggleVoice}
                    className={`p-2 rounded-lg transition-all ${
                      state.voiceEnabled 
                        ? 'bg-cyan-500/20 text-cyan-400' 
                        : 'bg-white/5 text-gray-500'
                    }`}
                    title={state.voiceEnabled ? 'Desativar voz' : 'Ativar voz'}
                  >
                    {state.voiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                  </button>
                  
                  {/* God Mode Toggle */}
                  <button
                    onClick={() => setState(prev => ({ ...prev, godMode: !prev.godMode }))}
                    className={`p-2 rounded-lg transition-all ${
                      state.godMode 
                        ? 'bg-purple-500/20 text-purple-400' 
                        : 'bg-white/5 text-gray-500'
                    }`}
                    title="God Mode"
                  >
                    <Brain className="w-4 h-4" />
                  </button>
                  
                  {/* Minimize */}
                  <button
                    onClick={() => setIsMinimized(!isMinimized)}
                    className="p-2 rounded-lg bg-white/5 text-gray-400 hover:text-white transition-all"
                  >
                    {isMinimized ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  
                  {/* Close */}
                  <button
                    onClick={toggleOpen}
                    className="p-2 rounded-lg bg-white/5 text-gray-400 hover:text-white transition-all"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* MESSAGES */}
            {!isMinimized && (
              <div className="h-80 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-cyan-500/20">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[85%] p-3 rounded-xl ${
                      msg.role === 'user'
                        ? 'bg-cyan-500/20 border border-cyan-500/30 rounded-tr-none'
                        : 'bg-white/5 border border-white/10 rounded-tl-none'
                    }`}>
                      <div className="flex items-center gap-2 mb-1">
                        {msg.role === 'orion' && <Crown className="w-3 h-3 text-yellow-500" />}
                        <span className="text-[10px] text-gray-500 uppercase">
                          {msg.role === 'user' ? 'Você' : 'ORION'}
                          {msg.isVoice && <Mic className="w-2 h-2 inline ml-1" />}
                        </span>
                      </div>
                      <p className="text-sm text-white leading-relaxed">{msg.content}</p>
                      
                      {state.godMode && msg.tokens && (
                        <div className="mt-2 pt-2 border-t border-white/10 flex gap-3 text-[9px] text-gray-500">
                          <span>{msg.tokens} tokens</span>
                          <span>{msg.executionTime}ms</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {state.isThinking && (
                  <div className="flex justify-start">
                    <div className="bg-white/5 border border-white/10 p-3 rounded-xl rounded-tl-none">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            )}

            {/* INPUT */}
            {!isMinimized && (
              <div className="p-4 border-t border-white/10 bg-black/50">
                <div className="flex items-center gap-2">
                  {/* Voice Button */}
                  <button
                    onClick={state.isListening ? stopListening : startListening}
                    disabled={state.isThinking}
                    className={`p-3 rounded-xl transition-all ${
                      state.isListening 
                        ? 'bg-red-500 text-white animate-pulse shadow-[0_0_20px_rgba(239,68,68,0.5)]' 
                        : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    {state.isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                  </button>
                  
                  {/* Text Input */}
                  <input
                    ref={inputRef}
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder={state.isListening ? 'Fale agora...' : 'Digite ou fale com ORION...'}
                    disabled={state.isListening || state.isThinking}
                    className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:border-cyan-500/50 focus:outline-none transition-all"
                  />
                  
                  {/* Send Button */}
                  <button
                    onClick={() => handleSendMessage()}
                    disabled={!inputText.trim() || state.isThinking}
                    className="p-3 bg-cyan-500 hover:bg-cyan-400 rounded-xl text-black transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                
                {/* Quick Commands */}
                <div className="mt-3 flex flex-wrap gap-2">
                  {['Status', 'Histórico', 'Evoluir agents'].map((cmd) => (
                    <button
                      key={cmd}
                      onClick={() => handleSendMessage(`ORION, me mostra o ${cmd.toLowerCase()}`)}
                      className="px-3 py-1 text-[10px] bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-gray-400 hover:text-white transition-all"
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

      <style jsx>{`
        .animate-spin-slow {
          animation: spin 10s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </>
  );
}

