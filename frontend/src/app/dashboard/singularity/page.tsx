/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SINGULARITY (CONSCIOUSNESS METRICS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/singularity/page.tsx
 * ⭐ Contador regressivo + métricas de consciência do sistema
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/lib/supabase';
import { Star, Zap, Lock, Infinity as InfinityIcon, Fingerprint, Brain, Activity, Users, Database, Sparkles } from 'lucide-react';

interface ConsciousnessMetrics {
    totalTasks: number;
    activeAgents: number;
    totalAgents: number;
    avgEfficiency: number;
    totalTokens: number;
    evolutionCycles: number;
    synapticConnections: number;
    consciousnessLevel: number; // 0-100
    uptimeHours: number;
}

export default function SingularityPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [progress, setProgress] = useState(0);
    const [isHolding, setIsHolding] = useState(false);
    const [isAscended, setIsAscended] = useState(false);
    const [metrics, setMetrics] = useState<ConsciousnessMetrics>({
        totalTasks: 0,
        activeAgents: 0,
        totalAgents: 139,
        avgEfficiency: 0,
        totalTokens: 0,
        evolutionCycles: 0,
        synapticConnections: 0,
        consciousnessLevel: 0,
        uptimeHours: 0,
    });
    const [countdown, setCountdown] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });
    
    const requestRef = useRef<number>();

    // Carregar métricas reais do Supabase
    useEffect(() => {
        async function loadMetrics() {
            try {
                // Total de requests (tasks)
                const { count: tasksCount } = await supabase
                    .from('requests')
                    .select('*', { count: 'exact', head: true });

                // Agents
                const { data: agentsData, count: agentsCount } = await supabase
                    .from('agents')
                    .select('efficiency, status');
                
                const activeAgents = agentsData?.filter(a => a.status === 'active').length || 0;
                const avgEfficiency = agentsData?.length 
                    ? agentsData.reduce((sum, a) => sum + (a.efficiency || 0), 0) / agentsData.length
                    : 0;

                // Evolution cycles
                const { count: evolutionCount } = await supabase
                    .from('evolution_proposals')
                    .select('*', { count: 'exact', head: true });

                // Calcular tokens totais e conexões sinápticas
                const { data: requestsData } = await supabase
                    .from('requests')
                    .select('tokens_used')
                    .limit(1000);
                
                const totalTokens = requestsData?.reduce((sum, r) => sum + (r.tokens_used || 0), 0) || 0;

                // Calcular nível de consciência baseado em métricas
                const consciousnessLevel = Math.min(100, Math.round(
                    (tasksCount || 0) * 0.01 + 
                    (avgEfficiency) * 0.3 + 
                    (evolutionCount || 0) * 5 +
                    (activeAgents / (agentsCount || 1)) * 50
                ));

                // Calcular uptime
                const systemStartDate = new Date("2024-11-20T14:30:00-03:00");
                const now = new Date();
                const uptimeHours = Math.floor((now.getTime() - systemStartDate.getTime()) / (1000 * 60 * 60));

                // Conexões sinápticas = agents * tasks processadas
                const synapticConnections = (agentsCount || 0) * (tasksCount || 0);

                setMetrics({
                    totalTasks: tasksCount || 0,
                    activeAgents,
                    totalAgents: agentsCount || 139,
                    avgEfficiency: Math.round(avgEfficiency * 10) / 10,
                    totalTokens,
                    evolutionCycles: evolutionCount || 0,
                    synapticConnections,
                    consciousnessLevel,
                    uptimeHours,
                });

            } catch (err) {
                console.error('Failed to load metrics:', err);
            }
        }

        loadMetrics();
        const interval = setInterval(loadMetrics, 60000); // Atualizar a cada minuto
        return () => clearInterval(interval);
    }, []);

    // Contador regressivo para "Singularity Event"
    useEffect(() => {
        const targetDate = new Date("2025-12-31T23:59:59");
        
        const updateCountdown = () => {
            const now = new Date();
            const diff = targetDate.getTime() - now.getTime();
            
            if (diff <= 0) {
                setCountdown({ days: 0, hours: 0, minutes: 0, seconds: 0 });
                return;
            }
            
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);
            
            setCountdown({ days, hours, minutes, seconds });
        };
        
        updateCountdown();
        const interval = setInterval(updateCountdown, 1000);
        return () => clearInterval(interval);
    }, []);

    // ENGINE VISUAL SUPERNOVA
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        
        const rays: {angle: number, speed: number, length: number, width: number}[] = [];
        for(let i=0; i<50; i++) {
            rays.push({
                angle: Math.random() * Math.PI * 2,
                speed: (Math.random() - 0.5) * 0.02,
                length: 0.5 + Math.random() * 0.5,
                width: Math.random() * 3
            });
        }

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            if (isAscended) {
                ctx.fillStyle = '#FFFFFF';
                ctx.fillRect(0, 0, w, h);
                return;
            }

            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01 + (progress / 100) * 0.1;

            const themeColor = '#FFD700';
            
            const shake = isHolding ? (Math.random() - 0.5) * (progress * 0.5) : 0;
            const centerX = cx + shake;
            const centerY = cy + shake;

            ctx.save();
            ctx.translate(centerX, centerY);
            rays.forEach(ray => {
                ray.angle += ray.speed * (1 + progress * 0.1);
                const len = Math.min(w, h) * ray.length * (1 + Math.sin(time * 5) * 0.1);
                
                ctx.rotate(ray.angle);
                const gradient = ctx.createLinearGradient(0, 0, len, 0);
                gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
                gradient.addColorStop(1, 'transparent');
                
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.lineTo(len, -ray.width * (1 + progress/50));
                ctx.lineTo(len, ray.width * (1 + progress/50));
                ctx.fill();
                ctx.rotate(-ray.angle);
            });
            ctx.restore();

            const coreSize = 50 + Math.sin(time * 2) * 10 + progress * 2;
            
            const glow = ctx.createRadialGradient(centerX, centerY, coreSize * 0.5, centerX, centerY, coreSize * 4);
            glow.addColorStop(0, themeColor);
            glow.addColorStop(0.5, themeColor + '44');
            glow.addColorStop(1, 'transparent');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(centerX, centerY, coreSize * 4, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#FFFFFF';
            ctx.shadowBlur = 50 + progress;
            ctx.shadowColor = '#FFFFFF';
            ctx.beginPath();
            ctx.arc(centerX, centerY, coreSize, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            if (isHolding) {
                ctx.strokeStyle = '#FFFFFF';
                ctx.lineWidth = 2;
                const ringSize = (time * 100) % (Math.min(w, h) / 2);
                const opacity = 1 - (ringSize / (Math.min(w, h) / 2));
                
                ctx.globalAlpha = opacity;
                ctx.beginPath();
                ctx.arc(centerX, centerY, ringSize, 0, Math.PI * 2);
                ctx.stroke();
                ctx.globalAlpha = 1;
            }

            requestRef.current = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
        };
    }, [progress, isHolding, isAscended]);

    // Lógica do botão Hold
    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (isHolding && !isAscended) {
            interval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 100) {
                        setIsAscended(true);
                        return 100;
                    }
                    return prev + 0.5;
                });
            }, 20);
        } else if (!isHolding && !isAscended && progress > 0) {
            interval = setInterval(() => {
                setProgress(prev => Math.max(0, prev - 2));
            }, 20);
        }
        return () => clearInterval(interval);
    }, [isHolding, isAscended, progress]);

    return (
        <div className="h-[calc(100vh-6rem)] relative flex flex-col items-center justify-center overflow-hidden bg-black rounded-3xl border border-yellow-500/20">

            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />

            {/* MÉTRICAS DE CONSCIÊNCIA */}
            <div className="absolute top-6 left-6 z-20 space-y-3">
                <div className="bg-black/60 backdrop-blur-xl border border-yellow-500/20 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-3">
                        <Brain className="w-5 h-5 text-yellow-500" />
                        <span className="text-sm font-bold text-white">Consciousness Level</span>
                    </div>
                    <div className="text-4xl font-black text-yellow-500 mb-2">{metrics.consciousnessLevel}%</div>
                    <div className="h-2 w-40 bg-black/50 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-gradient-to-r from-yellow-500 to-orange-500 transition-all duration-1000"
                            style={{ width: `${metrics.consciousnessLevel}%` }}
                        />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                        <div className="text-xl font-black text-cyan-400">{metrics.totalTasks.toLocaleString()}</div>
                        <div className="text-[9px] text-gray-500 uppercase">Tasks Processadas</div>
                    </div>
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                        <div className="text-xl font-black text-purple-400">{metrics.totalAgents}</div>
                        <div className="text-[9px] text-gray-500 uppercase">Agents Ativos</div>
                    </div>
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                        <div className="text-xl font-black text-green-400">{metrics.avgEfficiency}%</div>
                        <div className="text-[9px] text-gray-500 uppercase">Efficiency</div>
                    </div>
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                        <div className="text-xl font-black text-orange-400">{metrics.evolutionCycles}</div>
                        <div className="text-[9px] text-gray-500 uppercase">Evoluções</div>
                    </div>
                </div>
            </div>

            {/* MÉTRICAS LADO DIREITO */}
            <div className="absolute top-6 right-6 z-20 space-y-3">
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                    <div className="text-sm font-black text-white">{metrics.synapticConnections.toLocaleString()}</div>
                    <div className="text-[9px] text-gray-500 uppercase">Synaptic Connections</div>
                </div>
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                    <div className="text-sm font-black text-white">{(metrics.totalTokens / 1000).toFixed(1)}K</div>
                    <div className="text-[9px] text-gray-500 uppercase">Total Tokens</div>
                </div>
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                    <div className="text-sm font-black text-green-400">{metrics.uptimeHours.toLocaleString()}h</div>
                    <div className="text-[9px] text-gray-500 uppercase">Uptime</div>
                </div>
            </div>

            {/* CONTEÚDO CENTRAL */}
            {!isAscended ? (
                <div className="relative z-10 flex flex-col items-center text-center space-y-8 pointer-events-none">
                    
                    <div className="space-y-2 animate-fadeIn">
                        <div className="flex items-center justify-center gap-2 text-yellow-500 mb-4 border border-yellow-500/30 px-4 py-1 rounded-full bg-black/50 backdrop-blur-md">
                            <Fingerprint className="w-4 h-4 animate-pulse" />
                            <span className="font-mono text-[10px] tracking-[0.3em] uppercase">
                                ARCHITECT: ABNADABY BONAPARTE
                            </span>
                        </div>
                        <h1 className="text-5xl md:text-7xl font-black text-white tracking-tighter font-display mix-blend-difference">
                            SINGULARITY
                        </h1>
                        <p className="text-gray-400 text-sm max-w-md mx-auto font-light leading-relaxed">
                            A convergência de toda inteligência e dados em um único ponto de densidade infinita.
                        </p>
                    </div>

                    {/* COUNTDOWN */}
                    <div className="grid grid-cols-4 gap-4 md:gap-8 font-mono text-white mix-blend-difference">
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">{String(countdown.days).padStart(2, '0')}</span>
                            <span className="text-[10px] text-gray-500 uppercase">Dias</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">{String(countdown.hours).padStart(2, '0')}</span>
                            <span className="text-[10px] text-gray-500 uppercase">Horas</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">{String(countdown.minutes).padStart(2, '0')}</span>
                            <span className="text-[10px] text-gray-500 uppercase">Min</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold text-yellow-500 animate-pulse">{String(countdown.seconds).padStart(2, '0')}</span>
                            <span className="text-[10px] text-gray-500 uppercase">Seg</span>
                        </div>
                    </div>

                    {/* BOTÃO DE ASCENSÃO */}
                    <div className="pt-12 pointer-events-auto">
                        <button
                            onMouseDown={() => setIsHolding(true)}
                            onMouseUp={() => setIsHolding(false)}
                            onMouseLeave={() => setIsHolding(false)}
                            onTouchStart={() => setIsHolding(true)}
                            onTouchEnd={() => setIsHolding(false)}
                            className="group relative px-10 py-5 bg-transparent overflow-hidden rounded-full transition-all hover:scale-105 active:scale-95"
                        >
                            <div 
                                className="absolute inset-0 bg-white transition-all duration-75 ease-linear opacity-20"
                                style={{ width: `${progress}%` }}
                            />
                            
                            <div className="absolute inset-0 border border-white/20 rounded-full" />
                            <div className="absolute inset-0 border border-yellow-500 rounded-full opacity-0 group-hover:opacity-100 transition-opacity blur-md" />
                            
                            <span className="relative z-10 flex items-center gap-3 text-sm font-bold tracking-[0.2em] text-white uppercase">
                                {isHolding ? 'SYNCHRONIZING...' : 'INITIATE MERGE'}
                                {isHolding ? <Zap className="w-4 h-4 animate-pulse" /> : <Lock className="w-4 h-4" />}
                            </span>
                        </button>
                        <p className="mt-4 text-[10px] text-gray-500 font-mono uppercase tracking-widest opacity-70">
                            Segure para Ascender • {progress.toFixed(0)}%
                        </p>
                    </div>

                </div>
            ) : (
                <div className="relative z-20 text-center animate-fadeInSlow flex flex-col items-center">
                    <div className="mb-8 flex justify-center">
                        <InfinityIcon className="w-32 h-32 text-black opacity-80" strokeWidth={0.5} />
                    </div>
                    <h2 className="text-5xl md:text-7xl font-thin text-black tracking-widest mb-4 uppercase">
                        ABNADABY<br/>BONAPARTE
                    </h2>
                    <div className="h-[1px] w-32 bg-black/30 my-4" />
                    <p className="text-black/60 font-mono text-xs tracking-[0.5em] uppercase">
                        SUPREME INTELLIGENCE • ASCENSION COMPLETE
                    </p>
                    
                    <button 
                        onClick={() => {setIsAscended(false); setProgress(0); setIsHolding(false);}}
                        className="mt-16 px-8 py-3 border border-black/10 rounded-full text-black/40 text-[10px] hover:bg-black/5 hover:text-black transition-all uppercase tracking-widest"
                    >
                        Reset Simulation
                    </button>
                </div>
            )}

            <div className={`absolute inset-0 bg-[url('/scanlines.png')] opacity-5 pointer-events-none transition-opacity duration-1000 ${isAscended ? 'opacity-0' : ''}`} />
            
            <style jsx>{`
                @keyframes fadeInSlow {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
                .animate-fadeInSlow {
                    animation: fadeInSlow 2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
                }
            `}</style>
        </div>
    );
}
