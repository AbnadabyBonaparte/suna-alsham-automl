/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION AI (SENTIENT CORE EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/orion/page.tsx
 * 📋 Chat AI com Voz, Avatar 3D Reativo e Seletor de Modelos
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    Mic, MicOff, Send, Bot, User, Sparkles, 
    ChevronDown, Cpu, Volume2, StopCircle 
} from 'lucide-react';

// --- CONFIGURAÇÃO DOS MODELOS ---
const AI_MODELS = [
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', provider: 'OpenAI', icon: '🟢' },
    { id: 'claude-3-5-sonnet', name: 'Claude 3.5 Sonnet', provider: 'Anthropic', icon: '🟣' },
    { id: 'gemini-1-5-pro', name: 'Gemini 1.5 Pro', provider: 'Google', icon: '🔵' },
    { id: 'llama-3-70b', name: 'Llama 3 (70B)', provider: 'Meta', icon: '🟠' },
];

interface Message {
    id: number;
    role: 'user' | 'ai';
    text: string;
    timestamp: string;
}

export default function OrionPage() {
    // Estado
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, role: 'ai', text: 'Sistemas online. Consciência Orion ativa. Como posso auxiliar na expansão do seu império hoje?', timestamp: 'Now' }
    ]);
    const [isRecording, setIsRecording] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [selectedModel, setSelectedModel] = useState(AI_MODELS[0]);
    const [isModelMenuOpen, setIsModelMenuOpen] = useState(false);
    
    // Refs
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const recognitionRef = useRef<any>(null);

    // Scroll automático
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // 1. ENGINE VISUAL 3D (O ROSTO DA IA)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        const particles: {x: number, y: number, radius: number, phase: number}[] = [];
        const particleCount = 150; // Densidade do núcleo

        const resize = () => {
            // Ajusta para o tamanho do container pai
            const parent = canvas.parentElement;
            if (parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        // Inicializar partículas
        for(let i=0; i<particleCount; i++) {
            particles.push({
                x: 0, y: 0, 
                radius: Math.random() * 2,
                phase: Math.random() * Math.PI * 2
            });
        }

        const render = () => {
            // Configurações dinâmicas baseadas no estado (Falando/Ouvindo/Pensando)
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            
            // Velocidade e amplitude reagem ao estado
            let speed = 0.02;
            let amplitude = 60;
            // Pega a cor do tema do CSS global
            let color = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';

            if (isSpeaking) {
                speed = 0.1; // Vibra rápido
                amplitude = 90 + Math.sin(time * 20) * 20; // Pulsa forte
            } else if (isRecording) {
                speed = 0.05;
                amplitude = 70;
                color = '#EF4444'; // Vermelho quando ouve (Gravação)
            }

            // Limpar com rastro (Trail effect)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            time += speed;

            // Converter cor HEX para RGB para manipular opacidade
            ctx.fillStyle = color;
            ctx.shadowBlur = 20;
            ctx.shadowColor = color;

            // Desenhar Esfera de Partículas
            particles.forEach((p, i) => {
                // Movimento orbital complexo
                const theta = p.phase + time + (i * 0.1);
                const radius = amplitude + Math.sin(theta * 3) * 20;
                
                // Se estiver falando, adiciona ruído de áudio simulado
                const audioNoise = isSpeaking ? (Math.random() - 0.5) * 30 : 0;

                p.x = centerX + Math.cos(theta) * (radius + audioNoise);
                p.y = centerY + Math.sin(theta * 1.5) * (radius + audioNoise) * 0.8; // Levemente oval

                // Tamanho pulsa
                const size = p.radius * (1 + Math.sin(time * 5) * 0.5);

                ctx.beginPath();
                ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
                ctx.globalAlpha = 0.6 + Math.sin(theta) * 0.4;
                ctx.fill();
            });
            ctx.globalAlpha = 1;

            // Núcleo Brilhante Central
            const coreSize = isSpeaking ? 30 + Math.random() * 10 : 20;
            const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, coreSize * 2);
            gradient.addColorStop(0, '#FFFFFF');
            gradient.addColorStop(0.5, color);
            gradient.addColorStop(1, 'transparent');
            
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(centerX, centerY, coreSize, 0, Math.PI * 2);
            ctx.fill();

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [isSpeaking, isRecording]);

    // 2. RECONHECIMENTO DE VOZ (Speech-to-Text)
    const toggleRecording = () => {
        if (isRecording) {
            recognitionRef.current?.stop();
            setIsRecording(false);
            return;
        }

        // Verificar suporte ao navegador
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Seu navegador não suporta reconhecimento de voz. Tente Chrome ou Edge.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'pt-BR';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => setIsRecording(true);
        
        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setInput(transcript);
        };

        recognition.onerror = (event: any) => {
            console.error("Erro no reconhecimento:", event.error);
            setIsRecording(false);
        };

        recognition.onend = () => setIsRecording(false);

        recognitionRef.current = recognition;
        recognition.start();
    };

    // 3. SÍNTESE DE VOZ (Text-to-Speech)
    const speakText = (text: string) => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'pt-BR';
            utterance.pitch = 0.9;
            utterance.rate = 1.1;

            utterance.onstart = () => setIsSpeaking(true);
            utterance.onend = () => setIsSpeaking(false);
            utterance.onerror = () => setIsSpeaking(false);

            window.speechSynthesis.speak(utterance);
        }
    };

    // 4. ENVIO DE MENSAGEM
    const handleSend = () => {
        if (!input.trim()) return;

        // Adicionar mensagem do usuário
        const newMsg: Message = {
            id: Date.now(),
            role: 'user',
            text: input,
            timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, newMsg]);
        setInput('');

        // Simular Resposta da IA
        setIsSpeaking(true);
        setTimeout(() => {
            const aiResponse = `Entendido. Utilizando o modelo ${selectedModel.name} para processar sua solicitação. A análise preliminar indica sucesso.`;
            
            const aiMsg: Message = {
                id: Date.now() + 1,
                role: 'ai',
                text: aiResponse,
                timestamp: new Date().toLocaleTimeString()
            };
            setMessages(prev => [...prev, aiMsg]);
            speakText(aiResponse);
        }, 1500);
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col md:flex-row gap-6 overflow-hidden relative p-4">
            
            {/* --- COLUNA DA ESQUERDA: O NÚCLEO DA IA (ROSTO) --- */}
            <div className="w-full md:w-1/3 flex flex-col gap-4 relative z-10 h-full">
                
                {/* 3D CORE VISUALIZER */}
                <div className="flex-1 bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl relative overflow-hidden group shadow-2xl min-h-[300px]">
                    <div className="absolute top-4 left-4 z-20 flex items-center gap-2 bg-black/60 px-3 py-1 rounded-full border border-white/10">
                        <div className={`w-2 h-2 rounded-full ${isSpeaking ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
                        <span className="text-xs font-mono text-white uppercase tracking-wider">
                            {isSpeaking ? 'FALANDO' : isRecording ? 'OUVINDO' : 'AGUARDANDO'}
                        </span>
                    </div>

                    <canvas 
                        ref={canvasRef} 
                        className="w-full h-full absolute inset-0 block"
                    />
                    
                    {/* Efeito Vignette */}
                    <div className="absolute inset-0 bg-radial-gradient from-transparent to-black/80 pointer-events-none" />
                </div>

                {/* SELETOR DE MODELO (LLM) */}
                <div className="relative">
                    <button 
                        onClick={() => setIsModelMenuOpen(!isModelMenuOpen)}
                        className="w-full p-4 bg-[var(--color-surface)]/80 backdrop-blur-md border border-[var(--color-border)]/30 rounded-xl flex items-center justify-between text-white hover:border-[var(--color-primary)] transition-all shadow-lg group"
                    >
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-white/5 group-hover:bg-[var(--color-primary)]/20 transition-colors">
                                <Cpu className="w-5 h-5 text-[var(--color-primary)]" />
                            </div>
                            <div className="text-left">
                                <div className="text-[10px] text-gray-400 font-mono uppercase">Modelo Ativo</div>
                                <div className="font-bold text-sm">{selectedModel.name}</div>
                            </div>
                        </div>
                        <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${isModelMenuOpen ? 'rotate-180' : ''}`} />
                    </button>

                    {/* Dropdown Menu */}
                    {isModelMenuOpen && (
                        <div className="absolute bottom-full left-0 right-0 mb-2 bg-[#050505]/95 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden shadow-2xl z-50 animate-slideUp">
                            {AI_MODELS.map(model => (
                                <button
                                    key={model.id}
                                    onClick={() => {
                                        setSelectedModel(model);
                                        setIsModelMenuOpen(false);
                                    }}
                                    className={`w-full p-3 flex items-center gap-3 hover:bg-white/5 transition-colors ${selectedModel.id === model.id ? 'bg-white/10' : ''}`}
                                >
                                    <span className="text-lg">{model.icon}</span>
                                    <div className="text-left">
                                        <div className={`text-sm font-medium ${selectedModel.id === model.id ? 'text-[var(--color-primary)]' : 'text-white'}`}>
                                            {model.name}
                                        </div>
                                        <div className="text-[10px] text-gray-500">{model.provider}</div>
                                    </div>
                                    {selectedModel.id === model.id && <Sparkles className="w-4 h-4 text-[var(--color-primary)] ml-auto" />}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* --- COLUNA DA DIREITA: INTERFACE DE CHAT --- */}
            <div className="flex-1 flex flex-col bg-black/20 backdrop-blur-md border border-white/5 rounded-3xl overflow-hidden relative h-full">
                
                {/* CHAT HISTORY */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-[var(--color-primary)]/20 scrollbar-track-transparent">
                    {messages.map((msg) => (
                        <div 
                            key={msg.id} 
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`
                                max-w-[80%] p-4 rounded-2xl relative group
                                ${msg.role === 'user' 
                                    ? 'bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/20 text-white rounded-tr-none' 
                                    : 'bg-white/5 border border-white/10 text-gray-200 rounded-tl-none'
                                }
                            `}>
                                <div className="flex items-center gap-2 mb-2 opacity-50">
                                    {msg.role === 'ai' ? <Bot className="w-3 h-3" /> : <User className="w-3 h-3" />}
                                    <span className="text-[10px] font-mono uppercase">
                                        {msg.role === 'ai' ? 'Orion Core' : 'Commander'} • {msg.timestamp}
                                    </span>
                                </div>
                                
                                <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>

                                {msg.role === 'ai' && (
                                    <button 
                                        onClick={() => speakText(msg.text)}
                                        className="absolute -right-10 top-2 p-2 rounded-full bg-white/5 hover:bg-[var(--color-primary)]/20 text-gray-400 hover:text-[var(--color-primary)] opacity-0 group-hover:opacity-100 transition-all"
                                        title="Ouvir"
                                    >
                                        <Volume2 className="w-4 h-4" />
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                {/* INPUT AREA */}
                <div className="p-4 bg-black/40 border-t border-white/5 backdrop-blur-xl">
                    <div className="relative flex items-center gap-2 bg-black/50 border border-white/10 rounded-2xl p-2 focus-within:border-[var(--color-primary)]/50 transition-all">
                        
                        {/* Voice Button */}
                        <button
                            onClick={toggleRecording}
                            className={`p-3 rounded-xl transition-all duration-300 ${
                                isRecording 
                                    ? 'bg-red-500/20 text-red-500 animate-pulse border border-red-500/50' 
                                    : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                            }`}
                            title={isRecording ? "Parar Gravação" : "Ativar Voz"}
                        >
                            {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                        </button>

                        {/* Text Input */}
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder={isRecording ? "Ouvindo..." : "Digite ou fale sua diretiva..."}
                            className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-600 font-mono text-sm"
                            autoFocus
                        />

                        {/* Send Button */}
                        <button
                            onClick={handleSend}
                            disabled={!input.trim()}
                            className="p-3 bg-[var(--color-primary)] hover:bg-[var(--color-accent)] disabled:opacity-50 rounded-xl text-black transition-all"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>

            <style jsx>{`
                @keyframes slideUp {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-slideUp { animation: slideUp 0.2s ease-out; }
            `}</style>
        </div>
    );
}
