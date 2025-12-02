/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - EVOLUTION LAB (GENESIS EDITION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/evolution/page.tsx
 * 📋 Simulação de DNA Digital e Algoritmos Genéticos
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useAgents } from '@/hooks/useAgents';
import {
    Dna, GitBranch, Zap, RefreshCw,
    TrendingUp, AlertTriangle, CheckCircle, Microscope
} from 'lucide-react';

export default function EvolutionPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const { agents, loading } = useAgents();

    // Calcular stats REAIS dos agents
    const avgEfficiency = agents.length > 0
        ? agents.reduce((sum, a) => sum + a.efficiency, 0) / agents.length
        : 87.4;

    const mutationsByRole = agents.reduce((acc, agent) => {
        acc[agent.role] = (acc[agent.role] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);

    // Estado da Simulação
    const [generation, setGeneration] = useState(agents.length || 12);
    const [fitness, setFitness] = useState(avgEfficiency);
    const [mutationRate, setMutationRate] = useState(0.05);
    const [isEvolving, setIsEvolving] = useState(false);
    const [logs, setLogs] = useState<string[]>([]);

    // Atualizar fitness quando agents mudarem
    useEffect(() => {
        if (agents.length > 0) {
            setFitness(avgEfficiency);
            setGeneration(agents.length);
        }
    }, [agents, avgEfficiency]);

    // 1. ENGINE VISUAL (DNA HELIX)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        // Configuração do DNA
        const strands = 2; // Dupla hélice
        const particlesPerStrand = 40;
        const particles: {y: number, offset: number}[] = [];

        for(let i=0; i<particlesPerStrand; i++) {
            particles.push({
                y: i * 15, // Espaçamento vertical
                offset: i * 0.2 // Defasagem da onda
            });
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
            const cx = w / 2;
            
            // Limpar
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'; // Trail suave
            ctx.fillRect(0, 0, w, h);

            // Velocidade baseada no estado
            time += isEvolving ? 0.15 : 0.02;

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
            const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--color-accent').trim() || '#0EA5E9';

            // Desenhar Hélice
            particles.forEach((p, i) => {
                const y = p.y + (h/2 - (particlesPerStrand * 15)/2); // Centralizar verticalmente
                
                // Largura da hélice (pulsa se estiver evoluindo)
                const amplitude = isEvolving ? 120 + Math.sin(time * 10)*20 : 100;

                // Calcular posições X das duas fitas
                const x1 = cx + Math.sin(time + p.offset) * amplitude;
                const x2 = cx + Math.sin(time + p.offset + Math.PI) * amplitude; // +PI para oposto (180 graus)

                // Profundidade (Z) simulada pelo tamanho/cor
                const z1 = Math.cos(time + p.offset); 
                const z2 = Math.cos(time + p.offset + Math.PI);

                // Desenhar Conexões (Pares de Base)
                if (i % 2 === 0) { // Apenas a cada 2 pontos para não poluir
                    ctx.beginPath();
                    ctx.moveTo(x1, y);
                    ctx.lineTo(x2, y);
                    ctx.strokeStyle = `rgba(255, 255, 255, 0.1)`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }

                // Desenhar Fita 1
                const size1 = 3 + z1 * 2;
                const alpha1 = 0.5 + z1 * 0.4;
                ctx.beginPath();
                ctx.arc(x1, y, size1, 0, Math.PI * 2);
                ctx.fillStyle = isEvolving && Math.random() > 0.8 ? '#FFF' : themeColor; // Flash branco na evolução
                ctx.globalAlpha = alpha1;
                ctx.shadowBlur = isEvolving ? 20 : 10;
                ctx.shadowColor = themeColor;
                ctx.fill();

                // Desenhar Fita 2
                const size2 = 3 + z2 * 2;
                const alpha2 = 0.5 + z2 * 0.4;
                ctx.beginPath();
                ctx.arc(x2, y, size2, 0, Math.PI * 2);
                ctx.fillStyle = isEvolving && Math.random() > 0.8 ? '#FFF' : accentColor;
                ctx.globalAlpha = alpha2;
                ctx.shadowColor = accentColor;
                ctx.fill();

                // Reset
                ctx.globalAlpha = 1;
                ctx.shadowBlur = 0;
            });

            animationId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [isEvolving]);

    // 2. SIMULAÇÃO DE DADOS
    const handleEvolve = () => {
        if(isEvolving) return;
        setIsEvolving(true);
        setLogs(prev => ["Iniciando sequência de mutação genética...", ...prev]);

        let steps = 0;
        const interval = setInterval(() => {
            steps++;
            
            // Atualizar dados aleatoriamente
            setFitness(prev => Math.min(99.9, prev + (Math.random() - 0.3)));
            setGeneration(prev => prev + 1);
            
            // Logs fake
            if(Math.random() > 0.7) {
                const mutations = ['Optimizing Neural Weights', 'Pruning Synapses', 'Recompiling Kernel', 'Genetic Drift Detected'];
                setLogs(prev => [`> ${mutations[Math.floor(Math.random()*mutations.length)]} [OK]`, ...prev].slice(0, 8));
            }

            if(steps > 20) {
                clearInterval(interval);
                setIsEvolving(false);
                setLogs(prev => ["Evolução concluída. Sistema estável.", ...prev]);
            }
        }, 150);
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* ESQUERDA: O DNA VISUALIZER */}
            <div className="lg:w-2/3 w-full h-full relative rounded-3xl overflow-hidden border border-white/10 bg-[#02040a] group shadow-2xl flex flex-col">
                
                {/* Header Flutuante */}
                <div className="absolute top-6 left-6 z-20">
                    <div className="flex items-center gap-3 mb-2">
                        <div className={`p-2 rounded-lg border ${isEvolving ? 'bg-purple-500/20 border-purple-500 text-purple-400 animate-pulse' : 'bg-[var(--color-primary)]/10 border-[var(--color-primary)] text-[var(--color-primary)]'}`}>
                            <Dna className="w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-white tracking-tight font-display">GENESIS CHAMBER</h1>
                            <p className="text-xs text-gray-400 font-mono uppercase tracking-widest">Genetic Algorithm v9.2</p>
                        </div>
                    </div>
                </div>

                {/* CANVAS */}
                <canvas ref={canvasRef} className="flex-1 w-full h-full cursor-crosshair" />

                {/* Footer de Controle */}
                <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/90 to-transparent flex items-end justify-between">
                    <div className="flex gap-8">
                        <div>
                            <div className="text-[10px] text-gray-500 font-mono uppercase mb-1">Generation</div>
                            <div className="text-3xl font-mono text-white tabular-nums">
                                #{generation.toLocaleString()}
                            </div>
                        </div>
                        <div>
                            <div className="text-[10px] text-gray-500 font-mono uppercase mb-1">Fitness Score</div>
                            <div className={`text-3xl font-mono tabular-nums flex items-center gap-2 ${fitness > 90 ? 'text-emerald-400' : 'text-[var(--color-primary)]'}`}>
                                {fitness.toFixed(1)}%
                                {isEvolving && <TrendingUp className="w-5 h-5 animate-bounce" />}
                            </div>
                        </div>
                    </div>

                    <button 
                        onClick={handleEvolve}
                        disabled={isEvolving}
                        className={`
                            px-8 py-4 rounded-xl font-bold text-sm tracking-widest uppercase transition-all
                            flex items-center gap-3
                            ${isEvolving 
                                ? 'bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700' 
                                : 'bg-[var(--color-primary)] text-black hover:bg-[var(--color-accent)] shadow-[0_0_30px_rgba(var(--color-primary-rgb),0.3)] hover:scale-105'
                            }
                        `}
                    >
                        {isEvolving ? (
                            <><RefreshCw className="w-5 h-5 animate-spin" /> MUTATING...</>
                        ) : (
                            <><Zap className="w-5 h-5" /> DEPLOY EVOLUTION</>
                        )}
                    </button>
                </div>
            </div>

            {/* DIREITA: PAINEL DE DADOS (GENÉTICA) */}
            <div className="lg:w-1/3 w-full h-full flex flex-col gap-4">

                {/* Loading State */}
                {loading && (
                    <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex items-center justify-center gap-3">
                        <RefreshCw className="w-5 h-5 text-[var(--color-primary)] animate-spin" />
                        <span className="text-gray-400 font-mono text-sm">Loading Genetic Data...</span>
                    </div>
                )}

                {/* Card: Mutations by Role */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex-shrink-0">
                    <div className="flex items-center gap-2 mb-6 text-white/80">
                        <Microscope className="w-5 h-5 text-[var(--color-secondary)]" />
                        <span className="font-bold text-sm tracking-wider">MUTATIONS BY ROLE</span>
                    </div>

                    <div className="space-y-4">
                        {Object.entries(mutationsByRole).length > 0 ? (
                            Object.entries(mutationsByRole).map(([role, count]) => (
                                <div key={role}>
                                    <div className="flex justify-between text-xs mb-2">
                                        <span className="text-gray-400 uppercase font-mono">{role}</span>
                                        <span className="text-white font-mono">{count} units</span>
                                    </div>
                                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)]"
                                            style={{ width: `${(count / agents.length) * 100}%` }}
                                        />
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="text-center text-gray-600 text-sm italic">
                                No agents detected
                            </div>
                        )}
                    </div>
                </div>

                {/* Card: Status Atual */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex-1 flex flex-col">
                    <div className="flex items-center gap-2 mb-6 text-white/80">
                        <TrendingUp className="w-5 h-5 text-emerald-400" />
                        <span className="font-bold text-sm tracking-wider">SYSTEM PARAMETERS</span>
                    </div>

                    <div className="space-y-6 flex-1">
                        {/* Stat 1 */}
                        <div>
                            <div className="flex justify-between text-xs mb-2">
                                <span className="text-gray-400">Mutation Rate</span>
                                <span className="text-white font-mono">{(mutationRate * 100).toFixed(1)}%</span>
                            </div>
                            <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-purple-500" style={{ width: `${mutationRate * 1000}%` }} />
                            </div>
                            <div className="flex justify-between mt-1">
                                <button onClick={() => setMutationRate(Math.max(0, mutationRate - 0.01))} className="text-gray-600 hover:text-white">-</button>
                                <button onClick={() => setMutationRate(Math.min(0.2, mutationRate + 0.01))} className="text-gray-600 hover:text-white">+</button>
                            </div>
                        </div>

                        {/* Stat 2 */}
                        <div>
                            <div className="flex justify-between text-xs mb-2">
                                <span className="text-gray-400">Avg Efficiency (Real)</span>
                                <span className="text-emerald-400 font-mono">{avgEfficiency.toFixed(1)}%</span>
                            </div>
                            <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500" style={{ width: `${avgEfficiency}%` }} />
                            </div>
                        </div>

                        {/* Stat 3 */}
                        <div>
                            <div className="flex justify-between text-xs mb-2">
                                <span className="text-gray-400">Total Agents</span>
                                <span className="text-[var(--color-primary)] font-mono">{agents.length}</span>
                            </div>
                            <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-[var(--color-primary)]" style={{ width: `${Math.min(100, (agents.length / 20) * 100)}%` }} />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Card: Logs de Compilação */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 h-1/2 flex flex-col">
                    <div className="flex items-center gap-2 mb-4 text-white/80">
                        <GitBranch className="w-5 h-5 text-[var(--color-primary)]" />
                        <span className="font-bold text-sm tracking-wider">EVOLUTION LOGS</span>
                    </div>
                    
                    <div className="flex-1 overflow-hidden relative font-mono text-xs space-y-2">
                        <div className="absolute inset-0 overflow-y-auto scrollbar-hide">
                            {logs.length === 0 && <span className="text-gray-600 italic">Awaiting initialization...</span>}
                            {logs.map((log, i) => (
                                <div key={i} className="flex gap-2 animate-fadeIn">
                                    <span className="text-gray-600">[{new Date().toLocaleTimeString()}]</span>
                                    <span className={log.includes('Error') ? 'text-red-400' : 'text-[var(--color-text-secondary)]'}>
                                        {log}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </div>

            <style jsx>{`
                @keyframes fadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
                .animate-fadeIn { animation: fadeIn 0.2s ease-out; }
            `}</style>
        </div>
    );
}
