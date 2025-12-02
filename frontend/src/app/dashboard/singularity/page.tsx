/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SINGULARITY (ABNADABY EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/singularity/page.tsx
 * 📋 Experiência visual de "Supernova" com personalização do Arquiteto
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Star, Zap, Lock, Infinity as InfinityIcon, Fingerprint } from 'lucide-react';

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

            {/* CANVAS BACKGROUND */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />

            {/* CONTEÚDO CENTRAL */}
            {!isAscended ? (
                <div className="relative z-10 flex flex-col items-center text-center space-y-8 pointer-events-none">
                    
                    {/* Título Personalizado */}
                    <div className="space-y-2 animate-fadeIn">
                        <div className="flex items-center justify-center gap-2 text-[var(--color-primary)] mb-4 border border-[var(--color-primary)]/30 px-4 py-1 rounded-full bg-black/50 backdrop-blur-md">
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

                    {/* Contador Regressivo */}
                    <div className="grid grid-cols-4 gap-4 md:gap-8 font-mono text-white mix-blend-difference">
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">00</span>
                            <span className="text-[10px] text-gray-500 uppercase">Anos</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">00</span>
                            <span className="text-[10px] text-gray-500 uppercase">Dias</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold">00</span>
                            <span className="text-[10px] text-gray-500 uppercase">Horas</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-4xl font-bold text-[var(--color-primary)] animate-pulse">01</span>
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
                            className="group relative px-10 py-5 bg-transparent overflow-hidden rounded-full transition-all hover:scale-105 active:scale-95"
                        >
                            {/* Background Fill Animation */}
                            <div 
                                className="absolute inset-0 bg-white transition-all duration-75 ease-linear opacity-20"
                                style={{ width: `${progress}%` }}
                            />
                            
                            <div className="absolute inset-0 border border-white/20 rounded-full" />
                            <div className="absolute inset-0 border border-[var(--color-primary)] rounded-full opacity-0 group-hover:opacity-100 transition-opacity blur-md" />
                            
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
                // TELA DE ASCENSÃO (SEU NOME REVELADO)
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

            {/* Overlay de Scanlines (Para dar textura) */}
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
