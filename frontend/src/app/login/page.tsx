/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - LOGIN (QUANTUM GATEWAY V2)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/login/page.tsx
 * 📋 Autenticação REAL com Supabase + Social Login (Google/GitHub)
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import Link from 'next/link';
import {
    Fingerprint, Scan, ShieldCheck, AlertOctagon, Lock, Key,
    Mail, Sparkles, Github, Chrome
} from 'lucide-react';

export default function LoginPage() {
    const { signIn, loading, error: authError } = useAuth();
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estados
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState<'idle' | 'scanning' | 'success' | 'denied'>('idle');
    const [scanProgress, setScanProgress] = useState(0);
    const [errorMessage, setErrorMessage] = useState('');
    
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

    // AUTENTICAÇÃO EMAIL/PASSWORD (REAL)
    const handleEmailLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!email || !password || loading) return;

        setStatus('scanning');
        setErrorMessage('');

        // Animação de progresso
        let p = 0;
        const interval = setInterval(() => {
            p += 4;
            setScanProgress(p);
            if (p >= 100) clearInterval(interval);
        }, 30);

        try {
            // AUTENTICAÇÃO REAL COM SUPABASE
            const { ok, error: signInError } = await signIn(email, password);

            clearInterval(interval);
            setScanProgress(100);

            if (!ok || signInError) {
                setStatus('denied');
                setErrorMessage(signInError?.message || 'Authentication failed');
                setTimeout(() => {
                    setStatus('idle');
                    setScanProgress(0);
                }, 2000);
            } else {
                setStatus('success');
                // Router.push já é chamado dentro do signIn
            }
        } catch (err: any) {
            clearInterval(interval);
            setStatus('denied');
            setErrorMessage('Connection error. Please try again.');
            setTimeout(() => {
                setStatus('idle');
                setScanProgress(0);
            }, 2000);
        }
    };

    // GOOGLE LOGIN
    const handleGoogleLogin = async () => {
        try {
            setStatus('scanning');
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: `${window.location.origin}/auth/callback`
                }
            });
            
            if (error) {
                setStatus('denied');
                setErrorMessage(error.message);
                setTimeout(() => setStatus('idle'), 2000);
            }
        } catch (err: any) {
            setStatus('denied');
            setErrorMessage('Google login failed');
            setTimeout(() => setStatus('idle'), 2000);
        }
    };

    // GITHUB LOGIN
    const handleGithubLogin = async () => {
        try {
            setStatus('scanning');
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: 'github',
                options: {
                    redirectTo: `${window.location.origin}/auth/callback`
                }
            });
            
            if (error) {
                setStatus('denied');
                setErrorMessage(error.message);
                setTimeout(() => setStatus('idle'), 2000);
            }
        } catch (err: any) {
            setStatus('denied');
            setErrorMessage('GitHub login failed');
            setTimeout(() => setStatus('idle'), 2000);
        }
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
            <div className="relative z-10 w-full max-w-md p-4">
                {/* Borda Brilhante Animada */}
                <div className={`absolute inset-0 rounded-3xl blur-md transition-all duration-500 ${
                    status === 'scanning' ? 'bg-[var(--color-primary)] opacity-50' : 
                    status === 'success' ? 'bg-green-500 opacity-80 scale-105' :
                    status === 'denied' ? 'bg-red-500 opacity-80 animate-shake' :
                    'bg-white/10 opacity-20'
                }`} />

                <div className="relative bg-black/80 backdrop-blur-2xl border border-white/10 rounded-3xl p-8 shadow-2xl overflow-hidden">
                    
                    {/* SCANNER CANVAS */}
                    <div className="flex justify-center mb-4 relative">
                        <div className="w-24 h-24 relative">
                            <canvas ref={canvasRef} className="w-full h-full" />
                            {/* Icon Overlay */}
                            <div className="absolute inset-0 flex items-center justify-center text-white/50">
                                {status === 'success' ? <ShieldCheck className="w-8 h-8 text-black z-10" /> : 
                                 status === 'denied' ? <AlertOctagon className="w-8 h-8 text-black z-10" /> :
                                 <Scan className="w-8 h-8 opacity-50" />}
                            </div>
                        </div>
                    </div>

                    {/* HEADER TEXT */}
                    <div className="text-center mb-6">
                        <h1 className="text-2xl font-black text-white tracking-tight font-display flex items-center justify-center gap-2">
                            ALSHAM <Sparkles className="w-4 h-4 text-[var(--color-primary)]" />
                        </h1>
                        <p className={`text-[10px] font-mono mt-1 tracking-[0.2em] uppercase transition-colors ${
                            status === 'success' ? 'text-green-400' : 
                            status === 'denied' ? 'text-red-400' : 
                            'text-gray-500'
                        }`}>
                            {status === 'idle' && 'Identity Verification Required'}
                            {status === 'scanning' && 'Processing Biometrics...'}
                            {status === 'success' && 'Access Granted. Welcome Architect.'}
                            {status === 'denied' && errorMessage}
                        </p>
                    </div>

                    {/* EMAIL FORM */}
                    <form onSubmit={handleEmailLogin} className="space-y-4 relative">
                        
                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Mail className="w-4 h-4" />
                            </div>
                            <input 
                                type="email" 
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Commander ID"
                                disabled={status !== 'idle'}
                                className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-600 focus:border-[var(--color-primary)] focus:bg-black transition-all outline-none font-mono text-sm"
                            />
                        </div>

                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Key className="w-4 h-4" />
                            </div>
                            <input 
                                type="password" 
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Access Code"
                                disabled={status !== 'idle'}
                                className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-600 focus:border-[var(--color-primary)] focus:bg-black transition-all outline-none font-mono text-sm tracking-widest"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={status !== 'idle' || loading}
                            className={`
                                w-full py-3 rounded-xl font-bold text-xs tracking-widest uppercase transition-all relative overflow-hidden group
                                ${status === 'success' ? 'bg-green-500 text-black' :
                                  status === 'denied' ? 'bg-red-500 text-white' :
                                  'bg-[var(--color-primary)] text-black hover:bg-[var(--color-accent)]'}
                            `}
                        >
                            <div className="relative z-10 flex items-center justify-center gap-2">
                                {status === 'idle' && <><Fingerprint className="w-4 h-4" /> AUTHENTICATE</>}
                                {(status === 'scanning' || loading) && 'SCANNING...'}
                                {status === 'success' && <><ShieldCheck className="w-4 h-4" /> GRANTED</>}
                                {status === 'denied' && <><Lock className="w-4 h-4" /> LOCKED</>}
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

                    {/* DIVIDER */}
                    <div className="my-6 flex items-center gap-4">
                        <div className="h-[1px] flex-1 bg-white/10" />
                        <span className="text-[10px] font-mono text-gray-600 uppercase">OR CONNECT WITH</span>
                        <div className="h-[1px] flex-1 bg-white/10" />
                    </div>

                    {/* SOCIAL BUTTONS */}
                    <div className="grid grid-cols-2 gap-4">
                        <button
                            onClick={handleGoogleLogin}
                            disabled={status !== 'idle' || loading}
                            className="flex items-center justify-center gap-2 py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/30 transition-all group"
                        >
                            <Chrome className="w-4 h-4 text-white group-hover:text-blue-400 transition-colors" />
                            <span className="text-xs font-bold text-gray-400 group-hover:text-white">GOOGLE</span>
                        </button>

                        <button
                            onClick={handleGithubLogin}
                            disabled={status !== 'idle' || loading}
                            className="flex items-center justify-center gap-2 py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/30 transition-all group"
                        >
                            <Github className="w-4 h-4 text-white group-hover:text-purple-400 transition-colors" />
                            <span className="text-xs font-bold text-gray-400 group-hover:text-white">GITHUB</span>
                        </button>
                    </div>

                    {(authError || errorMessage) && (
                        <p className="mt-4 text-sm text-red-400 text-center">
                            {errorMessage || authError}
                        </p>
                    )}

                    {/* Signup Link */}
                    <div className="mt-6 text-center">
                        <Link href="/signup" className="text-xs text-gray-500 hover:text-[var(--color-primary)] transition-colors font-mono">
                            Não tem conta? <span className="font-bold">Criar conta</span>
                        </Link>
                    </div>

                    {/* Footer Links */}
                    <div className="mt-6 flex justify-between text-[9px] text-gray-700 font-mono uppercase">
                        <button className="hover:text-white transition-colors">Reset Protocol</button>
                        <button className="hover:text-white transition-colors">Emergency Override</button>
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
