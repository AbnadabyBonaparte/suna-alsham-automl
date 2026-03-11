/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - CONTAINMENT (DIGITAL FORTRESS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/containment/page.tsx
 * 🛡️ Painel de segurança com DEFCON level e ameaças detectadas
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/lib/supabase';
import { Shield, ShieldAlert, Lock, Unlock, AlertTriangle, Activity, XOctagon, CheckCircle, Clock, Zap, Eye, RefreshCw } from 'lucide-react';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';

const DEFCON_LEVELS = [
    { lvl: 5, label: 'NORMAL', color: '#10B981', desc: 'Protocolos padrão ativos. Sistema operando normalmente.' },
    { lvl: 4, label: 'ELEVATED', color: '#3B82F6', desc: 'Monitoramento aumentado. Atenção redobrada.' },
    { lvl: 3, label: 'GUARDED', color: '#F59E0B', desc: 'Tráfego externo limitado. Verificações extras.' },
    { lvl: 2, label: 'HIGH', color: '#EF4444', desc: 'Contramedidas letais ativas. Alerta máximo.' },
    { lvl: 1, label: 'MAXIMUM', color: '#7F1D1D', desc: 'LOCKDOWN TOTAL DO SISTEMA.' },
];

interface SecurityEvent {
    id: string;
    type: 'blocked' | 'warning' | 'info';
    source: string;
    message: string;
    timestamp: string;
}

export default function ContainmentPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    const [defcon, setDefcon] = useState(5);
    const [integrity, setIntegrity] = useState(100);
    const [threatsBlocked, setThreatsBlocked] = useState(0);
    const [isLockdown, setIsLockdown] = useState(false);
    const [events, setEvents] = useState<SecurityEvent[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [stats, setStats] = useState({
        totalRequests: 0,
        failedRequests: 0,
        activeAgents: 0,
        uptime: 0,
    });

    const refetch = () => { setError(null); setLoading(true); };

    useEffect(() => {
        async function loadSecurityData() {
            try {
                setLoading(true);
                // Total requests
                const { count: totalRequests } = await supabase
                    .from('requests')
                    .select('*', { count: 'exact', head: true });

                // Failed requests
                const { count: failedRequests } = await supabase
                    .from('requests')
                    .select('*', { count: 'exact', head: true })
                    .eq('status', 'failed');

                // Active agents
                const { count: activeAgents } = await supabase
                    .from('agents')
                    .select('*', { count: 'exact', head: true })
                    .eq('status', 'active');

                const total = totalRequests || 0;
                const failed = failedRequests || 0;
                const uptimePercent = total > 0
                    ? Math.round(((total - failed) / total) * 1000) / 10
                    : 0;

                setStats({
                    totalRequests: total,
                    failedRequests: failed,
                    activeAgents: activeAgents || 0,
                    uptime: uptimePercent,
                });

                setThreatsBlocked(failed);

                // Calcular integridade
                const integrityScore = totalRequests && totalRequests > 0 
                    ? Math.round(((totalRequests - (failedRequests || 0)) / totalRequests) * 100)
                    : 100;
                setIntegrity(integrityScore);

                // Auto-definir DEFCON baseado em métricas
                const failRate = failedRequests && totalRequests ? (failedRequests / totalRequests) * 100 : 0;
                if (failRate > 20) setDefcon(2);
                else if (failRate > 10) setDefcon(3);
                else if (failRate > 5) setDefcon(4);
                else setDefcon(5);

            } catch (err) {
                console.error('Failed to load security data:', err);
                setError('Erro ao carregar dados de segurança');
            } finally {
                setLoading(false);
            }
        }

        loadSecurityData();
        const interval = setInterval(loadSecurityData, 30000);
        return () => clearInterval(interval);
    }, []);

    // ENGINE VISUAL (FORCE FIELD 3D)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        
        const points: {x: number, y: number, z: number}[] = [];
        const SPHERE_OPACITY = 200;
        
        for(let i=0; i<SPHERE_OPACITY; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);
            const r = 150;
            points.push({
                x: r * Math.sin(phi) * Math.cos(theta),
                y: r * Math.sin(phi) * Math.sin(theta),
                z: r * Math.cos(phi)
            });
        }

        const attacks: {x: number, y: number, z: number, speed: number, active: boolean}[] = [];

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        const styles = getComputedStyle(document.documentElement);
        const textColor = styles.getPropertyValue('--color-text').trim() || '#FFFFFF';
        const canvasErrorColor = styles.getPropertyValue('--color-error').trim() || '#EF4444';

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            const currentDefcon = DEFCON_LEVELS.find(d => d.lvl === defcon) || DEFCON_LEVELS[0];
            const shieldColor = isLockdown ? textColor : currentDefcon.color;

            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            const angleY = time * (0.2 + (6 - defcon) * 0.1);
            const sinY = Math.sin(angleY);
            const cosY = Math.cos(angleY);

            points.forEach(p => {
                const x1 = p.x * cosY - p.z * sinY;
                const z1 = p.z * cosY + p.x * sinY;

                const scale = 400 / (400 + z1);
                const px = cx + x1 * scale;
                const py = cy + p.y * scale;

                const alpha = (z1 + 150) / 300;
                if (alpha > 0) {
                    ctx.beginPath();
                    ctx.fillStyle = shieldColor;
                    ctx.globalAlpha = alpha * (integrity/100);
                    ctx.arc(px, py, scale * 1.5, 0, Math.PI * 2);
                    ctx.fill();
                    
                    if (Math.random() > 0.95) {
                        ctx.beginPath();
                        ctx.strokeStyle = shieldColor;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(px, py);
                        ctx.lineTo(cx + (x1 + Math.random()*20) * scale, cy + (p.y + Math.random()*20) * scale);
                        ctx.stroke();
                    }
                }
            });
            ctx.globalAlpha = 1;

            // Simular ataques
            if (Math.random() > (defcon * 0.15) && !isLockdown) {
                const theta = Math.random() * Math.PI * 2;
                const r = 400;
                attacks.push({
                    x: r * Math.cos(theta),
                    y: (Math.random() - 0.5) * 200,
                    z: r * Math.sin(theta),
                    speed: 2 + Math.random() * 3,
                    active: true
                });
            }

            attacks.forEach((att) => {
                if (!att.active) return;

                const dist = Math.sqrt(att.x*att.x + att.y*att.y + att.z*att.z);
                const dx = -att.x / dist;
                const dy = -att.y / dist;
                const dz = -att.z / dist;

                att.x += dx * att.speed;
                att.y += dy * att.speed;
                att.z += dz * att.speed;

                if (dist < 160) {
                    att.active = false;
                    ctx.beginPath();
                    ctx.strokeStyle = textColor;
                    ctx.lineWidth = 2;
                    ctx.arc(cx + att.x, cy + att.y, 10, 0, Math.PI * 2);
                    ctx.stroke();
                }

                const scale = 400 / (400 + att.z);
                const px = cx + att.x * scale;
                const py = cy + att.y * scale;

                ctx.beginPath();
                ctx.fillStyle = canvasErrorColor;
                ctx.arc(px, py, 3 * scale, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.beginPath();
                ctx.strokeStyle = canvasErrorColor;
                ctx.lineWidth = 1;
                ctx.moveTo(px, py);
                ctx.lineTo(px - dx*20*scale, py - dy*20*scale);
                ctx.stroke();
            });

            requestAnimationFrame(render);
        };

        render();

        return () => window.removeEventListener('resize', resize);
    }, [defcon, isLockdown, integrity]);

    // Gerador de eventos de segurança
    useEffect(() => {
        const threats = ['SQL Injection', 'DDoS Packet', 'XSS Attempt', 'Brute Force', 'Malware Signature', 'Port Scan', 'Auth Bypass'];
        
        const interval = setInterval(() => {
            if (Math.random() > 0.7) {
                const newEvent: SecurityEvent = {
                    id: Date.now().toString(),
                    type: Math.random() > 0.9 ? 'warning' : 'blocked',
                    source: `${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.X`,
                    message: threats[Math.floor(Math.random() * threats.length)],
                    timestamp: new Date().toLocaleTimeString(),
                };
                setEvents(prev => [newEvent, ...prev].slice(0, 6));
                setThreatsBlocked(prev => prev + 1);
            }
        }, 2000);
        
        return () => clearInterval(interval);
    }, []);

    const currentDefcon = DEFCON_LEVELS.find(d => d.lvl === defcon) || DEFCON_LEVELS[0];

    if (loading) return <LoadingState message="Inicializando protocolos de segurança..." />;
    if (error) return <ErrorState message={error} onRetry={refetch} />;

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">

            {/* ESQUERDA: PAINEL DE CONTROLE */}
            <div className="lg:w-1/3 w-full flex flex-col gap-4 relative z-10">
                
                {/* DEFCON STATUS */}
                <div className="bg-background/60 backdrop-blur-xl border border-border/10 rounded-2xl p-6 shadow-2xl">
                    <div className="flex items-center gap-3 mb-6">
                        <ShieldAlert className="w-6 h-6" style={{ color: currentDefcon.color }} />
                        <div>
                            <h2 className="text-xl font-bold text-text tracking-tight">THREAT LEVEL</h2>
                            <p className="text-xs text-textSecondary font-mono">Global Security Protocol</p>
                        </div>
                    </div>

                    <div className="space-y-3">
                        {DEFCON_LEVELS.map((level) => (
                            <button
                                key={level.lvl}
                                onClick={() => { setDefcon(level.lvl); setIsLockdown(false); }}
                                className={`w-full p-3 rounded-lg border flex items-center justify-between transition-all duration-300 ${
                                    defcon === level.lvl 
                                    ? 'scale-105' 
                                    : 'bg-transparent border-border/5 text-textSecondary hover:bg-surface/5'
                                }`}
                                style={{ 
                                    borderColor: defcon === level.lvl ? level.color : '',
                                    backgroundColor: defcon === level.lvl ? `${level.color}20` : ''
                                }}
                            >
                                <div className="flex items-center gap-3">
                                    <span className={`font-black text-lg ${defcon === level.lvl ? 'text-text' : ''}`}>
                                        {level.lvl}
                                    </span>
                                    <span className={`text-xs font-bold tracking-widest ${defcon === level.lvl ? 'text-text' : ''}`}>
                                        {level.label}
                                    </span>
                                </div>
                                {defcon === level.lvl && <div className="w-2 h-2 rounded-full animate-pulse" style={{background: level.color}} />}
                            </button>
                        ))}
                    </div>
                    
                    <div className="mt-6 pt-4 border-t border-border/10">
                        <p className="text-xs text-textSecondary font-mono leading-relaxed">
                            STATUS: <span style={{color: currentDefcon.color}}>{currentDefcon.desc}</span>
                        </p>
                    </div>
                </div>

                {/* STATS */}
                <div className="grid grid-cols-2 gap-3">
                    <div className="bg-background/60 backdrop-blur-xl border border-border/10 rounded-xl p-4 text-center">
                        <CheckCircle className="w-5 h-5 mx-auto mb-2" style={{ color: 'var(--color-success)' }} />
                        <div className="text-xl font-black text-text">{stats.totalRequests}</div>
                        <div className="text-[9px] text-textSecondary uppercase">Total Requests</div>
                    </div>
                    <div className="bg-background/60 backdrop-blur-xl border border-border/10 rounded-xl p-4 text-center">
                        <XOctagon className="w-5 h-5 mx-auto mb-2" style={{ color: 'var(--color-error)' }} />
                        <div className="text-xl font-black text-text">{stats.failedRequests}</div>
                        <div className="text-[9px] text-textSecondary uppercase">Failed</div>
                    </div>
                </div>

                {/* LOCKDOWN */}
                <button 
                    onClick={() => setIsLockdown(!isLockdown)}
                    className={`group relative overflow-hidden rounded-2xl p-6 border transition-all duration-500 flex items-center justify-center gap-4 ${
                        isLockdown 
                        ? 'bg-[var(--color-error)] border-[var(--color-error)] shadow-[0_0_50px_var(--color-error)/50]' 
                        : 'bg-background/40 border-border/10 hover:border-border/30'
                    }`}
                >
                    {isLockdown ? <Lock className="w-8 h-8 text-text animate-bounce" /> : <Unlock className="w-8 h-8 text-textSecondary group-hover:text-text" />}
                    <div className="text-left">
                        <h3 className={`text-lg font-black tracking-widest ${isLockdown ? 'text-text' : 'text-textSecondary group-hover:text-text'}`}>
                            {isLockdown ? 'SYSTEM LOCKDOWN' : 'INITIATE LOCKDOWN'}
                        </h3>
                        <p className={`text-xs font-mono ${isLockdown ? 'text-text/80' : 'text-textSecondary'}`}>
                            {isLockdown ? 'ALL EXTERNAL CONNECTIONS SEVERED' : 'Emergency Protocol Override'}
                        </p>
                    </div>
                </button>

            </div>

            {/* DIREITA: VISUALIZAÇÃO DO ESCUDO */}
            <div className="flex-1 relative bg-background rounded-3xl border border-border/10 overflow-hidden shadow-2xl group">
                
                {/* Stats Overlay */}
                <div className="absolute top-6 left-6 z-20 flex gap-6">
                    <div>
                        <div className="text-[10px] text-textSecondary font-mono uppercase mb-1">Shield Integrity</div>
                        <div className="text-2xl font-mono text-text flex items-center gap-2">
                            {integrity.toFixed(1)}%
                            <div className="h-2 w-24 bg-surface rounded-full overflow-hidden ml-2">
                                <div 
                                    className="h-full transition-all duration-300"
                                    style={{ 
                                        width: `${integrity}%`,
                                        backgroundColor: integrity > 70 ? 'var(--color-success)' : integrity > 40 ? 'var(--color-warning)' : 'var(--color-error)'
                                    }}
                                />
                            </div>
                        </div>
                    </div>
                    <div>
                        <div className="text-[10px] text-textSecondary font-mono uppercase mb-1">Threats Blocked</div>
                        <div className="text-2xl font-mono" style={{ color: 'var(--color-success)' }}>{threatsBlocked.toLocaleString()}</div>
                    </div>
                </div>

                {/* Events Overlay */}
                <div className="absolute bottom-6 right-6 z-20 w-80">
                    <div className="space-y-2">
                        {events.map((event) => (
                            <div key={event.id} className="bg-background/60 backdrop-blur border border-border/10 p-2 rounded flex items-center gap-2 text-xs font-mono animate-fadeIn">
                                {event.type === 'blocked' ? (
                                    <XOctagon className="w-3 h-3" style={{ color: 'var(--color-error)' }} />
                                ) : (
                                    <AlertTriangle className="w-3 h-3" style={{ color: 'var(--color-warning)' }} />
                                )}
                                <span className="text-textSecondary">[{event.type.toUpperCase()}] {event.message} from {event.source}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />
                
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-background/80 pointer-events-none" />
                
                {/* Warning Flash */}
                <div 
                    className="absolute inset-0 pointer-events-none transition-opacity duration-100"
                    style={{ background: 'var(--color-error)/20', opacity: (defcon <= 2 || isLockdown) ? (Math.sin(Date.now()/200) > 0 ? 0.2 : 0) : 0 }}
                />
            </div>

            <style jsx>{`
                .animate-fadeIn { animation: fadeIn 0.2s ease-out; }
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            `}</style>
        </div>
    );
}
