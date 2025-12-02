/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - REQUESTS (FABRICATION DECK)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/requests/page.tsx
 * 📋 Interface de input holográfico para criar tarefas para agentes
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useRequests } from '@/hooks/useRequests';
import { useNotificationStore } from '@/stores/useNotificationStore';
import {
    Send, FileText, UploadCloud, Zap,
    Box, Cpu, CheckCircle2, Clock, AlertCircle
} from 'lucide-react';

interface RequestJob {
    id: number;
    title: string;
    status: 'processing' | 'queued' | 'completed';
    priority: 'high' | 'normal' | 'low';
    timestamp: string;
}

export default function RequestsPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Estados do Formulário
    const { requests, loading, createRequest } = useRequests();
    const { addNotification } = useNotificationStore();
    const [title, setTitle] = useState('');
    const [desc, setDesc] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    // 1. ENGINE VISUAL (HOLOGRAMA DE CONSTRUÇÃO)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        
        // Vértices de um cubo complexo (Hypercube simplificado)
        const vertices = [
            {x: -1, y: -1, z: -1}, {x: 1, y: -1, z: -1},
            {x: 1, y: 1, z: -1}, {x: -1, y: 1, z: -1},
            {x: -1, y: -1, z: 1}, {x: 1, y: -1, z: 1},
            {x: 1, y: 1, z: 1}, {x: -1, y: 1, z: 1}
        ];

        // Arestas
        const edges = [
            [0,1], [1,2], [2,3], [3,0], // Face Traseira
            [4,5], [5,6], [6,7], [7,4], // Face Frontal
            [0,4], [1,5], [2,6], [3,7]  // Conexões
        ];

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
            const cy = h / 2;

            ctx.clearRect(0, 0, w, h);
            time += 0.02;

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';

            // Animação baseada no input (Se digitando, gira mais rápido e fica complexo)
            const inputIntensity = Math.min(1, (title.length + desc.length) / 50);
            const rotationSpeed = 0.01 + (inputIntensity * 0.05);
            const scaleBase = 100 + (inputIntensity * 50);
            
            // Efeito de Materialização (Linhas tracejadas se pouco texto)
            ctx.setLineDash(inputIntensity < 0.5 ? [5, 15] : []);
            
            // Matrizes de Rotação
            const angleX = time * rotationSpeed;
            const angleY = time * rotationSpeed * 1.5;
            const sinX = Math.sin(angleX), cosX = Math.cos(angleX);
            const sinY = Math.sin(angleY), cosY = Math.cos(angleY);

            // Desenhar Cubo
            const projected = vertices.map(v => {
                // Rotação Y
                let x = v.x * cosY - v.z * sinY;
                let z = v.z * cosY + v.x * sinY;
                // Rotação X
                let y = v.y * cosX - z * sinX;
                z = z * cosX + v.y * sinX;

                // Perspectiva
                const scale = 400 / (400 + z);
                return {
                    x: cx + x * scaleBase * scale,
                    y: cy + y * scaleBase * scale
                };
            });

            ctx.strokeStyle = themeColor;
            ctx.lineWidth = 2;
            ctx.shadowBlur = 15;
            ctx.shadowColor = themeColor;

            edges.forEach(edge => {
                ctx.beginPath();
                ctx.moveTo(projected[edge[0]].x, projected[edge[0]].y);
                ctx.lineTo(projected[edge[1]].x, projected[edge[1]].y);
                ctx.stroke();
            });

            // Se submetendo, efeito de "Upload"
            if (isSubmitting) {
                ctx.fillStyle = themeColor;
                ctx.globalAlpha = Math.abs(Math.sin(time * 10));
                ctx.beginPath();
                ctx.arc(cx, cy, scaleBase * 1.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }

            requestAnimationFrame(render);
        };

        render();
        return () => window.removeEventListener('resize', resize);
    }, [title, desc, isSubmitting]);

    const handleSubmit = async () => {
        if (!title) {
            addNotification({
                type: 'warning',
                title: 'Missing Title',
                message: 'Please provide a directive title before initializing.',
            });
            return;
        }
        setIsSubmitting(true);

        try {
            await createRequest(title, desc, 'normal');
            addNotification({
                type: 'success',
                title: 'Request Created',
                message: `"${title}" has been successfully materialized.`,
            });
            setTitle('');
            setDesc('');
        } catch (err) {
            console.error('Failed to create request:', err);
            addNotification({
                type: 'error',
                title: 'Creation Failed',
                message: 'Failed to materialize request. Please try again.',
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* ESQUERDA: CONSOLE DE COMANDO (FORM) */}
            <div className="lg:w-1/2 w-full flex flex-col gap-6 relative z-10">
                
                <div className="flex-1 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-8 overflow-y-auto shadow-2xl flex flex-col relative overflow-hidden group">
                    
                    {/* Header */}
                    <div className="flex items-center gap-3 mb-8">
                        <div className="p-3 rounded-xl bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/30">
                            <Zap className="w-6 h-6 text-[var(--color-primary)]" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-white tracking-tight font-display">FABRICATION DECK</h1>
                            <p className="text-xs text-gray-400 font-mono uppercase">Initialize New Protocol</p>
                        </div>
                    </div>

                    {/* Inputs */}
                    <div className="space-y-6 flex-1">
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-gray-500 uppercase tracking-widest ml-1">Directive Title</label>
                            <input 
                                type="text" 
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                placeholder="Ex: Analyze Competitor Data..."
                                className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder-gray-600 focus:border-[var(--color-primary)] focus:bg-white/10 transition-all outline-none font-mono"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-xs font-bold text-gray-500 uppercase tracking-widest ml-1">Parameters / Context</label>
                            <textarea 
                                value={desc}
                                onChange={(e) => setDesc(e.target.value)}
                                placeholder="// Enter complex instructions here..."
                                className="w-full h-32 bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder-gray-600 focus:border-[var(--color-primary)] focus:bg-white/10 transition-all outline-none font-mono resize-none"
                            />
                        </div>

                        {/* Upload Zone */}
                        <div className="border-2 border-dashed border-white/10 rounded-xl p-6 flex flex-col items-center justify-center text-gray-500 hover:border-[var(--color-primary)]/50 hover:bg-[var(--color-primary)]/5 transition-all cursor-pointer group/upload">
                            <UploadCloud className="w-8 h-8 mb-2 group-hover/upload:text-[var(--color-primary)] transition-colors" />
                            <span className="text-xs uppercase font-bold tracking-wider">Drop Data Fragments Here</span>
                        </div>
                    </div>

                    {/* Footer Action */}
                    <div className="mt-8 pt-6 border-t border-white/10 flex justify-between items-center">
                        <div className="flex gap-2">
                            <span className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-pulse" />
                            <span className="text-xs text-[var(--color-primary)] font-mono">SYSTEM READY</span>
                        </div>
                        <button 
                            onClick={handleSubmit}
                            disabled={isSubmitting || !title}
                            className={`
                                px-8 py-3 rounded-xl font-bold text-sm tracking-widest uppercase transition-all flex items-center gap-2
                                ${isSubmitting 
                                    ? 'bg-gray-700 text-gray-400 cursor-not-allowed' 
                                    : 'bg-[var(--color-primary)] text-black hover:bg-[var(--color-accent)] hover:shadow-[0_0_20px_rgba(var(--color-primary-rgb),0.4)]'
                                }
                            `}
                        >
                            {isSubmitting ? 'MATERIALIZING...' : 'INITIALIZE'} <Send className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>

            {/* CENTRO: VISUALIZADOR HOLOGRÁFICO */}
            <div className="hidden lg:flex w-1/4 items-center justify-center relative">
                {/* Efeito de Tubo de Luz */}
                <div className="absolute inset-y-0 w-full bg-gradient-to-r from-transparent via-[var(--color-primary)]/5 to-transparent pointer-events-none blur-xl" />
                <canvas ref={canvasRef} className="w-full h-[400px]" />
            </div>

            {/* DIREITA: FILA DE PROCESSAMENTO (JOB QUEUE) */}
            <div className="lg:w-1/4 w-full flex flex-col h-full relative z-10">
                <div className="bg-[#02040a] border border-white/10 rounded-3xl p-0 overflow-hidden flex flex-col h-full shadow-2xl">
                    <div className="p-6 border-b border-white/5 bg-white/5">
                        <h2 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                            <Cpu className="w-4 h-4 text-purple-400" />
                            Active Queue
                        </h2>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin scrollbar-thumb-white/10">
                        {requests.map((job, index) => (
                            <div
                                key={job.id}
                                style={{
                                    animation: `slideInRight 0.4s ease-out ${index * 0.05}s both`
                                }}
                                className="group relative bg-black/40 border border-white/5 hover:border-[var(--color-primary)]/30 rounded-xl p-4 transition-all hover:translate-x-[-5px] hover:scale-105 cursor-pointer overflow-hidden"
                            >
                                {/* Hover Preview Overlay */}
                                <div className="absolute inset-0 bg-gradient-to-r from-[var(--color-primary)]/0 via-[var(--color-primary)]/5 to-[var(--color-primary)]/0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                                <div className="flex justify-between items-start mb-2">
                                    <div className="p-2 rounded-lg bg-white/5 text-gray-300 group-hover:text-[var(--color-primary)] transition-colors">
                                        <Box className="w-4 h-4" />
                                    </div>
                                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase border ${
                                        job.status === 'processing' ? 'text-yellow-400 border-yellow-400/30 bg-yellow-400/10' :
                                        job.status === 'completed' ? 'text-green-400 border-green-400/30 bg-green-400/10' :
                                        'text-blue-400 border-blue-400/30 bg-blue-400/10'
                                    }`}>
                                        {job.status}
                                    </span>
                                </div>
                                <h3 className="font-bold text-white text-sm mb-1 truncate">{job.title}</h3>
                                <div className="flex items-center gap-2 text-xs text-gray-500 font-mono">
                                    <Clock className="w-3 h-3" /> {job.timestamp}
                                </div>
                                
                                {/* Progress Bar (Fake) */}
                                {job.status === 'processing' && (
                                    <div className="mt-3 h-1 w-full bg-white/10 rounded-full overflow-hidden">
                                        <div className="h-full bg-yellow-400 w-2/3 animate-pulse" />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <style jsx>{`
                @keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
                .animate-slideInRight { animation: slideInRight 0.3s ease-out forwards; }
            `}</style>
        </div>
    );
}



