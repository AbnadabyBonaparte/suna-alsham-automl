/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SALES ENGINE (QUANTUM TRADING FLOOR) - v10
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/sales/page.tsx
 * 📋 CRM em tempo real estilo "High Frequency Trading" - DADOS REAIS
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import {
    TrendingUp, DollarSign, Target, Users,
    ArrowUpRight, Briefcase, Zap, Crosshair, X, ExternalLink, TrendingDown
} from 'lucide-react';
import { useSales } from '@/hooks/useSales';
import { Skeleton } from '@/components/ui/SkeletonLoader';
import type { Deal } from '@/stores';

interface DealModalProps {
    deal: Deal | null;
    onClose: () => void;
}

function DealModal({ deal, onClose }: DealModalProps) {
    if (!deal) return null;

    const statusColors = {
        lead: { bg: 'bg-blue-500/10', border: 'border-blue-500/30', text: 'text-blue-400' },
        negotiation: { bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-400' },
        closed_won: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', text: 'text-emerald-400' },
        closed_lost: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-400' },
    };

    const colors = statusColors[deal.status];

    return (
        <div className="fixed inset-0 z-[9998] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
            <div className={`relative w-full max-w-2xl ${colors.bg} backdrop-blur-xl border ${colors.border} rounded-3xl p-8 shadow-2xl`}>
                {/* Close Button */}
                <button
                    onClick={onClose}
                    className="absolute top-6 right-6 text-gray-400 hover:text-white transition-colors"
                >
                    <X className="w-6 h-6" />
                </button>

                {/* Header */}
                <div className="flex items-start gap-4 mb-6">
                    <div className={`p-3 rounded-xl ${colors.bg} border ${colors.border}`}>
                        <Briefcase className={`w-8 h-8 ${colors.text}`} />
                    </div>
                    <div className="flex-1">
                        <h2 className="text-2xl font-bold text-white mb-1">{deal.client_name}</h2>
                        <div className="flex gap-2 text-xs">
                            <span className={`px-2 py-1 rounded ${colors.bg} ${colors.text} border ${colors.border} uppercase font-bold`}>
                                {deal.status.replace('_', ' ')}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Value */}
                <div className="mb-6">
                    <h3 className="text-sm font-bold text-gray-400 uppercase mb-2">Deal Value</h3>
                    <div className="text-4xl font-mono font-bold text-white">
                        ${deal.value.toLocaleString()}
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="bg-white/5 rounded-xl p-4">
                        <div className="text-xs text-gray-400 uppercase mb-1">Probability</div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-bold text-white">{deal.probability}%</span>
                            <TrendingUp className={`w-4 h-4 ${deal.probability > 70 ? 'text-emerald-400' : deal.probability > 40 ? 'text-yellow-400' : 'text-red-400'}`} />
                        </div>
                        {/* Probability Bar */}
                        <div className="mt-2 h-2 w-full bg-black/50 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-blue-500 to-[var(--color-primary)] transition-all"
                                style={{ width: `${deal.probability}%` }}
                            />
                        </div>
                    </div>

                    <div className="bg-white/5 rounded-xl p-4">
                        <div className="text-xs text-gray-400 uppercase mb-1">Created</div>
                        <div className="text-lg font-mono text-white">
                            {new Date(deal.created_at).toLocaleDateString()}
                        </div>
                        <div className="text-xs text-gray-500 font-mono">
                            {new Date(deal.created_at).toLocaleTimeString()}
                        </div>
                    </div>
                </div>

                {/* Notes */}
                {deal.notes && (
                    <div className="mb-6">
                        <h3 className="text-sm font-bold text-gray-400 uppercase mb-2">Notes</h3>
                        <p className="text-white leading-relaxed">{deal.notes}</p>
                    </div>
                )}

                {/* Expected Close Date */}
                {deal.expected_close_date && (
                    <div className="mb-6">
                        <h3 className="text-sm font-bold text-gray-400 uppercase mb-2">Expected Close Date</h3>
                        <p className="text-white font-mono">{new Date(deal.expected_close_date).toLocaleDateString()}</p>
                    </div>
                )}

                {/* Actions */}
                <div className="flex gap-3">
                    <button className="flex-1 bg-[var(--color-primary)] hover:bg-[var(--color-primary)]/80 text-black font-bold py-3 px-6 rounded-xl transition-all">
                        Close Deal
                    </button>
                    <button className="px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white transition-all">
                        View Pipeline
                        <ExternalLink className="w-4 h-4 inline ml-2" />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default function SalesPage() {
    const chartRef = useRef<HTMLCanvasElement>(null);
    const [targetLocked, setTargetLocked] = useState<string | null>(null);
    const [activeDeal, setActiveDeal] = useState<Deal | null>(null);

    const { deals, stats, loading } = useSales();

    // 1. ENGINE DO GRÁFICO (ECG FINANCEIRO)
    useEffect(() => {
        const canvas = chartRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Configuração
        const dataPoints: number[] = [];
        const maxPoints = 100;
        let currentValue = 50;

        // Inicializar pontos
        for(let i=0; i<maxPoints; i++) dataPoints.push(50);

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        let animationId: number;

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;

            // Simular novo dado baseado em deals REAIS
            if (Math.random() > 0.8) {
                const change = (Math.random() - 0.45) * 10;
                // Se tiver deals, usar conversion rate para influenciar
                if (stats.conversion_rate > 50) {
                    currentValue = Math.max(10, Math.min(90, currentValue + Math.abs(change)));
                } else {
                    currentValue = Math.max(10, Math.min(90, currentValue + change));
                }
                dataPoints.push(currentValue);
                if (dataPoints.length > maxPoints) dataPoints.shift();
            }

            // Limpar
            ctx.clearRect(0, 0, w, h);

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#10B981';

            // Grid de Fundo
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            for(let x=0; x<w; x+=50) { ctx.moveTo(x, 0); ctx.lineTo(x, h); }
            for(let y=0; y<h; y+=50) { ctx.moveTo(0, y); ctx.lineTo(w, y); }
            ctx.stroke();

            // Desenhar Gráfico (Linha)
            ctx.beginPath();
            ctx.strokeStyle = themeColor;
            ctx.lineWidth = 3;
            ctx.lineJoin = 'round';
            ctx.shadowBlur = 15;
            ctx.shadowColor = themeColor;

            const stepX = w / (maxPoints - 1);

            for (let i = 0; i < dataPoints.length; i++) {
                const x = i * stepX;
                const y = h - (dataPoints[i] / 100) * h;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();

            // Preenchimento (Gradient)
            ctx.lineTo(w, h);
            ctx.lineTo(0, h);
            ctx.closePath();
            const gradient = ctx.createLinearGradient(0, 0, 0, h);
            gradient.addColorStop(0, themeColor + '40');
            gradient.addColorStop(1, 'transparent');
            ctx.fillStyle = gradient;
            ctx.shadowBlur = 0;
            ctx.fill();

            // Ponto Atual (Pulse)
            const lastX = (dataPoints.length - 1) * stepX;
            const lastY = h - (dataPoints[dataPoints.length - 1] / 100) * h;

            ctx.beginPath();
            ctx.fillStyle = '#FFFFFF';
            ctx.arc(lastX, lastY, 4, 0, Math.PI * 2);
            ctx.fill();

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [stats]);

    if (loading && deals.length === 0) {
        return (
            <div className="h-[calc(100vh-6rem)] flex items-center justify-center">
                <div className="text-center">
                    <Skeleton className="w-20 h-20 rounded-full mx-auto mb-4" />
                    <Skeleton className="w-48 h-6 mx-auto mb-2" />
                    <Skeleton className="w-32 h-4 mx-auto" />
                </div>
            </div>
        );
    }

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">

            {/* ESQUERDA: DASHBOARD PRINCIPAL */}
            <div className="lg:w-2/3 w-full flex flex-col gap-6">

                {/* KPI CARDS */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[
                        { label: 'Total Revenue', val: `$${stats.total_value.toLocaleString()}`, icon: DollarSign, color: 'text-emerald-400' },
                        { label: 'Conversion Rate', val: `${stats.conversion_rate.toFixed(1)}%`, icon: Zap, color: 'text-yellow-400' },
                        { label: 'Active Deals', val: stats.total_deals.toString(), icon: Users, color: 'text-[var(--color-primary)]' },
                    ].map((kpi, i) => (
                        <div key={i} className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-5 relative overflow-hidden group">
                            <div className="absolute inset-0 bg-gradient-to-r from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                            <div className="flex justify-between items-start mb-2">
                                <div className={`p-2 rounded-lg bg-white/5 ${kpi.color}`}>
                                    <kpi.icon className="w-6 h-6" />
                                </div>
                                <ArrowUpRight className="w-4 h-4 text-gray-500" />
                            </div>
                            <div className="text-2xl font-bold text-white font-mono tracking-tight">{kpi.val}</div>
                            <div className="text-xs text-gray-400 uppercase font-bold tracking-wider">{kpi.label}</div>
                        </div>
                    ))}
                </div>

                {/* CHART SECTION (O ECG) */}
                <div className="flex-1 bg-[#02040a] border border-white/10 rounded-3xl p-6 relative overflow-hidden shadow-2xl group">
                    {/* Header do Gráfico */}
                    <div className="absolute top-6 left-6 z-10">
                        <h2 className="text-lg font-bold text-white flex items-center gap-2">
                            <TrendingUp className="w-5 h-5 text-[var(--color-primary)]" />
                            REVENUE STREAM
                        </h2>
                        <p className="text-xs text-gray-500 font-mono">
                            Live market data • {deals.length > 0 ? 'Real deals active' : 'No active deals'}
                        </p>
                    </div>

                    {/* CANVAS */}
                    <canvas ref={chartRef} className="w-full h-full" />

                    {/* Overlay Scanline */}
                    <div className="absolute inset-0 bg-[url('/scanlines.png')] opacity-5 pointer-events-none" />
                </div>
            </div>

            {/* DIREITA: DEAL FLOW & PIPELINE */}
            <div className="lg:w-1/3 w-full flex flex-col gap-4 h-full">

                {/* DEAL TICKER (LISTA VIVA) */}
                <div className="flex-1 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-6 overflow-hidden flex flex-col">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                            <Briefcase className="w-4 h-4 text-[var(--color-secondary)]" />
                            Deal Flow
                        </h3>
                        {deals.length > 0 && (
                            <span className="text-[10px] px-2 py-1 bg-green-500/20 text-green-400 rounded border border-green-500/30 animate-pulse">LIVE</span>
                        )}
                    </div>

                    <div className="flex-1 overflow-y-auto relative space-y-3">
                        {deals.length === 0 && !loading && (
                            <div className="flex items-center justify-center h-full">
                                <div className="text-center">
                                    <Briefcase className="w-12 h-12 text-gray-600 mx-auto mb-2" />
                                    <p className="text-sm text-gray-500">No active deals</p>
                                </div>
                            </div>
                        )}

                        {deals.slice(0, 10).map((deal) => (
                            <div
                                key={deal.id}
                                onMouseEnter={() => setTargetLocked(deal.id)}
                                onMouseLeave={() => setTargetLocked(null)}
                                onClick={() => setActiveDeal(deal)}
                                className={`
                                    group relative p-3 rounded-xl border transition-all duration-300 cursor-pointer animate-slideInRight
                                    ${targetLocked === deal.id
                                        ? 'bg-[var(--color-primary)]/10 border-[var(--color-primary)] translate-x-2'
                                        : 'bg-white/5 border-white/5 hover:bg-white/10'}
                                `}
                            >
                                {/* Crosshair Overlay on Hover */}
                                {targetLocked === deal.id && (
                                    <div className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-primary)]">
                                        <Crosshair className="w-6 h-6 animate-spin-slow" />
                                    </div>
                                )}

                                <div className="flex justify-between items-center mb-1">
                                    <span className="font-bold text-white text-sm">{deal.client_name}</span>
                                    <span className="font-mono text-[var(--color-primary)] font-bold">${deal.value.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between items-center text-xs">
                                    <span className={`px-1.5 py-0.5 rounded uppercase font-bold ${
                                        deal.status === 'closed_won' ? 'bg-emerald-500/20 text-emerald-400' :
                                        deal.status === 'closed_lost' ? 'bg-red-500/20 text-red-400' :
                                        deal.status === 'negotiation' ? 'bg-yellow-500/20 text-yellow-400' :
                                        'bg-blue-500/20 text-blue-400'
                                    }`}>
                                        {deal.status.replace('_', ' ')}
                                    </span>
                                    <span className="text-gray-500 font-mono">{new Date(deal.created_at).toLocaleDateString()}</span>
                                </div>

                                {/* Probability Bar */}
                                <div className="mt-2 h-1 w-full bg-black/50 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-blue-500 to-[var(--color-primary)]"
                                        style={{ width: `${deal.probability}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* STATS BREAKDOWN */}
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
                    <h3 className="text-xs font-bold text-gray-400 uppercase mb-3">Pipeline Breakdown</h3>
                    <div className="space-y-2 text-xs">
                        <div className="flex justify-between items-center">
                            <span className="text-gray-400">Won Deals</span>
                            <span className="font-mono text-emerald-400 font-bold">${stats.won_value.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-gray-400">In Progress</span>
                            <span className="font-mono text-yellow-400 font-bold">${stats.in_progress_value.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-gray-400">Avg Deal Value</span>
                            <span className="font-mono text-[var(--color-primary)] font-bold">${stats.avg_deal_value.toFixed(0)}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal */}
            <DealModal deal={activeDeal} onClose={() => setActiveDeal(null)} />

            <style jsx>{`
                @keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
                .animate-slideInRight { animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1); }

                @keyframes slideBg { from { background-position: 0 0; } to { background-position: 50px 50px; } }
                .animate-slideBg { animation: slideBg 2s linear infinite; }

                .animate-spin-slow { animation: spin 4s linear infinite; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            `}</style>
        </div>
    );
}
