/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - LOGIN (QUANTUM GATEWAY)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/login/page.tsx
 * 📋 Tela de autenticação com scanner biométrico e efeitos visuais
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Fingerprint, Scan, ShieldCheck, AlertOctagon, Lock, Key, Mail, Sparkles } from 'lucide-react';

export default function LoginPage() {
    const router = useRouter();
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estados
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState<'idle' | 'scanning' | 'success' | 'denied'>('idle');
    const [scanProgress, setScanProgress] = useState(0);
    
    // 1. ENGINE VISUAL (IRIS SCANNER)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        const resize = () => {
            canvas.width = 300;
            canvas.height = 300;
        };
        resize();

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            ctx.clearRect(0, 0, w, h);
            time += 0.05;

            // Cor do Tema (Baseada no Status)
            let color = '#00FFD0'; // Idle (Ciano)
            if (status === 'scanning') color = '#F59E0B'; // Scanning (Amarelo)
            if (status === 'success') color = '#10B981'; // Success (Verde)
            if (status === 'denied') color = '#EF4444'; // Denied (Vermelho)

            // 1. Anéis Giratórios (Íris)
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            
            // Anel Externo
            ctx.beginPath();
            ctx.arc(cx, cy, 80, time * 0.5, time * 0.5 + Math.PI * 1.5);
            ctx.stroke();

            // Anel Médio (Contrário)
            ctx.beginPath();
            ctx.arc(cx, cy, 60, -time, -time + Math.PI);
            ctx.stroke();

            // Anel Interno (Rápido)
            ctx.beginPath();
            ctx.arc(cx, cy, 40, time * 2, time * 2 + Math.PI * 0.5);
            ctx.stroke();

            // 2. Efeito de Scan (Laser)
            if (status === 'scanning' || status === 'idle') {
                const scanY = cy + Math.sin(time * 2) * 80;
                
                ctx.fillStyle = color;
                ctx.globalAlpha = 0.2;
                ctx.beginPath();
                ctx.fillRect(cx - 90, scanY, 180, 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }

            // 3. Núcleo (Pupila)
            ctx.fillStyle = color;
            ctx.shadowBlur = 20;
            ctx.shadowColor = color;
            ctx.beginPath();
            const pupilSize = status === 'success' ? 80 : 10 + Math.sin(time * 3) * 2;
            ctx.arc(cx, cy, pupilSize, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            animationId = requestAnimationFrame(render);
        };

        render();
        return () => cancelAnimationFrame(animationId);
    }, [status]);

    // Lógica de Login Simulado
    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        if (!email || !password) return;

        setStatus('scanning');
        
        // Simular progresso de scan
        let p = 0;
        const interval = setInterval(() => {
            p += 2;
            setScanProgress(p);
            if (p >= 100) {
                clearInterval(interval);
                
                // Verificação Fake
                if (password === '123' || password.length > 3) {
                    setStatus('success');
                    setTimeout(() => router.push('/dashboard'), 1000);
                } else {
                    setStatus('denied');
                    setTimeout(() => {
                        setStatus('idle');
                        setScanProgress(0);
                    }, 2000);
                }
            }
        }, 30);
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-black relative overflow-hidden">
            
            {/* BACKGROUND ANIMADO (GRID + PARTICLES) */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 animate-pulse" />
            <div className="absolute inset-0 bg-radial-gradient from-transparent via-black/80 to-black pointer-events-none" />
            
            {/* SCANNER VISUALIZER (ABSOLUTE CENTER BACKGROUND) */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-30 blur-3xl">
                <div className={`w-96 h-96 rounded-full transition-colors duration-1000 ${
                    status === 'success' ? 'bg-green-500' : 
                    status === 'denied' ? 'bg-red-500' : 
                    'bg-[var(--color-primary)]'
                }`} />
            </div>

            {/* LOGIN CARD (GLASSLITH) */}
            <div className="relative z-10 w-full max-w-md p-1">
                {/* Borda Brilhante Animada */}
                <div className={`absolute inset-0 rounded-3xl blur-md transition-all duration-500 ${
                    status === 'scanning' ? 'bg-[var(--color-primary)] opacity-50' : 
                    status === 'success' ? 'bg-green-500 opacity-80 scale-105' :
                    status === 'denied' ? 'bg-red-500 opacity-80 animate-shake' :
                    'bg-white/10 opacity-20'
                }`} />

                <div className="relative bg-black/80 backdrop-blur-2xl border border-white/10 rounded-3xl p-8 shadow-2xl overflow-hidden">
                    
                    {/* SCANNER CANVAS */}
                    <div className="flex justify-center mb-6 relative">
                        <div className="w-32 h-32 relative">
                            <canvas ref={canvasRef} className="w-full h-full" />
                            {/* Icon Overlay */}
                            <div className="absolute inset-0 flex items-center justify-center text-white/50">
                                {status === 'success' ? <ShieldCheck className="w-10 h-10 text-black z-10" /> : 
                                 status === 'denied' ? <AlertOctagon className="w-10 h-10 text-black z-10" /> :
                                 <Scan className="w-10 h-10 opacity-50" />}
                            </div>
                        </div>
                    </div>

                    {/* HEADER TEXT */}
                    <div className="text-center mb-8">
                        <h1 className="text-3xl font-black text-white tracking-tight font-display flex items-center justify-center gap-2">
                            ALSHAM <Sparkles className="w-4 h-4 text-[var(--color-primary)]" />
                        </h1>
                        <p className={`text-xs font-mono mt-2 tracking-[0.3em] uppercase transition-colors ${
                            status === 'success' ? 'text-green-400' : 
                            status === 'denied' ? 'text-red-400' : 
                            'text-gray-500'
                        }`}>
                            {status === 'idle' && 'Identity Verification Required'}
                            {status === 'scanning' && 'Biometric Scan in Progress...'}
                            {status === 'success' && 'Access Granted. Welcome Architect.'}
                            {status === 'denied' && 'Access Denied. Security Alert.'}
                        </p>
                    </div>

                    {/* FORM */}
                    <form onSubmit={handleLogin} className="space-y-6 relative">
                        
                        {/* Email Input */}
                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Mail className="w-5 h-5" />
                            </div>
                            <input 
                                type="email" 
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Commander ID"
                                disabled={status !== 'idle'}
                                className="w-full bg-white/5 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-white placeholder-gray-600 focus:border-[var(--color-primary)] focus:bg-black transition-all outline-none font-mono text-sm"
                            />
                        </div>

                        {/* Password Input */}
                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Key className="w-5 h-5" />
                            </div>
                            <input 
                                type="password" 
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Access Code"
                                disabled={status !== 'idle'}
                                className="w-full bg-white/5 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-white placeholder-gray-600 focus:border-[var(--color-primary)] focus:bg-black transition-all outline-none font-mono text-sm tracking-widest"
                            />
                        </div>

                        {/* SUBMIT BUTTON (FINGERPRINT) */}
                        <button 
                            type="submit"
                            disabled={status !== 'idle'}
                            className={`
                                w-full py-4 rounded-xl font-bold text-sm tracking-widest uppercase transition-all relative overflow-hidden group
                                ${status === 'success' ? 'bg-green-500 text-black' : 
                                  status === 'denied' ? 'bg-red-500 text-white' : 
                                  'bg-[var(--color-primary)] text-black hover:bg-[var(--color-accent)]'}
                            `}
                        >
                            <div className="relative z-10 flex items-center justify-center gap-2">
                                {status === 'idle' && <><Fingerprint className="w-5 h-5" /> AUTHENTICATE</>}
                                {status === 'scanning' && 'SCANNING...'}
                                {status === 'success' && <><ShieldCheck className="w-5 h-5" /> GRANTED</>}
                                {status === 'denied' && <><Lock className="w-5 h-5" /> LOCKED</>}
                            </div>

                            {/* Progress Bar Overlay */}
                            {status === 'scanning' && (
                                <div 
                                    className="absolute inset-0 bg-white/30 transition-all duration-100 ease-linear"
                                    style={{ width: `${scanProgress}%` }}
                                />
                            )}
                        </button>

                    </form>

                    {/* Footer Links */}
                    <div className="mt-8 flex justify-between text-[10px] text-gray-600 font-mono uppercase">
                        <button className="hover:text-white transition-colors">Recover Key</button>
                        <button className="hover:text-white transition-colors">Emergency Protocol</button>
                    </div>
                </div>
            </div>

            <style jsx>{`
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-5px); }
                    75% { transform: translateX(5px); }
                }
                .animate-shake { animation: shake 0.2s ease-in-out 0s 2; }
            `}</style>
        </div>
    );
}
