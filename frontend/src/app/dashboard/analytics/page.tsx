/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ANALYTICS (OMNISCIENCE FIELD)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/analytics/page.tsx
 * 📋 Terreno 3D de dados (Data Scape) e previsões preditivas
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    BarChart3, TrendingUp, Activity, 
    Eye, AlertTriangle, BrainCircuit 
} from 'lucide-react';

export default function AnalyticsPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estados
    const [growth, setGrowth] = useState(124.5);
    const [users, setUsers] = useState(45231);
    const [prediction, setPrediction] = useState("Stable Growth");
    const [anomaly, setAnomaly] = useState(false);

    // 1. ENGINE VISUAL (DATA SCAPE 3D)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        const GRID_SIZE = 40; // Tamanho da célula
        const ROWS = 30;
        const COLS = 40;
        
        // Matriz de altura do terreno
        const terrain: number[][] = [];
        for(let r=0; r<ROWS; r++) {
            terrain[r] = [];
            for(let c=0; c<COLS; c++) {
                terrain[r][c] = 0;
            }
        }

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
            
            // Limpar com Fade (Céu noturno)
            const bg = getComputedStyle(document.documentElement).getPropertyValue('--color-background').trim();
            ctx.fillStyle = bg === '#F8FAFC' ? '#F1F5F9' : '#020617'; // Ajuste para tema claro/escuro
            ctx.fillRect(0, 0, w, h);

            time += 0.05;

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
            const errorColor = '#EF4444';

            // 1. ATUALIZAR DADOS DO TERRENO (Simulação de Tráfego)
            // Mover linhas para baixo (efeito de scroll infinito)
            for(let r=ROWS-1; r>0; r--) {
                for(let c=0; c<COLS; c++) {
                    terrain[r][c] = terrain[r-1][c];
                }
            }
            // Gerar nova linha no topo (Horizonte)
            for(let c=0; c<COLS; c++) {
                // Perlin Noise simplificado (Senoide combinada)
                const noise = Math.sin(c * 0.2 + time) * Math.cos(c * 0.5 - time) * 50;
                // Pico aleatório (Tráfego)
                const spike = Math.random() > 0.95 ? Math.random() * 100 : 0;
                terrain[0][c] = Math.max(0, noise + spike + 20);
                
                // Detectar anomalia visualmente
                if (spike > 80) setAnomaly(true);
                else if (Math.random() > 0.9) setAnomaly(false);
            }

            // 2. DESENHAR TERRENO (RETRO-WAVE GRID)
            ctx.lineWidth = 1;
            
            // Perspectiva isométrica central
            const centerX = w / 2;
            const centerY = h / 2;
            
            for(let r=0; r<ROWS; r++) {
                ctx.beginPath();
                
                let isRowAnomaly = false;

                for(let c=0; c<COLS; c++) {
                    // Transformação 3D -> 2D
                    // X: Espalhar horizontalmente baseado na linha (trapézio)
                    // Y: Descer na tela + Altura do dado (Z)
                    
                    const perspective = (r / ROWS); // 0 (longe) a 1 (perto)
                    const widthScale = 0.2 + perspective * 2; // Fica mais largo perto da tela
                    
                    const x = centerX + (c - COLS/2) * GRID_SIZE * widthScale;
                    const y = centerY - 100 + (r * 20 * perspective) - (terrain[r][c] * perspective);

                    // Se o valor for muito alto, pintar de vermelho
                    if (terrain[r][c] > 80) isRowAnomaly = true;

                    if (c === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }

                // Estilo da Linha
                ctx.strokeStyle = isRowAnomaly ? errorColor : themeColor;
                ctx.globalAlpha = (r / ROWS); // Fade out no horizonte
                
                // Glow
                ctx.shadowBlur = isRowAnomaly ? 20 : 10;
                ctx.shadowColor = isRowAnomaly ? errorColor : themeColor;
                
                ctx.stroke();
                ctx.shadowBlur = 0; // Reset
            }

            // Linhas Verticais (Conectando o grid)
            // Opcional: Removido para visual mais limpo ("Scanlines horizontais")

            // 3. DESENHAR "SOL" (HORIZONTE DE DADOS) - Apenas estética
            /*
            const sunY = centerY - 150;
            const sunGrad = ctx.createRadialGradient(centerX, sunY, 0, centerX, sunY, 200);
            sunGrad.addColorStop(0, themeColor);
            sunGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = sunGrad;
            ctx.globalAlpha = 0.2;
            ctx.beginPath();
            ctx.arc(centerX, sunY, 200, 0, Math.PI * 2);
            ctx.fill();
            */

            requestAnimationFrame(render);
        };

        render();

        return () => window.removeEventListener('resize', resize);
    }, []);

    // Simulador de Números
    useEffect(() => {
        const interval = setInterval(() => {
            setUsers(prev => prev + Math.floor(Math.random() * 5));
            setGrowth(prev => prev + (Math.random() - 0.4));
            
            // Mudar previsão aleatoriamente
            if(Math.random() > 0.9) {
                const preds = ["Exponential Spike", "Stable Plateau", "Market Correction", "Neural Optimization"];
                setPrediction(preds[Math.floor(Math.random() * preds.length)]);
            }
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col gap-6 p-2 overflow-hidden relative">
            
            {/* FUNDO (DATA SCAPE 3D) */}
            <div className="absolute inset-0 rounded-3xl overflow-hidden bg-[#020617] border border-white/10 shadow-2xl -z-10">
                <canvas ref={canvasRef} className="w-full h-full" />
                {/* Vignette Suave */}
                <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/80 pointer-events-none" />
                {/* Grid Overlay Textura */}
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />
            </div>

            {/* CAMADA SUPERIOR: HEADER & KPIs */}
            <div className="flex flex-col md:flex-row justify-between items-end px-8 pt-8 pb-4 relative z-10">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <BarChart3 className="w-8 h-8 text-[var(--color-primary)]" />
                        <h1 className="text-4xl font-black text-white tracking-tight font-display drop-shadow-lg">
                            OMNISCIENCE
                        </h1>
                    </div>
                    <p className="text-sm text-gray-400 font-mono uppercase tracking-widest">
                        Predictive Analytics Module v9.0
                    </p>
                </div>

                {/* Alerta de Anomalia */}
                <div className={`
                    px-6 py-3 rounded-xl border backdrop-blur-md transition-all duration-500 flex items-center gap-3
                    ${anomaly 
                        ? 'bg-red-500/20 border-red-500 text-red-400 animate-pulse' 
                        : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'}
                `}>
                    {anomaly ? <AlertTriangle className="w-5 h-5" /> : <CheckCircleIcon className="w-5 h-5" />}
                    <span className="font-bold font-mono text-sm">
                        {anomaly ? 'DATA ANOMALY DETECTED' : 'SYSTEM NOMINAL'}
                    </span>
                </div>
            </div>

            {/* CAMADA CENTRAL: CARDS FLUTUANTES */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 px-8 relative z-10">
                
                {/* Card 1: Growth */}
                <div className="group bg-black/40 backdrop-blur-lg border border-white/10 rounded-2xl p-6 hover:border-[var(--color-primary)]/50 transition-all duration-500">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 rounded-xl bg-[var(--color-primary)]/10 text-[var(--color-primary)]">
                            <TrendingUp className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-bold bg-green-500/20 text-green-400 px-2 py-1 rounded">+12%</span>
                    </div>
                    <div className="text-4xl font-bold text-white font-mono">{growth.toFixed(2)}%</div>
                    <div className="text-xs text-gray-400 mt-1 uppercase tracking-wider">Growth Velocity</div>
                    
                    {/* Mini Sparkline (CSS) */}
                    <div className="mt-4 flex items-end gap-1 h-8 opacity-50 group-hover:opacity-100 transition-opacity">
                        {Array.from({length: 15}).map((_, i) => (
                            <div 
                                key={i} 
                                className="flex-1 bg-[var(--color-primary)] rounded-t-sm"
                                style={{ height: `${20 + Math.random() * 80}%` }}
                            />
                        ))}
                    </div>
                </div>

                {/* Card 2: Active Users */}
                <div className="group bg-black/40 backdrop-blur-lg border border-white/10 rounded-2xl p-6 hover:border-purple-500/50 transition-all duration-500">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400">
                            <Eye className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-bold bg-purple-500/20 text-purple-400 px-2 py-1 rounded">LIVE</span>
                    </div>
                    <div className="text-4xl font-bold text-white font-mono">{users.toLocaleString()}</div>
                    <div className="text-xs text-gray-400 mt-1 uppercase tracking-wider">Active Sentience</div>
                    
                    {/* Pulse Dot */}
                    <div className="mt-6 flex items-center gap-2 text-xs text-gray-500">
                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-ping" />
                        Synchronizing global nodes...
                    </div>
                </div>

                {/* Card 3: AI Prediction */}
                <div className="group bg-black/40 backdrop-blur-lg border border-white/10 rounded-2xl p-6 hover:border-yellow-500/50 transition-all duration-500 relative overflow-hidden">
                    {/* AI Gradient BG */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-yellow-500/10 blur-3xl rounded-full pointer-events-none" />
                    
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 rounded-xl bg-yellow-500/10 text-yellow-400">
                            <BrainCircuit className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-bold bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">AI FORECAST</span>
                    </div>
                    <div className="text-2xl font-bold text-white font-display leading-tight mb-2">
                        "{prediction}"
                    </div>
                    <div className="text-xs text-gray-400 uppercase tracking-wider">Confidence: 98.4%</div>
                    
                    <div className="mt-4 w-full bg-white/10 h-1 rounded-full overflow-hidden">
                        <div className="h-full bg-yellow-400 w-[98%] animate-pulse" />
                    </div>
                </div>

            </div>

            {/* RODAPÉ: LOGS DE ANÁLISE (Terminal Style) */}
            <div className="absolute bottom-0 left-0 right-0 bg-black/60 backdrop-blur-xl border-t border-white/10 p-3 px-8 z-20 flex justify-between items-center text-xs font-mono text-gray-500">
                <div className="flex items-center gap-4">
                    <Activity className="w-4 h-4 text-[var(--color-primary)]" />
                    <span>Ingesting 4.2TB/s</span>
                    <span className="hidden md:inline text-gray-700">|</span>
                    <span className="hidden md:inline">Processing Neural Weights...</span>
                </div>
                <div>
                    LATENCY: <span className="text-white">12ms</span>
                </div>
            </div>

        </div>
    );
}

// Ícone auxiliar
function CheckCircleIcon({className}: {className?: string}) {
    return (
        <svg className={className} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
    );
}
