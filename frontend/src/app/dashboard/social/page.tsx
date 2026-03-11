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
    Globe, Radio, Zap, Search, Hash, RefreshCw, Inbox
} from 'lucide-react';
import { supabase } from '@/lib/supabase';

interface SocialPost {
    id: string;
    user: string;
    content: string;
    likes: number;
    shares: number;
    platform: string;
    sentiment?: string;
    created_at?: string;
}

function formatCount(n: number): string {
    if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
    return String(n);
}

export default function SocialPage() {
    const waveCanvasRef = useRef<HTMLCanvasElement>(null);
    const [activeTrend, setActiveTrend] = useState<string | null>(null);
    const [sentimentScore, setSentimentScore] = useState(50);
    const [posts, setPosts] = useState<SocialPost[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadSocialData() {
            setLoading(true);
            setError(null);
            try {
                const { data, error: fetchError } = await supabase
                    .from('social_posts')
                    .select('*')
                    .order('created_at', { ascending: false })
                    .limit(20);

                if (fetchError) throw fetchError;

                const mapped: SocialPost[] = (data || []).map((p) => ({
                    id: p.id,
                    user: p.user || '@unknown',
                    content: p.content || '',
                    likes: p.likes || 0,
                    shares: p.shares || 0,
                    platform: p.platform || 'Web',
                    sentiment: p.sentiment,
                    created_at: p.created_at,
                }));
                setPosts(mapped);

                if (mapped.length > 0) {
                    const positive = mapped.filter(p => p.sentiment === 'positive').length;
                    setSentimentScore(Math.round((positive / mapped.length) * 100));
                }
            } catch (err) {
                console.error('Failed to load social data:', err);
                setError('Erro ao carregar dados sociais');
            } finally {
                setLoading(false);
            }
        }

        loadSocialData();
    }, []);

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


    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">

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
                            <div className="text-3xl font-mono font-bold" style={{ color: sentimentScore > 60 ? 'var(--color-success)' : 'var(--color-error)' }}>
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

                {/* 2. SENTIMENT SUMMARY */}
                <div className="h-48 flex gap-4">
                    {loading ? (
                        <div className="flex-1 flex items-center justify-center">
                            <RefreshCw className="w-8 h-8 animate-spin text-[var(--color-primary)]" />
                        </div>
                    ) : posts.length === 0 ? (
                        <div className="flex-1 flex flex-col items-center justify-center bg-black/40 rounded-2xl border border-white/5">
                            <Inbox className="w-10 h-10 text-gray-600 mb-2" />
                            <p className="text-sm text-gray-500">Nenhum post encontrado</p>
                        </div>
                    ) : (
                        ['positive', 'neutral', 'negative'].map((sentiment, i) => {
                            const count = posts.filter(p => p.sentiment === sentiment).length;
                            const pct = posts.length > 0 ? Math.round((count / posts.length) * 100) : 0;
                            return (
                                <div 
                                    key={sentiment}
                                    onMouseEnter={() => setActiveTrend(sentiment)}
                                    onMouseLeave={() => setActiveTrend(null)}
                                    className={`
                                        flex-1 rounded-2xl border transition-all duration-500 cursor-pointer relative overflow-hidden flex flex-col items-center justify-center
                                        ${activeTrend === sentiment
                                            ? 'bg-[var(--color-primary)]/20 border-[var(--color-primary)] scale-105 z-10' 
                                            : 'bg-black/40 border-white/5 hover:bg-white/10'}
                                    `}
                                >
                                    <div 
                                        className="absolute w-32 h-32 rounded-full blur-2xl opacity-20 transition-all duration-1000"
                                        style={{
                                            background: sentiment === 'positive' ? 'var(--color-success)' : sentiment === 'negative' ? 'var(--color-error)' : 'var(--color-primary)',
                                            transform: activeTrend === sentiment ? 'scale(1.5)' : 'scale(1)'
                                        }}
                                    />
                                    
                                    <div className="relative z-10 text-center">
                                        <div className="text-xs text-gray-400 font-mono mb-1 uppercase">{sentiment}</div>
                                        <div className="text-3xl font-bold text-white">{pct}%</div>
                                        <div className="mt-2 flex items-center justify-center gap-1 text-xs font-mono">
                                            <TrendingUp className="w-3 h-3" />
                                            <span>{count} posts</span>
                                        </div>
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>
            </div>

            {/* DIREITA: LIVE FEED WATERFALL */}
            <div className="lg:w-1/3 w-full bg-[#02040a] border border-white/10 rounded-3xl p-0 overflow-hidden relative flex flex-col shadow-2xl">
                {/* Header */}
                <div className="p-6 border-b border-white/5 bg-black/20 backdrop-blur-xl z-10">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                            <Globe className="w-4 h-4" style={{ color: 'var(--color-accent)' }} />
                            Live Feed
                        </h3>
                        <div className="flex gap-2">
                            <span className="w-2 h-2 rounded-full animate-ping" style={{ background: 'var(--color-error)' }} />
                            <span className="text-[10px] font-bold" style={{ color: 'var(--color-error)' }}>LIVE</span>
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
                    
                    {loading ? (
                        <div className="flex items-center justify-center py-12">
                            <RefreshCw className="w-8 h-8 animate-spin text-[var(--color-primary)]" />
                        </div>
                    ) : error ? (
                        <div className="text-center py-12">
                            <p className="text-sm text-[var(--color-error)]">{error}</p>
                        </div>
                    ) : posts.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12">
                            <Inbox className="w-12 h-12 text-gray-600 mb-3" />
                            <p className="text-sm text-gray-500">Nenhum post social encontrado</p>
                            <p className="text-xs text-gray-600 mt-1">Os dados aparecerão aqui quando disponíveis</p>
                        </div>
                    ) : (
                        posts.map((post, i) => (
                            <div 
                                key={post.id}
                                className="bg-white/5 hover:bg-white/10 border border-white/5 hover:border-[var(--color-primary)]/30 rounded-xl p-4 transition-all duration-300 animate-slideInBottom group"
                                style={{ animationDelay: `${i * 0.1}s` }}
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center gap-2">
                                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-black border border-white/10 flex items-center justify-center font-bold text-xs text-white">
                                            {post.user.charAt(1)?.toUpperCase() || '?'}
                                        </div>
                                        <div>
                                            <div className="text-xs font-bold text-white group-hover:text-[var(--color-primary)] transition-colors">{post.user}</div>
                                            <div className="text-[10px] text-gray-500">{post.platform} • {post.created_at ? new Date(post.created_at).toLocaleString('pt-BR') : 'Recente'}</div>
                                        </div>
                                    </div>
                                    <Hash className="w-3 h-3 text-gray-600" />
                                </div>
                                
                                <p className="text-sm text-gray-300 leading-relaxed mb-3">
                                    {post.content}
                                </p>

                                <div className="flex gap-4 text-xs text-gray-500 font-mono">
                                    <div className="flex items-center gap-1 hover:text-[var(--color-error)] transition-colors cursor-pointer">
                                        <Heart className="w-3 h-3" /> {formatCount(post.likes)}
                                    </div>
                                    <div className="flex items-center gap-1 hover:text-[var(--color-primary)] transition-colors cursor-pointer">
                                        <Share2 className="w-3 h-3" /> {formatCount(post.shares)}
                                    </div>
                                    <div className="flex items-center gap-1 hover:text-white transition-colors cursor-pointer">
                                        <MessageCircle className="w-3 h-3" /> Reply
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                    
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
