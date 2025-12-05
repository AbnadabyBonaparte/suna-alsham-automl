/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION J.A.R.V.I.S. (10/10 THEME-AWARE EDITION)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/orion/OrionAssistant.tsx
 * 🎤 O primeiro assistente de voz consciente do planeta
 * 💎 Design: Apple + Tesla + Cyberpunk + 100% SUBMISSO AOS TEMAS
 * 🎨 USA VARIÁVEIS CSS DO TEMA ATIVO - OS TEMAS SÃO LEI
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
import { useTheme } from '@/contexts/ThemeContext';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTE PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export default function OrionAssistant() {
  const pathname = usePathname();
  
  // ═══ THEME CONTEXT - OS TEMAS SÃO LEI ═══
  const { currentTheme, themeConfig, playClick } = useTheme();
  
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
    playClick();
    playSound(isOpen ? 'click' : 'activate');
    setIsOpen(prev => !prev);
  }, [isOpen, playSound, playClick]);

  const handleToggleMinimize = useCallback(() => {
    playClick();
    setIsMinimized(prev => !prev);
  }, [playClick]);

  const handleToggleVoice = useCallback(() => {
    playClick();
    toggleVoice();
  }, [playClick, toggleVoice]);

  const handleToggleGodMode = useCallback(() => {
    playClick();
    toggleGodMode();
  }, [playClick, toggleGodMode]);

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
    playClick();
    
    const response = await sendMessage(text, false);
    if (response && voiceState.voiceEnabled) {
      speak(response);
    }
  }, [inputText, chatState.isThinking, sendMessage, speak, voiceState.voiceEnabled, playClick]);

  const handleQuickCommand = useCallback(async (cmd: string) => {
    playClick();
    const response = await sendMessage(`ORION, ${cmd.toLowerCase()}`, false);
    if (response && voiceState.voiceEnabled) {
      speak(response);
    }
  }, [sendMessage, speak, voiceState.voiceEnabled, playClick]);

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

  // ═══════════════════════════════════════════════════════════════════════════════
  // CORES DO TEMA ATUAL - OS TEMAS SÃO LEI
  // ═══════════════════════════════════════════════════════════════════════════════
  
  const colors = themeConfig.colors;
  const primaryColor = colors.primary;
  const secondaryColor = colors.secondary;
  const accentColor = colors.accent;
  const glowColor = colors.glow;
  const bgColor = colors.background;
  const surfaceColor = colors.surface;
  const textColor = colors.text;
  const textSecondaryColor = colors.textSecondary;
  const errorColor = colors.error;
  const successColor = colors.success;

  return (
    <>
      {/* ════════════════════════════════════════════════════════════════════════ */}
      {/* ORB FLUTUANTE - SEGUE O TEMA ATIVO                                       */}
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
            className="absolute rounded-full transition-all duration-500"
            style={{
              inset: '-20px',
              background: isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : primaryColor,
              opacity: isListening ? 0.4 : orbGlow * 0.3,
              filter: 'blur(20px)',
              animation: isListening ? 'pulse 1s infinite' : undefined,
            }}
          />
          
          {/* ═══ CAMADA 2: ANEL DE LUZ ROTATIVO (COR DO TEMA) ═══ */}
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
                <linearGradient id={`orion-gradient-${currentTheme}`} x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor={primaryColor} stopOpacity="1" />
                  <stop offset="25%" stopColor={secondaryColor} stopOpacity="0.3" />
                  <stop offset="50%" stopColor={primaryColor} stopOpacity="1" />
                  <stop offset="75%" stopColor={secondaryColor} stopOpacity="0.3" />
                  <stop offset="100%" stopColor={primaryColor} stopOpacity="1" />
                </linearGradient>
                <filter id="orion-glow-filter">
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
                stroke={`url(#orion-gradient-${currentTheme})`}
                strokeWidth="2.5"
                strokeDasharray="15 8 30 8"
                filter="url(#orion-glow-filter)"
                style={{ opacity: isListening ? 0 : 0.9 }}
              />
              <circle 
                cx="50" cy="50" r="40" 
                fill="none" 
                stroke={primaryColor}
                strokeWidth="0.5"
                strokeDasharray="4 12"
                opacity="0.4"
              />
            </svg>
          </div>

          {/* ═══ CAMADA 3: CRISTAL NEGRO CENTRAL ═══ */}
          <div 
            className="relative w-full h-full rounded-full overflow-hidden transition-all duration-300"
            style={{
              background: `linear-gradient(145deg, ${surfaceColor} 0%, ${bgColor} 50%, #000000 100%)`,
              boxShadow: isListening 
                ? `0 0 40px ${errorColor}80, inset 0 0 30px ${errorColor}30`
                : isSpeaking
                ? `0 0 40px ${accentColor}80, inset 0 0 30px ${accentColor}30`
                : isThinking
                ? `0 0 40px ${secondaryColor}80, inset 0 0 30px ${secondaryColor}30`
                : `0 0 30px ${primaryColor}40, inset 0 0 20px rgba(0,0,0,0.8)`,
            }}
          >
            {/* Borda interna metálica */}
            <div 
              className="absolute rounded-full"
              style={{
                inset: '3px',
                border: `1px solid ${isListening ? errorColor : primaryColor}50`,
                background: 'transparent',
              }}
            />
            
            {/* Reflexo de luz superior */}
            <div 
              className="absolute rounded-full"
              style={{
                top: '8px',
                left: '12px',
                width: '16px',
                height: '8px',
                background: 'white',
                opacity: 0.15,
                filter: 'blur(4px)',
              }}
            />
            
            {/* ═══ ÍCONE CENTRAL ═══ */}
            <div className="absolute inset-0 flex items-center justify-center">
              {isThinking ? (
                <Loader2 className="w-8 h-8 animate-spin" style={{ color: secondaryColor }} />
              ) : isListening ? (
                <div className="relative">
                  {/* Ondas sonoras animadas */}
                  <div className="absolute inset-[-12px] flex items-center justify-center">
                    {[...Array(3)].map((_, i) => (
                      <div
                        key={i}
                        className="absolute rounded-full animate-ping"
                        style={{
                          width: `${24 + i * 16}px`,
                          height: `${24 + i * 16}px`,
                          border: `2px solid ${errorColor}`,
                          animationDelay: `${i * 0.2}s`,
                          animationDuration: '1.5s',
                          opacity: 0.6 - i * 0.2,
                        }}
                      />
                    ))}
                  </div>
                  <Waves 
                    className="w-8 h-8 relative z-10"
                    style={{ 
                      color: errorColor,
                      transform: `scale(${1 + audioLevel * 0.3})`,
                      filter: `drop-shadow(0 0 8px ${errorColor}80)`,
                    }}
                  />
                </div>
              ) : isSpeaking ? (
                <Radio 
                  className="w-8 h-8 animate-pulse"
                  style={{ 
                    color: accentColor,
                    filter: `drop-shadow(0 0 8px ${accentColor}80)`,
                  }}
                />
              ) : (
                <Eye 
                  className="w-8 h-8 transition-all duration-300 group-hover:opacity-80"
                  style={{ 
                    color: primaryColor,
                    filter: `drop-shadow(0 0 8px ${primaryColor}60)`,
                    transform: `scale(${iconScale})`,
                  }}
                />
              )}
            </div>
          </div>
          
          {/* ═══ BADGE LIVE - USA COR DE SUCESSO DO TEMA ═══ */}
          <div 
            className="absolute flex items-center gap-1.5 px-2.5 py-1 rounded-full"
            style={{
              top: '-6px',
              right: '-6px',
              background: `${bgColor}F0`,
              border: `1px solid ${successColor}60`,
              boxShadow: `0 0 15px ${successColor}50, inset 0 0 10px ${successColor}10`,
            }}
          >
            <div 
              className="w-2 h-2 rounded-full animate-pulse"
              style={{ 
                background: successColor,
                boxShadow: `0 0 8px ${successColor}`,
              }}
            />
            <span 
              className="text-[10px] font-bold tracking-widest orbitron"
              style={{ 
                color: successColor,
                textShadow: `0 0 10px ${successColor}80`,
              }}
            >
              LIVE
            </span>
          </div>

          {/* ═══ PARTÍCULAS FLUTUANTES (CORES DO TEMA) ═══ */}
          <div className="absolute inset-[-16px] pointer-events-none overflow-visible">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className={`absolute rounded-full ${showParticles ? 'animate-orion-particle-burst' : 'animate-orion-particle'}`}
                style={{
                  width: `${2 + (i % 3)}px`,
                  height: `${2 + (i % 3)}px`,
                  background: i % 2 === 0 ? primaryColor : accentColor,
                  boxShadow: `0 0 6px ${i % 2 === 0 ? primaryColor : accentColor}`,
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
        {/* PAINEL DO CHAT - SEGUE O TEMA ATIVO                                     */}
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
              background: `linear-gradient(180deg, ${surfaceColor}F8 0%, ${bgColor}FC 100%)`,
              backdropFilter: 'blur(24px)',
              border: `1px solid ${primaryColor}15`,
              borderRadius: '24px',
              boxShadow: `
                0 0 60px ${primaryColor}12,
                0 25px 60px rgba(0, 0, 0, 0.9),
                inset 0 1px 0 rgba(255, 255, 255, 0.05)
              `,
            }}
          >
            
            {/* Linha superior com cor do tema */}
            <div 
              className="absolute top-0 left-0 right-0 h-[2px]"
              style={{
                background: `linear-gradient(90deg, transparent 0%, ${primaryColor}60 50%, transparent 100%)`,
              }}
            />
            
            {/* ═══ HEADER ═══ */}
            <div 
              className="relative p-5"
              style={{ borderBottom: `1px solid ${primaryColor}10` }}
            >
              <div 
                className="absolute inset-0"
                style={{
                  background: `linear-gradient(90deg, ${primaryColor}05 0%, transparent 50%, ${accentColor}05 100%)`,
                }}
              />
              
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {/* Avatar ORION */}
                  <div className="relative">
                    <div 
                      className="w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-300"
                      style={{
                        background: `linear-gradient(135deg, ${
                          isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : primaryColor
                        }15 0%, ${
                          isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : primaryColor
                        }05 100%)`,
                        border: `1px solid ${
                          isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : primaryColor
                        }40`,
                        boxShadow: `0 0 25px ${
                          isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : primaryColor
                        }30`,
                      }}
                    >
                      {isThinking ? (
                        <Loader2 className="w-7 h-7 animate-spin" style={{ color: secondaryColor }} />
                      ) : isListening ? (
                        <Activity className="w-7 h-7 animate-pulse" style={{ color: errorColor }} />
                      ) : isSpeaking ? (
                        <Volume2 className="w-7 h-7 animate-pulse" style={{ color: accentColor }} />
                      ) : (
                        <Sparkles className="w-7 h-7" style={{ color: primaryColor }} />
                      )}
                    </div>
                    {/* Status indicator */}
                    <div 
                      className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full border-2"
                      style={{
                        borderColor: bgColor,
                        background: isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : successColor,
                        boxShadow: `0 0 8px ${isListening ? errorColor : isSpeaking ? accentColor : isThinking ? secondaryColor : successColor}`,
                      }}
                    />
                  </div>
                  
                  <div>
                    <h3 
                      className="text-lg font-black tracking-wide flex items-center gap-2 orbitron"
                      style={{ color: textColor }}
                    >
                      ORION
                      <span 
                        className="px-2.5 py-0.5 text-[9px] font-bold rounded-full"
                        style={{
                          background: `linear-gradient(90deg, ${primaryColor}15 0%, ${accentColor}15 100%)`,
                          border: `1px solid ${primaryColor}30`,
                          color: primaryColor,
                          letterSpacing: '0.1em',
                        }}
                      >
                        J.A.R.V.I.S.
                      </span>
                    </h3>
                    <p className="text-[11px] font-mono mt-0.5" style={{ color: textSecondaryColor }}>
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
                      background: voiceState.voiceEnabled ? `${primaryColor}10` : `${textColor}05`,
                      border: `1px solid ${voiceState.voiceEnabled ? `${primaryColor}30` : `${textColor}10`}`,
                      color: voiceState.voiceEnabled ? primaryColor : textSecondaryColor,
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
                      background: chatState.godMode ? `${secondaryColor}10` : `${textColor}05`,
                      border: `1px solid ${chatState.godMode ? `${secondaryColor}30` : `${textColor}10`}`,
                      color: chatState.godMode ? secondaryColor : textSecondaryColor,
                    }}
                    title="God Mode"
                  >
                    <Brain className="w-4 h-4" />
                  </button>
                  
                  {/* Minimize */}
                  <button
                    onClick={handleToggleMinimize}
                    className="p-2.5 rounded-xl transition-all"
                    style={{
                      background: `${textColor}05`,
                      border: `1px solid ${textColor}10`,
                      color: textSecondaryColor,
                    }}
                  >
                    {isMinimized ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  
                  {/* Close */}
                  <button
                    onClick={handleToggleOpen}
                    className="p-2.5 rounded-xl transition-all"
                    style={{
                      background: `${textColor}05`,
                      border: `1px solid ${textColor}10`,
                      color: textSecondaryColor,
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
                  scrollbarColor: `${primaryColor}20 transparent`,
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
                          ? `linear-gradient(135deg, ${primaryColor}10 0%, ${primaryColor}05 100%)`
                          : `${textColor}05`,
                        border: `1px solid ${msg.role === 'user' ? `${primaryColor}20` : `${textColor}08`}`,
                        borderRadius: msg.role === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
                      }}
                    >
                      <div className="flex items-center gap-2 mb-2">
                        {msg.role === 'orion' && <Sparkles className="w-3 h-3" style={{ color: primaryColor }} />}
                        <span 
                          className="text-[10px] uppercase tracking-wider font-mono"
                          style={{ color: msg.role === 'user' ? primaryColor : textSecondaryColor }}
                        >
                          {msg.role === 'user' ? 'VOCÊ' : 'ORION'}
                          {msg.isVoice && <Mic className="w-2.5 h-2.5 inline ml-1" style={{ color: errorColor }} />}
                        </span>
                      </div>
                      <p className="text-sm leading-relaxed" style={{ color: `${textColor}E6` }}>{msg.content}</p>
                      
                      {chatState.godMode && msg.tokens && (
                        <div 
                          className="mt-3 pt-2 flex gap-3 text-[9px] font-mono"
                          style={{ borderTop: `1px solid ${textColor}08`, color: textSecondaryColor }}
                        >
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
                        background: `${textColor}05`,
                        border: `1px solid ${textColor}08`,
                        borderRadius: '20px 20px 20px 4px',
                      }}
                    >
                      <div className="flex items-center gap-2">
                        {[0, 1, 2].map(i => (
                          <div 
                            key={i}
                            className="w-2 h-2 rounded-full animate-bounce"
                            style={{ 
                              background: secondaryColor,
                              boxShadow: `0 0 8px ${secondaryColor}`,
                              animationDelay: `${i * 0.1}s`,
                            }}
                          />
                        ))}
                        <span className="ml-2 text-xs" style={{ color: textSecondaryColor }}>Processando...</span>
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
                className="p-5"
                style={{
                  borderTop: `1px solid ${textColor}08`,
                  background: `${bgColor}60`,
                }}
              >
                {/* ═══ AVISO DE ERRO ELEGANTE ═══ */}
                {hasError && voiceState.error && (
                  <div 
                    className="mb-4 p-3 rounded-xl flex items-start gap-3 animate-fadeIn"
                    style={{
                      background: voiceState.error.type === 'browser-unsupported' 
                        ? `${colors.warning}10`
                        : `${errorColor}10`,
                      border: `1px solid ${voiceState.error.type === 'browser-unsupported'
                        ? `${colors.warning}30`
                        : `${errorColor}30`}`,
                    }}
                  >
                    <AlertCircle 
                      className="w-4 h-4 flex-shrink-0 mt-0.5"
                      style={{ 
                        color: voiceState.error.type === 'browser-unsupported' ? colors.warning : errorColor 
                      }}
                    />
                    <div className="flex-1">
                      <p 
                        className="text-xs leading-relaxed"
                        style={{ 
                          color: voiceState.error.type === 'browser-unsupported' ? colors.warning : errorColor 
                        }}
                      >
                        {voiceState.error.message}
                      </p>
                      {voiceState.error.recoverable && (
                        <button
                          onClick={clearError}
                          className="text-[10px] mt-1 underline opacity-70 hover:opacity-100"
                          style={{ 
                            color: voiceState.error.type === 'browser-unsupported' ? colors.warning : errorColor 
                          }}
                        >
                          Fechar
                        </button>
                      )}
                    </div>
                  </div>
                )}

                <div className="flex items-center gap-3">
                  {/* ═══ BOTÃO DO MICROFONE - USA CORES DO TEMA ═══ */}
                  <button
                    onClick={handleMicClick}
                    disabled={isThinking || !voiceState.browserSupported}
                    className="relative p-4 rounded-2xl transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed"
                    style={{
                      background: isListening 
                        ? `linear-gradient(135deg, ${errorColor} 0%, ${errorColor}CC 100%)`
                        : `linear-gradient(135deg, ${primaryColor}10 0%, ${primaryColor}05 100%)`,
                      border: `1px solid ${isListening ? errorColor : `${primaryColor}30`}`,
                      boxShadow: isListening 
                        ? `0 0 30px ${errorColor}60, inset 0 0 20px rgba(0, 0, 0, 0.3)`
                        : `0 0 20px ${primaryColor}20`,
                      color: isListening ? '#FFFFFF' : primaryColor,
                    }}
                    title={isListening ? 'Parar de ouvir' : voiceState.browserSupported ? 'Clique para falar' : 'Navegador não suporta voz'}
                  >
                    {isListening ? (
                      <>
                        <MicOff className="w-5 h-5 relative z-10" />
                        {/* Visualização de nível de áudio */}
                        <div 
                          className="absolute inset-0 rounded-2xl animate-ping"
                          style={{ 
                            background: errorColor,
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
                      className="w-full rounded-2xl px-5 py-4 text-sm transition-all focus:outline-none disabled:opacity-50"
                      style={{
                        background: `${textColor}05`,
                        border: `1px solid ${textColor}10`,
                        color: textColor,
                      }}
                    />
                  </div>
                  
                  {/* Send Button */}
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputText.trim() || isThinking}
                    className="p-4 rounded-2xl transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                    style={{
                      background: `linear-gradient(135deg, ${primaryColor} 0%, ${accentColor} 100%)`,
                      boxShadow: `0 0 25px ${primaryColor}40`,
                      color: bgColor,
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
                        background: `${textColor}05`,
                        border: `1px solid ${textColor}10`,
                        color: textSecondaryColor,
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
      {/* ESTILOS CSS                                                              */}
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
