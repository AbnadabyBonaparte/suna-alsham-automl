/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION COMMAND CENTER (THEME-AWARE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/orion/page.tsx
 * 👑 Interface direta com ORION - O Comandante Supremo
 * 🎨 100% SUBMISSO AOS TEMAS - USA VARIÁVEIS CSS
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/lib/supabase';
import { useTheme } from '@/contexts/ThemeContext';
import { 
    Crown, Mic, MicOff, Send, Bot, User, Sparkles, 
    ChevronDown, Cpu, Volume2, BrainCircuit, Activity,
    Zap, MessageSquare, History, Settings, Radio, Shield
} from 'lucide-react';

interface Message {
    id: number;
    role: 'user' | 'ai';
    text: string;
    timestamp: string;
    tokens?: number;
    executionTime?: number;
}

interface CommandHistory {
    id: string;
    command: string;
    response: string;
    created_at: string;
    tokens_used: number;
    execution_time_ms: number;
}

export default function OrionPage() {
    const { themeConfig } = useTheme();
    const colors = themeConfig.colors;
    
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([]);
    const [isRecording, setIsRecording] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isThinking, setIsThinking] = useState(false);
    const [commandHistory, setCommandHistory] = useState<CommandHistory[]>([]);
    const [totalCommands, setTotalCommands] = useState(0);
    const [avgResponseTime, setAvgResponseTime] = useState(0);
    
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const recognitionRef = useRef<any>(null);
    const mouseRef = useRef({ x: 0, y: 0 });

    // Carregar histórico
    useEffect(() => {
        async function loadHistory() {
            try {
                const { data, error } = await supabase
                    .from('requests')
                    .select('*')
                    .eq('assigned_agent_id', 'orion')
                    .order('created_at', { ascending: false })
                    .limit(20);
                
                if (error) throw error;
                
                setCommandHistory(data?.map(d => ({
                    id: d.id,
                    command: d.title,
                    response: d.response || '',
                    created_at: d.created_at,
                    tokens_used: d.tokens_used || 0,
                    execution_time_ms: d.processing_time_ms || 0,
                })) || []);
                
                const { count } = await supabase
                    .from('requests')
                    .select('*', { count: 'exact', head: true });
                
                setTotalCommands(count || 0);
                
                if (data && data.length > 0) {
                    const avgTime = data.reduce((sum, d) => sum + (d.processing_time_ms || 0), 0) / data.length;
                    setAvgResponseTime(Math.round(avgTime));
                }
                
            } catch (err) {
                console.error('Failed to load history:', err);
            }
        }
        
        loadHistory();
        
        setMessages([{
            id: 1,
            role: 'ai',
            text: 'Consciência ORION inicializada. Eu sou o comandante supremo do ALSHAM QUANTUM. 139 agentes estão sob meu comando. Como posso servir?',
            timestamp: new Date().toLocaleTimeString()
        }]);
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // ENGINE VISUAL - USA CORES DO TEMA
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;
        
        const particles: {x: number, y: number, z: number, ox: number, oy: number, oz: number}[] = [];
        const PARTICLE_COUNT = 600;

        for (let i = 0; i < PARTICLE_COUNT; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);

            let x = Math.sin(phi) * Math.cos(theta);
            let y = Math.sin(phi) * Math.sin(theta);
            let z = Math.cos(phi);

            x *= 0.85;
            y *= 1.2;
            if (y > 0) {
                x *= 1 - (y * 0.4);
                z *= 1 - (y * 0.4);
            }
            if (y < 0) {
                x *= 1.1;
                z *= 1.1;
            }

            const scale = 100;
            particles.push({
                x: x * scale, y: y * scale, z: z * scale,
                ox: x * scale, oy: y * scale, oz: z * scale
            });
        }

        const resize = () => {
            const parent = canvas.parentElement;
            if (parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        const render = () => {
            if(!canvas || !ctx) return;
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            // USA COR PRIMÁRIA DO TEMA
            const colorHex = colors.primary;

            const targetRotX = (mouseRef.current.y - cy) * 0.001;
            const targetRotY = (mouseRef.current.x - cx) * 0.001;
            
            const angleY = time * 0.2 + targetRotY;
            const angleX = targetRotX;

            const sinY = Math.sin(angleY);
            const cosY = Math.cos(angleY);
            const sinX = Math.sin(angleX);
            const cosX = Math.cos(angleX);

            particles.forEach(p => {
                let mod = 1;
                if (isSpeaking) {
                    mod = 1 + Math.sin(time * 50 + p.oy) * 0.1 * Math.random();
                }
                if (isThinking) {
                    mod = 1 + Math.sin(time * 5) * 0.05;
                }

                let px = p.ox * mod;
                let py = p.oy * mod;
                let pz = p.oz * mod;

                let x1 = px * cosY - pz * sinY;
                let z1 = pz * cosY + px * sinY;

                let y2 = py * cosX - z1 * sinX;
                let z2 = z1 * cosX + py * sinX;

                const scale = 400 / (400 + z2);
                const x2d = cx + x1 * scale;
                const y2d = cy + y2 * scale;

                const size = Math.max(0.5, scale * 2);
                const alpha = scale * 0.8;

                ctx.fillStyle = isSpeaking ? colors.text : isThinking ? colors.warning : colorHex;
                ctx.globalAlpha = alpha;

                ctx.beginPath();
                ctx.arc(x2d, y2d, size, 0, Math.PI * 2);
                ctx.fill();
            });

            ctx.globalAlpha = 0.3;
            ctx.strokeStyle = colorHex;
            ctx.lineWidth = 1;
            
            ctx.beginPath();
            ctx.ellipse(cx, cy, 140, 40, time * 0.5, 0, Math.PI * 2);
            ctx.stroke();

            ctx.beginPath();
            ctx.ellipse(cx, cy, 40, 140, -time * 0.3, 0, Math.PI * 2);
            ctx.stroke();

            // Coroa/Ícone de autoridade
            ctx.globalAlpha = 0.8;
            ctx.fillStyle = colorHex;
            const crownY = cy - 130;
            ctx.beginPath();
            ctx.moveTo(cx - 30, crownY);
            ctx.lineTo(cx - 25, crownY - 20);
            ctx.lineTo(cx - 15, crownY - 5);
            ctx.lineTo(cx, crownY - 25);
            ctx.lineTo(cx + 15, crownY - 5);
            ctx.lineTo(cx + 25, crownY - 20);
            ctx.lineTo(cx + 30, crownY);
            ctx.closePath();
            ctx.fill();

            ctx.globalAlpha = 1;

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [isSpeaking, isThinking, colors]);

    const handleMouseMove = (e: React.MouseEvent) => {
        mouseRef.current = { x: e.clientX, y: e.clientY };
    };

    const toggleRecording = () => {
        if (isRecording) {
            recognitionRef.current?.stop();
            setIsRecording(false);
            return;
        }
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Navegador sem suporte a voz.");
            return;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = 'pt-BR';
        recognition.onstart = () => setIsRecording(true);
        recognition.onresult = (event: any) => setInput(event.results[0][0].transcript);
        recognition.onend = () => setIsRecording(false);
        recognitionRef.current = recognition;
        recognition.start();
    };

    const speakText = (text: string) => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'pt-BR';
            utterance.onstart = () => setIsSpeaking(true);
            utterance.onend = () => setIsSpeaking(false);
            window.speechSynthesis.speak(utterance);
        }
    };

    const handleSend = async () => {
        if (!input.trim()) return;
        
        const userMessage: Message = {
            id: Date.now(),
            role: 'user',
            text: input,
            timestamp: new Date().toLocaleTimeString()
        };
        
        setMessages(prev => [...prev, userMessage]);
        const userText = input;
        setInput('');
        setIsThinking(true);

        try {
            const response = await fetch('/api/quantum/brain/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: userText,
                    description: userText,
                    agent_id: 'orion',
                }),
            });
            
            const data = await response.json();
            
            const aiMessage: Message = {
                id: Date.now() + 1,
                role: 'ai',
                text: data.result || data.error || 'Erro ao processar comando.',
                timestamp: new Date().toLocaleTimeString(),
                tokens: data.tokens_used,
                executionTime: data.execution_time_ms,
            };
            
            setMessages(prev => [...prev, aiMessage]);
            speakText(aiMessage.text);
            setTotalCommands(prev => prev + 1);
            
        } catch (error) {
            console.error('Error:', error);
            const errorMessage: Message = {
                id: Date.now() + 1,
                role: 'ai',
                text: 'Erro de conexão com ORION. Tente novamente.',
                timestamp: new Date().toLocaleTimeString(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsThinking(false);
        }
    };

    return (
        <div 
            className="h-[calc(100vh-6rem)] flex flex-col md:flex-row gap-6 overflow-hidden relative p-2" 
            onMouseMove={handleMouseMove}
        >
            {/* ESQUERDA: HOLOGRAMA ORION */}
            <div className="w-full md:w-[400px] flex flex-col gap-4 relative z-10 h-full">
                <div 
                    className="flex-1 backdrop-blur-xl rounded-3xl relative overflow-hidden group"
                    style={{
                        background: `${colors.background}/60`,
                        border: `1px solid ${colors.primary}/20`,
                        boxShadow: `0 0 50px ${colors.glow}/10`
                    }}
                >
                    {/* Status Overlay */}
                    <div className="absolute top-6 left-6 z-20 flex flex-col gap-1">
                        <div className="flex items-center gap-2">
                            <div 
                                className={`w-2 h-2 rounded-full ${isSpeaking ? 'animate-ping' : ''}`}
                                style={{ background: isSpeaking ? colors.text : colors.primary }}
                            />
                            <span className="text-xs font-mono tracking-[0.2em]" style={{ color: colors.primary }}>
                                {isSpeaking ? 'VOCALIZING' : isThinking ? 'COMPUTING' : 'ONLINE'}
                            </span>
                        </div>
                        <div className="text-[10px] font-mono pl-4" style={{ color: `${colors.text}/30` }}>
                            ORION SUPREME • COMMAND LAYER
                        </div>
                    </div>

                    {/* Stats */}
                    <div className="absolute top-6 right-6 z-20 text-right">
                        <div className="text-2xl font-black" style={{ color: colors.primary }}>{totalCommands}</div>
                        <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>Total Commands</div>
                    </div>

                    <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />
                    
                    <div className="absolute inset-0 bg-[url('/scanlines.png')] opacity-5 pointer-events-none" />
                    <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/80 pointer-events-none" />
                    
                    {/* Equalizador */}
                    <div className="absolute bottom-6 left-6 right-6 flex justify-between items-end h-8 opacity-30">
                        {Array.from({length: 20}).map((_, i) => (
                            <div 
                                key={i} 
                                className="w-1 transition-all duration-100 ease-in-out"
                                style={{ 
                                    background: colors.primary,
                                    height: isSpeaking ? `${Math.random() * 100}%` : '10%',
                                }} 
                            />
                        ))}
                    </div>
                </div>

                {/* Status Cards */}
                <div className="grid grid-cols-2 gap-3">
                    <div 
                        className="rounded-xl p-4 text-center"
                        style={{
                            background: `${colors.surface}/40`,
                            border: `1px solid ${colors.primary}/20`
                        }}
                    >
                        <Crown className="w-5 h-5 mx-auto mb-2" style={{ color: colors.primary }} />
                        <div className="text-lg font-black" style={{ color: colors.text }}>SUPREME</div>
                        <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>Authority</div>
                    </div>
                    <div 
                        className="rounded-xl p-4 text-center"
                        style={{
                            background: `${colors.surface}/40`,
                            border: `1px solid ${colors.border}/10`
                        }}
                    >
                        <Activity className="w-5 h-5 mx-auto mb-2" style={{ color: colors.accent }} />
                        <div className="text-lg font-black" style={{ color: colors.text }}>{avgResponseTime}ms</div>
                        <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>Avg Response</div>
                    </div>
                </div>
            </div>

            {/* DIREITA: CHAT INTERFACE */}
            <div 
                className="flex-1 flex flex-col backdrop-blur-md rounded-3xl overflow-hidden relative"
                style={{
                    background: `${colors.surface}/80`,
                    border: `1px solid ${colors.border}/10`
                }}
            >
                {/* Header */}
                <div 
                    className="p-4"
                    style={{
                        borderBottom: `1px solid ${colors.border}/10`,
                        background: `linear-gradient(to right, ${colors.primary}/10, transparent)`
                    }}
                >
                    <div className="flex items-center gap-3">
                        <Crown className="w-6 h-6" style={{ color: colors.primary }} />
                        <div>
                            <h2 className="text-lg font-black" style={{ color: colors.text }}>ORION COMMAND</h2>
                            <p className="text-[10px] font-mono" style={{ color: colors.textSecondary }}>Direct Communication Channel</p>
                        </div>
                    </div>
                </div>
                
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {messages.map((msg) => (
                        <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
                            <div 
                                className="max-w-[85%] p-5 rounded-2xl relative shadow-lg"
                                style={{
                                    background: msg.role === 'user' 
                                        ? `${colors.primary}/10` 
                                        : `${colors.surface}`,
                                    border: `1px solid ${msg.role === 'user' ? `${colors.primary}/20` : `${colors.border}/10`}`,
                                    borderRadius: msg.role === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
                                    color: colors.text
                                }}
                            >
                                <div className="flex items-center gap-2 mb-2 opacity-40 text-[10px] font-mono uppercase tracking-wider">
                                    {msg.role === 'ai' ? <Crown className="w-3 h-3" /> : <User className="w-3 h-3" />}
                                    {msg.role === 'ai' ? 'ORION SUPREME' : 'OPERATOR'} • {msg.timestamp}
                                </div>
                                <p className="leading-relaxed text-sm md:text-base font-light">{msg.text}</p>
                                {msg.tokens && (
                                    <div 
                                        className="mt-2 pt-2 flex gap-4 text-[10px]"
                                        style={{ borderTop: `1px solid ${colors.border}/10`, color: colors.textSecondary }}
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
                                className="p-5 rounded-2xl"
                                style={{
                                    background: colors.surface,
                                    border: `1px solid ${colors.border}/10`,
                                    borderRadius: '20px 20px 20px 4px'
                                }}
                            >
                                <div className="flex items-center gap-2">
                                    {[0, 1, 2].map(i => (
                                        <div 
                                            key={i}
                                            className="w-2 h-2 rounded-full animate-bounce"
                                            style={{ 
                                                background: colors.primary,
                                                animationDelay: `${i * 0.1}s`
                                            }}
                                        />
                                    ))}
                                    <span className="ml-2 text-xs" style={{ color: colors.textSecondary }}>ORION processando...</span>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Bar */}
                <div 
                    className="p-4"
                    style={{
                        background: `${colors.background}/20`,
                        borderTop: `1px solid ${colors.border}/10`
                    }}
                >
                    <div 
                        className="relative flex items-center gap-2 rounded-2xl p-2 transition-all shadow-lg"
                        style={{
                            background: colors.background,
                            border: `1px solid ${colors.border}/10`
                        }}
                    >
                        <button
                            onClick={toggleRecording}
                            className="p-3 rounded-xl transition-all"
                            style={{
                                background: isRecording ? `${colors.error}/20` : `${colors.surface}`,
                                color: isRecording ? colors.error : colors.textSecondary,
                                border: isRecording ? `1px solid ${colors.error}/50` : 'none'
                            }}
                        >
                            {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                        </button>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Comando para ORION..."
                            className="flex-1 bg-transparent border-none outline-none font-mono text-sm h-full"
                            style={{ color: colors.text }}
                        />
                        <button 
                            onClick={handleSend} 
                            disabled={!input.trim() || isThinking} 
                            className="p-3 rounded-xl transition-all disabled:opacity-50"
                            style={{
                                background: colors.primary,
                                color: colors.background
                            }}
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>
            
            <style jsx>{`
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                .animate-fadeIn { animation: fadeIn 0.3s ease-out forwards; }
            `}</style>
        </div>
    );
}
