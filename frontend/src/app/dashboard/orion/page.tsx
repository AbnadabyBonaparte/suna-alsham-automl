/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION AI (LIDAR EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/orion/page.tsx
 * 📋 Nuvem de pontos LIDAR 3D + Anéis de Dados + Chat de Voz
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    Mic, MicOff, Send, Bot, User, Sparkles, 
    ChevronDown, Cpu, Volume2, BrainCircuit, Activity 
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
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, role: 'ai', text: 'Consciência inicializada. Aguardando input sensorial.', timestamp: 'Now' }
    ]);
    const [isRecording, setIsRecording] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isThinking, setIsThinking] = useState(false);
    const [selectedModel, setSelectedModel] = useState(AI_MODELS[0]);
    const [isModelMenuOpen, setIsModelMenuOpen] = useState(false);
    
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const recognitionRef = useRef<any>(null);
    const mouseRef = useRef({ x: 0, y: 0 });

    // Scroll automático
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // 1. ENGINE VISUAL LIDAR (A MÁGICA ACONTECE AQUI)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;
        
        // Definição da Nuvem de Pontos
        const particles: {x: number, y: number, z: number, ox: number, oy: number, oz: number}[] = [];
        const PARTICLE_COUNT = 600; // Muito mais pontos para definição

        // Inicializar Cabeça (Geometria melhorada)
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            // Algoritmo de distribuição esférica modificado para formato de cabeça
            const theta = Math.random() * Math.PI * 2; // Ângulo horizontal
            const phi = Math.acos((Math.random() * 2) - 1); // Ângulo vertical

            let x = Math.sin(phi) * Math.cos(theta);
            let y = Math.sin(phi) * Math.sin(theta);
            let z = Math.cos(phi);

            // --- ESCULTURA DIGITAL (Deformar a esfera para virar cabeça) ---
            // 1. Achatar laterais (orelhas)
            x *= 0.85;
            // 2. Alongar verticalmente (rosto)
            y *= 1.2;
            // 3. Definir queixo (afinar parte de baixo)
            if (y > 0) {
                x *= 1 - (y * 0.4);
                z *= 1 - (y * 0.4);
            }
            // 4. Definir crânio (alargar parte de cima)
            if (y < 0) {
                x *= 1.1;
                z *= 1.1;
            }

            const scale = 100; // Tamanho base
            particles.push({
                x: x * scale, y: y * scale, z: z * scale,
                ox: x * scale, oy: y * scale, oz: z * scale // Posições originais para memória
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

            // Limpar com fade (Rastro tecnológico)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            // Pegar cor do tema
            const colorHex = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';

            // --- ROTAÇÃO PELO MOUSE (Parallax) ---
            // A cabeça olha para o mouse
            const targetRotX = (mouseRef.current.y - cy) * 0.001;
            const targetRotY = (mouseRef.current.x - cx) * 0.001;
            
            // Rotação base automática + Mouse
            const angleY = time * 0.2 + targetRotY;
            const angleX = targetRotX;

            const sinY = Math.sin(angleY);
            const cosY = Math.cos(angleY);
            const sinX = Math.sin(angleX);
            const cosX = Math.cos(angleX);

            // --- RENDERIZAR PARTÍCULAS ---
            particles.forEach(p => {
                // Modulação de Voz (Explosão)
                let mod = 1;
                if (isSpeaking) {
                    // Vibração baseada em ruído
                    mod = 1 + Math.sin(time * 50 + p.oy) * 0.1 * Math.random();
                }
                if (isThinking) {
                    // Respiração lenta
                    mod = 1 + Math.sin(time * 5) * 0.05;
                }

                // Aplicar modulação
                let px = p.ox * mod;
                let py = p.oy * mod;
                let pz = p.oz * mod;

                // Rotação Y
                let x1 = px * cosY - pz * sinY;
                let z1 = pz * cosY + px * sinY;

                // Rotação X
                let y2 = py * cosX - z1 * sinX;
                let z2 = z1 * cosX + py * sinX;

                // Perspectiva
                const scale = 400 / (400 + z2);
                const x2d = cx + x1 * scale;
                const y2d = cy + y2 * scale;

                // Tamanho e Opacidade baseados na profundidade (Z)
                const size = Math.max(0.5, scale * 2);
                const alpha = scale * 0.8;

                // Cor (Muda se estiver falando/pensando)
                ctx.fillStyle = isSpeaking ? '#FFFFFF' : isThinking ? '#FCD34D' : colorHex;
                ctx.globalAlpha = alpha;

                ctx.beginPath();
                ctx.arc(x2d, y2d, size, 0, Math.PI * 2);
                ctx.fill();
            });

            // --- ANÉIS ORBITAIS (Visual Jarvis) ---
            ctx.globalAlpha = 0.2;
            ctx.strokeStyle = colorHex;
            ctx.lineWidth = 1;
            
            // Anel Horizontal
            ctx.beginPath();
            ctx.ellipse(cx, cy, 140, 40, time * 0.5, 0, Math.PI * 2);
            ctx.stroke();

            // Anel Vertical
            ctx.beginPath();
            ctx.ellipse(cx, cy, 40, 140, -time * 0.3, 0, Math.PI * 2);
            ctx.stroke();

            ctx.globalAlpha = 1; // Reset

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [isSpeaking, isThinking]);

    // Funções de Mouse para Parallax
    const handleMouseMove = (e: React.MouseEvent) => {
        mouseRef.current = { x: e.clientX, y: e.clientY };
    };

    // Funções de Áudio (Iguais)
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

    const handleSend = () => {
        if (!input.trim()) return;
        setMessages(prev => [...prev, { id: Date.now(), role: 'user', text: input, timestamp: 'Now' }]);
        const userText = input;
        setInput('');
        setIsThinking(true);

        setTimeout(() => {
            setIsThinking(false);
            const response = `Entendido. Processando "${userText}" através do núcleo neural ${selectedModel.name}. A probabilidade de êxito é de 99.8%.`;
            setMessages(prev => [...prev, { id: Date.now()+1, role: 'ai', text: response, timestamp: 'Now' }]);
            speakText(response);
        }, 2000);
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col md:flex-row gap-6 overflow-hidden relative p-2" onMouseMove={handleMouseMove}>

            {/* COMING SOON BADGE */}
            <div className="absolute top-4 right-4 z-50 animate-pulse">
                <div className="bg-gradient-to-r from-[var(--color-primary)]/20 via-[var(--color-accent)]/20 to-[var(--color-secondary)]/20 backdrop-blur-xl border-2 border-[var(--color-primary)]/50 rounded-2xl px-6 py-3 shadow-[0_0_30px_var(--color-primary)]">
                    <div className="flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-ping" />
                        <span className="text-sm font-black text-white uppercase tracking-widest orbitron">
                            Coming Soon
                        </span>
                    </div>
                    <div className="text-[10px] text-gray-400 text-center mt-1 font-mono">
                        Feature in development
                    </div>
                </div>
            </div>

            {/* ESQUERDA: HOLOGRAMA DA IA */}
            <div className="w-full md:w-[400px] flex flex-col gap-4 relative z-10 h-full">
                <div className="flex-1 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl relative overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] group">
                    
                    {/* Status Overlay */}
                    <div className="absolute top-6 left-6 z-20 flex flex-col gap-1">
                        <div className="flex items-center gap-2">
                            <div className={`w-2 h-2 rounded-full ${isSpeaking ? 'bg-white animate-ping' : 'bg-[var(--color-primary)]'}`} />
                            <span className="text-xs font-mono text-[var(--color-primary)] tracking-[0.2em]">
                                {isSpeaking ? 'VOCALIZING' : isThinking ? 'COMPUTING' : 'ONLINE'}
                            </span>
                        </div>
                        <div className="text-[10px] text-white/30 font-mono pl-4">
                            ID: ORION-X7 • {selectedModel.name}
                        </div>
                    </div>

                    {/* CANVAS LIDAR */}
                    <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />
                    
                    {/* Efeitos Visuais */}
                    <div className="absolute inset-0 bg-[url('/scanlines.png')] opacity-5 pointer-events-none" />
                    <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/80 pointer-events-none" />
                    
                    {/* Equalizador Visual (Fake) */}
                    <div className="absolute bottom-6 left-6 right-6 flex justify-between items-end h-8 opacity-30">
                        {Array.from({length: 20}).map((_, i) => (
                            <div 
                                key={i} 
                                className="w-1 bg-[var(--color-primary)] transition-all duration-100 ease-in-out"
                                style={{ 
                                    height: isSpeaking ? `${Math.random() * 100}%` : '10%',
                                    animation: isSpeaking ? 'none' : 'pulse 2s infinite'
                                }} 
                            />
                        ))}
                    </div>
                </div>

                {/* MODEL SELECTOR */}
                <div className="relative">
                    <button 
                        onClick={() => setIsModelMenuOpen(!isModelMenuOpen)}
                        className="w-full p-4 bg-[#0a0a0a] border border-white/10 rounded-xl flex items-center justify-between text-white hover:border-[var(--color-primary)] transition-all group"
                    >
                        <div className="flex items-center gap-3">
                            <BrainCircuit className="w-5 h-5 text-[var(--color-primary)]" />
                            <div className="text-left">
                                <div className="text-[10px] text-gray-500 font-mono uppercase tracking-wider">Neural Core</div>
                                <div className="font-bold text-sm">{selectedModel.name}</div>
                            </div>
                        </div>
                        <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isModelMenuOpen ? 'rotate-180' : ''}`} />
                    </button>

                    {isModelMenuOpen && (
                        <div className="absolute bottom-full left-0 right-0 mb-2 bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden shadow-2xl z-50 animate-slideUp">
                            {AI_MODELS.map(model => (
                                <button
                                    key={model.id}
                                    onClick={() => { setSelectedModel(model); setIsModelMenuOpen(false); }}
                                    className={`w-full p-3 flex items-center gap-3 hover:bg-white/5 transition-colors ${selectedModel.id === model.id ? 'bg-white/5' : ''}`}
                                >
                                    <span className="text-lg filter grayscale group-hover:grayscale-0">{model.icon}</span>
                                    <span className={`text-sm ${selectedModel.id === model.id ? 'text-[var(--color-primary)]' : 'text-white'}`}>{model.name}</span>
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* DIREITA: CHAT INTERFACE (Glassmorphism Refined) */}
            <div className="flex-1 flex flex-col bg-[#050505]/80 backdrop-blur-md border border-white/5 rounded-3xl overflow-hidden relative">
                <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-[var(--color-primary)]/20 scrollbar-track-transparent">
                    {messages.map((msg) => (
                        <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
                            <div className={`max-w-[85%] p-5 rounded-2xl relative shadow-lg ${
                                msg.role === 'user' 
                                ? 'bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/20 text-white rounded-tr-none' 
                                : 'bg-white/5 border border-white/10 text-gray-200 rounded-tl-none'
                            }`}>
                                <div className="flex items-center gap-2 mb-2 opacity-40 text-[10px] font-mono uppercase tracking-wider">
                                    {msg.role === 'ai' ? <Bot className="w-3 h-3" /> : <User className="w-3 h-3" />}
                                    {msg.role === 'ai' ? 'ORION SYSTEM' : 'OPERATOR'} • {msg.timestamp}
                                </div>
                                <p className="leading-relaxed text-sm md:text-base font-light">{msg.text}</p>
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                {/* INPUT BAR */}
                <div className="p-4 bg-black/20 border-t border-white/5">
                    <div className="relative flex items-center gap-2 bg-[#0a0a0a] border border-white/10 rounded-2xl p-2 focus-within:border-[var(--color-primary)]/50 transition-all shadow-lg">
                        <button
                            onClick={toggleRecording}
                            className={`p-3 rounded-xl transition-all ${isRecording ? 'bg-red-500/20 text-red-500 animate-pulse border border-red-500/50' : 'bg-white/5 text-gray-400 hover:text-white'}`}
                        >
                            {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                        </button>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Digite ou fale com a consciência..."
                            className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-600 font-mono text-sm h-full"
                        />
                        <button onClick={handleSend} disabled={!input.trim()} className="p-3 bg-[var(--color-primary)] hover:bg-[var(--color-accent)] rounded-xl text-black transition-all disabled:opacity-50">
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
