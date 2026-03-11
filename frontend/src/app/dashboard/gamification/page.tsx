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
import { Trophy, Crown, Medal, Star, Zap, Target, Award, Gift, Lock as LockIconLucide, RefreshCw } from 'lucide-react';
import { supabase } from '@/lib/supabase';

interface Achievement {
    id: string;
    title: string;
    description: string;
    rarity: string;
    unlocked: boolean;
    icon_type?: string;
}

interface LeaderboardEntry {
    rank: number;
    name: string;
    xp: number;
    role: string;
}

function getAchievementIcon(iconType: string | undefined) {
    switch (iconType) {
        case 'cpu': return Zap;
        case 'network': return Target;
        case 'ghost': return Award;
        case 'diamond': return Gift;
        case 'lock': return Medal;
        case 'clock': return Star;
        default: return Award;
    }
}

export default function GamificationPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    const [xp, setXp] = useState(0);
    const [level, setLevel] = useState(0);
    const [targetXp] = useState(75);
    const [hoveredCard, setHoveredCard] = useState<string | null>(null);
    const [achievements, setAchievements] = useState<Achievement[]>([]);
    const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadData() {
            setLoading(true);
            setError(null);
            try {
                const { data: achData, error: achError } = await supabase
                    .from('achievements')
                    .select('*');

                if (achError) throw achError;

                const mapped: Achievement[] = (achData || []).map((a) => ({
                    id: a.id,
                    title: a.title || 'Achievement',
                    description: a.description || '',
                    rarity: a.rarity || 'rare',
                    unlocked: a.unlocked ?? false,
                    icon_type: a.icon_type,
                }));
                setAchievements(mapped);

                const { data: lbData, error: lbError } = await supabase
                    .from('leaderboard')
                    .select('*')
                    .order('xp', { ascending: false })
                    .limit(10);

                if (lbError) throw lbError;

                const lbMapped: LeaderboardEntry[] = (lbData || []).map((entry, idx) => ({
                    rank: idx + 1,
                    name: entry.name || `User ${idx + 1}`,
                    xp: entry.xp || 0,
                    role: entry.role || 'OPERATOR',
                }));
                setLeaderboard(lbMapped);

                if (lbMapped.length > 0) {
                    const topXp = lbMapped[0].xp;
                    setLevel(Math.floor(topXp / 1000));
                }
            } catch (err) {
                console.error('Failed to load gamification data:', err);
                setError('Erro ao carregar dados');
            } finally {
                setLoading(false);
            }
        }

        loadData();
    }, []);

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
                        <Trophy className="w-5 h-5" style={{ color: 'var(--color-warning)' }} />
                        <h3 className="text-sm font-bold text-white uppercase tracking-widest">Elite Leaderboard</h3>
                    </div>
                    
                    <div className="space-y-2">
                        {loading ? (
                            <div className="flex items-center justify-center py-8">
                                <RefreshCw className="w-6 h-6 animate-spin text-[var(--color-primary)]" />
                            </div>
                        ) : leaderboard.length === 0 ? (
                            <div className="text-center py-8">
                                <Trophy className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                                <p className="text-xs text-gray-500 font-mono">Nenhum dado no leaderboard</p>
                            </div>
                        ) : (
                            leaderboard.map((user) => (
                                <div key={user.rank} className="flex items-center justify-between p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-white/5 group">
                                    <div className="flex items-center gap-3">
                                        <div className={`
                                            w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm
                                            ${user.rank === 1 ? 'bg-[var(--color-warning)] text-black shadow-[0_0_10px_var(--color-warning)]' : 
                                              user.rank === 2 ? 'bg-gray-300 text-black' : 
                                              user.rank === 3 ? 'bg-[#B45309] text-white' : 'bg-gray-800 text-gray-400'}
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
                            ))
                        )}
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
                            {achievements.filter(a => a.unlocked).length}/{achievements.length} UNLOCKED
                        </span>
                    </div>
                </div>

                {loading ? (
                    <div className="flex items-center justify-center h-64">
                        <RefreshCw className="w-10 h-10 animate-spin text-[var(--color-primary)]" />
                    </div>
                ) : error ? (
                    <div className="flex flex-col items-center justify-center h-64">
                        <p className="text-sm text-[var(--color-error)]">{error}</p>
                    </div>
                ) : achievements.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-64">
                        <Award className="w-16 h-16 mb-4 text-gray-600" />
                        <p className="text-xl font-bold text-white">Nenhuma conquista cadastrada</p>
                        <p className="text-sm text-gray-500 mt-2">As conquistas aparecerão aqui quando configuradas</p>
                    </div>
                ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {achievements.map((ach) => {
                        const IconComponent = getAchievementIcon(ach.icon_type);
                        return (
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
                            {ach.unlocked && (
                                <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity bg-gradient-to-tr from-transparent via-white to-transparent pointer-events-none" />
                            )}

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
                                <IconComponent className="w-10 h-10" />
                            </div>

                            <h3 className={`text-lg font-bold mb-2 ${ach.unlocked ? 'text-white' : 'text-gray-500'}`}>
                                {ach.title}
                            </h3>
                            <p className="text-xs text-gray-400 leading-relaxed">
                                {ach.description}
                            </p>

                            <div className={`
                                absolute top-4 right-4 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider
                                ${ach.rarity === 'legendary' ? 'text-[var(--color-warning)] border border-[var(--color-warning)]/30' : 
                                  ach.rarity === 'epic' ? 'text-[var(--color-accent)] border border-[var(--color-accent)]/30' : 
                                  'text-[var(--color-primary)] border border-[var(--color-primary)]/30'}
                            `}>
                                {ach.rarity}
                            </div>

                            {!ach.unlocked && (
                                <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-[2px] rounded-2xl">
                                    <LockIconLucide className="w-8 h-8 text-gray-500" />
                                </div>
                            )}
                        </div>
                        );
                    })}
                </div>
                )}
            </div>

            {/* Efeitos de Fundo */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none z-0" />
        </div>
    );
}
