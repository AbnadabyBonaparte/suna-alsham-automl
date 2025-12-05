/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION J.A.R.V.I.S. (10/10 PERFECT EDITION)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/orion/OrionAssistant.tsx
 * 🎤 O primeiro assistente de voz consciente do planeta
 * 💎 Design: Apple + Tesla + Cyberpunk + $100M Aesthetic
 * 🔊 Voice: J.A.R.V.I.S. Real - Grave, Confiante, Elegante
 * 🎙️ Mic: Web Speech API com fallback completo
 * 📦 100% Modular - Usa custom hooks para toda lógica
 * ═══════════════════════════════════════════════════════════════════════════════
 */

'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { usePathname } from 'next/navigation';
import {
  Mic, MicOff, Send, X, Volume2, VolumeX, 
  Brain, Sparkles, ChevronUp, ChevronDown, 
  Loader2, Activity, Eye, Radio, Waves, AlertCircle
} from 'lucide-react';

// ═══════════════════════════════════════════════════════════════════════════════
// CUSTOM HOOKS
// ═══════════════════════════════════════════════════════════════════════════════

import { useOrionVoice } from '@/hooks/useOrionVoice';
import { useAudioVisualizer, useOrionPulse } from '@/hooks/useAudioVisualizer';
import { useOrionChat, type Message } from '@/hooks/useOrionChat';
import { useOrionSounds } from '@/hooks/useOrionSounds';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTE PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export default function OrionAssistant() {
  const pathname = usePathname();
  
  // ═══ STATE LOCAL (UI ONLY) ═══
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [inputText, setInputText] = useState('');
  const [showParticles, setShowParticles] = useState(false);
  
  // ═══ REFS ═══
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // ═══ CUSTOM HOOKS ═══
  const { playSound } = useOrionSounds();
  const { pulseIntensity, getGlow, getRotation, getScale } = useOrionPulse();
  const { state: audioState, startAnalysis, stopAnalysis } = useAudioVisualizer();
  const { state: chatState, sendMessage, addGreeting, toggleGodMode } = useOrionChat(pathname);
  
  // Callback para quando transcrição estiver completa
  const handleTranscriptComplete = useCallback(async (transcript: string) => {
    playSound('success');
    setInputText('');
    
    // Verificar se é um "wake word"
    if (transcript.toLowerCase().includes('orion')) {
      playSound('wakeup');
      setShowParticles(true);
      setTimeout(() => setShowParticles(false), 2000);
    }
    
    const response = await sendMessage(transcript, true);
    if (response) {
      speak(response);
    }
  }, [sendMessage, playSound]);
  
  const { 
    state: voiceState, 
    startListening, 
    stopListening, 
    speak, 
    toggleVoice,
    clearError,
    getMediaStream,
  } = useOrionVoice(handleTranscriptComplete);

  // ═══════════════════════════════════════════════════════════════════════════════
  // EFEITOS
  // ═══════════════════════════════════════════════════════════════════════════════

  // Auto-scroll para última mensagem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatState.messages]);

  // Saudação inicial quando abre
  useEffect(() => {
    if (isOpen && !chatState.hasGreeted) {
      addGreeting();
      if (voiceState.voiceEnabled) {
        setTimeout(() => {
          speak('Olá. Sou ORION, comandante do ALSHAM QUANTUM. 139 agentes estão sob meu comando. Como posso ajudar?');
        }, 500);
      }
    }
  }, [isOpen, chatState.hasGreeted, addGreeting, speak, voiceState.voiceEnabled]);

  // Atualizar input com transcrição em tempo real
  useEffect(() => {
    if (voiceState.currentTranscript) {
      setInputText(voiceState.currentTranscript);
    }
  }, [voiceState.currentTranscript]);

  // Gerenciar visualização de áudio
  useEffect(() => {
    if (voiceState.isListening) {
      const stream = getMediaStream();
      if (stream) {
        startAnalysis(stream);
      }
    } else {
      stopAnalysis();
    }
  }, [voiceState.isListening, getMediaStream, startAnalysis, stopAnalysis]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // HANDLERS
  // ═══════════════════════════════════════════════════════════════════════════════

  const handleToggleOpen = useCallback(() => {
    playSound(isOpen ? 'click' : 'activate');
    setIsOpen(prev => !prev);
  }, [isOpen, playSound]);

  const handleToggleMinimize = useCallback(() => {
    playSound('click');
    setIsMinimized(prev => !prev);
  }, [playSound]);

  const handleToggleVoice = useCallback(() => {
    playSound('click');
    toggleVoice();
  }, [playSound, toggleVoice]);

  const handleToggleGodMode = useCallback(() => {
    playSound('click');
    toggleGodMode();
  }, [playSound, toggleGodMode]);

  const handleMicClick = useCallback(async () => {
    if (voiceState.isListening) {
      stopListening();
    } else {
      clearError();
      await startListening();
    }
  }, [voiceState.isListening, startListening, stopListening, clearError]);

  const handleSendMessage = useCallback(async () => {
    const text = inputText.trim();
    if (!text || chatState.isThinking) return;
    
    setInputText('');
    playSound('click');
    
    const response = await sendMessage(text, false);
    if (response && voiceState.voiceEnabled) {
      speak(response);
    }
  }, [inputText, chatState.isThinking, sendMessage, speak, voiceState.voiceEnabled, playSound]);

  const handleQuickCommand = useCallback(async (cmd: string) => {
    playSound('click');
    const response = await sendMessage(`ORION, ${cmd.toLowerCase()}`, false);
    if (response && voiceState.voiceEnabled) {
      speak(response);
    }
  }, [sendMessage, speak, voiceState.voiceEnabled, playSound]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // VARIÁVEIS DE ESTILO CALCULADAS
  // ═══════════════════════════════════════════════════════════════════════════════

  const orbGlow = getGlow();
  const ringRotation = getRotation();
  const iconScale = getScale();
  const audioLevel = audioState.audioLevel;

  // Estado combinado para UI
  const isListening = voiceState.isListening;
  const isSpeaking = voiceState.isSpeaking;
  const isThinking = chatState.isThinking;
  const hasError = !!voiceState.error;

  return (
    <>
      {/* ════════════════════════════════════════════════════════════════════════ */}
      {/* ORB FLUTUANTE - DESIGN BILIONÁRIO ($100M AESTHETIC)                      */}
      {/* ════════════════════════════════════════════════════════════════════════ */}
      <div 
        className="fixed"
        style={{ 
          bottom: '28px', 
          right: '28px', 
          zIndex: 99999,
          pointerEvents: 'auto',
        }}
      >
        {/* ORB Principal */}
        <button
          onClick={handleToggleOpen}
          className={`relative transition-all duration-700 ease-out group ${
            isOpen ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'
          }`}
          style={{ width: '72px', height: '72px' }}
          aria-label="Abrir ORION J.A.R.V.I.S."
        >
          {/* ═══ CAMADA 1: GLOW EXTERNO DIFUSO ═══ */}
          <div 
            className={`absolute rounded-full transition-all duration-500 ${
              isListening ? 'bg-red-500' :
              isSpeaking ? 'bg-amber-400' :
              isThinking ? 'bg-violet-500' :
              'bg-amber-500'
            }`}
            style={{
              inset: '-20px',
              opacity: isListening ? 0.4 : orbGlow * 0.3,
              filter: 'blur(20px)',
              animation: isListening ? 'pulse 1s infinite' : undefined,
            }}
          />
          
          {/* ═══ CAMADA 2: ANEL DE LUZ DOURADO ROTATIVO ═══ */}
          <div 
            className="absolute rounded-full"
            style={{
              inset: '-8px',
              transform: `rotate(${ringRotation}deg)`,
              transition: 'transform 0.05s linear',
            }}
          >
            <svg className="w-full h-full" viewBox="0 0 100 100">
              <defs>
                <linearGradient id="orion-gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#FFD700" stopOpacity="1" />
                  <stop offset="25%" stopColor="#FFA500" stopOpacity="0.3" />
                  <stop offset="50%" stopColor="#FFD700" stopOpacity="1" />
                  <stop offset="75%" stopColor="#FFA500" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#FFD700" stopOpacity="1" />
                </linearGradient>
                <filter id="orion-glow">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>
              <circle 
                cx="50" cy="50" r="46" 
                fill="none" 
                stroke="url(#orion-gold-gradient)" 
                strokeWidth="2.5"
                strokeDasharray="15 8 30 8"
                filter="url(#orion-glow)"
                style={{ opacity: isListening ? 0 : 0.9 }}
              />
              <circle 
                cx="50" cy="50" r="40" 
                fill="none" 
                stroke="#FFD700" 
                strokeWidth="0.5"
                strokeDasharray="4 12"
                opacity="0.4"
              />
            </svg>
          </div>

          {/* ═══ CAMADA 3: CRISTAL NEGRO CENTRAL ═══ */}
          <div 
            className={`relative w-full h-full rounded-full overflow-hidden transition-all duration-300 ${
              isListening ? 'shadow-[0_0_40px_rgba(239,68,68,0.8),inset_0_0_30px_rgba(239,68,68,0.3)]' :
              isSpeaking ? 'shadow-[0_0_40px_rgba(251,191,36,0.8),inset_0_0_30px_rgba(251,191,36,0.3)]' :
              isThinking ? 'shadow-[0_0_40px_rgba(139,92,246,0.8),inset_0_0_30px_rgba(139,92,246,0.3)]' :
              'shadow-[0_0_30px_rgba(251,191,36,0.4),inset_0_0_20px_rgba(0,0,0,0.8)]'
            }`}
            style={{
              background: isListening 
                ? 'linear-gradient(145deg, #1a0000 0%, #0a0000 50%, #000000 100%)'
                : isSpeaking
                ? 'linear-gradient(145deg, #1a1500 0%, #0a0a00 50%, #000000 100%)'
                : isThinking
                ? 'linear-gradient(145deg, #0a0015 0%, #050008 50%, #000000 100%)'
                : 'linear-gradient(145deg, #0a0a0a 0%, #050505 50%, #000000 100%)',
            }}
          >
            {/* Borda interna metálica */}
            <div 
              className="absolute rounded-full"
              style={{
                inset: '3px',
                border: isListening 
                  ? '1px solid rgba(239, 68, 68, 0.5)'
                  : '1px solid rgba(255, 215, 0, 0.3)',
                background: 'transparent',
              }}
            />
            
            {/* Reflexo de luz superior */}
            <div 
              className="absolute rounded-full bg-white"
              style={{
                top: '8px',
                left: '12px',
                width: '16px',
                height: '8px',
                opacity: 0.15,
                filter: 'blur(4px)',
              }}
            />
            
            {/* ═══ ÍCONE CENTRAL ═══ */}
            <div className="absolute inset-0 flex items-center justify-center">
              {isThinking ? (
                <Loader2 className="w-8 h-8 text-violet-400 animate-spin" />
              ) : isListening ? (
                <div className="relative">
                  {/* Ondas sonoras animadas */}
                  <div className="absolute inset-[-12px] flex items-center justify-center">
                    {[...Array(3)].map((_, i) => (
                      <div
                        key={i}
                        className="absolute rounded-full border-2 border-red-400 animate-ping"
                        style={{
                          width: `${24 + i * 16}px`,
                          height: `${24 + i * 16}px`,
                          animationDelay: `${i * 0.2}s`,
                          animationDuration: '1.5s',
                          opacity: 0.6 - i * 0.2,
                        }}
                      />
                    ))}
                  </div>
                  <Waves 
                    className="w-8 h-8 text-red-400 relative z-10"
                    style={{ 
                      transform: `scale(${1 + audioLevel * 0.3})`,
                      filter: 'drop-shadow(0 0 8px rgba(239, 68, 68, 0.8))',
                    }}
                  />
                </div>
              ) : isSpeaking ? (
                <Radio 
                  className="w-8 h-8 text-amber-400 animate-pulse"
                  style={{ filter: 'drop-shadow(0 0 8px rgba(251, 191, 36, 0.8))' }}
                />
              ) : (
                <Eye 
                  className="w-8 h-8 text-amber-400 transition-all duration-300 group-hover:text-amber-300"
                  style={{ 
                    filter: 'drop-shadow(0 0 8px rgba(251, 191, 36, 0.6))',
                    transform: `scale(${iconScale})`,
                  }}
                />
              )}
            </div>
          </div>
          
          {/* ═══ BADGE LIVE - NEON CIANO ═══ */}
          <div 
            className="absolute flex items-center gap-1.5 px-2.5 py-1 rounded-full"
            style={{
              top: '-6px',
              right: '-6px',
              background: 'rgba(0, 0, 0, 0.9)',
              border: '1px solid rgba(34, 211, 238, 0.6)',
              boxShadow: '0 0 15px rgba(34, 211, 238, 0.5), inset 0 0 10px rgba(34, 211, 238, 0.1)',
            }}
          >
            <div 
              className="w-2 h-2 rounded-full animate-pulse"
              style={{ 
                background: '#22D3EE',
                boxShadow: '0 0 8px #22D3EE',
              }}
            />
            <span 
              className="text-[10px] font-bold tracking-widest orbitron"
              style={{ 
                color: '#22D3EE',
                textShadow: '0 0 10px rgba(34, 211, 238, 0.8)',
              }}
            >
              LIVE
            </span>
          </div>

          {/* ═══ PARTÍCULAS FLUTUANTES DOURADAS ═══ */}
          <div className="absolute inset-[-16px] pointer-events-none overflow-visible">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className={`absolute rounded-full ${showParticles ? 'animate-orion-particle-burst' : 'animate-orion-particle'}`}
                style={{
                  width: `${2 + (i % 3)}px`,
                  height: `${2 + (i % 3)}px`,
                  background: i % 2 === 0 ? '#FFD700' : '#22D3EE',
                  boxShadow: i % 2 === 0 ? '0 0 6px #FFD700' : '0 0 6px #22D3EE',
                  left: `${15 + i * 10}%`,
                  top: `${10 + (i % 4) * 25}%`,
                  animationDelay: `${i * 0.4}s`,
                  animationDuration: showParticles ? '0.8s' : `${3 + i * 0.3}s`,
                }}
              />
            ))}
          </div>
        </button>

        {/* ════════════════════════════════════════════════════════════════════════ */}
        {/* PAINEL DO CHAT - DESIGN PREMIUM CYBERPUNK                               */}
        {/* ════════════════════════════════════════════════════════════════════════ */}
        <div 
          className={`absolute bottom-0 right-0 w-[420px] transition-all duration-500 ease-out ${
            isOpen 
              ? 'opacity-100 scale-100 translate-y-0' 
              : 'opacity-0 scale-95 translate-y-4 pointer-events-none'
          }`}
        >
          <div 
            className="relative overflow-hidden"
            style={{
              background: 'linear-gradient(180deg, rgba(5,5,5,0.98) 0%, rgba(0,0,0,0.99) 100%)',
              backdropFilter: 'blur(24px)',
              border: '1px solid rgba(255, 215, 0, 0.15)',
              borderRadius: '24px',
              boxShadow: `
                0 0 60px rgba(251, 191, 36, 0.12),
                0 25px 60px rgba(0, 0, 0, 0.9),
                inset 0 1px 0 rgba(255, 255, 255, 0.05)
              `,
            }}
          >
            
            {/* Linha dourada superior */}
            <div 
              className="absolute top-0 left-0 right-0 h-[2px]"
              style={{
                background: 'linear-gradient(90deg, transparent 0%, rgba(255, 215, 0, 0.6) 50%, transparent 100%)',
              }}
            />
            
            {/* ═══ HEADER ═══ */}
            <div className="relative p-5 border-b border-white/5">
              <div 
                className="absolute inset-0"
                style={{
                  background: 'linear-gradient(90deg, rgba(255, 215, 0, 0.03) 0%, transparent 50%, rgba(34, 211, 238, 0.03) 100%)',
                }}
              />
              
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {/* Avatar ORION */}
                  <div className="relative">
                    <div 
                      className="w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-300"
                      style={{
                        background: isListening 
                          ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%)'
                          : isSpeaking
                          ? 'linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(251, 191, 36, 0.05) 100%)'
                          : isThinking
                          ? 'linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%)'
                          : 'linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(34, 211, 238, 0.05) 100%)',
                        border: isListening 
                          ? '1px solid rgba(239, 68, 68, 0.4)'
                          : isSpeaking
                          ? '1px solid rgba(251, 191, 36, 0.4)'
                          : isThinking
                          ? '1px solid rgba(139, 92, 246, 0.4)'
                          : '1px solid rgba(255, 215, 0, 0.25)',
                        boxShadow: isListening 
                          ? '0 0 25px rgba(239, 68, 68, 0.3)'
                          : isSpeaking
                          ? '0 0 25px rgba(251, 191, 36, 0.3)'
                          : isThinking
                          ? '0 0 25px rgba(139, 92, 246, 0.3)'
                          : '0 0 20px rgba(255, 215, 0, 0.15)',
                      }}
                    >
                      {isThinking ? (
                        <Loader2 className="w-7 h-7 text-violet-400 animate-spin" />
                      ) : isListening ? (
                        <Activity className="w-7 h-7 text-red-400 animate-pulse" />
                      ) : isSpeaking ? (
                        <Volume2 className="w-7 h-7 text-amber-400 animate-pulse" />
                      ) : (
                        <Sparkles className="w-7 h-7 text-amber-400" />
                      )}
                    </div>
                    {/* Status indicator */}
                    <div 
                      className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full border-2 border-black"
                      style={{
                        background: isListening ? '#EF4444' :
                          isSpeaking ? '#FBBF24' :
                          isThinking ? '#8B5CF6' : '#10B981',
                        boxShadow: isListening ? '0 0 8px #EF4444' :
                          isSpeaking ? '0 0 8px #FBBF24' :
                          isThinking ? '0 0 8px #8B5CF6' : '0 0 8px #10B981',
                      }}
                    />
                  </div>
                  
                  <div>
                    <h3 
                      className="text-lg font-black text-white tracking-wide flex items-center gap-2 orbitron"
                    >
                      ORION
                      <span 
                        className="px-2.5 py-0.5 text-[9px] font-bold rounded-full"
                        style={{
                          background: 'linear-gradient(90deg, rgba(255, 215, 0, 0.15) 0%, rgba(34, 211, 238, 0.15) 100%)',
                          border: '1px solid rgba(255, 215, 0, 0.3)',
                          color: '#FFD700',
                          letterSpacing: '0.1em',
                        }}
                      >
                        J.A.R.V.I.S.
                      </span>
                    </h3>
                    <p className="text-[11px] text-gray-500 font-mono mt-0.5">
                      {isListening ? '🎤 Ouvindo você...' :
                       isSpeaking ? '🔊 Falando...' :
                       isThinking ? '🧠 Processando...' :
                       '● Online • 139 agents • Ready'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-1.5">
                  {/* Toggle Voice */}
                  <button
                    onClick={handleToggleVoice}
                    className="p-2.5 rounded-xl transition-all"
                    style={{
                      background: voiceState.voiceEnabled ? 'rgba(255, 215, 0, 0.1)' : 'rgba(255, 255, 255, 0.03)',
                      border: voiceState.voiceEnabled ? '1px solid rgba(255, 215, 0, 0.3)' : '1px solid rgba(255, 255, 255, 0.08)',
                      color: voiceState.voiceEnabled ? '#FFD700' : '#6B7280',
                    }}
                    title={voiceState.voiceEnabled ? 'Desativar voz' : 'Ativar voz'}
                  >
                    {voiceState.voiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                  </button>
                  
                  {/* God Mode */}
                  <button
                    onClick={handleToggleGodMode}
                    className="p-2.5 rounded-xl transition-all"
                    style={{
                      background: chatState.godMode ? 'rgba(139, 92, 246, 0.1)' : 'rgba(255, 255, 255, 0.03)',
                      border: chatState.godMode ? '1px solid rgba(139, 92, 246, 0.3)' : '1px solid rgba(255, 255, 255, 0.08)',
                      color: chatState.godMode ? '#8B5CF6' : '#6B7280',
                    }}
                    title="God Mode"
                  >
                    <Brain className="w-4 h-4" />
                  </button>
                  
                  {/* Minimize */}
                  <button
                    onClick={handleToggleMinimize}
                    className="p-2.5 rounded-xl transition-all hover:bg-white/5"
                    style={{
                      background: 'rgba(255, 255, 255, 0.03)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      color: '#9CA3AF',
                    }}
                  >
                    {isMinimized ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  
                  {/* Close */}
                  <button
                    onClick={handleToggleOpen}
                    className="p-2.5 rounded-xl transition-all hover:bg-red-500/10 hover:border-red-500/30"
                    style={{
                      background: 'rgba(255, 255, 255, 0.03)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      color: '#9CA3AF',
                    }}
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* ═══ MESSAGES ═══ */}
            {!isMinimized && (
              <div 
                className="h-80 overflow-y-auto p-5 space-y-4"
                style={{
                  scrollbarWidth: 'thin',
                  scrollbarColor: 'rgba(255, 215, 0, 0.2) transparent',
                }}
              >
                {chatState.messages.map((msg: Message) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
                  >
                    <div 
                      className="max-w-[85%] p-4 rounded-2xl"
                      style={{
                        background: msg.role === 'user'
                          ? 'linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%)'
                          : 'rgba(255, 255, 255, 0.03)',
                        border: msg.role === 'user'
                          ? '1px solid rgba(255, 215, 0, 0.2)'
                          : '1px solid rgba(255, 255, 255, 0.06)',
                        borderRadius: msg.role === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
                      }}
                    >
                      <div className="flex items-center gap-2 mb-2">
                        {msg.role === 'orion' && <Sparkles className="w-3 h-3 text-amber-400" />}
                        <span 
                          className="text-[10px] uppercase tracking-wider font-mono"
                          style={{ color: msg.role === 'user' ? '#FFD700' : '#6B7280' }}
                        >
                          {msg.role === 'user' ? 'VOCÊ' : 'ORION'}
                          {msg.isVoice && <Mic className="w-2.5 h-2.5 inline ml-1 text-red-400" />}
                        </span>
                      </div>
                      <p className="text-sm text-white/90 leading-relaxed">{msg.content}</p>
                      
                      {chatState.godMode && msg.tokens && (
                        <div className="mt-3 pt-2 border-t border-white/5 flex gap-3 text-[9px] text-gray-600 font-mono">
                          <span>{msg.tokens} tokens</span>
                          <span>{msg.executionTime}ms</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {isThinking && (
                  <div className="flex justify-start animate-fadeIn">
                    <div 
                      className="p-4 rounded-2xl"
                      style={{
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid rgba(255, 255, 255, 0.06)',
                        borderRadius: '20px 20px 20px 4px',
                      }}
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-violet-500 rounded-full animate-bounce" style={{ boxShadow: '0 0 8px #8B5CF6' }} />
                        <div className="w-2 h-2 bg-violet-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s', boxShadow: '0 0 8px #8B5CF6' }} />
                        <div className="w-2 h-2 bg-violet-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s', boxShadow: '0 0 8px #8B5CF6' }} />
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
              <div 
                className="p-5 border-t"
                style={{
                  borderColor: 'rgba(255, 255, 255, 0.05)',
                  background: 'rgba(0, 0, 0, 0.4)',
                }}
              >
                {/* ═══ AVISO DE ERRO ELEGANTE ═══ */}
                {hasError && voiceState.error && (
                  <div 
                    className="mb-4 p-3 rounded-xl flex items-start gap-3 animate-fadeIn"
                    style={{
                      background: voiceState.error.type === 'browser-unsupported' 
                        ? 'rgba(251, 191, 36, 0.1)'
                        : 'rgba(239, 68, 68, 0.1)',
                      border: voiceState.error.type === 'browser-unsupported'
                        ? '1px solid rgba(251, 191, 36, 0.3)'
                        : '1px solid rgba(239, 68, 68, 0.3)',
                    }}
                  >
                    <AlertCircle 
                      className="w-4 h-4 flex-shrink-0 mt-0.5"
                      style={{ 
                        color: voiceState.error.type === 'browser-unsupported' ? '#FBBF24' : '#EF4444' 
                      }}
                    />
                    <div className="flex-1">
                      <p 
                        className="text-xs leading-relaxed"
                        style={{ 
                          color: voiceState.error.type === 'browser-unsupported' ? '#FBBF24' : '#EF4444' 
                        }}
                      >
                        {voiceState.error.message}
                      </p>
                      {voiceState.error.recoverable && (
                        <button
                          onClick={clearError}
                          className="text-[10px] mt-1 underline opacity-70 hover:opacity-100"
                          style={{ 
                            color: voiceState.error.type === 'browser-unsupported' ? '#FBBF24' : '#EF4444' 
                          }}
                        >
                          Fechar
                        </button>
                      )}
                    </div>
                  </div>
                )}

                <div className="flex items-center gap-3">
                  {/* ═══ BOTÃO DO MICROFONE - PREMIUM ═══ */}
                  <button
                    onClick={handleMicClick}
                    disabled={isThinking || !voiceState.browserSupported}
                    className="relative p-4 rounded-2xl transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed"
                    style={{
                      background: isListening 
                        ? 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)'
                        : 'linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%)',
                      border: isListening 
                        ? '1px solid #EF4444'
                        : '1px solid rgba(255, 215, 0, 0.3)',
                      boxShadow: isListening 
                        ? '0 0 30px rgba(239, 68, 68, 0.6), inset 0 0 20px rgba(0, 0, 0, 0.3)'
                        : '0 0 20px rgba(255, 215, 0, 0.2)',
                      color: isListening ? '#FFFFFF' : '#FFD700',
                    }}
                    title={isListening ? 'Parar de ouvir' : voiceState.browserSupported ? 'Clique para falar' : 'Navegador não suporta voz'}
                  >
                    {isListening ? (
                      <>
                        <MicOff className="w-5 h-5 relative z-10" />
                        {/* Visualização de nível de áudio */}
                        <div 
                          className="absolute inset-0 rounded-2xl bg-red-400 animate-ping"
                          style={{ 
                            opacity: 0.3,
                            transform: `scale(${1 + audioLevel * 0.5})`,
                          }}
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
                      onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                      placeholder={isListening ? 'Fale agora...' : 'Digite ou clique no mic...'}
                      disabled={isListening || isThinking}
                      className="w-full rounded-2xl px-5 py-4 text-sm text-white placeholder-gray-500 transition-all focus:outline-none disabled:opacity-50"
                      style={{
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                      }}
                    />
                  </div>
                  
                  {/* Send Button */}
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputText.trim() || isThinking}
                    className="p-4 rounded-2xl transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                    style={{
                      background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
                      boxShadow: '0 0 25px rgba(255, 215, 0, 0.4)',
                      color: '#000000',
                    }}
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                
                {/* Quick Commands */}
                <div className="mt-4 flex flex-wrap gap-2">
                  {['Status', 'Histórico', 'Evoluir', 'Processar'].map((cmd) => (
                    <button
                      key={cmd}
                      onClick={() => handleQuickCommand(cmd)}
                      disabled={isThinking}
                      className="px-4 py-2 text-[11px] rounded-xl transition-all font-medium tracking-wide disabled:opacity-40"
                      style={{
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        color: '#9CA3AF',
                      }}
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

      {/* ════════════════════════════════════════════════════════════════════════ */}
      {/* ESTILOS CSS PREMIUM                                                       */}
      {/* ════════════════════════════════════════════════════════════════════════ */}
      <style jsx>{`
        @keyframes orion-particle {
          0%, 100% { 
            transform: translateY(0) translateX(0) scale(1); 
            opacity: 0.6; 
          }
          25% {
            transform: translateY(-15px) translateX(8px) scale(1.2);
            opacity: 1;
          }
          50% { 
            transform: translateY(-25px) translateX(-5px) scale(0.8); 
            opacity: 0.8; 
          }
          75% {
            transform: translateY(-10px) translateX(12px) scale(1.1);
            opacity: 0.9;
          }
        }
        .animate-orion-particle {
          animation: orion-particle 4s ease-in-out infinite;
        }
        @keyframes orion-particle-burst {
          0% { 
            transform: translateY(0) translateX(0) scale(1); 
            opacity: 1; 
          }
          100% { 
            transform: translateY(-60px) translateX(var(--tx, 20px)) scale(0); 
            opacity: 0; 
          }
        }
        .animate-orion-particle-burst {
          animation: orion-particle-burst 0.8s ease-out forwards;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.4; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(1.1); }
        }
      `}</style>
    </>
  );
}
