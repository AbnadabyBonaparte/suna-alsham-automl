/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - VALUE DASH (THE TREASURY)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/value/page.tsx
 * 📋 Cofre Digital com chuva de partículas douradas e contadores
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Wallet, TrendingUp, ArrowUpRight, Gem, Lock, CreditCard, RefreshCw, Inbox } from 'lucide-react';
import { supabase } from '@/lib/supabase';

interface Transaction {
    id: string;
    name: string;
    amount: number;
    created_at: string;
}

// Componente de Contador Rolante (Odometer Effect)
const RollingNumber = ({ value, prefix = "" }: { value: number, prefix?: string }) => {
    const [displayValue, setDisplayValue] = useState(0);

    useEffect(() => {
        let start = displayValue;
        const end = value;
        const duration = 2000; // 2 segundos
        const startTime = performance.now();

        const animate = (currentTime: number) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (easeOutExpo)
            const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
            
            const current = start + (end - start) * ease;
            setDisplayValue(current);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }, [value]);

    return (
        <span className="tabular-nums tracking-tight">
            {prefix}{displayValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </span>
    );
};

export default function ValuePage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [balance, setBalance] = useState(0);
    const [profit, setProfit] = useState(0);
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadFinancialData() {
            setLoading(true);
            setError(null);
            try {
                const { data: txData, error: txError } = await supabase
                    .from('transactions')
                    .select('*')
                    .order('created_at', { ascending: false })
                    .limit(20);

                if (txError) throw txError;

                const mapped: Transaction[] = (txData || []).map((t) => ({
                    id: t.id,
                    name: t.name || t.description || 'Transação',
                    amount: t.amount || 0,
                    created_at: t.created_at,
                }));
                setTransactions(mapped);

                const totalBalance = mapped.reduce((sum, t) => sum + t.amount, 0);
                setBalance(totalBalance);

                const { data: invoiceData, error: invError } = await supabase
                    .from('invoices')
                    .select('amount, status')
                    .eq('status', 'paid');

                if (invError) throw invError;

                const totalProfit = (invoiceData || []).reduce((sum, inv) => sum + (inv.amount || 0), 0);
                setProfit(totalProfit);
            } catch (err) {
                console.error('Failed to load financial data:', err);
                setError('Erro ao carregar dados financeiros');
            } finally {
                setLoading(false);
            }
        }

        loadFinancialData();
    }, []);
    
    // 1. ENGINE VISUAL (CHUVA DE OURO/DIAMANTE)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        
        const particles: {x: number, y: number, speed: number, size: number, type: 'gold' | 'diamond'}[] = [];
        const PARTICLE_COUNT = 100;

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        // Inicializar
        for(let i=0; i<PARTICLE_COUNT; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                speed: 1 + Math.random() * 3,
                size: 1 + Math.random() * 3,
                type: Math.random() > 0.7 ? 'diamond' : 'gold'
            });
        }

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;

            ctx.clearRect(0, 0, w, h);

            // Desenhar partículas
            particles.forEach(p => {
                p.y += p.speed;
                
                // Reset se sair da tela
                if (p.y > h) {
                    p.y = -10;
                    p.x = Math.random() * w;
                }

                ctx.beginPath();
                if (p.type === 'gold') {
                    ctx.fillStyle = '#D4AF37'; // Ouro
                    ctx.shadowColor = '#D4AF37';
                } else {
                    ctx.fillStyle = '#E0F2FE'; // Diamante (Azul claro)
                    ctx.shadowColor = '#FFFFFF';
                }
                
                ctx.shadowBlur = 10;
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                
                // Brilho extra (cruz) para diamantes
                if (p.type === 'diamond' && Math.random() > 0.95) {
                    ctx.beginPath();
                    ctx.strokeStyle = 'white';
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(p.x - 4, p.y);
                    ctx.lineTo(p.x + 4, p.y);
                    ctx.moveTo(p.x, p.y - 4);
                    ctx.lineTo(p.x, p.y + 4);
                    ctx.stroke();
                }
            });

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);


    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col gap-6 overflow-hidden relative p-2">

            {/* FUNDO ANIMADO (O COFRE) */}
            <div className="absolute inset-0 rounded-3xl overflow-hidden bg-[#050505] border border-white/10 shadow-2xl">
                <canvas ref={canvasRef} className="absolute inset-0 w-full h-full opacity-30" />
                {/* Vignette */}
                <div className="absolute inset-0 bg-radial-gradient from-transparent via-black/50 to-black pointer-events-none" />
            </div>

            {/* CONTEÚDO SUPERIOR: TOTAL BALANCE */}
            <div className="relative z-10 flex flex-col items-center justify-center h-[40%] mt-8 animate-fadeIn">
                <div className="flex items-center gap-2 mb-4 px-4 py-1 rounded-full bg-white/5 border border-white/10 backdrop-blur-md">
                    <Lock className="w-3 h-3 text-[var(--color-accent)]" />
                    <span className="text-[10px] text-gray-400 font-mono uppercase tracking-[0.3em]">Secure Vault Access</span>
                </div>
                
                <h1 className="text-gray-500 text-sm uppercase tracking-widest font-serif mb-2">Total Value Locked</h1>
                <div className="text-6xl md:text-8xl font-black text-white font-mono tracking-tighter drop-shadow-2xl flex items-baseline gap-2">
                    <RollingNumber value={balance} prefix="$" />
                </div>
                
                <div className="mt-4 flex items-center gap-2 px-3 py-1 rounded-lg" style={{ color: 'var(--color-success)', background: 'var(--color-success)/10', border: '1px solid var(--color-success)/20' }}>
                    <TrendingUp className="w-4 h-4" />
                    <span className="text-sm font-mono font-bold">+2.4% (24h)</span>
                </div>
            </div>

            {/* CONTEÚDO INFERIOR: CARTÕES DE ATIVOS */}
            <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-4 h-[60%] pb-4 px-4">
                
                {/* CARD 1: REVENUE */}
                <div className="group bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-[var(--color-primary)]/50 transition-all duration-500 flex flex-col justify-between hover:bg-black/60">
                    <div className="flex justify-between items-start">
                        <div className="p-3 bg-white/5 rounded-xl group-hover:scale-110 transition-transform">
                            <Wallet className="w-6 h-6 text-[var(--color-primary)]" />
                        </div>
                        <button className="text-gray-500 hover:text-white transition-colors">
                            <ArrowUpRight className="w-5 h-5" />
                        </button>
                    </div>
                    <div>
                        <p className="text-gray-400 text-xs uppercase tracking-widest mb-1">Monthly Revenue</p>
                        <div className="text-3xl font-bold text-white font-mono">
                            <RollingNumber value={profit} prefix="$" />
                        </div>
                        <div className="w-full h-1 bg-white/10 rounded-full mt-4 overflow-hidden">
                            <div className="h-full bg-[var(--color-primary)] w-[75%] group-hover:w-[85%] transition-all duration-1000" />
                        </div>
                    </div>
                </div>

                {/* CARD 2: ASSET ALLOCATION (VISUALIZER) */}
                <div className="group bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-[var(--color-accent)]/50 transition-all duration-500 flex flex-col justify-center items-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />
                    
                    <div className="relative w-32 h-32 flex items-center justify-center mb-4">
                        {/* Gem Spinning */}
                        <Gem className="w-16 h-16 text-[var(--color-accent)] animate-pulse absolute" />
                        <div className="absolute inset-0 border-2 border-dashed border-white/20 rounded-full animate-spin-slow" />
                        <div className="absolute inset-2 border border-white/10 rounded-full animate-reverse-spin" />
                    </div>
                    
                    <h3 className="text-white font-bold tracking-widest text-sm">ASSET DIVERSIFICATION</h3>
                    <p className="text-xs text-gray-500 font-mono mt-1">Crypto • Fiat • Stocks</p>
                </div>

                {/* CARD 3: RECENT TRANSACTIONS */}
                <div className="group bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-emerald-500/30 transition-all duration-500 flex flex-col overflow-hidden">
                    <div className="flex items-center gap-3 mb-6">
                        <CreditCard className="w-5 h-5" style={{ color: 'var(--color-success)' }} />
                        <span className="text-sm font-bold text-white tracking-wider">LIVE TRANSACTIONS</span>
                    </div>
                    
                    <div className="flex-1 space-y-3 overflow-hidden">
                        {loading ? (
                            <div className="flex items-center justify-center py-6">
                                <RefreshCw className="w-5 h-5 animate-spin text-[var(--color-primary)]" />
                            </div>
                        ) : transactions.length === 0 ? (
                            <div className="text-center py-6">
                                <Inbox className="w-6 h-6 mx-auto mb-2 text-gray-600" />
                                <p className="text-xs text-gray-500">Nenhuma transação</p>
                            </div>
                        ) : (
                            transactions.slice(0, 4).map((tx) => {
                                const isPositive = tx.amount >= 0;
                                const formatted = `${isPositive ? '+' : ''}$${Math.abs(tx.amount).toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
                                const timeAgo = tx.created_at ? new Date(tx.created_at).toLocaleString('pt-BR') : '';
                                return (
                                    <div key={tx.id} className="flex justify-between items-center text-xs p-2 hover:bg-white/5 rounded-lg transition-colors cursor-default">
                                        <div className="flex flex-col">
                                            <span className="text-gray-300 font-medium">{tx.name}</span>
                                            <span className="text-gray-600 font-mono">{timeAgo}</span>
                                        </div>
                                        <span className="font-mono font-bold" style={{ color: isPositive ? 'var(--color-success)' : 'var(--color-error)' }}>
                                            {formatted}
                                        </span>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>

            </div>

            <style jsx>{`
                @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
                .animate-fadeIn { animation: fadeIn 0.5s ease-out forwards; }
                .animate-spin-slow { animation: spin 10s linear infinite; }
                .animate-reverse-spin { animation: spin 15s linear infinite reverse; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            `}</style>
        </div>
    );
}
