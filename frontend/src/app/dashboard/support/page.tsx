/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SUPPORT OPS (CRISIS CENTER) - ENTERPRISE v10
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/support/page.tsx
 * 📋 Colmeia de Tickets Hexagonais e Triagem por IA - DADOS REAIS
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import {
    LifeBuoy, CheckCircle, Clock, AlertOctagon,
    Bot, User, MessageSquare, Zap, Activity, X, ExternalLink
} from 'lucide-react';
import { useSupport } from '@/hooks/useSupport';
import { Skeleton } from '@/components/ui/SkeletonLoader';
import type { SupportTicket } from '@/stores';

interface HexTicket extends SupportTicket {
    x: number;
    y: number;
}

interface TicketModalProps {
    ticket: SupportTicket | null;
    onClose: () => void;
}

function TicketModal({ ticket, onClose }: TicketModalProps) {
    if (!ticket) return null;

    const statusColors = {
        open: { bg: 'var(--color-error)/10', border: 'var(--color-error)/30', text: 'var(--color-error)' },
        in_progress: { bg: 'var(--color-warning)/10', border: 'var(--color-warning)/30', text: 'var(--color-warning)' },
        resolved: { bg: 'var(--color-success)/10', border: 'var(--color-success)/30', text: 'var(--color-success)' },
        closed: { bg: 'rgba(107, 114, 128, 0.1)', border: 'rgba(107, 114, 128, 0.3)', text: '#9CA3AF' },
    };

    const priorityColors = {
        low: 'var(--color-primary)',
        normal: '#9CA3AF',
        high: 'var(--color-warning)',
        critical: 'var(--color-error)',
    };

    const colors = statusColors[ticket.status];

    return (
        <div className="fixed inset-0 z-[9998] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
            <div className="relative w-full max-w-2xl backdrop-blur-xl rounded-3xl p-8 shadow-2xl" style={{ background: colors.bg, border: `1px solid ${colors.border}` }}>
                {/* Close Button */}
                <button
                    onClick={onClose}
                    className="absolute top-6 right-6 text-gray-400 hover:text-white transition-colors"
                >
                    <X className="w-6 h-6" />
                </button>

                {/* Header */}
                <div className="flex items-start gap-4 mb-6">
                    <div className="p-3 rounded-xl" style={{ background: colors.bg, border: `1px solid ${colors.border}` }}>
                        <LifeBuoy className="w-8 h-8" style={{ color: colors.text }} />
                    </div>
                    <div className="flex-1">
                        <h2 className="text-2xl font-bold text-white mb-1">{ticket.title}</h2>
                        <div className="flex gap-2 text-xs">
                            <span className="px-2 py-1 rounded uppercase font-bold" style={{ background: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
                                {ticket.status.replace('_', ' ')}
                            </span>
                            <span className="px-2 py-1 rounded bg-white/5 border border-white/10 uppercase font-bold" style={{ color: priorityColors[ticket.priority] }}>
                                {ticket.priority}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Description */}
                <div className="mb-6">
                    <h3 className="text-sm font-bold text-gray-400 uppercase mb-2">Description</h3>
                    <p className="text-white leading-relaxed">{ticket.description || 'No description provided'}</p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="bg-white/5 rounded-xl p-4">
                        <div className="text-xs text-gray-400 uppercase mb-1">Sentiment Score</div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-bold text-white">{ticket.sentiment}/100</span>
                            <Activity className="w-4 h-4" style={{ color: ticket.sentiment > 70 ? 'var(--color-success)' : ticket.sentiment > 40 ? 'var(--color-warning)' : 'var(--color-error)' }} />
                        </div>
                        {/* Sentiment Bar */}
                        <div className="mt-2 h-2 w-full bg-black/50 rounded-full overflow-hidden">
                            <div
                                className="h-full transition-all"
                                style={{
                                    width: `${ticket.sentiment}%`,
                                    background: ticket.sentiment > 70 ? 'var(--color-success)' : ticket.sentiment > 40 ? 'var(--color-warning)' : 'var(--color-error)'
                                }}
                            />
                        </div>
                    </div>

                    <div className="bg-white/5 rounded-xl p-4">
                        <div className="text-xs text-gray-400 uppercase mb-1">Created</div>
                        <div className="text-lg font-mono text-white">
                            {new Date(ticket.created_at).toLocaleDateString()}
                        </div>
                        <div className="text-xs text-gray-500 font-mono">
                            {new Date(ticket.created_at).toLocaleTimeString()}
                        </div>
                    </div>
                </div>

                {/* Actions */}
                <div className="flex gap-3">
                    <button className="flex-1 bg-[var(--color-primary)] hover:bg-[var(--color-primary)]/80 text-black font-bold py-3 px-6 rounded-xl transition-all">
                        Assign to AI Agent
                    </button>
                    <button className="px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white transition-all">
                        View Details
                        <ExternalLink className="w-4 h-4 inline ml-2" />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default function SupportPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [hexTickets, setHexTickets] = useState<HexTicket[]>([]);
    const [activeTicket, setActiveTicket] = useState<SupportTicket | null>(null);

    const { tickets, stats, loading } = useSupport();

    // 1. ENGINE VISUAL (THE HIVE)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Configuração da Colmeia
        const HEX_SIZE = 30;
        const GAP = 4;
        const COLS = 12;
        const ROWS = 8;

        // Inicializar Grid de Tickets com dados REAIS
        const initialHexTickets: HexTicket[] = [];
        const maxVisibleTickets = COLS * ROWS;
        const visibleTickets = tickets.slice(0, maxVisibleTickets);

        let hexIndex = 0;
        for(let r=0; r<ROWS; r++) {
            for(let c=0; c<COLS; c++) {
                // Posição Hexagonal
                const xOffset = (r % 2 === 0) ? 0 : (HEX_SIZE + GAP) * Math.sqrt(3) / 2;
                const x = c * (HEX_SIZE * Math.sqrt(3) + GAP) + xOffset + 50;
                const y = r * (HEX_SIZE * 1.5 + GAP) + 50;

                if (hexIndex < visibleTickets.length) {
                    const ticket = visibleTickets[hexIndex];
                    initialHexTickets.push({
                        ...ticket,
                        x,
                        y
                    });
                    hexIndex++;
                }
            }
        }
        setHexTickets(initialHexTickets);

        let time = 0;
        let aiLaser = { active: false, targetX: 0, targetY: 0, progress: 0 };

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        // Loop de Renderização
        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            ctx.clearRect(0, 0, w, h);
            time += 0.02;

            // Desenhar Tickets (Hexágonos)
            initialHexTickets.forEach(t => {
                // Cor baseada no status REAL
                let color = '#374151'; // Default Gray
                let glow = false;

                if(t.status === 'resolved' || t.status === 'closed') color = '#10B981'; // Verde
                else if(t.status === 'in_progress') color = '#F59E0B'; // Amarelo
                else if(t.status === 'open' && t.priority === 'critical') {
                    color = '#EF4444'; // Vermelho
                    glow = true;
                }
                else if(t.status === 'open') color = '#F59E0B'; // Orange

                // Animação de pulso para críticos
                const pulse = glow ? Math.sin(time * 5) * 0.2 + 1 : 1;

                // Desenhar Hexágono
                ctx.beginPath();
                for (let i = 0; i < 6; i++) {
                    const angle = 2 * Math.PI / 6 * i;
                    const hx = t.x + HEX_SIZE * pulse * Math.cos(angle);
                    const hy = t.y + HEX_SIZE * pulse * Math.sin(angle);
                    if (i === 0) ctx.moveTo(hx, hy);
                    else ctx.lineTo(hx, hy);
                }
                ctx.closePath();

                ctx.fillStyle = color;
                ctx.shadowBlur = glow ? 15 : 0;
                ctx.shadowColor = color;
                ctx.globalAlpha = (t.status === 'resolved' || t.status === 'closed') ? 0.3 : 0.8;
                ctx.fill();

                // Reset
                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1;
            });

            // --- IA INTERVENTION (O LASER) ---
            if(Math.random() > 0.98 && !aiLaser.active) {
                // Escolher um alvo open/in_progress
                const target = initialHexTickets.find(t => t.status === 'open' || t.status === 'in_progress');
                if(target) {
                    aiLaser = { active: true, targetX: target.x, targetY: target.y, progress: 0 };
                }
            }

            if(aiLaser.active) {
                aiLaser.progress += 0.1;

                // Origem do Laser (Centro superior)
                const startX = w / 2;
                const startY = -50;

                // Desenhar Raio
                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(aiLaser.targetX, aiLaser.targetY);

                const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
                ctx.strokeStyle = themeColor;
                ctx.lineWidth = 2 * (1 - aiLaser.progress);
                ctx.shadowBlur = 20;
                ctx.shadowColor = themeColor;
                ctx.stroke();

                // Efeito de Impacto
                ctx.beginPath();
                ctx.arc(aiLaser.targetX, aiLaser.targetY, 10 * aiLaser.progress, 0, Math.PI * 2);
                ctx.fillStyle = '#FFFFFF';
                ctx.globalAlpha = 1 - aiLaser.progress;
                ctx.fill();
                ctx.globalAlpha = 1;

                // Terminar Laser
                if(aiLaser.progress >= 1) {
                    aiLaser.active = false;
                }
            }

            requestAnimationFrame(render);
        };

        render();
        return () => window.removeEventListener('resize', resize);
    }, [tickets]);

    // Handle click on canvas (detect hex click)
    const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;

        // Check if click is within any hex
        for (const hex of hexTickets) {
            const distance = Math.sqrt(Math.pow(clickX - hex.x, 2) + Math.pow(clickY - hex.y, 2));
            if (distance < 30) {
                setActiveTicket(hex);
                break;
            }
        }
    };

    if (loading && tickets.length === 0) {
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

    const autoResolutionRate = stats.resolved > 0
        ? ((stats.resolved / stats.total) * 100).toFixed(1)
        : '0.0';

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">

            {/* ESQUERDA: THE HIVE (VISUALIZER) */}
            <div className="lg:w-2/3 w-full h-full relative rounded-3xl overflow-hidden border border-white/10 bg-[#02040a] group shadow-2xl">

                {/* Header Flutuante */}
                <div className="absolute top-6 left-6 z-20">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg" style={{ background: 'var(--color-primary)/10', border: '1px solid var(--color-primary)/30', color: 'var(--color-primary)' }}>
                            <LifeBuoy className="w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-white tracking-tight font-display">SUPPORT HIVE</h1>
                            <p className="text-xs text-gray-400 font-mono uppercase">
                                {tickets.length > 0 ? `${tickets.length} Tickets Loaded • Click to View` : 'No tickets • System Ready'}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Legenda */}
                <div className="absolute bottom-6 left-6 z-20 flex gap-4 text-xs font-mono font-bold">
                    <div className="flex items-center gap-2" style={{ color: 'var(--color-error)' }}>
                        <div className="w-3 h-3 rounded-sm shadow-[0_0_10px_var(--color-error)]" style={{ background: 'var(--color-error)' }} /> CRITICAL ({stats.critical_count})
                    </div>
                    <div className="flex items-center gap-2" style={{ color: 'var(--color-warning)' }}>
                        <div className="w-3 h-3 rounded-sm" style={{ background: 'var(--color-warning)' }} /> PENDING ({stats.in_progress})
                    </div>
                    <div className="flex items-center gap-2" style={{ color: 'var(--color-success)' }}>
                        <div className="w-3 h-3 rounded-sm opacity-30" style={{ background: 'var(--color-success)' }} /> SOLVED ({stats.resolved})
                    </div>
                </div>

                {/* CANVAS */}
                <canvas
                    ref={canvasRef}
                    className="w-full h-full cursor-pointer"
                    onClick={handleCanvasClick}
                />

                {/* Overlay Tech */}
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />

                {/* Empty State */}
                {tickets.length === 0 && !loading && (
                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center">
                            <LifeBuoy className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-gray-400 mb-2">No Support Tickets</h3>
                            <p className="text-sm text-gray-500">System is running smoothly</p>
                        </div>
                    </div>
                )}
            </div>

            {/* DIREITA: DADOS E LIVE FEED */}
            <div className="lg:w-1/3 w-full flex flex-col gap-4">

                {/* Card: AI Performance */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex items-center justify-between relative overflow-hidden">
                    {/* Background Glow */}
                    <div className="absolute -right-10 -top-10 w-32 h-32 bg-[var(--color-primary)]/20 blur-3xl rounded-full" />

                    <div>
                        <div className="text-[10px] text-gray-400 font-mono uppercase mb-1">Auto-Resolution Rate</div>
                        <div className="text-4xl font-mono text-white font-bold flex items-baseline gap-2">
                            {autoResolutionRate}%
                            <span className="text-sm flex items-center" style={{ color: 'var(--color-success)' }}><Zap className="w-3 h-3" /></span>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">AI handling {stats.resolved} tickets</p>
                    </div>
                    <div className="h-16 w-16 rounded-full border-4 border-[var(--color-primary)]/30 border-t-[var(--color-primary)] animate-spin" />
                </div>

                {/* Card: User Patience (Average Sentiment) */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-sm font-bold text-white flex items-center gap-2">
                            <Activity className="w-4 h-4" style={{ color: 'var(--color-error)' }} />
                            AVG SENTIMENT
                        </h3>
                        <span className="text-xs font-mono font-bold" style={{ color: stats.avg_sentiment > 70 ? 'var(--color-success)' : stats.avg_sentiment > 40 ? 'var(--color-warning)' : 'var(--color-error)' }}>
                            {stats.avg_sentiment.toFixed(1)}/100
                        </span>
                    </div>
                    {/* Bar */}
                    <div className="h-3 w-full bg-black/50 rounded-full overflow-hidden">
                        <div
                            className="h-full transition-all"
                            style={{
                                width: `${stats.avg_sentiment}%`,
                                background: stats.avg_sentiment > 70 ? 'var(--color-success)' : stats.avg_sentiment > 40 ? 'var(--color-warning)' : 'var(--color-error)'
                            }}
                        />
                    </div>
                </div>

                {/* Card: Stats Grid */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-widest">Ticket Status</h3>
                    <div className="grid grid-cols-2 gap-3">
                        <div className="rounded-xl p-3" style={{ background: 'var(--color-error)/10', border: '1px solid var(--color-error)/20' }}>
                            <div className="text-2xl font-mono font-bold" style={{ color: 'var(--color-error)' }}>{stats.open}</div>
                            <div className="text-[10px] text-gray-400 uppercase">Open</div>
                        </div>
                        <div className="rounded-xl p-3" style={{ background: 'var(--color-warning)/10', border: '1px solid var(--color-warning)/20' }}>
                            <div className="text-2xl font-mono font-bold" style={{ color: 'var(--color-warning)' }}>{stats.in_progress}</div>
                            <div className="text-[10px] text-gray-400 uppercase">In Progress</div>
                        </div>
                        <div className="rounded-xl p-3" style={{ background: 'var(--color-success)/10', border: '1px solid var(--color-success)/20' }}>
                            <div className="text-2xl font-mono font-bold" style={{ color: 'var(--color-success)' }}>{stats.resolved}</div>
                            <div className="text-[10px] text-gray-400 uppercase">Resolved</div>
                        </div>
                        <div className="bg-gray-500/10 border border-gray-500/20 rounded-xl p-3">
                            <div className="text-2xl font-mono font-bold text-gray-400">{stats.total}</div>
                            <div className="text-[10px] text-gray-400 uppercase">Total</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal */}
            <TicketModal ticket={activeTicket} onClose={() => setActiveTicket(null)} />
        </div>
    );
}
