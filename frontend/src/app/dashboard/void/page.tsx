/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THE VOID (EVENT HORIZON EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/void/page.tsx
 * 📋 Visualização de Buraco Negro (Logs do Sistema)
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Eye, AlertTriangle, ShieldAlert, Database, XCircle, Trash2 } from 'lucide-react';

// Tipos
interface VoidLog {
    id: number;
    source: string;
    message: string;
    integrity: number; // 0-100
    timestamp: string;
}

export default function VoidPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [logs, setLogs] = useState<VoidLog[]>([]);
    const [hoveredLog, setHoveredLog] = useState<number | null>(null);

    // 1. GERADOR DE LOGS (WHISPERS FROM THE VOID)
    useEffect(() => {
        const sources = ['KERNEL_PANIC', 'DELETED_MEM', 'GHOST_PROCESS', 'NULL_POINTER', 'VOID_SIGNAL'];
        const messages = [
            'Tentativa de acesso não autorizado no Setor 7',
            'Fragmento de memória perdido na singularidade',
            'Eco detectado na rede neural profunda',
            'Conexão encerrada abruptamente pelo host',
            'Sobrecarga de entropia detectada',
            'O sistema está observando você...',
        ];

        const interval = setInterval(() => {
            const newLog: VoidLog = {
                id: Date.now(),
                source: sources[Math.floor(Math.random() * sources.length)],
                message: messages[Math.floor(Math.random() * messages.length)],
                integrity: Math.floor(Math.random() * 100),
                timestamp: new Date().toLocaleTimeString()
            };
            setLogs(prev => [newLog, ...prev].slice(0, 8)); // Manter apenas os 8 últimos visíveis
        }, 3000);

        return () => clearInterval(interval);
    }, []);

    // 2. ENGINE DO BURACO NEGRO (PHYSICS)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        // Configuração das Partículas (Disco de Acreção)
        const particles: { angle: number, radius: number, speed: number, size: number, colorOffset: number }[] = [];
        const PARTICLE_COUNT = 800;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        // Inicializar
        for(let i=0; i<PARTICLE_COUNT; i++) {
            particles.push({
                angle: Math.random() * Math.PI * 2,
                radius: 100 + Math.random() * 400, // Distância do centro
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

            // Limpar com rastro longo (Motion Blur pesado)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01;

            // Pegar cor do tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#8B5CF6'; // Roxo padrão pro Void

            // Desenhar Partículas
            particles.forEach(p => {
                // Física Orbital: Quanto mais perto do centro, mais rápido
                p.angle += p.speed * (500 / p.radius); 
                
                // Espiral da Morte: Partículas caem lentamente para o centro
                p.radius -= 0.2; 
                
                // Reset se cair no buraco negro (< 50px)
                if(p.radius < 50) {
                    p.radius = 400 + Math.random() * 100;
                    p.size = Math.random() * 2;
                }

                // Perspectiva 3D simulada (Inclinação do disco)
                const x = cx + Math.cos(p.angle) * p.radius;
                const y = cy + Math.sin(p.angle) * (p.radius * 0.4); // Achatamento vertical

                // Efeito Doppler de Cor e Tamanho
                // Partículas "atrás" são mais escuras/menores
                const isFront = Math.sin(p.angle) > 0;
                const depthScale = isFront ? 1.2 : 0.8;
                
                ctx.beginPath();
                ctx.arc(x, y, p.size * depthScale, 0, Math.PI * 2);
                
                // Cor dinâmica
                const opacity = (p.radius - 50) / 400; // Some nas bordas
                ctx.fillStyle = themeColor;
                ctx.globalAlpha = opacity * (isFront ? 1 : 0.3);
                
                ctx.fill();
            });
            ctx.globalAlpha = 1;

            // O BURACO NEGRO (Event Horizon)
            // Glow externo
            const glow = ctx.createRadialGradient(cx, cy, 40, cx, cy, 120);
            glow.addColorStop(0, '#000000');
            glow.addColorStop(0.5, themeColor + '66'); // 40% opacity
            glow.addColorStop(1, 'transparent');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(cx, cy, 120, 0, Math.PI * 2);
            ctx.fill();

            // Núcleo Preto Absoluto
            ctx.fillStyle = '#000000';
            ctx.beginPath();
            ctx.arc(cx, cy, 48, 0, Math.PI * 2); // Um pouco menor que o glow
            ctx.fill();
            
            // Anel de Fótons (Borda branca brilhante)
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(cx, cy, 50, 0, Math.PI * 2);
            ctx.stroke();

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);

    return (
        <div className="relative h-[calc(100vh-6rem)] w-full overflow-hidden rounded-3xl border border-white/5 bg-black group">

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

            {/* CANVAS (BACKGROUND) */}
            <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />

            {/* UI: HEADER CENTRAL */}
            <div className="absolute top-10 left-1/2 -translate-x-1/2 text-center pointer-events-none z-10">
                <h1 className="text-4xl font-black text-white tracking-[0.5em] mb-2 font-display opacity-80">THE VOID</h1>
                <p className="text-xs font-mono text-[var(--color-primary)] uppercase tracking-widest">
                    System Entropy Monitor • Event Horizon Active
                </p>
            </div>

            {/* UI: LOGS FLUTUANTES (DIREITA) */}
            <div className="absolute right-0 top-0 bottom-0 w-full md:w-96 p-6 flex flex-col justify-center pointer-events-none">
                <div className="space-y-4 pointer-events-auto">
                    {logs.map((log, index) => (
                        <div 
                            key={log.id}
                            onMouseEnter={() => setHoveredLog(log.id)}
                            onMouseLeave={() => setHoveredLog(null)}
                            className={`
                                relative p-4 rounded-xl border backdrop-blur-md transition-all duration-500 ease-out
                                ${hoveredLog === log.id 
                                    ? 'bg-[var(--color-primary)]/10 border-[var(--color-primary)] translate-x-[-10px]' 
                                    : 'bg-black/40 border-white/5 translate-x-0 hover:bg-white/5'
                                }
                            `}
                            style={{
                                opacity: 1 - (index * 0.15), // Fade out os mais antigos
                                transform: `scale(${1 - index * 0.05}) translateX(${index * 10}px)`
                            }}
                        >
                            <div className="flex justify-between items-start mb-1">
                                <div className="flex items-center gap-2">
                                    {log.integrity < 50 ? <AlertTriangle className="w-4 h-4 text-red-500" /> : <Database className="w-4 h-4 text-[var(--color-primary)]" />}
                                    <span className="text-[10px] font-mono text-gray-400 uppercase tracking-wider">{log.source}</span>
                                </div>
                                <span className="text-[10px] text-gray-600 font-mono">{log.timestamp}</span>
                            </div>
                            <p className="text-sm text-gray-200 font-light leading-snug">{log.message}</p>
                            
                            {/* Barra de Integridade */}
                            <div className="mt-3 h-1 w-full bg-black/50 rounded-full overflow-hidden">
                                <div 
                                    className={`h-full ${log.integrity < 30 ? 'bg-red-500' : 'bg-[var(--color-primary)]'}`} 
                                    style={{ width: `${log.integrity}%` }} 
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* UI: CONTROLES INFERIORES */}
            <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex gap-4 z-10">
                <button className="flex items-center gap-2 px-6 py-3 bg-red-900/20 border border-red-500/30 text-red-400 rounded-full hover:bg-red-500 hover:text-white transition-all uppercase text-xs font-bold tracking-widest backdrop-blur-md group">
                    <Trash2 className="w-4 h-4" />
                    <span>Purge Memory</span>
                </button>
                <button className="flex items-center gap-2 px-6 py-3 bg-white/5 border border-white/10 text-white rounded-full hover:bg-white/10 transition-all uppercase text-xs font-bold tracking-widest backdrop-blur-md">
                    <Eye className="w-4 h-4" />
                    <span>Deep Scan</span>
                </button>
            </div>

            {/* Efeito Vignette Estático */}
            <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black pointer-events-none" />
        </div>
    );
}
