/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SOCIAL PULSE (THE HIVE MIND)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/social/page.tsx
 * 📋 Visualizador de Sentimento, Viralidade e Feed em Cascata
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    MessageCircle, Heart, Share2, TrendingUp, 
    Globe, Radio, Zap, Search, Hash 
} from 'lucide-react';

// Dados Mockados
const TRENDS = [
    { id: 1, tag: '#AIRevolution', volume: 98, sentiment: 'positive' },
    { id: 2, tag: '#CryptoCrash', volume: 85, sentiment: 'negative' },
    { id: 3, tag: '#AlshamQuantum', volume: 92, sentiment: 'positive' },
    { id: 4, tag: '#CyberSec', volume: 60, sentiment: 'neutral' },
    { id: 5, tag: '#MarsColony', volume: 75, sentiment: 'positive' },
];

const POSTS = [
    { id: 1, user: '@elon_musk_ai', content: 'A singularidade está mais próxima do que imaginamos. 🚀', likes: '42k', shares: '12k', platform: 'X' },
    { id: 2, user: '@dev_squad', content: 'Alguém já testou o novo protocolo Orion? Absurdo.', likes: '1.2k', shares: '300', platform: 'Reddit' },
    { id: 3, user: '@tech_insider', content: 'Vazou a nova arquitetura de rede neural. Thread 🧵', likes: '8k', shares: '4k', platform: 'X' },
    { id: 4, user: '@crypto_whale', content: 'Mercado derretendo. HODL! 📉', likes: '500', shares: '50', platform: 'Discord' },
    { id: 5, user: '@future_is_now', content: 'A era biológica acabou.', likes: '900', shares: '120', platform: 'Instagram' },
];

