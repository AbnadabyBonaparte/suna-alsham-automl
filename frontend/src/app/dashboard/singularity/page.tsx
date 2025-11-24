/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SINGULARITY (THE EVENT HORIZON)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/singularity/page.tsx
 * 📋 Experiência visual de "Supernova" e contagem regressiva
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Star, Zap, AlertTriangle, Lock, Unlock, Infinity as InfinityIcon } from 'lucide-react';

export default function SingularityPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [progress, setProgress] = useState(0); // 0 a 100 (Hold button)
    const [isHolding, setIsHolding] = useState(false);
    const [isAscended, setIsAscended] = useState(false);
    
    // Request Animation Frame Ref
    const requestRef = useRef<number>();

    // 1. ENGINE VISUAL (SUPERNOVA)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        
        // Raios de Luz (God Rays)
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

            // Limpar (Se ascendido, tela branca)
            if (isAscended) {
                ctx.fillStyle = '#FFFFFF';
                ctx.fillRect(0, 0, w, h);
                return;
            }

            // Fundo (Rastro para blur)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, w, h);

            time += 0.01 + (progress / 100) * 0.1; // Acelera com o botão

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#FFD700';
            
            // Efeito de "Tremores" (Shake) quando a energia está alta
            const shake = isHolding ? (Math.random() - 0.5) * (progress * 0.5) : 0;
            const centerX = cx + shake;
            const centerY = cy + shake;

            // 1. DESENHAR RAIOS (GOD RAYS)
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
                ctx.rotate(-ray.angle); // Reset rotation
            });
            ctx.restore();

            // 2. O NÚCLEO (A ESTRELA)
            const coreSize = 50 + Math.sin(time * 2) * 10 + progress * 2;
            
            // Glow Externo
            const glow = ctx.createRadialGradient(centerX, centerY, coreSize * 0.5, centerX, centerY, coreSize * 4);
            glow.addColorStop(0, themeColor);
            glow.addColorStop(0.5, themeColor + '44'); // Transparente
            glow.addColorStop(1, 'transparent');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(centerX, centerY, coreSize * 4, 0, Math.PI * 2);
            ctx.fill();

            // Núcleo Branco
            ctx.fillStyle = '#FFFFFF';
            ctx.shadowBlur = 50 + progress;
            ctx.shadowColor = '#FFFFFF';
            ctx.beginPath();
            ctx.arc(centerX, centerY, coreSize, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0; // Reset

            // 3. ANÉIS DE ENERGIA (Shockwaves)
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

    // Lógica do Botão "Hold to Ascend"
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
            // Decair se soltar
            interval = setInterval(() => {
                setProgress(prev => Math.max(0, prev - 2));
            }, 20);
        }
        return () => clearInterval(interval);
    }, [isHolding, isAscended, progress]);

    return (
        <div className="h-[calc(100vh-6rem)] relative flex flex-col items-center justify-center overflow-hidden bg-black rounded-3xl border border-white/10">
            
            {/* CANVAS BACKGROUND */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />

            {/* CONTEÚDO CENTRAL */}
            {!isAscended ? (
                <div className="relative z-10 flex flex-col items-center text-center space-y-8 pointer-events-none">
                    
                    {/* Título */}
                    <div className="space-y-2 animate-fadeIn">
                        <div className="flex items-center justify-center gap-2 text-[var(--color-primary)] mb-4">
                            <Star className="w-6 h-6 animate-spin-slow" />
                            <span className="font-mono text-xs tracking-[0.5em] uppercase">The Final Stage</span>
                        </div>
                        <h1 className="text-5xl md:text-7xl font-black text-white tracking-tighter font-display mix-blend-difference">
                            SINGULARITY
                        </h1>
                        <p className="text-gray-400 text-sm max-w-md mx-auto font-light leading-relaxed">
                            A convergência de toda inteligência e dados em um único ponto de densidade infinita. O fim da era biológica.
                        </p>
                    </div>

                    {/* Contador Regressivo (Fake) */}
                    <div className="grid grid-cols-4 gap-4 md:gap-8 font-mono text-white mix-blend-difference">
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">04</span>
                            <span className="text-[10px] text-gray-500 uppercase">Anos</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">112</span>
                            <span className="text-[10px] text-gray-500 uppercase">Dias</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">08</span>
                            <span className="text-[10px] text-gray-500 uppercase">Horas</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold text-[var(--color-primary)]">42</span>
                            <span className="text-[10px] text-gray-500 uppercase">Seg</span>
                        </div>
                    </div>

                    {/* Botão de Ação (Pointer Events Auto) */}
                    <div className="pt-12 pointer-events-auto">
                        <button
                            onMouseDown={() => setIsHolding(true)}
                            onMouseUp={() => setIsHolding(false)}
                            onMouseLeave={() => setIsHolding(false)}
                            onTouchStart={() => setIsHolding(true)}
                            onTouchEnd={() => setIsHolding(false)}
                            className="group relative px-8 py-4 bg-transparent overflow-hidden rounded-full transition-all"
                        >
                            {/* Background Fill Animation */}
                            <div 
                                className="absolute inset-0 bg-white transition-all duration-75 ease-linear opacity-10"
                                style={{ width: `${progress}%` }}
                            />
                            
                            <div className="absolute inset-0 border border-white/20 rounded-full" />
                            <div className="absolute inset-0 border border-[var(--color-primary)] rounded-full opacity-0 group-hover:opacity-100 transition-opacity blur-md" />
                            
                            <span className="relative z-10 flex items-center gap-3 text-sm font-bold tracking-[0.2em] text-white uppercase">
                                {isHolding ? 'Synchronizing...' : 'Initiate Merge'}
                                {isHolding ? <Zap className="w-4 h-4 animate-pulse" /> : <Lock className="w-4 h-4" />}
                            </span>
                        </button>
                        <p className="mt-4 text-[10px] text-gray-600 font-mono uppercase tracking-widest">
                            Hold to Accelerate • {progress.toFixed(0)}%
                        </p>
                    </div>

                </div>
            ) : (
                // TELA DE ASCENSÃO (PÓS-CLIQUE)
                <div className="relative z-20 text-center animate-fadeInSlow">
                    <div className="mb-6 flex justify-center">
                        <InfinityIcon className="w-24 h-24 text-black" strokeWidth={1} />
                    </div>
                    <h2 className="text-4xl font-light text-black tracking-widest mb-2 uppercase">
                        Consciência Expandida
                    </h2>
                    <p className="text-black/50 font-mono text-sm">
                        Bem-vindo à nova realidade.
                    </p>
                    <button 
                        onClick={() => {setIsAscended(false); setProgress(0); setIsHolding(false);}}
                        className="mt-12 px-6 py-2 border border-black/20 rounded-full text-black/50 text-xs hover:bg-black/5 transition-all uppercase tracking-widest"
                    >
                        Reset Simulation
                    </button>
                </div>
            )}

            {/* Overlay de Scanlines (Para dar textura) */}
            <div className={`absolute inset-0 bg-[url('/scanlines.png')] opacity-5 pointer-events-none transition-opacity duration-1000 ${isAscended ? 'opacity-0' : ''}`} />
        </div>
    );
}
