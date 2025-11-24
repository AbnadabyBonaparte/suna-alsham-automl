/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - GAMIFICATION (HALL OF LEGENDS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/gamification/page.tsx
 * 📋 Sistema de XP, Badges Holográficos e Leaderboard
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Trophy, Crown, Medal, Star, Zap, Target, Award, Gift } from 'lucide-react';

const ACHIEVEMENTS = [
    { id: 1, title: 'Genesis Architect', desc: 'Criou o primeiro Agente', icon: CpuIcon, rarity: 'legendary', unlocked: true },
    { id: 2, title: 'Neural Master', desc: 'Atingiu 1000 conexões', icon: NetworkIcon, rarity: 'epic', unlocked: true },
    { id: 3, title: 'Void Walker', desc: 'Sobreviveu a um Kernel Panic', icon: GhostIcon, rarity: 'rare', unlocked: false },
    { id: 4, title: 'Diamond Hands', desc: 'Acumulou $1M em valor', icon: DiamondIcon, rarity: 'epic', unlocked: true },
    { id: 5, title: 'Security Breaker', desc: 'Venceu o sistema de defesa', icon: LockIcon, rarity: 'rare', unlocked: false },
    { id: 6, title: 'Time Traveler', desc: 'Uptime de 99.9% por 1 ano', icon: ClockIcon, rarity: 'legendary', unlocked: false },
];

const LEADERBOARD = [
    { rank: 1, name: 'Admin Prime', xp: 99420, role: 'ARCHITECT' },
    { rank: 2, name: 'Sentinel X', xp: 84300, role: 'GUARD' },
    { rank: 3, name: 'Nexus Core', xp: 76100, role: 'AI' },
    { rank: 4, name: 'Deep Blue', xp: 62400, role: 'ANALYST' },
    { rank: 5, name: 'User_007', xp: 51200, role: 'OPERATOR' },
];

// Ícones personalizados para evitar imports excessivos
function CpuIcon({className}: {className?: string}) { return <Zap className={className} /> }
function NetworkIcon({className}: {className?: string}) { return <Target className={className} /> }
function GhostIcon({className}: {className?: string}) { return <Award className={className} /> }
function DiamondIcon({className}: {className?: string}) { return <Gift className={className} /> }
function LockIcon({className}: {className?: string}) { return <Medal className={className} /> }
function ClockIcon({className}: {className?: string}) { return <Star className={className} /> }

