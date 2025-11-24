/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - CONTAINMENT (DIGITAL FORTRESS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/containment/page.tsx
 * 📋 Escudo de energia 3D, monitoramento de ameaças e DEFCON
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Shield, ShieldAlert, Lock, Unlock, AlertTriangle, Activity, XOctagon } from 'lucide-react';

// Níveis de Segurança
const DEFCON_LEVELS = [
    { lvl: 5, label: 'NORMAL', color: '#10B981', desc: 'Protocolos padrão ativos.' },
    { lvl: 4, label: 'ELEVATED', color: '#3B82F6', desc: 'Monitoramento aumentado.' },
    { lvl: 3, label: 'GUARDED', color: '#F59E0B', desc: 'Tráfego externo limitado.' },
    { lvl: 2, label: 'HIGH', color: '#EF4444', desc: 'Contramedidas letais ativas.' },
    { lvl: 1, label: 'MAXIMUM', color: '#7F1D1D', desc: 'LOCKDOWN TOTAL DO SISTEMA.' },
];

export default function ContainmentPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estados
    const [defcon, setDefcon] = useState(5); // 5 (Safe) a 1 (Critical)
    const [integrity, setIntegrity] = useState(100);
    const [threatsBlocked, setThreatsBlocked] = useState(8432);
    const [isLockdown, setIsLockdown] = useState(false);
    const [logs, setLogs] = useState<string[]>([]);

    // 1. ENGINE VISUAL (FORCE FIELD 3D)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        
        // Definição do Escudo (Esfera Geodésica simplificada)
        const points: {x: number, y: number, z: number}[] = [];
        const SPHERE_OPACITY = 200; // Quantos pontos
        
        for(let i=0; i<SPHERE_OPACITY; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);
            const r = 150; // Raio
            points.push({
                x: r * Math.sin(phi) * Math.cos(theta),
                y: r * Math.sin(phi) * Math.sin(theta),
                z: r * Math.cos(phi)
            });
        }

        // Partículas de Ataque
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

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            // Cor baseada no DEFCON
            const currentDefcon = DEFCON_LEVELS.find(d => d.lvl === defcon) || DEFCON_LEVELS[0];
            const shieldColor = isLockdown ? '#FFFFFF' : currentDefcon.color;

            // Limpar
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            // --- 1. DESENHAR ESCUDO (PONTOS GIRATÓRIOS) ---
            const angleY = time * (0.2 + (6 - defcon) * 0.1); // Gira mais rápido se perigo alto
            const sinY = Math.sin(angleY);
            const cosY = Math.cos(angleY);

            points.forEach(p => {
                // Rotação Y
                const x1 = p.x * cosY - p.z * sinY;
                const z1 = p.z * cosY + p.x * sinY;

                // Perspectiva
                const scale = 400 / (400 + z1);
                const px = cx + x1 * scale;
                const py = cy + p.y * scale;

                // Desenhar conexão (Mesh)
                // (Simplificado para performance: desenha pontos com glow)
                
                const alpha = (z1 + 150) / 300; // Fade atrás
                if (alpha > 0) {
                    ctx.beginPath();
                    ctx.fillStyle = shieldColor;
                    ctx.globalAlpha = alpha * (integrity/100);
                    ctx.arc(px, py, scale * 1.5, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Conectar com vizinhos próximos (Mesh Effect)
                    // (Custo de CPU alto, vamos simular com linhas aleatórias)
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

            // --- 2. SIMULAR ATAQUES ---
            // Gerar novos ataques
            if (Math.random() > (defcon * 0.1) && !isLockdown) { // Mais ataques se DEFCON baixo
                const theta = Math.random() * Math.PI * 2;
                const r = 400; // Longe
                attacks.push({
                    x: r * Math.cos(theta),
                    y: (Math.random() - 0.5) * 200,
                    z: r * Math.sin(theta),
                    speed: 2 + Math.random() * 3,
                    active: true
                });
            }

            // Desenhar Ataques
            attacks.forEach((att, i) => {
                if (!att.active) return;

                // Mover em direção ao centro (0,0,0)
                const dist = Math.sqrt(att.x*att.x + att.y*att.y + att.z*att.z);
                const dx = -att.x / dist;
                const dy = -att.y / dist;
                const dz = -att.z / dist;

                att.x += dx * att.speed;
                att.y += dy * att.speed;
                att.z += dz * att.speed;

                // Colisão com Escudo (Raio 150)
                if (dist < 160) {
                    att.active = false;
                    // Efeito de Impacto
                    ctx.beginPath();
                    ctx.strokeStyle = '#FFFFFF';
                    ctx.lineWidth = 2;
                    ctx.arc(cx + att.x, cy + att.y, 10, 0, Math.PI * 2);
                    ctx.stroke();
                    
                    // Atualizar stats visualmente (apenas trigger)
                    if (Math.random() > 0.5) {
                        // Hack para atualizar state fora do loop sem travar
                        // (Em prod, usar refs, mas aqui é visual)
                    }
                }

                // Desenhar Projetil
                const scale = 400 / (400 + att.z);
                const px = cx + att.x * scale;
                const py = cy + att.y * scale;

                ctx.beginPath();
                ctx.fillStyle = '#EF4444'; // Vermelho Ataque
                ctx.arc(px, py, 3 * scale, 0, Math.PI * 2);
                ctx.fill();
                
                // Rastro
                ctx.beginPath();
                ctx.strokeStyle = '#EF4444';
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

    // Simulador de Dados
    useEffect(() => {
        const interval = setInterval(() => {
            if (Math.random() > 0.7) {
                setThreatsBlocked(prev => prev + 1);
                const threats = ['SQL Injection', 'DDoS Packet', 'XSS Attempt', 'Brute Force', 'Malware Signature'];
                const threat = threats[Math.floor(Math.random() * threats.length)];
                const ip = `${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.X`;
                setLogs(prev => [`[BLOCKED] ${threat} from ${ip}`, ...prev].slice(0, 6));
                
                // Dano no escudo se DEFCON baixo
                if (defcon < 3 && !isLockdown) {
                    setIntegrity(prev => Math.max(0, prev - 0.1));
                } else {
                    setIntegrity(prev => Math.min(100, prev + 0.5)); // Regeneração
                }
            }
        }, 500);
        return () => clearInterval(interval);
    }, [defcon, isLockdown]);

    const currentDefcon = DEFCON_LEVELS.find(d => d.lvl === defcon) || DEFCON_LEVELS[0];

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* ESQUERDA: PAINEL DE CONTROLE */}
            <div className="lg:w-1/3 w-full flex flex-col gap-4 relative z-10">
                
                {/* Card: DEFCON STATUS */}
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl">
                    <div className="flex items-center gap-3 mb-6">
                        <ShieldAlert className="w-6 h-6" style={{ color: currentDefcon.color }} />
                        <div>
                            <h2 className="text-xl font-bold text-white tracking-tight">THREAT LEVEL</h2>
                            <p className="text-xs text-gray-400 font-mono">Global Security Protocol</p>
                        </div>
                    </div>

                    <div className="space-y-3">
                        {DEFCON_LEVELS.map((level) => (
                            <button
                                key={level.lvl}
                                onClick={() => { setDefcon(level.lvl); setIsLockdown(false); }}
                                className={`w-full p-3 rounded-lg border flex items-center justify-between transition-all duration-300 ${
                                    defcon === level.lvl 
                                    ? `bg-[${level.color}]/20 border-[${level.color}] scale-105` 
                                    : 'bg-transparent border-white/5 text-gray-500 hover:bg-white/5'
                                }`}
                                style={{ 
                                    borderColor: defcon === level.lvl ? level.color : '',
                                    backgroundColor: defcon === level.lvl ? `${level.color}20` : ''
                                }}
                            >
                                <div className="flex items-center gap-3">
                                    <span className={`font-black text-lg ${defcon === level.lvl ? 'text-white' : ''}`}>
                                        {level.lvl}
                                    </span>
                                    <span className={`text-xs font-bold tracking-widest ${defcon === level.lvl ? 'text-white' : ''}`}>
                                        {level.label}
                                    </span>
                                </div>
                                {defcon === level.lvl && <div className="w-2 h-2 rounded-full animate-pulse" style={{background: level.color}} />}
                            </button>
                        ))}
                    </div>
                    
                    <div className="mt-6 pt-4 border-t border-white/10">
                        <p className="text-xs text-gray-400 font-mono leading-relaxed">
                            STATUS: <span style={{color: currentDefcon.color}}>{currentDefcon.desc}</span>
                        </p>
                    </div>
                </div>

                {/* Card: LOCKDOWN SWITCH */}
                <button 
                    onClick={() => setIsLockdown(!isLockdown)}
                    className={`group relative overflow-hidden rounded-2xl p-6 border transition-all duration-500 flex items-center justify-center gap-4 ${
                        isLockdown 
                        ? 'bg-red-500 border-red-600 shadow-[0_0_50px_rgba(220,38,38,0.5)]' 
                        : 'bg-black/40 border-white/10 hover:border-white/30'
                    }`}
                >
                    {isLockdown ? <Lock className="w-8 h-8 text-white animate-bounce" /> : <Unlock className="w-8 h-8 text-gray-400 group-hover:text-white" />}
                    <div className="text-left">
                        <h3 className={`text-lg font-black tracking-widest ${isLockdown ? 'text-white' : 'text-gray-400 group-hover:text-white'}`}>
                            {isLockdown ? 'SYSTEM LOCKDOWN' : 'INITIATE LOCKDOWN'}
                        </h3>
                        <p className={`text-xs font-mono ${isLockdown ? 'text-white/80' : 'text-gray-600'}`}>
                            {isLockdown ? 'ALL EXTERNAL CONNECTIONS SEVERED' : 'Emergency Protocol Override'}
                        </p>
                    </div>
                    
                    {/* Background Warning Stripes */}
                    {isLockdown && (
                        <div className="absolute inset-0 opacity-10 bg-[url('/stripes.png')] animate-slideBg pointer-events-none" />
                    )}
                </button>

            </div>

            {/* DIREITA: VISUALIZAÇÃO DO ESCUDO */}
            <div className="flex-1 relative bg-[#02040a] rounded-3xl border border-white/10 overflow-hidden shadow-2xl group">
                
                {/* Stats Overlay */}
                <div className="absolute top-6 left-6 z-20 flex gap-6">
                    <div>
                        <div className="text-[10px] text-gray-500 font-mono uppercase mb-1">Shield Integrity</div>
                        <div className="text-2xl font-mono text-white flex items-center gap-2">
                            {integrity.toFixed(1)}%
                            <div className="h-2 w-24 bg-gray-800 rounded-full overflow-hidden ml-2">
                                <div 
                                    className="h-full transition-all duration-300"
                                    style={{ 
                                        width: `${integrity}%`,
                                        backgroundColor: integrity > 50 ? '#10B981' : integrity > 20 ? '#F59E0B' : '#EF4444'
                                    }}
                                />
                            </div>
                        </div>
                    </div>
                    <div>
                        <div className="text-[10px] text-gray-500 font-mono uppercase mb-1">Threats Blocked</div>
                        <div className="text-2xl font-mono text-[var(--color-primary)]">{threatsBlocked.toLocaleString()}</div>
                    </div>
                </div>

                {/* Logs Overlay (Bottom Right) */}
                <div className="absolute bottom-6 right-6 z-20 w-80">
                    <div className="space-y-2">
                        {logs.map((log, i) => (
                            <div key={i} className="bg-black/60 backdrop-blur border border-white/10 p-2 rounded flex items-center gap-2 text-xs font-mono animate-fadeIn">
                                <XOctagon className="w-3 h-3 text-red-500" />
                                <span className="text-gray-300">{log}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* CANVAS 3D */}
                <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />
                
                {/* Efeito Vignette & Grid */}
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/80 pointer-events-none" />
                
                {/* Warning Flash Overlay */}
                <div 
                    className="absolute inset-0 bg-red-500/20 pointer-events-none transition-opacity duration-100"
                    style={{ opacity: (defcon <= 2 || isLockdown) ? (Math.sin(Date.now()/200) > 0 ? 0.2 : 0) : 0 }}
                />
            </div>

            <style jsx>{`
                @keyframes slideBg { from { background-position: 0 0; } to { background-position: 50px 50px; } }
                .animate-slideBg { animation: slideBg 2s linear infinite; }
                .animate-fadeIn { animation: fadeIn 0.2s ease-out; }
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            `}</style>
        </div>
    );
}
