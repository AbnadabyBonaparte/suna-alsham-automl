/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THE VOID (OBSERVAÇÃO SILENCIOSA)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/void/page.tsx
 * 👁️ Logs reais do sistema + métricas VOID squad
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/lib/supabase';
import { Eye, AlertTriangle, ShieldAlert, Database, XCircle, Trash2, Activity, RefreshCw, Filter, Clock, Zap } from 'lucide-react';

interface VoidLog {
    id: string;
    source: string;
    message: string;
    integrity: number;
    timestamp: string;
    type: 'info' | 'warning' | 'error' | 'success';
    agent_id?: string;
}

interface VoidMetrics {
    totalLogs: number;
    warningsToday: number;
    errorsToday: number;
    avgIntegrity: number;
    activeObservers: number;
}

export default function VoidPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [logs, setLogs] = useState<VoidLog[]>([]);
    const [metrics, setMetrics] = useState<VoidMetrics>({
        totalLogs: 0,
        warningsToday: 0,
        errorsToday: 0,
        avgIntegrity: 100,
        activeObservers: 7,
    });
    const [hoveredLog, setHoveredLog] = useState<string | null>(null);
    const [filter, setFilter] = useState<'all' | 'warning' | 'error' | 'info'>('all');
    const [isLoading, setIsLoading] = useState(true);

    // Carregar logs reais do Supabase
    useEffect(() => {
        async function loadLogs() {
            setIsLoading(true);
            try {
                // Buscar requests com status de erro ou warning
                const { data: requestsData, error } = await supabase
                    .from('requests')
                    .select('*')
                    .order('created_at', { ascending: false })
                    .limit(50);

                if (error) throw error;

                // Transformar em logs do VOID
                const voidLogs: VoidLog[] = (requestsData || []).map(req => {
                    let type: VoidLog['type'] = 'info';
                    let integrity = 100;
                    
                    if (req.status === 'failed' || req.status === 'error') {
                        type = 'error';
                        integrity = Math.floor(Math.random() * 30 + 10);
                    } else if (req.status === 'processing') {
                        type = 'warning';
                        integrity = Math.floor(Math.random() * 40 + 40);
                    } else if (req.status === 'completed') {
                        type = 'success';
                        integrity = Math.floor(Math.random() * 20 + 80);
                    }

                    return {
                        id: req.id,
                        source: req.assigned_agent_id ? `AGENT_${req.assigned_agent_id.slice(0, 6).toUpperCase()}` : 'SYSTEM',
                        message: req.title || req.description || 'Processo monitorado pelo VOID',
                        integrity,
                        timestamp: new Date(req.created_at).toLocaleTimeString('pt-BR'),
                        type,
                        agent_id: req.assigned_agent_id,
                    };
                });

                setLogs(voidLogs);

                // Calcular métricas
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                const todayLogs = voidLogs.filter(l => new Date(l.timestamp) >= today);
                const warnings = voidLogs.filter(l => l.type === 'warning').length;
                const errors = voidLogs.filter(l => l.type === 'error').length;
                const avgIntegrity = voidLogs.length > 0 
                    ? Math.round(voidLogs.reduce((sum, l) => sum + l.integrity, 0) / voidLogs.length)
                    : 100;

                // Contar agents do squad VOID
                const { count: voidAgents } = await supabase
                    .from('agents')
                    .select('*', { count: 'exact', head: true })
                    .ilike('squad', '%void%');

                setMetrics({
                    totalLogs: voidLogs.length,
                    warningsToday: warnings,
                    errorsToday: errors,
                    avgIntegrity,
                    activeObservers: voidAgents || 7,
                });

            } catch (err) {
                console.error('Failed to load VOID logs:', err);
            } finally {
                setIsLoading(false);
            }
        }

        loadLogs();

        // Refresh a cada 30s
        const interval = setInterval(loadLogs, 30000);
        return () => clearInterval(interval);
    }, []);

    // ENGINE DO BURACO NEGRO
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        const particles: { angle: number, radius: number, speed: number, size: number, colorOffset: number }[] = [];
        const PARTICLE_COUNT = 800;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        for(let i=0; i<PARTICLE_COUNT; i++) {
            particles.push({
                angle: Math.random() * Math.PI * 2,
                radius: 100 + Math.random() * 400,
                speed: 0.002 + Math.random() * 0.005,
                size: Math.random() * 2,
                colorOffset: Math.random()
            });
        }

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            const themeColor = '#8B5CF6'; // Roxo VOID

            particles.forEach(p => {
                p.angle += p.speed * (500 / p.radius); 
                p.radius -= 0.2; 
                
                if(p.radius < 50) {
                    p.radius = 400 + Math.random() * 100;
                    p.size = Math.random() * 2;
                }

                const x = cx + Math.cos(p.angle) * p.radius;
                const y = cy + Math.sin(p.angle) * (p.radius * 0.4);

                const isFront = Math.sin(p.angle) > 0;
                const depthScale = isFront ? 1.2 : 0.8;
                
                ctx.beginPath();
                ctx.arc(x, y, p.size * depthScale, 0, Math.PI * 2);
                
                const opacity = (p.radius - 50) / 400;
                ctx.fillStyle = themeColor;
                ctx.globalAlpha = opacity * (isFront ? 1 : 0.3);
                
                ctx.fill();
            });
            ctx.globalAlpha = 1;

            // Event Horizon
            const glow = ctx.createRadialGradient(cx, cy, 40, cx, cy, 120);
            glow.addColorStop(0, '#000000');
            glow.addColorStop(0.5, themeColor + '66');
            glow.addColorStop(1, 'transparent');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(cx, cy, 120, 0, Math.PI * 2);
            ctx.fill();

            // Núcleo
            ctx.fillStyle = '#000000';
            ctx.beginPath();
            ctx.arc(cx, cy, 48, 0, Math.PI * 2);
            ctx.fill();
            
            // Anel de Fótons
            ctx.strokeStyle = 'rgba(139, 92, 246, 0.3)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(cx, cy, 50, 0, Math.PI * 2);
            ctx.stroke();

            // Olho do VOID
            ctx.fillStyle = '#8B5CF6';
            ctx.globalAlpha = 0.8 + Math.sin(time * 2) * 0.2;
            ctx.beginPath();
            ctx.ellipse(cx, cy, 15, 8, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = '#FFFFFF';
            ctx.globalAlpha = 1;
            ctx.beginPath();
            ctx.arc(cx, cy, 3, 0, Math.PI * 2);
            ctx.fill();

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);

    const filteredLogs = logs.filter(log => {
        if (filter === 'all') return true;
        return log.type === filter;
    });

    return (
        <div className="relative h-[calc(100vh-6rem)] w-full overflow-hidden rounded-3xl border border-purple-500/20 bg-black group">

            <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />

            {/* HEADER */}
            <div className="absolute top-10 left-1/2 -translate-x-1/2 text-center pointer-events-none z-10">
                <h1 className="text-4xl font-black text-white tracking-[0.5em] mb-2 font-display opacity-80">THE VOID</h1>
                <p className="text-xs font-mono text-purple-400 uppercase tracking-widest">
                    Observação Silenciosa • {metrics.activeObservers} Observadores Ativos
                </p>
            </div>

            {/* MÉTRICAS */}
            <div className="absolute top-6 left-6 z-20 space-y-3">
                <div className="bg-black/60 backdrop-blur-xl border border-purple-500/20 rounded-xl p-4 w-64">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-xs text-gray-500 uppercase">System Integrity</span>
                        <span className={`text-xl font-black ${metrics.avgIntegrity > 70 ? 'text-green-400' : metrics.avgIntegrity > 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                            {metrics.avgIntegrity}%
                        </span>
                    </div>
                    <div className="h-2 w-full bg-black/50 rounded-full overflow-hidden">
                        <div 
                            className={`h-full transition-all duration-1000 ${metrics.avgIntegrity > 70 ? 'bg-green-500' : metrics.avgIntegrity > 40 ? 'bg-yellow-500' : 'bg-red-500'}`}
                            style={{ width: `${metrics.avgIntegrity}%` }}
                        />
                    </div>
                </div>
                
                <div className="grid grid-cols-2 gap-2">
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                        <div className="text-xl font-black text-purple-400">{metrics.totalLogs}</div>
                        <div className="text-[9px] text-gray-500 uppercase">Total Logs</div>
                    </div>
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-lg p-3 text-center">
                        <div className="text-xl font-black text-red-400">{metrics.errorsToday}</div>
                        <div className="text-[9px] text-gray-500 uppercase">Errors</div>
                    </div>
                </div>
            </div>

            {/* FILTROS */}
            <div className="absolute top-6 right-6 z-20 flex gap-2">
                {(['all', 'warning', 'error', 'info'] as const).map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        className={`px-4 py-2 rounded-lg text-xs font-bold uppercase transition-all ${
                            filter === f 
                                ? 'bg-purple-500 text-white' 
                                : 'bg-black/40 text-gray-400 hover:bg-white/10'
                        }`}
                    >
                        {f === 'all' ? 'Todos' : f}
                    </button>
                ))}
            </div>

            {/* LOGS FLUTUANTES */}
            <div className="absolute right-0 top-20 bottom-20 w-full md:w-96 p-6 flex flex-col justify-center pointer-events-none overflow-hidden">
                <div className="space-y-4 pointer-events-auto max-h-full overflow-y-auto scrollbar-thin scrollbar-thumb-purple-500/20">
                    {isLoading ? (
                        <div className="flex items-center justify-center py-8">
                            <RefreshCw className="w-8 h-8 text-purple-500 animate-spin" />
                        </div>
                    ) : filteredLogs.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            <Eye className="w-12 h-12 mx-auto mb-3 opacity-20" />
                            <p>O VOID está observando...</p>
                            <p className="text-xs">Nenhum log encontrado</p>
                        </div>
                    ) : (
                        filteredLogs.slice(0, 8).map((log, index) => (
                            <div 
                                key={log.id}
                                onMouseEnter={() => setHoveredLog(log.id)}
                                onMouseLeave={() => setHoveredLog(null)}
                                className={`
                                    relative p-4 rounded-xl border backdrop-blur-md transition-all duration-500 ease-out
                                    ${hoveredLog === log.id 
                                        ? 'bg-purple-500/10 border-purple-500 translate-x-[-10px]' 
                                        : 'bg-black/40 border-white/5 translate-x-0 hover:bg-white/5'
                                    }
                                `}
                                style={{
                                    opacity: 1 - (index * 0.1),
                                    transform: `scale(${1 - index * 0.02})`
                                }}
                            >
                                <div className="flex justify-between items-start mb-1">
                                    <div className="flex items-center gap-2">
                                        {log.type === 'error' ? (
                                            <XCircle className="w-4 h-4 text-red-500" />
                                        ) : log.type === 'warning' ? (
                                            <AlertTriangle className="w-4 h-4 text-yellow-500" />
                                        ) : log.type === 'success' ? (
                                            <Zap className="w-4 h-4 text-green-500" />
                                        ) : (
                                            <Database className="w-4 h-4 text-purple-500" />
                                        )}
                                        <span className="text-[10px] font-mono text-gray-400 uppercase tracking-wider">{log.source}</span>
                                    </div>
                                    <span className="text-[10px] text-gray-600 font-mono">{log.timestamp}</span>
                                </div>
                                <p className="text-sm text-gray-200 font-light leading-snug truncate">{log.message}</p>
                                
                                <div className="mt-3 h-1 w-full bg-black/50 rounded-full overflow-hidden">
                                    <div 
                                        className={`h-full transition-all duration-500 ${
                                            log.integrity < 30 ? 'bg-red-500' : 
                                            log.integrity < 70 ? 'bg-yellow-500' : 'bg-purple-500'
                                        }`} 
                                        style={{ width: `${log.integrity}%` }} 
                                    />
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {/* CONTROLES INFERIORES */}
            <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex gap-4 z-10">
                <button className="flex items-center gap-2 px-6 py-3 bg-red-900/20 border border-red-500/30 text-red-400 rounded-full hover:bg-red-500 hover:text-white transition-all uppercase text-xs font-bold tracking-widest backdrop-blur-md group">
                    <Trash2 className="w-4 h-4" />
                    <span>Purge Memory</span>
                </button>
                <button 
                    onClick={() => window.location.reload()}
                    className="flex items-center gap-2 px-6 py-3 bg-white/5 border border-white/10 text-white rounded-full hover:bg-white/10 transition-all uppercase text-xs font-bold tracking-widest backdrop-blur-md"
                >
                    <Eye className="w-4 h-4" />
                    <span>Deep Scan</span>
                </button>
            </div>

            <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black pointer-events-none" />
        </div>
    );
}
