/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SIGNUP (QUANTUM GATEWAY V2)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/signup/page.tsx
 * 📋 Cadastro REAL com Supabase + Social Login (Google/GitHub)
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/stores/useAuthStore';
import { supabase } from '@/lib/supabase';
import {
    Fingerprint, Scan, ShieldCheck, AlertOctagon, Lock, Key,
    Mail, Sparkles, Github, Chrome, UserPlus
} from 'lucide-react';
import Link from 'next/link';

export default function SignupPage() {
    const signUp = useAuthStore((s) => s.signUp);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Estados
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
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
            const style = getComputedStyle(document.documentElement);
            let color = style.getPropertyValue('--color-primary').trim() || '#00FFD0';
            if (status === 'scanning') color = style.getPropertyValue('--color-warning').trim() || '#F59E0B';
            if (status === 'success') color = style.getPropertyValue('--color-success').trim() || '#10B981';
            if (status === 'denied') color = style.getPropertyValue('--color-error').trim() || '#EF4444';

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

    // VALIDAÇÃO DE SENHA
    const validatePasswords = () => {
        if (password.length < 6) {
            setErrorMessage('Password must be at least 6 characters');
            return false;
        }
        if (password !== confirmPassword) {
            setErrorMessage('Passwords do not match');
            return false;
        }
        return true;
    };

    // AUTENTICAÇÃO EMAIL/PASSWORD (REAL)
    const handleEmailSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!email || !password || !confirmPassword) return;

        if (!validatePasswords()) {
            setStatus('denied');
            setTimeout(() => setStatus('idle'), 2000);
            return;
        }

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
            // CADASTRO REAL COM SUPABASE
            const { error } = await signUp(email, password);

            clearInterval(interval);
            setScanProgress(100);

            if (error) {
                setStatus('denied');
                setErrorMessage(error.message || 'Registration failed');
                setTimeout(() => {
                    setStatus('idle');
                    setScanProgress(0);
                }, 2000);
            } else {
                setStatus('success');
                // Router.push já é chamado dentro do signUp
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
    const handleGoogleSignup = async () => {
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
            setErrorMessage('Google signup failed');
            setTimeout(() => setStatus('idle'), 2000);
        }
    };

    // GITHUB LOGIN
    const handleGithubSignup = async () => {
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
            setErrorMessage('GitHub signup failed');
            setTimeout(() => setStatus('idle'), 2000);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-background relative overflow-hidden">

            {/* BACKGROUND ANIMADO (GRID + PARTICLES) */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 animate-pulse" />
            <div className="absolute inset-0 bg-radial-gradient from-transparent via-background/80 to-background pointer-events-none" />

            {/* SCANNER VISUALIZER (ABSOLUTE CENTER BACKGROUND) */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-30 blur-3xl">
                <div className={`w-96 h-96 rounded-full transition-colors duration-1000 ${
                    status === 'success' ? 'bg-[var(--color-success)]' :
                    status === 'denied' ? 'bg-[var(--color-error)]' :
                    'bg-[var(--color-primary)]'
                }`} />
            </div>

            {/* SIGNUP CARD (GLASSLITH) */}
            <div className="relative z-10 w-full max-w-md p-4">
                {/* Borda Brilhante Animada */}
                <div className={`absolute inset-0 rounded-3xl blur-md transition-all duration-500 ${
                    status === 'scanning' ? 'bg-[var(--color-primary)] opacity-50' :
                    status === 'success' ? 'bg-[var(--color-success)] opacity-80 scale-105' :
                    status === 'denied' ? 'bg-[var(--color-error)] opacity-80 animate-shake' :
                    'bg-surface/10 opacity-20'
                }`} />

                <div className="relative bg-background/80 backdrop-blur-2xl border border-border/10 rounded-3xl p-8 shadow-2xl overflow-hidden">

                    {/* SCANNER CANVAS */}
                    <div className="flex justify-center mb-4 relative">
                        <div className="w-24 h-24 relative">
                            <canvas ref={canvasRef} className="w-full h-full" />
                            {/* Icon Overlay */}
                            <div className="absolute inset-0 flex items-center justify-center text-text/50">
                                {status === 'success' ? <ShieldCheck className="w-8 h-8 text-background z-10" /> :
                                 status === 'denied' ? <AlertOctagon className="w-8 h-8 text-background z-10" /> :
                                 <UserPlus className="w-8 h-8 opacity-50" />}
                            </div>
                        </div>
                    </div>

                    {/* HEADER TEXT */}
                    <div className="text-center mb-6">
                        <h1 className="text-2xl font-black text-text tracking-tight font-display flex items-center justify-center gap-2">
                            ALSHAM <Sparkles className="w-4 h-4 text-[var(--color-primary)]" />
                        </h1>
                        <p className={`text-[10px] font-mono mt-1 tracking-[0.2em] uppercase transition-colors ${
                            status === 'success' ? 'text-[var(--color-success)]' :
                            status === 'denied' ? 'text-[var(--color-error)]' :
                            'text-[var(--color-textSecondary)]'
                        }`}>
                            {status === 'idle' && 'Create New Identity'}
                            {status === 'scanning' && 'Registering Biometrics...'}
                            {status === 'success' && 'Registration Complete. Welcome Architect.'}
                            {status === 'denied' && errorMessage}
                        </p>
                    </div>

                    {/* EMAIL FORM */}
                    <form onSubmit={handleEmailSignup} className="space-y-4 relative">

                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-textSecondary group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Mail className="w-4 h-4" />
                            </div>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Commander ID"
                                disabled={status !== 'idle'}
                                className="w-full bg-surface/5 border border-border/10 rounded-xl py-3 pl-10 pr-4 text-text placeholder-textSecondary focus:border-[var(--color-primary)] focus:bg-background transition-all outline-none font-mono text-sm"
                            />
                        </div>

                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-textSecondary group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Key className="w-4 h-4" />
                            </div>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Access Code"
                                disabled={status !== 'idle'}
                                className="w-full bg-surface/5 border border-border/10 rounded-xl py-3 pl-10 pr-4 text-text placeholder-textSecondary focus:border-[var(--color-primary)] focus:bg-background transition-all outline-none font-mono text-sm tracking-widest"
                            />
                        </div>

                        <div className="group relative">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-textSecondary group-focus-within:text-[var(--color-primary)] transition-colors">
                                <Lock className="w-4 h-4" />
                            </div>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm Access Code"
                                disabled={status !== 'idle'}
                                className="w-full bg-surface/5 border border-border/10 rounded-xl py-3 pl-10 pr-4 text-text placeholder-textSecondary focus:border-[var(--color-primary)] focus:bg-background transition-all outline-none font-mono text-sm tracking-widest"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={status !== 'idle'}
                            className={`
                                w-full py-3 rounded-xl font-bold text-xs tracking-widest uppercase transition-all relative overflow-hidden group
                                ${status === 'success' ? 'bg-[var(--color-success)] text-black' :
                                  status === 'denied' ? 'bg-[var(--color-error)] text-text' :
                                  'bg-[var(--color-primary)] text-background hover:bg-[var(--color-accent)]'}
                            `}
                        >
                            <div className="relative z-10 flex items-center justify-center gap-2">
                                {status === 'idle' && <><UserPlus className="w-4 h-4" /> CREATE ACCOUNT</>}
                                {status === 'scanning' && 'REGISTERING...'}
                                {status === 'success' && <><ShieldCheck className="w-4 h-4" /> COMPLETE</>}
                                {status === 'denied' && <><Lock className="w-4 h-4" /> FAILED</>}
                            </div>

                            {/* Progress Bar Overlay */}
                            {status === 'scanning' && (
                                <div
                                    className="absolute inset-0 bg-surface/30 transition-all duration-100 ease-linear"
                                    style={{ width: `${scanProgress}%` }}
                                />
                            )}
                        </button>
                    </form>

                    {/* DIVIDER */}
                    <div className="my-6 flex items-center gap-4">
                        <div className="h-[1px] flex-1 bg-border/10" />
                        <span className="text-[10px] font-mono text-textSecondary uppercase">OR CONNECT WITH</span>
                        <div className="h-[1px] flex-1 bg-border/10" />
                    </div>

                    {/* SOCIAL BUTTONS */}
                    <div className="grid grid-cols-2 gap-4">
                        <button
                            onClick={handleGoogleSignup}
                            disabled={status !== 'idle'}
                            className="flex items-center justify-center gap-2 py-3 rounded-xl bg-surface/5 hover:bg-surface/10 border border-border/10 hover:border-border/30 transition-all group"
                        >
                            <Chrome className="w-4 h-4 text-text group-hover:text-[var(--color-primary)] transition-colors" />
                            <span className="text-xs font-bold text-textSecondary group-hover:text-text">GOOGLE</span>
                        </button>

                        <button
                            onClick={handleGithubSignup}
                            disabled={status !== 'idle'}
                            className="flex items-center justify-center gap-2 py-3 rounded-xl bg-surface/5 hover:bg-surface/10 border border-border/10 hover:border-border/30 transition-all group"
                        >
                            <Github className="w-4 h-4 text-text group-hover:text-[var(--color-accent)] transition-colors" />
                            <span className="text-xs font-bold text-textSecondary group-hover:text-text">GITHUB</span>
                        </button>
                    </div>

                    {/* Login Link */}
                    <div className="mt-6 text-center">
                        <Link href="/login" className="text-xs text-textSecondary hover:text-[var(--color-primary)] transition-colors font-mono">
                            Já tem conta? <span className="font-bold">Faça login</span>
                        </Link>
                    </div>

                    {/* Footer Links */}
                    <div className="mt-6 flex justify-between text-[9px] text-textSecondary font-mono uppercase">
                        <button className="hover:text-text transition-colors">Reset Protocol</button>
                        <button className="hover:text-text transition-colors">Emergency Override</button>
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
