/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SALES ENGINE (QUANTUM TRADING FLOOR)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/sales/page.tsx
 * 📋 CRM em tempo real estilo "High Frequency Trading"
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    TrendingUp, DollarSign, Target, Users, 
    ArrowUpRight, Briefcase, Zap, Crosshair 
} from 'lucide-react';

// Tipos
interface Deal {
    id: number;
    client: string;
    value: number;
    status: 'closed' | 'negotiation' | 'lead';
    probability: number;
    timestamp: string;
}

export default function SalesPage() {
    const chartRef = useRef<HTMLCanvasElement>(null);
    
    // Estados
    const [revenue, setRevenue] = useState(842500);
    const [deals, setDeals] = useState<Deal[]>([]);
    const [targetLocked, setTargetLocked] = useState<number | null>(null);

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

            // Simular novo dado
            if (Math.random() > 0.8) {
                const change = (Math.random() - 0.45) * 10;
                currentValue = Math.max(10, Math.min(90, currentValue + change));
                dataPoints.push(currentValue);
                if (dataPoints.length > maxPoints) dataPoints.shift();
                
                // Atualizar Receita Total (Fake)
                if (change > 0) setRevenue(prev => prev + Math.floor(Math.random() * 100));
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
            gradient.addColorStop(0, themeColor + '40'); // 25% opacity
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
    }, []);

    // 2. GERADOR DE DEALS (TICKER)
    useEffect(() => {
        const clients = ['CyberDyne', 'Tyrell Corp', 'Stark Ind', 'Wayne Ent', 'Massive Dynamic', 'Omni Corp'];
        
        const interval = setInterval(() => {
            const newDeal: Deal = {
                id: Date.now(),
                client: clients[Math.floor(Math.random() * clients.length)],
                value: Math.floor(Math.random() * 50000) + 1000,
                status: Math.random() > 0.7 ? 'closed' : 'negotiation',
                probability: Math.floor(Math.random() * 100),
                timestamp: new Date().toLocaleTimeString()
            };
            setDeals(prev => [newDeal, ...prev].slice(0, 7));
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* ESQUERDA: DASHBOARD PRINCIPAL */}
            <div className="lg:w-2/3 w-full flex flex-col gap-6">
                
                {/* KPI CARDS */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[
                        { label: 'Total Revenue', val: `$${revenue.toLocaleString()}`, icon: DollarSign, color: 'text-emerald-400' },
                        { label: 'Conversion Rate', val: '42.8%', icon: Zap, color: 'text-yellow-400' },
                        { label: 'Active Leads', val: '1,204', icon: Users, color: 'text-[var(--color-primary)]' },
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
                        <p className="text-xs text-gray-500 font-mono">Live market data • 50ms Latency</p>
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
                        <span className="text-[10px] px-2 py-1 bg-green-500/20 text-green-400 rounded border border-green-500/30 animate-pulse">LIVE</span>
                    </div>

                    <div className="flex-1 overflow-hidden relative space-y-3">
                        {deals.map((deal) => (
                            <div 
                                key={deal.id}
                                onMouseEnter={() => setTargetLocked(deal.id)}
                                onMouseLeave={() => setTargetLocked(null)}
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
                                    <span className="font-bold text-white text-sm">{deal.client}</span>
                                    <span className="font-mono text-[var(--color-primary)] font-bold">${deal.value.toLocaleString()}</span>
                                </div>
                                <div className="flex justify-between items-center text-xs">
                                    <span className={`px-1.5 py-0.5 rounded uppercase font-bold ${
                                        deal.status === 'closed' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-blue-500/20 text-blue-400'
                                    }`}>
                                        {deal.status}
                                    </span>
                                    <span className="text-gray-500 font-mono">{deal.timestamp}</span>
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

                {/* MANUAL ACTION */}
                <button className="group relative h-20 bg-[var(--color-primary)] rounded-2xl overflow-hidden flex items-center justify-center shadow-[0_0_30px_rgba(var(--color-primary-rgb),0.3)] hover:scale-[1.02] transition-transform">
                    <div className="absolute inset-0 bg-[url('/stripes.png')] opacity-10 animate-slideBg" />
                    <div className="relative z-10 flex items-center gap-3 text-black font-black text-lg tracking-widest uppercase">
                        <Target className="w-6 h-6 group-hover:rotate-90 transition-transform duration-500" />
                        Initiate Closer AI
                    </div>
                </button>

            </div>

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