export default function GamificationPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estado
    const [xp, setXp] = useState(0);
    const [level, setLevel] = useState(42);
    const [targetXp] = useState(75); // Porcentagem para o próximo nível
    const [hoveredCard, setHoveredCard] = useState<number | null>(null);

    // 1. ENGINE DE PARTÍCULAS (CONFETE DIGITAL)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let particles: {x: number, y: number, vx: number, vy: number, color: string, size: number}[] = [];
        let animationId: number;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        // Criar explosão de partículas
        const createExplosion = (x: number, y: number) => {
            const colors = ['#FFD700', '#00FFD0', '#EF4444', '#FFFFFF'];
            for(let i=0; i<50; i++) {
                particles.push({
                    x, y,
                    vx: (Math.random() - 0.5) * 10,
                    vy: (Math.random() - 0.5) * 10,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    size: Math.random() * 4
                });
            }
        };

        // Loop de Animação
        const render = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach((p, i) => {
                p.x += p.vx;
                p.y += p.vy;
                p.vy += 0.2; // Gravidade
                p.size *= 0.95; // Diminuir tamanho

                ctx.fillStyle = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();

                if(p.size < 0.1) particles.splice(i, 1);
            });

            animationId = requestAnimationFrame(render);
        };
        render();

        // Expor função para o React usar
        (window as any).triggerConfetti = createExplosion;

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);

    // Animação de XP Inicial
    useEffect(() => {
        let current = 0;
        const interval = setInterval(() => {
            if (current >= targetXp) clearInterval(interval);
            else {
                current++;
                setXp(current);
            }
        }, 20);
        return () => clearInterval(interval);
    }, [targetXp]);

    const handleClaim = (e: React.MouseEvent) => {
        const rect = (e.target as HTMLElement).getBoundingClientRect();
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;
        if ((window as any).triggerConfetti) {
            (window as any).triggerConfetti(x, y);
        }
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* CANVAS DE PARTÍCULAS (OVERLAY) */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full pointer-events-none z-50" />

            {/* ESQUERDA: PERFIL & REATOR XP */}
            <div className="w-full lg:w-96 flex flex-col gap-6 relative z-10">
                
                {/* Card: Level Reactor */}
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center shadow-2xl relative overflow-hidden group">
                    {/* Background Glow */}
                    <div className="absolute inset-0 bg-radial-gradient from-[var(--color-primary)]/20 to-transparent opacity-20 animate-pulse" />
                    
                    <div className="relative w-48 h-48 mb-6">
                        {/* Círculos SVG animados */}
                        <svg className="w-full h-full -rotate-90">
                            {/* Track */}
                            <circle cx="96" cy="96" r="80" fill="none" stroke="#333" strokeWidth="12" />
                            {/* Progress */}
                            <circle 
                                cx="96" cy="96" r="80" fill="none" 
                                stroke="var(--color-primary)" strokeWidth="12"
                                strokeDasharray={502}
                                strokeDashoffset={502 - (502 * xp) / 100}
                                strokeLinecap="round"
                                className="transition-all duration-1000 ease-out"
                                style={{ filter: 'drop-shadow(0 0 10px var(--color-primary))' }}
                            />
                        </svg>
                        
                        {/* Conteúdo Central */}
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                            <span className="text-gray-400 text-xs font-mono uppercase tracking-widest">Level</span>
                            <span className="text-5xl font-black text-white font-display">{level}</span>
                            <span className="text-[var(--color-primary)] text-sm font-bold mt-1">{xp}%</span>
                        </div>
                    </div>

                    <h2 className="text-2xl font-bold text-white text-center mb-1">Supreme Commander</h2>
                    <p className="text-gray-500 text-xs font-mono uppercase tracking-widest">Class S • Architect</p>

                    <button 
                        onClick={handleClaim}
                        className="mt-8 w-full py-3 bg-[var(--color-primary)] hover:bg-[var(--color-accent)] text-black font-bold rounded-xl transition-all shadow-[0_0_20px_rgba(var(--color-primary-rgb),0.4)] flex items-center justify-center gap-2"
                    >
                        <Gift className="w-4 h-4" />
                        CLAIM DAILY REWARD
                    </button>
                </div>

                {/* Card: Leaderboard */}
                <div className="flex-1 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-6 overflow-hidden">
                    <div className="flex items-center gap-3 mb-6">
                        <Trophy className="w-5 h-5 text-yellow-400" />
                        <h3 className="text-sm font-bold text-white uppercase tracking-widest">Elite Leaderboard</h3>
                    </div>
                    
                    <div className="space-y-2">
                        {LEADERBOARD.map((user) => (
                            <div key={user.rank} className="flex items-center justify-between p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-white/5 group">
                                <div className="flex items-center gap-3">
                                    <div className={`
                                        w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm
                                        ${user.rank === 1 ? 'bg-yellow-400 text-black shadow-[0_0_10px_#FACC15]' : 
                                          user.rank === 2 ? 'bg-gray-300 text-black' : 
                                          user.rank === 3 ? 'bg-amber-700 text-white' : 'bg-gray-800 text-gray-400'}
                                    `}>
                                        {user.rank}
                                    </div>
                                    <div className="flex flex-col">
                                        <span className="text-sm text-white font-medium">{user.name}</span>
                                        <span className="text-[10px] text-gray-500 font-mono">{user.role}</span>
                                    </div>
                                </div>
                                <span className="text-xs font-mono text-[var(--color-primary)] group-hover:scale-110 transition-transform">
                                    {user.xp.toLocaleString()} XP
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* DIREITA: HALL OF ACHIEVEMENTS (GRID 3D) */}
            <div className="flex-1 bg-[#02040a] rounded-3xl border border-white/10 p-8 overflow-y-auto scrollbar-thin scrollbar-thumb-white/10">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-black text-white tracking-tight font-display">HALL OF LEGENDS</h1>
                        <p className="text-gray-400 text-sm mt-1">Desbloqueie protocolos secretos para evoluir.</p>
                    </div>
                    <div className="flex gap-2">
                        <span className="px-3 py-1 rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] border border-[var(--color-primary)]/20 text-xs font-bold">
                            {ACHIEVEMENTS.filter(a => a.unlocked).length}/{ACHIEVEMENTS.length} UNLOCKED
                        </span>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {ACHIEVEMENTS.map((ach) => (
                        <div 
                            key={ach.id}
                            onMouseEnter={() => setHoveredCard(ach.id)}
                            onMouseLeave={() => setHoveredCard(null)}
                            className={`
                                relative group h-64 rounded-2xl border transition-all duration-500 cursor-pointer
                                flex flex-col items-center justify-center text-center p-6 perspective-1000
                                ${ach.unlocked 
                                    ? 'bg-white/5 border-white/10 hover:border-[var(--color-primary)]/50' 
                                    : 'bg-black/40 border-white/5 opacity-50 grayscale hover:opacity-70'}
                            `}
                            style={{
                                transformStyle: 'preserve-3d',
                                transform: hoveredCard === ach.id ? 'translateY(-10px) scale(1.02)' : 'none'
                            }}
                        >
                            {/* Efeito de Brilho (Foil Effect) */}
                            {ach.unlocked && (
                                <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity bg-gradient-to-tr from-transparent via-white to-transparent pointer-events-none" />
                            )}

                            {/* Ícone 3D */}
                            <div className={`
                                w-20 h-20 rounded-full flex items-center justify-center mb-6 text-3xl
                                transition-transform duration-500 shadow-xl
                                ${ach.unlocked 
                                    ? `bg-gradient-to-br ${
                                        ach.rarity === 'legendary' ? 'from-yellow-400 to-amber-600 text-black' : 
                                        ach.rarity === 'epic' ? 'from-purple-500 to-indigo-600 text-white' : 
                                        'from-blue-400 to-cyan-600 text-white'
                                      }` 
                                    : 'bg-gray-800 text-gray-600'}
                                ${hoveredCard === ach.id ? 'scale-110 rotate-y-180' : ''}
                            `}>
                                <ach.icon className="w-10 h-10" />
                            </div>

                            <h3 className={`text-lg font-bold mb-2 ${ach.unlocked ? 'text-white' : 'text-gray-500'}`}>
                                {ach.title}
                            </h3>
                            <p className="text-xs text-gray-400 leading-relaxed">
                                {ach.desc}
                            </p>

                            {/* Badge de Raridade */}
                            <div className={`
                                absolute top-4 right-4 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider
                                ${ach.rarity === 'legendary' ? 'text-yellow-400 border border-yellow-400/30' : 
                                  ach.rarity === 'epic' ? 'text-purple-400 border border-purple-400/30' : 
                                  'text-blue-400 border border-blue-400/30'}
                            `}>
                                {ach.rarity}
                            </div>

                            {/* Cadeado se bloqueado */}
                            {!ach.unlocked && (
                                <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-[2px] rounded-2xl">
                                    <LockIcon className="w-8 h-8 text-gray-500" />
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Efeitos de Fundo */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none z-0" />
        </div>
    );
}
