/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SUPPORT OPS (CRISIS CENTER)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/support/page.tsx
 * 📋 Colmeia de Tickets Hexagonais e Triagem por IA
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    LifeBuoy, CheckCircle, Clock, AlertOctagon, 
    Bot, User, MessageSquare, Zap, Activity 
} from 'lucide-react';

interface Ticket {
    id: number;
    user: string;
    issue: string;
    status: 'critical' | 'pending' | 'solved';
    sentiment: number; // 0-100
    x: number;
    y: number;
}

export default function SupportPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [solvedCount, setSolvedCount] = useState(1240);
    const [patienceLevel, setPatienceLevel] = useState(85);
    const [activeTicket, setActiveTicket] = useState<Ticket | null>(null);

    // 1. ENGINE VISUAL (THE HIVE)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Configuração da Colmeia
        const HEX_SIZE = 30;
        const GAP = 4;
        const COLS = 12;
        const ROWS = 8;
        
        // Inicializar Grid de Tickets
        const initialTickets: Ticket[] = [];
        for(let r=0; r<ROWS; r++) {
            for(let c=0; c<COLS; c++) {
                // Posição Hexagonal
                const xOffset = (r % 2 === 0) ? 0 : (HEX_SIZE + GAP) * Math.sqrt(3) / 2;
                const x = c * (HEX_SIZE * Math.sqrt(3) + GAP) + xOffset + 50;
                const y = r * (HEX_SIZE * 1.5 + GAP) + 50;

                if(Math.random() > 0.6) { // 40% de chance de ter ticket
                    initialTickets.push({
                        id: r * COLS + c,
                        user: `User_${Math.floor(Math.random()*999)}`,
                        issue: ['Login Error', 'Payment Failed', 'API Limit', 'Bug Report'][Math.floor(Math.random()*4)],
                        status: Math.random() > 0.8 ? 'critical' : Math.random() > 0.5 ? 'pending' : 'solved',
                        sentiment: Math.random() * 100,
                        x, y
                    });
                }
            }
        }
        setTickets(initialTickets);

        let time = 0;
        let aiLaser = { active: false, targetX: 0, targetY: 0, progress: 0 };

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        // Loop de Renderização
        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            ctx.clearRect(0, 0, w, h);
            time += 0.02;

            // Desenhar Tickets (Hexágonos)
            tickets.forEach(t => {
                // Cor baseada no status
                let color = '#374151'; // Default Gray
                let glow = false;

                if(t.status === 'solved') color = '#10B981'; // Verde
                else if(t.status === 'pending') color = '#F59E0B'; // Amarelo
                else if(t.status === 'critical') {
                    color = '#EF4444'; // Vermelho
                    glow = true;
                }

                // Animação de pulso para críticos
                const pulse = glow ? Math.sin(time * 5) * 0.2 + 1 : 1;

                // Desenhar Hexágono
                ctx.beginPath();
                for (let i = 0; i < 6; i++) {
                    const angle = 2 * Math.PI / 6 * i;
                    const hx = t.x + HEX_SIZE * pulse * Math.cos(angle);
                    const hy = t.y + HEX_SIZE * pulse * Math.sin(angle);
                    if (i === 0) ctx.moveTo(hx, hy);
                    else ctx.lineTo(hx, hy);
                }
                ctx.closePath();

                ctx.fillStyle = color;
                ctx.shadowBlur = glow ? 15 : 0;
                ctx.shadowColor = color;
                ctx.globalAlpha = t.status === 'solved' ? 0.3 : 0.8; // Solved fica transparente
                ctx.fill();
                
                // Reset
                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1;
            });

            // --- IA INTERVENTION (O LASER) ---
            if(Math.random() > 0.98 && !aiLaser.active) {
                // Escolher um alvo pendente/crítico
                const target = tickets.find(t => t.status !== 'solved');
                if(target) {
                    aiLaser = { active: true, targetX: target.x, targetY: target.y, progress: 0 };
                }
            }

            if(aiLaser.active) {
                aiLaser.progress += 0.1;
                
                // Origem do Laser (Centro superior)
                const startX = w / 2;
                const startY = -50;

                // Desenhar Raio
                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(aiLaser.targetX, aiLaser.targetY);
                
                const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
                ctx.strokeStyle = themeColor;
                ctx.lineWidth = 2 * (1 - aiLaser.progress); // Fica mais fino ao acabar
                ctx.shadowBlur = 20;
                ctx.shadowColor = themeColor;
                ctx.stroke();

                // Efeito de Impacto
                ctx.beginPath();
                ctx.arc(aiLaser.targetX, aiLaser.targetY, 10 * aiLaser.progress, 0, Math.PI * 2);
                ctx.fillStyle = '#FFFFFF';
                ctx.globalAlpha = 1 - aiLaser.progress;
                ctx.fill();
                ctx.globalAlpha = 1;

                // Terminar Laser e Resolver Ticket
                if(aiLaser.progress >= 1) {
                    aiLaser.active = false;
                    // Atualizar status do ticket (apenas visual no canvas loop)
                    // Em app real, usaria state, mas aqui é para performance visual
                    const tIndex = tickets.findIndex(t => t.x === aiLaser.targetX && t.y === aiLaser.targetY);
                    if(tIndex !== -1) {
                        // Hack visual: desenha por cima para não re-renderizar react
                        tickets[tIndex].status = 'solved';
                        setSolvedCount(prev => prev + 1);
                    }
                }
            }

            requestAnimationFrame(render);
        };

        render();
        return () => window.removeEventListener('resize', resize);
    }, []);

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* ESQUERDA: THE HIVE (VISUALIZER) */}
            <div className="lg:w-2/3 w-full h-full relative rounded-3xl overflow-hidden border border-white/10 bg-[#02040a] group shadow-2xl">
                
                {/* Header Flutuante */}
                <div className="absolute top-6 left-6 z-20">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-blue-500/10 border border-blue-500/30 text-blue-400">
                            <LifeBuoy className="w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-white tracking-tight font-display">SUPPORT HIVE</h1>
                            <p className="text-xs text-gray-400 font-mono uppercase">AI Triage System Active</p>
                        </div>
                    </div>
                </div>

                {/* Legenda */}
                <div className="absolute bottom-6 left-6 z-20 flex gap-4 text-xs font-mono font-bold">
                    <div className="flex items-center gap-2 text-red-400">
                        <div className="w-3 h-3 bg-red-500 rounded-sm shadow-[0_0_10px_red]" /> CRITICAL
                    </div>
                    <div className="flex items-center gap-2 text-yellow-400">
                        <div className="w-3 h-3 bg-yellow-500 rounded-sm" /> PENDING
                    </div>
                    <div className="flex items-center gap-2 text-emerald-400">
                        <div className="w-3 h-3 bg-emerald-500 rounded-sm opacity-30" /> SOLVED
                    </div>
                </div>

                {/* CANVAS */}
                <canvas ref={canvasRef} className="w-full h-full" />
                
                {/* Overlay Tech */}
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />
            </div>

            {/* DIREITA: DADOS E LIVE FEED */}
            <div className="lg:w-1/3 w-full flex flex-col gap-4">
                
                {/* Card: AI Performance */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex items-center justify-between relative overflow-hidden">
                    {/* Background Glow */}
                    <div className="absolute -right-10 -top-10 w-32 h-32 bg-[var(--color-primary)]/20 blur-3xl rounded-full" />
                    
                    <div>
                        <div className="text-[10px] text-gray-400 font-mono uppercase mb-1">Auto-Resolution Rate</div>
                        <div className="text-4xl font-mono text-white font-bold flex items-baseline gap-2">
                            94.2%
                            <span className="text-sm text-emerald-400 flex items-center"><Zap className="w-3 h-3" /> +2%</span>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">AI is handling {solvedCount} tickets</p>
                    </div>
                    <div className="h-16 w-16 rounded-full border-4 border-[var(--color-primary)]/30 border-t-[var(--color-primary)] animate-spin" />
                </div>

                {/* Card: User Patience (Biometric) */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-sm font-bold text-white flex items-center gap-2">
                            <Activity className="w-4 h-4 text-red-400" />
                            USER PATIENCE
                        </h3>
                        <span className={`text-xs font-mono font-bold ${patienceLevel > 80 ? 'text-emerald-400' : 'text-yellow-400'}`}>
                            {patienceLevel}/100
                        </span>
                    </div>
                    {/* Waveform Fake */}
                    <div className="flex items-end gap-1 h-10 w-full overflow-hidden">
                        {Array.from({length: 30}).map((_, i) => (
                            <div 
                                key={i} 
                                className={`w-full rounded-sm transition-all duration-300 ${i > 25 ? 'bg-red-500 animate-pulse' : 'bg-emerald-500/50'}`}
                                style={{ height: `${20 + Math.random() * 80}%` }}
                            />
                        ))}
                    </div>
                </div>

                {/* Card: Live Transcript (Matrix Style) */}
                <div className="flex-1 bg-[#050505] border border-white/10 rounded-2xl overflow-hidden flex flex-col">
                    <div className="p-3 bg-white/5 border-b border-white/5 flex justify-between items-center">
                        <span className="text-xs font-mono text-gray-400 flex items-center gap-2">
                            <MessageSquare className="w-3 h-3" /> LIVE TRANSCRIPT
                        </span>
                        <div className="flex gap-1">
                            <div className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
                        </div>
                    </div>
                    
                    <div className="flex-1 p-4 space-y-3 overflow-hidden relative font-mono text-xs">
                        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#050505] z-10 pointer-events-none" />
                        
                        {/* Fake Chat Items */}
                        <div className="animate-slideUp opacity-50">
                            <span className="text-blue-400">User_992:</span> My dashboard is not loading...
                        </div>
                        <div className="animate-slideUp opacity-70">
                            <span className="text-[var(--color-primary)]">AI_Agent:</span> Rerouting connection to US-EAST. Fixed?
                        </div>
                        <div className="animate-slideUp">
                            <span className="text-blue-400">User_992:</span> Yes! Thanks.
                        </div>
                        <div className="animate-slideUp mt-4 border-t border-white/5 pt-2">
                            <span className="text-red-400">User_X:</span> CRITICAL ERROR ON PAYMENT...
                        </div>
                        <div className="animate-slideUp">
                            <span className="text-[var(--color-primary)]">AI_Agent:</span> Initiating refund protocol...
                        </div>
                    </div>
                </div>

            </div>

            <style jsx>{`
                @keyframes slideUp { from { transform: translateY(10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
                .animate-slideUp { animation: slideUp 0.3s ease-out forwards; }
            `}</style>
        </div>
    );
}