export default function SocialPage() {
    const waveCanvasRef = useRef<HTMLCanvasElement>(null);
    const [activeTrend, setActiveTrend] = useState<number | null>(null);
    const [sentimentScore, setSentimentScore] = useState(78); // 0-100

    // 1. ENGINE VISUAL (ONDA DE SENTIMENTO)
    useEffect(() => {
        const canvas = waveCanvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        
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
            const cy = h / 2;

            ctx.clearRect(0, 0, w, h);
            time += 0.05;

            // Cor baseada no sentimento
            let color = '#10B981'; // Verde
            if (sentimentScore < 40) color = '#EF4444'; // Vermelho
            else if (sentimentScore < 60) color = '#F59E0B'; // Amarelo

            // Desenhar múltiplas ondas
            for(let i = 0; i < 3; i++) {
                ctx.beginPath();
                ctx.lineWidth = 2;
                ctx.strokeStyle = i === 0 ? color : `${color}44`; // Opacidade nas ondas secundárias
                
                for(let x = 0; x < w; x++) {
                    // Fórmula da onda complexa
                    const frequency = 0.01 + (i * 0.005);
                    const amplitude = 50 + (Math.sin(time * 0.5) * 20);
                    const y = cy + Math.sin(x * frequency + time + (i * 2)) * amplitude * (sentimentScore/100);
                    
                    if (x === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.stroke();
            }

            // Efeito de "Ruído" se sentimento for negativo
            if (sentimentScore < 40) {
                const imageData = ctx.getImageData(0, 0, w, h);
                const data = imageData.data;
                for(let i=0; i<data.length; i+=4) {
                    if (Math.random() > 0.9) {
                        data[i] = 255; // R
                        data[i+1] = 0; // G
                        data[i+2] = 0; // B
                    }
                }
                ctx.putImageData(imageData, 0, 0);
            }

            requestAnimationFrame(render);
        };

        render();
        return () => window.removeEventListener('resize', resize);
    }, [sentimentScore]);

    // Simulador de Live Data
    useEffect(() => {
        const interval = setInterval(() => {
            // Flutuar sentimento
            setSentimentScore(prev => {
                const change = (Math.random() - 0.5) * 10;
                return Math.max(0, Math.min(100, prev + change));
            });
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">

            {/* COMING SOON BADGE */}
            <div className="absolute top-4 right-4 z-50 animate-pulse">
                <div className="bg-gradient-to-r from-[var(--color-primary)]/20 via-[var(--color-accent)]/20 to-[var(--color-secondary)]/20 backdrop-blur-xl border-2 border-[var(--color-primary)]/50 rounded-2xl px-6 py-3 shadow-[0_0_30px_var(--color-primary)]">
                    <div className="flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-ping" />
                        <span className="text-sm font-black text-white uppercase tracking-widest orbitron">
                            Coming Soon
                        </span>
                        <Zap className="w-4 h-4 text-[var(--color-accent)]" />
                    </div>
                    <div className="text-[10px] text-gray-400 text-center mt-1 font-mono">
                        Feature in development
                    </div>
                </div>
            </div>

            {/* ESQUERDA: VISUALIZAÇÃO MACRO */}
            <div className="lg:w-2/3 w-full flex flex-col gap-6">
                
                {/* 1. SENTIMENT WAVE VISUALIZER */}
                <div className="flex-1 bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-0 relative overflow-hidden shadow-2xl group flex flex-col">
                    {/* Header Flutuante */}
                    <div className="absolute top-6 left-6 z-10 flex justify-between w-[calc(100%-3rem)]">
                        <div>
                            <h2 className="text-lg font-bold text-white flex items-center gap-2 tracking-tight">
                                <Radio className="w-5 h-5 text-[var(--color-primary)] animate-pulse" />
                                GLOBAL SENTIMENT
                            </h2>
                            <p className="text-xs text-gray-400 font-mono">Real-time emotional analysis</p>
                        </div>
                        <div className="text-right">
                            <div className={`text-3xl font-mono font-bold ${sentimentScore > 60 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {sentimentScore.toFixed(0)}%
                            </div>
                            <div className="text-[10px] text-gray-500 uppercase tracking-widest">Positive Index</div>
                        </div>
                    </div>

                    {/* Canvas */}
                    <canvas ref={waveCanvasRef} className="w-full h-full" />
                    
                    {/* Grid Overlay */}
                    <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                </div>

                {/* 2. TRENDING BUBBLES */}
                <div className="h-48 flex gap-4">
                    {TRENDS.map((trend, i) => (
                        <div 
                            key={trend.id}
                            onMouseEnter={() => setActiveTrend(trend.id)}
                            onMouseLeave={() => setActiveTrend(null)}
                            className={`
                                flex-1 rounded-2xl border transition-all duration-500 cursor-pointer relative overflow-hidden flex flex-col items-center justify-center
                                ${activeTrend === trend.id 
                                    ? 'bg-[var(--color-primary)]/20 border-[var(--color-primary)] scale-105 z-10' 
                                    : 'bg-black/40 border-white/5 hover:bg-white/10'}
                            `}
                        >
                            {/* Bubble Visual */}
                            <div 
                                className={`absolute w-32 h-32 rounded-full blur-2xl opacity-20 transition-all duration-1000
                                ${trend.sentiment === 'positive' ? 'bg-green-500' : trend.sentiment === 'negative' ? 'bg-red-500' : 'bg-blue-500'}`}
                                style={{ transform: activeTrend === trend.id ? 'scale(1.5)' : 'scale(1)' }}
                            />
                            
                            <div className="relative z-10 text-center">
                                <div className="text-xs text-gray-400 font-mono mb-1">#{i + 1} TRENDING</div>
                                <div className="text-lg font-bold text-white">{trend.tag}</div>
                                <div className="mt-2 flex items-center justify-center gap-1 text-xs font-mono">
                                    <TrendingUp className="w-3 h-3" />
                                    <span>{trend.volume}k Vol</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* DIREITA: LIVE FEED WATERFALL */}
            <div className="lg:w-1/3 w-full bg-[#02040a] border border-white/10 rounded-3xl p-0 overflow-hidden relative flex flex-col shadow-2xl">
                {/* Header */}
                <div className="p-6 border-b border-white/5 bg-black/20 backdrop-blur-xl z-10">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                            <Globe className="w-4 h-4 text-purple-400" />
                            Live Feed
                        </h3>
                        <div className="flex gap-2">
                            <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
                            <span className="text-[10px] text-red-400 font-bold">LIVE</span>
                        </div>
                    </div>
                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                        <input 
                            type="text" 
                            placeholder="Filter stream..." 
                            className="w-full bg-white/5 border border-white/10 rounded-xl pl-9 pr-4 py-2 text-xs text-white focus:border-[var(--color-primary)] transition-all outline-none"
                        />
                    </div>
                </div>

                {/* Waterfall Container */}
                <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin scrollbar-thumb-white/10 relative">
                    <div className="absolute top-0 left-0 right-0 h-8 bg-gradient-to-b from-[#02040a] to-transparent z-10 pointer-events-none" />
                    
                    {POSTS.map((post, i) => (
                        <div 
                            key={post.id}
                            className="bg-white/5 hover:bg-white/10 border border-white/5 hover:border-[var(--color-primary)]/30 rounded-xl p-4 transition-all duration-300 animate-slideInBottom group"
                            style={{ animationDelay: `${i * 0.1}s` }}
                        >
                            <div className="flex justify-between items-start mb-2">
                                <div className="flex items-center gap-2">
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-black border border-white/10 flex items-center justify-center font-bold text-xs text-white">
                                        {post.user.charAt(1).toUpperCase()}
                                    </div>
                                    <div>
                                        <div className="text-xs font-bold text-white group-hover:text-[var(--color-primary)] transition-colors">{post.user}</div>
                                        <div className="text-[10px] text-gray-500">{post.platform} • Just now</div>
                                    </div>
                                </div>
                                <Hash className="w-3 h-3 text-gray-600" />
                            </div>
                            
                            <p className="text-sm text-gray-300 leading-relaxed mb-3">
                                {post.content}
                            </p>

                            <div className="flex gap-4 text-xs text-gray-500 font-mono">
                                <div className="flex items-center gap-1 hover:text-red-400 transition-colors cursor-pointer">
                                    <Heart className="w-3 h-3" /> {post.likes}
                                </div>
                                <div className="flex items-center gap-1 hover:text-blue-400 transition-colors cursor-pointer">
                                    <Share2 className="w-3 h-3" /> {post.shares}
                                </div>
                                <div className="flex items-center gap-1 hover:text-white transition-colors cursor-pointer">
                                    <MessageCircle className="w-3 h-3" /> Reply
                                </div>
                            </div>
                        </div>
                    ))}
                    
                    <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-[#02040a] to-transparent z-10 pointer-events-none" />
                </div>
            </div>

            <style jsx>{`
                @keyframes slideInBottom {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-slideInBottom { animation: slideInBottom 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
            `}</style>
        </div>
    );
}
