/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION AI (HOLOGRAM HEAD EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/orion/page.tsx
 * 📋 Rosto 3D Holográfico Procedural (Wireframe) + Voz + Chat
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    Mic, MicOff, Send, Bot, User, Sparkles, 
    ChevronDown, Cpu, Volume2, BrainCircuit 
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

interface Point3D {
    x: number; y: number; z: number;
    baseX: number; baseY: number; baseZ: number;
}

export default function OrionPage() {
    // Estado
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, role: 'ai', text: 'Conexão neural estabelecida. Sou Orion. Estou pronto para processar seus dados.', timestamp: 'Now' }
    ]);
    const [isRecording, setIsRecording] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isThinking, setIsThinking] = useState(false);
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

    // 1. ENGINE VISUAL 3D (CABEÇA HOLOGRÁFICA)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;
        let points: Point3D[] = [];

        const resize = () => {
            const parent = canvas.parentElement;
            if (parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        // --- GERAÇÃO DA CABEÇA (MATEMÁTICA PROCEDURAL) ---
        const initHead = () => {
            points = [];
            const layers = 20; // Camadas horizontais (fatias da cabeça)
            const pointsPerLayer = 30; // Pontos por volta

            for (let i = 0; i < layers; i++) {
                // y vai de -1 (topo) a 1 (queixo)
                const y = 1 - (i / (layers - 1)) * 2; 
                
                // Raio base da esfera
                let radius = Math.sqrt(1 - y * y);
                
                // DEFORMAÇÃO CRANIANA (Criar formato de rosto)
                // Alargar a parte de cima (crânio) e afinar a parte de baixo (queixo)
                if (y < -0.5) radius *= 0.9; // Topo da cabeça
                if (y > 0.2) radius *= 0.85; // Maxilar afinando
                if (y > 0.6) radius *= 0.7; // Queixo

                for (let j = 0; j < pointsPerLayer; j++) {
                    const theta = (j / pointsPerLayer) * Math.PI * 2;
                    
                    // Deformação Facial (Nariz/Orelhas)
                    let r = radius;
                    // Nariz (Z positivo, Y central)
                    const isFaceFront = Math.abs(theta - Math.PI/2) < 0.5;
                    if (isFaceFront && Math.abs(y) < 0.2) r *= 1.1;

                    const x = Math.cos(theta) * r * 100; // Escala 100
                    const z = Math.sin(theta) * r * 100;
                    const py = y * 130; // Altura alongada

                    points.push({
                        x, y: py, z,
                        baseX: x, baseY: py, baseZ: z
                    });
                }
            }
        };
        initHead();

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            // Limpar
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)'; // Trail para suavidade
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            // Cor do Tema
            const colorHex = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
            
            // Rotação Automática Suave
            const angleY = time * 0.5; // Gira no eixo Y
            const angleX = Math.sin(time * 0.5) * 0.1; // Leve movimento de "sim/não"

            const sinY = Math.sin(angleY);
            const cosY = Math.cos(angleY);
            const sinX = Math.sin(angleX);
            const cosX = Math.cos(angleX);

            // Desenhar Pontos e Linhas
            const projectedPoints: {x: number, y: number, z: number}[] = [];

            points.forEach(p => {
                // Animação de Fala (Maxilar se move)
                let animY = p.baseY;
                if (isSpeaking && p.baseY > 30) { // Apenas parte de baixo (boca/queixo)
                    animY += Math.sin(time * 30) * 10 * Math.random();
                }

                // Animação de Pensamento (Cabeça pulsa)
                let animX = p.baseX;
                let animZ = p.baseZ;
                if (isThinking) {
                    const pulse = 1 + Math.sin(time * 10) * 0.05;
                    animX *= pulse;
                    animY *= pulse;
                    animZ *= pulse;
                }

                // Rotação Y
                let x1 = animX * cosY - animZ * sinY;
                let z1 = animZ * cosY + animX * sinY;

                // Rotação X
                let y2 = animY * cosX - z1 * sinX;
                let z2 = z1 * cosX + animY * sinX;

                // Perspectiva
                const scale = 400 / (400 + z2);
                const x2d = cx + x1 * scale;
                const y2d = cy + y2 * scale;

                projectedPoints.push({ x: x2d, y: y2d, z: z2 });
            });

            // Desenhar Linhas (Wireframe)
            ctx.lineWidth = 0.5;
            ctx.strokeStyle = `${colorHex}33`; // 20% opacidade

            for (let i = 0; i < projectedPoints.length; i++) {
                const p = projectedPoints[i];
                if (p.z < -50) continue; // Ocultar parte de trás (backface culling simples)

                // Conectar com vizinho da direita (anel)
                const next = projectedPoints[(i + 1) % projectedPoints.length];
                // Evitar conectar o último da camada com o primeiro da próxima (hack visual simples)
                if ((i + 1) % 30 !== 0) {
                    const dist = Math.hypot(p.x - next.x, p.y - next.y);
                    if (dist < 50) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(next.x, next.y);
                        ctx.stroke();
                    }
                }

                // Conectar com vizinho de baixo (vertical)
                if (i + 30 < projectedPoints.length) {
                    const below = projectedPoints[i + 30];
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(below.x, below.y);
                    ctx.stroke();
                }
            }

            // Desenhar Pontos (Vértices)
            projectedPoints.forEach(p => {
                if (p.z < -50) return;

                const size = Math.max(0.5, (200 - p.z) / 100);
                ctx.fillStyle = colorHex;
                
                // Efeito de "Mente Brilhante" (No centro da testa)
                if (p.y < -20 && Math.abs(p.x - cx) < 40) {
                    ctx.shadowBlur = 15;
                    ctx.shadowColor = colorHex;
                    ctx.fillStyle = '#FFFFFF';
                } else {
                    ctx.shadowBlur = 0;
                }

                ctx.beginPath();
                ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
                ctx.fill();
            });

            // Núcleo de Energia (Brilho Central)
            if (isThinking || isSpeaking) {
                const gradient = ctx.createRadialGradient(cx, cy - 20, 0, cx, cy - 20, 100);
                gradient.addColorStop(0, `${colorHex}66`);
                gradient.addColorStop(1, 'transparent');
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(cx, cy - 20, 100, 0, Math.PI * 2);
                ctx.fill();
            }

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [isSpeaking, isThinking]);

    // --- FUNÇÕES DE ÁUDIO E CHAT ---

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
            utterance.pitch = 0.8; // Voz mais robótica/profunda
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
        setIsThinking(true); // Ativa brilho da mente

        // Simulação de Resposta
        setTimeout(() => {
            setIsThinking(false);
            const response = `Analisei sua solicitação: "${userText}". Utilizando a arquitetura ${selectedModel.name}, identifiquei 3 caminhos ótimos para execução. Iniciando protocolos.`;
            setMessages(prev => [...prev, { id: Date.now()+1, role: 'ai', text: response, timestamp: 'Now' }]);
            speakText(response);
        }, 2000);
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col md:flex-row gap-6 overflow-hidden relative p-2">
            
            {/* ESQUERDA: HOLOGRAMA DA IA */}
            <div className="w-full md:w-[400px] flex flex-col gap-4 relative z-10 h-full">
                <div className="flex-1 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl relative overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] group">
                    
                    {/* Status Badge */}
                    <div className="absolute top-6 left-6 z-20 flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${isSpeaking ? 'bg-green-400 animate-pulse' : isThinking ? 'bg-yellow-400 animate-bounce' : 'bg-gray-500'}`} />
                        <span className="text-xs font-mono text-white/70 tracking-[0.2em]">
                            {isSpeaking ? 'VOCALIZING' : isThinking ? 'PROCESSING' : 'ONLINE'}
                        </span>
                    </div>

                    {/* CANVAS DO ROSTO */}
                    <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />
                    
                    {/* Efeitos de Overlay (Scanlines) */}
                    <div className="absolute inset-0 bg-[url('/scanlines.png')] opacity-10 pointer-events-none bg-cover" />
                    <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/90 pointer-events-none" />
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
                                <div className="text-[10px] text-gray-500 font-mono uppercase tracking-wider">Neural Engine</div>
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

            {/* DIREITA: CHAT INTERFACE */}
            <div className="flex-1 flex flex-col bg-[#050505]/80 backdrop-blur-md border border-white/5 rounded-3xl overflow-hidden relative">
                <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-[var(--color-primary)]/20 scrollbar-track-transparent">
                    {messages.map((msg) => (
                        <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[85%] p-5 rounded-2xl relative ${
                                msg.role === 'user' 
                                ? 'bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/20 text-white rounded-tr-none' 
                                : 'bg-white/5 border border-white/10 text-gray-200 rounded-tl-none'
                            }`}>
                                <div className="flex items-center gap-2 mb-2 opacity-40 text-[10px] font-mono uppercase tracking-wider">
                                    {msg.role === 'ai' ? <Bot className="w-3 h-3" /> : <User className="w-3 h-3" />}
                                    {msg.role === 'ai' ? 'ORION SYSTEM' : 'OPERATOR'} • {msg.timestamp}
                                </div>
                                <p className="leading-relaxed text-sm md:text-base">{msg.text}</p>
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
                            className={`p-3 rounded-xl transition-all ${isRecording ? 'bg-red-500/20 text-red-500 animate-pulse' : 'bg-white/5 text-gray-400 hover:text-white'}`}
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
        </div>
    );
}
