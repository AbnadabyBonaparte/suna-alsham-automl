/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - 404 PAGE (REALITY FRACTURE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/not-found.tsx
 * 📋 Tela de erro com efeito Glitch e Ruído Digital
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { AlertTriangle, ArrowLeft, RefreshCw } from 'lucide-react';

export default function NotFound() {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // 1. ENGINE VISUAL (GLITCH NOISE)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;

            // Limpar
            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, w, h);

            time++;

            // 1. Static Noise (Chiado)
            const noiseData = ctx.createImageData(w, h);
            const buffer = new Uint32Array(noiseData.data.buffer);
            
            for(let i = 0; i < buffer.length; i++) {
                if (Math.random() < 0.05) { // 5% de pixels brancos/cinzas
                    const gray = Math.random() * 50;
                    // 0xFF000000 é Alpha (255)
                    // Little-endian: ABGR
                    buffer[i] = 0xFF000000 | (gray << 16) | (gray << 8) | gray; 
                }
            }
            ctx.putImageData(noiseData, 0, 0);

            // 2. Scanlines Horizontais
            ctx.fillStyle = 'rgba(0, 255, 208, 0.05)';
            for (let y = 0; y < h; y += 4) {
                ctx.fillRect(0, y, w, 1);
            }

            // 3. Glitch Bars (Faixas aleatórias)
            if (Math.random() > 0.9) {
                const barH = Math.random() * 100;
                const barY = Math.random() * h;
                ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
                ctx.fillRect(0, barY, w, barH);
                
                // Deslocamento cromático
                ctx.fillStyle = 'rgba(255, 0, 0, 0.2)';
                ctx.fillRect(5, barY, w, barH);
            }

            // 4. Texto "404" Desenhado no Canvas (Para glitch)
            ctx.font = 'bold 200px monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            const cx = w / 2;
            const cy = h / 2 - 50;

            // Sombra/Glitch do texto
            const offsetX = (Math.random() - 0.5) * 10;
            const offsetY = (Math.random() - 0.5) * 10;

            if (Math.random() > 0.8) {
                ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
                ctx.fillText('404', cx + offsetX + 5, cy + offsetY);
                ctx.fillStyle = 'rgba(0, 255, 255, 0.5)';
                ctx.fillText('404', cx - offsetX - 5, cy - offsetY);
            }

            ctx.fillStyle = '#FFFFFF';
            ctx.fillText('404', cx, cy);

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);

    return (
        <div className="relative min-h-screen w-full overflow-hidden flex flex-col items-center justify-center font-mono text-white">
            
            {/* CANVAS BACKGROUND */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0" />

            {/* CONTEÚDO (Sobreposto) */}
            <div className="relative z-10 text-center p-8 bg-black/60 backdrop-blur-md border border-red-500/30 rounded-3xl shadow-[0_0_50px_rgba(220,38,38,0.2)] animate-shake">
                
                <div className="flex justify-center mb-6">
                    <div className="p-4 rounded-full bg-red-500/10 border border-red-500/50 animate-pulse">
                        <AlertTriangle className="w-12 h-12 text-red-500" />
                    </div>
                </div>

                <h1 className="text-4xl font-black tracking-widest mb-2 text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-white">
                    REALITY FRACTURED
                </h1>
                
                <p className="text-gray-400 text-sm max-w-md mx-auto mb-8 leading-relaxed">
                    CRITICAL ERROR: SECTOR NOT FOUND. <br/>
                    The coordinates you provided do not exist in this timeline.
                </p>

                <div className="flex flex-col md:flex-row gap-4 justify-center">
                    <Link href="/dashboard">
                        <button className="group px-8 py-3 bg-white text-black font-bold rounded-full flex items-center gap-2 hover:bg-gray-200 transition-all hover:scale-105">
                            <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
                            RECONSTRUCT REALITY
                        </button>
                    </Link>
                    
                    <button 
                        onClick={() => window.history.back()}
                        className="px-8 py-3 border border-white/20 rounded-full text-white/70 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        ABORT JUMP
                    </button>
                </div>

                <div className="mt-8 pt-4 border-t border-white/10 text-[10px] text-red-500/50 uppercase tracking-[0.5em]">
                    Error Code: ID-10-T // Glitch Protocol Active
                </div>
            </div>

            <style jsx>{`
                @keyframes shake {
                    0%, 100% { transform: translate(0, 0) rotate(0deg); }
                    25% { transform: translate(-2px, 2px) rotate(-1deg); }
                    50% { transform: translate(2px, -2px) rotate(1deg); }
                    75% { transform: translate(-2px, -2px) rotate(-1deg); }
                }
                .animate-shake { animation: shake 5s infinite; }
            `}</style>
        </div>
    );
}
