/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - LANDING PAGE (THE GATEWAY)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/page.tsx
 * 📋 Portal de entrada cinemático com efeito Warp Speed interativo
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowRight, Zap, Hexagon, Circle } from 'lucide-react';

export default function LandingPage() {
    const router = useRouter();
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [isEntering, setIsEntering] = useState(false);
    const [mouseSpeed, setMouseSpeed] = useState(0);
    const lastMousePos = useRef({ x: 0, y: 0, time: 0 });

    // 1. ENGINE VISUAL (WARP TUNNEL)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let speed = 2; // Velocidade base
        
        // Estrelas do Túnel
        const stars: {x: number, y: number, z: number, angle: number}[] = [];
        const STAR_COUNT = 800;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        // Inicializar
        for(let i=0; i<STAR_COUNT; i++) {
            stars.push({
                x: (Math.random() - 0.5) * canvas.width,
                y: (Math.random() - 0.5) * canvas.height,
                z: Math.random() * 1000, // Profundidade
                angle: Math.atan2((Math.random() - 0.5) * canvas.height, (Math.random() - 0.5) * canvas.width)
            });
        }

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            // Target Speed (baseado no mouse ou entrada)
            const targetSpeed = isEntering ? 50 : 2 + (mouseSpeed * 0.5);
            speed += (targetSpeed - speed) * 0.05; // Suavização (Lerp)

            // Limpar com rastro (Motion Blur)
            ctx.fillStyle = `rgba(0, 0, 0, ${isEntering ? 0.1 : 0.4})`;
            ctx.fillRect(0, 0, w, h);

            // Desenhar Estrelas
            ctx.fillStyle = '#FFFFFF';
            stars.forEach(star => {
                star.z -= speed;

                // Reset se passar da tela
                if (star.z <= 0) {
                    star.z = 1000;
                    star.x = (Math.random() - 0.5) * w;
                    star.y = (Math.random() - 0.5) * h;
                }

                // Perspectiva
                const scale = 500 / (500 + star.z);
                const x = cx + star.x / (star.z * 0.001);
                const y = cy + star.y / (star.z * 0.001);

                // Tamanho e Brilho
                const size = (1 - star.z / 1000) * 4;
                const alpha = (1 - star.z / 1000);

                if (isEntering || speed > 10) {
                    // Modo Warp (Linhas)
                    const prevScale = 500 / (500 + star.z + speed * 2);
                    const prevX = cx + star.x / ((star.z + speed) * 0.001);
                    const prevY = cy + star.y / ((star.z + speed) * 0.001);

                    ctx.strokeStyle = `rgba(0, 255, 208, ${alpha})`; // Ciano
                    ctx.lineWidth = size;
                    ctx.beginPath();
                    ctx.moveTo(prevX, prevY);
                    ctx.lineTo(x, y);
                    ctx.stroke();
                } else {
                    // Modo Standby (Pontos)
                    ctx.globalAlpha = alpha;
                    ctx.beginPath();
                    ctx.arc(x, y, size, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.globalAlpha = 1;
                }
            });

            // Se entrando, flash branco no final
            if (isEntering && speed > 40) {
                ctx.fillStyle = `rgba(255, 255, 255, ${(speed - 40) / 10})`;
                ctx.fillRect(0, 0, w, h);
            }

            animationId = requestAnimationFrame(render);
        };

        render();
        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [isEntering, mouseSpeed]);

    // 2. DETECTAR VELOCIDADE DO MOUSE
    const handleMouseMove = (e: React.MouseEvent) => {
        const now = Date.now();
        const dt = now - lastMousePos.current.time;
        if (dt > 50) {
            const dx = e.clientX - lastMousePos.current.x;
            const dy = e.clientY - lastMousePos.current.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            setMouseSpeed(Math.min(50, dist)); // Cap na velocidade
            
            lastMousePos.current = { x: e.clientX, y: e.clientY, time: now };
        }
    };

    // 3. AÇÃO DE ENTRADA
    const handleEnter = () => {
        setIsEntering(true);
        setTimeout(() => {
            router.push('/login');
        }, 1500); // Tempo da transição
    };

    return (
        <div 
            className="min-h-screen w-full relative overflow-hidden bg-black cursor-none" 
            onMouseMove={handleMouseMove}
        >
            {/* CANVAS */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />

            {/* CONTEÚDO CENTRAL */}
            <div className={`relative z-10 h-screen flex flex-col items-center justify-center transition-opacity duration-500 ${isEntering ? 'opacity-0' : 'opacity-100'}`}>
                
                {/* Logo Hero */}
                <div className="text-center mb-12 space-y-4 cursor-default">
                    <div className="flex items-center justify-center gap-3 mb-6 animate-fadeInDown">
                        <Hexagon className="w-8 h-8 text-[var(--color-primary)] animate-spin-slow" />
                        <span className="text-sm font-mono text-[var(--color-primary)] tracking-[0.5em] uppercase">
                            System Online
                        </span>
                    </div>
                    
                    <h1 className="text-6xl md:text-9xl font-black text-white tracking-tighter font-display mix-blend-difference animate-scaleIn">
                        ALSHAM
                        <span className="block text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-600">QUANTUM</span>
                    </h1>
                    
                    <p className="text-gray-400 max-w-md mx-auto font-light text-sm md:text-base tracking-wide leading-relaxed animate-fadeInUp">
                        A convergência final entre inteligência artificial e controle operacional. 
                        Bem-vindo à Singularidade.
                    </p>
                </div>

                {/* Botão de Entrada (Magnetic) */}
                <button 
                    onClick={handleEnter}
                    className="group relative px-12 py-6 bg-transparent overflow-hidden rounded-full transition-all hover:scale-105"
                >
                    <div className="absolute inset-0 border border-white/20 rounded-full group-hover:border-[var(--color-primary)] transition-colors duration-500" />
                    <div className="absolute inset-0 bg-white/5 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl" />
                    
                    <span className="relative z-10 flex items-center gap-4 text-sm font-bold tracking-[0.3em] text-white uppercase">
                        Enter The System
                        <ArrowRight className="w-4 h-4 group-hover:translate-x-2 transition-transform duration-300" />
                    </span>
                </button>

            </div>

            {/* RODAPÉ */}
            <div className={`absolute bottom-8 w-full text-center transition-opacity duration-500 ${isEntering ? 'opacity-0' : 'opacity-100'}`}>
                <div className="flex justify-center gap-8 text-[10px] text-gray-600 font-mono uppercase tracking-widest">
                    <span className="flex items-center gap-2">
                        <Circle className="w-2 h-2 text-green-500 fill-green-500 animate-pulse" /> 
                        Neural Net Active
                    </span>
                    <span>v13.3.0 Stable</span>
                    <span>Latency: 12ms</span>
                </div>
            </div>

            {/* CURSOR PERSONALIZADO (Seguidor) */}
            {!isEntering && (
                <div 
                    className="fixed pointer-events-none z-50 w-8 h-8 border border-[var(--color-primary)] rounded-full flex items-center justify-center mix-blend-difference transition-transform duration-75"
                    style={{ 
                        left: lastMousePos.current.x, 
                        top: lastMousePos.current.y,
                        transform: 'translate(-50%, -50%)'
                    }}
                >
                    <div className="w-1 h-1 bg-white rounded-full" />
                </div>
            )}

            <style jsx>{`
                .animate-spin-slow { animation: spin 10s linear infinite; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                
                @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
                .animate-fadeInDown { animation: fadeInDown 1s ease-out forwards; }

                @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
                .animate-fadeInUp { animation: fadeInUp 1s ease-out 0.5s forwards; opacity: 0; }

                @keyframes scaleIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
                .animate-scaleIn { animation: scaleIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards; opacity: 0; }
            `}</style>
        </div>
    );
}
