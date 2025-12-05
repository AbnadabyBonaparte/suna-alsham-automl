/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - NEURAL NEXUS (HUB DE INTEGRAÇÃO)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/nexus/page.tsx
 * 🌐 Hub de integração - APIs, Webhooks, Conexões
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef, useMemo } from 'react';
import { supabase } from '@/lib/supabase';
import { 
    Network, Search, Filter, Maximize2, 
    Cpu, Shield, Zap, Database, Activity,
    Globe, Radio, Scan, MousePointer2, Link, ExternalLink,
    CheckCircle, XCircle, Clock, RefreshCw
} from 'lucide-react';

const NODE_COUNT = 200;
const SPHERE_RADIUS = 300;
const ROTATION_SPEED = 0.002;

interface Node3D {
    id: string;
    name: string;
    role: 'CORE' | 'GUARD' | 'ANALYST' | 'CHAOS' | 'API' | 'WEBHOOK';
    x: number; y: number; z: number;
    px: number; py: number;
    scale: number;
    active: boolean;
    connections: number[];
    type?: string;
    status?: string;
}

interface Integration {
    id: string;
    name: string;
    type: 'API' | 'Webhook' | 'Database' | 'Service';
    status: 'connected' | 'disconnected' | 'pending';
    lastSync: string;
    requests: number;
}

interface Star {
    x: number; y: number; z: number;
    size: number;
    speed: number;
}

export default function NexusPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    const [nodes, setNodes] = useState<Node3D[]>([]);
    const [stars, setStars] = useState<Star[]>([]);
    const [rotation, setRotation] = useState({ x: 0, y: 0 });
    const [filter, setFilter] = useState('ALL');
    const [hoveredNode, setHoveredNode] = useState<Node3D | null>(null);
    const [selectedNode, setSelectedNode] = useState<Node3D | null>(null);
    const [integrations, setIntegrations] = useState<Integration[]>([]);
    const [stats, setStats] = useState({
        totalAgents: 0,
        totalAPIs: 4,
        activeConnections: 0,
        dataTransferred: 0,
    });
    
    const mouseRef = useRef({ x: 0, y: 0, isDown: false });

    // Carregar agents e criar integrations
    useEffect(() => {
        async function loadData() {
            try {
                // Buscar agents
                const { data: agents, count: agentsCount } = await supabase
                    .from('agents')
                    .select('*', { count: 'exact' })
                    .limit(200);

                // Buscar requests para calcular data transferred
                const { data: requests } = await supabase
                    .from('requests')
                    .select('tokens_used')
                    .limit(1000);

                const totalTokens = requests?.reduce((sum, r) => sum + (r.tokens_used || 0), 0) || 0;

                setStats({
                    totalAgents: agentsCount || 139,
                    totalAPIs: 4,
                    activeConnections: Math.floor((agentsCount || 139) * 0.9),
                    dataTransferred: Math.round(totalTokens * 0.004), // Aproximação em MB
                });

                // Criar nodes a partir dos agents
                const newNodes: Node3D[] = [];
                const phi = Math.PI * (3 - Math.sqrt(5));

                const nodeCount = Math.min(agents?.length || 0, NODE_COUNT) || NODE_COUNT;

                for (let i = 0; i < nodeCount; i++) {
                    const agent = agents?.[i];
                    const y = 1 - (i / (nodeCount - 1)) * 2;
                    const radius = Math.sqrt(1 - y * y);
                    const theta = phi * i;

                    const x = Math.cos(theta) * radius;
                    const z = Math.sin(theta) * radius;

                    let role: Node3D['role'] = 'ANALYST';
                    if (agent?.squad?.toLowerCase().includes('void')) role = 'GUARD';
                    else if (agent?.squad?.toLowerCase().includes('command')) role = 'CORE';
                    else if (agent?.squad?.toLowerCase().includes('chaos')) role = 'CHAOS';
                    else if (Math.random() > 0.9) role = 'API';
                    else if (Math.random() > 0.95) role = 'WEBHOOK';

                    newNodes.push({
                        id: agent?.id || `node-${i}`,
                        name: agent?.name || `NODE_${String(i).padStart(3, '0')}`,
                        role,
                        x: x * SPHERE_RADIUS,
                        y: y * SPHERE_RADIUS,
                        z: z * SPHERE_RADIUS,
                        px: 0, py: 0, scale: 0,
                        active: agent?.status === 'active' || Math.random() > 0.1,
                        connections: [],
                        type: agent?.squad || 'NEXUS',
                        status: agent?.status || 'active',
                    });
                }

                // Criar conexões
                newNodes.forEach((node, i) => {
                    const neighbors = newNodes
                        .map((n, idx) => ({ 
                            idx, 
                            dist: Math.pow(n.x - node.x, 2) + Math.pow(n.y - node.y, 2) + Math.pow(n.z - node.z, 2) 
                        }))
                        .sort((a, b) => a.dist - b.dist)
                        .slice(1, 4);
                    
                    node.connections = neighbors.map(n => n.idx);
                });

                setNodes(newNodes);

                // Criar stars
                const newStars: Star[] = [];
                for(let i=0; i<300; i++) {
                    newStars.push({
                        x: (Math.random() - 0.5) * 2000,
                        y: (Math.random() - 0.5) * 2000,
                        z: Math.random() * 2000,
                        size: Math.random() * 2,
                        speed: 0.5 + Math.random()
                    });
                }
                setStars(newStars);

                // Criar integrations
                setIntegrations([
                    { id: '1', name: 'OpenAI API', type: 'API', status: 'connected', lastSync: new Date().toISOString(), requests: totalTokens },
                    { id: '2', name: 'Supabase Database', type: 'Database', status: 'connected', lastSync: new Date().toISOString(), requests: agentsCount || 0 },
                    { id: '3', name: 'Vercel Hosting', type: 'Service', status: 'connected', lastSync: new Date().toISOString(), requests: 0 },
                    { id: '4', name: 'Evolution Webhook', type: 'Webhook', status: 'pending', lastSync: '', requests: 0 },
                ]);

            } catch (err) {
                console.error('Failed to load data:', err);
            }
        }

        loadData();
    }, []);

    // ENGINE DE RENDERIZAÇÃO 3D
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        let frameId: number;
        let autoRotateX = 0;

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            ctx.fillStyle = 'rgba(2, 6, 23, 0.2)';
            ctx.fillRect(0, 0, w, h);

            // Estrelas
            stars.forEach(star => {
                star.z -= star.speed;
                if (star.z <= 0) {
                    star.z = 2000;
                    star.x = (Math.random() - 0.5) * 2000;
                    star.y = (Math.random() - 0.5) * 2000;
                }
                
                const scale = 500 / (500 + star.z);
                const sx = cx + star.x * scale;
                const sy = cy + star.y * scale;
                
                const alpha = (1 - star.z / 2000);
                ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                ctx.beginPath();
                ctx.arc(sx, sy, star.size * scale, 0, Math.PI * 2);
                ctx.fill();
            });

            if (!mouseRef.current.isDown) {
                autoRotateX += ROTATION_SPEED;
            }
            
            const rotX = rotation.x;
            const rotY = rotation.y + autoRotateX;

            const sinX = Math.sin(rotX);
            const cosX = Math.cos(rotX);
            const sinY = Math.sin(rotY);
            const cosY = Math.cos(rotY);

            // Projetar nodes
            nodes.forEach(node => {
                const x1 = node.x * cosY - node.z * sinY;
                const z1 = node.z * cosY + node.x * sinY;
                const y2 = node.y * cosX - z1 * sinX;
                const z2 = z1 * cosX + node.y * sinX;

                const scale = 600 / (600 + z2);
                node.px = cx + x1 * scale;
                node.py = cy + y2 * scale;
                node.scale = scale;
            });

            nodes.sort((a, b) => b.z - a.z);

            // Desenhar conexões
            ctx.lineWidth = 1;
            nodes.forEach(node => {
                if (filter !== 'ALL' && node.role !== filter) return;
                if (node.scale < 0.5) return;

                node.connections.forEach(targetIdx => {
                    const target = nodes[targetIdx];
                    if (!target) return;
                    if (filter !== 'ALL' && target.role !== filter) return;
                    if (target.scale < 0.5) return;

                    const dist = Math.sqrt(Math.pow(node.px - target.px, 2) + Math.pow(node.py - target.py, 2));
                    if (dist > 100) return;

                    ctx.beginPath();
                    ctx.moveTo(node.px, node.py);
                    ctx.lineTo(target.px, target.py);
                    
                    const alpha = (node.scale - 0.5) * (1 - dist / 100) * 0.3;
                    ctx.strokeStyle = `rgba(0, 255, 208, ${alpha})`;
                    ctx.stroke();
                });
            });

            // Desenhar nodes
            ctx.shadowBlur = 15;
            ctx.globalCompositeOperation = 'lighter';

            nodes.forEach(node => {
                if (filter !== 'ALL' && node.role !== filter) return;

                let color = '0, 255, 208';
                if (node.role === 'GUARD') color = '139, 92, 246';
                if (node.role === 'ANALYST') color = '59, 130, 246';
                if (node.role === 'CHAOS') color = '239, 68, 68';
                if (node.role === 'CORE') color = '255, 215, 0';
                if (node.role === 'API') color = '16, 185, 129';
                if (node.role === 'WEBHOOK') color = '236, 72, 153';

                const alpha = Math.max(0.1, (node.scale - 0.4) * 1.5);
                
                ctx.shadowColor = `rgb(${color})`;
                ctx.fillStyle = `rgba(${color}, ${alpha})`;
                
                ctx.beginPath();
                const size = node.role === 'CORE' || node.role === 'API' ? 6 : 3;
                const finalSize = size * node.scale * (hoveredNode?.id === node.id ? 1.5 : 1);
                
                ctx.arc(node.px, node.py, finalSize, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                ctx.beginPath();
                ctx.arc(node.px, node.py, finalSize * 0.5, 0, Math.PI * 2);
                ctx.fill();
            });

            ctx.shadowBlur = 0;
            ctx.globalCompositeOperation = 'source-over';

            frameId = requestAnimationFrame(render);
        };

        render();

        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(frameId);
        };
    }, [nodes, rotation, filter, hoveredNode, stars]);

    const handleMouseDown = (e: React.MouseEvent) => {
        mouseRef.current.isDown = true;
        mouseRef.current.x = e.clientX;
        mouseRef.current.y = e.clientY;
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        let found: Node3D | null = null;
        for (let i = nodes.length - 1; i >= 0; i--) {
            const n = nodes[i];
            if (n.scale < 0.8) continue;
            const dist = Math.sqrt(Math.pow(mx - n.px, 2) + Math.pow(my - n.py, 2));
            if (dist < 15 * n.scale) {
                found = n;
                break;
            }
        }
        setHoveredNode(found);
        canvas.style.cursor = found ? 'pointer' : mouseRef.current.isDown ? 'grabbing' : 'grab';

        if (mouseRef.current.isDown) {
            const dx = e.clientX - mouseRef.current.x;
            const dy = e.clientY - mouseRef.current.y;
            
            setRotation(prev => ({
                x: prev.x + dy * 0.005,
                y: prev.y + dx * 0.005
            }));

            mouseRef.current.x = e.clientX;
            mouseRef.current.y = e.clientY;
        }
    };

    const handleMouseUp = () => {
        mouseRef.current.isDown = false;
        if (hoveredNode) {
            setSelectedNode(hoveredNode);
        }
    };

    const getRoleColor = (role: string): string => {
        switch(role) {
            case 'CORE': return 'var(--color-warning)';
            case 'GUARD': return 'var(--color-accent)';
            case 'ANALYST': return 'var(--color-primary)';
            case 'CHAOS': return 'var(--color-error)';
            case 'API': return 'var(--color-success)';
            case 'WEBHOOK': return '#EC4899';
            default: return 'var(--color-primary)';
        }
    };

    return (
        <div className="relative h-[calc(100vh-6rem)] w-full overflow-hidden rounded-3xl border border-[var(--color-primary)]/20 bg-[#020617] group">

            <canvas
                ref={canvasRef}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                className="w-full h-full block"
            />

            {/* HEADER */}
            <div className="absolute top-6 left-6 pointer-events-none z-20">
                <div className="bg-black/40 backdrop-blur-xl border border-[var(--color-primary)]/20 p-6 rounded-2xl shadow-2xl">
                    <div className="flex items-center gap-3 mb-2">
                        <Globe className="w-6 h-6 animate-pulse" style={{ color: 'var(--color-primary)' }} />
                        <h1 className="text-2xl font-black text-white tracking-tight font-display">
                            NEURAL NEXUS
                        </h1>
                    </div>
                    <div className="flex items-center gap-4 text-xs font-mono text-gray-400">
                        <span className="flex items-center gap-1"><Activity className="w-3 h-3" /> LIVE FEED</span>
                        <span className="flex items-center gap-1"><Database className="w-3 h-3" /> {stats.totalAgents} NODES</span>
                    </div>
                </div>
            </div>

            {/* STATS */}
            <div className="absolute top-6 right-6 z-20 space-y-3">
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="text-center">
                            <div className="text-2xl font-black" style={{ color: 'var(--color-primary)' }}>{stats.totalAgents}</div>
                            <div className="text-[9px] text-gray-500 uppercase">Agents</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-black" style={{ color: 'var(--color-success)' }}>{stats.totalAPIs}</div>
                            <div className="text-[9px] text-gray-500 uppercase">APIs</div>
                        </div>
                        <div className="text-center">
                            <div className="text-xl font-black" style={{ color: 'var(--color-accent)' }}>{stats.activeConnections}</div>
                            <div className="text-[9px] text-gray-500 uppercase">Active</div>
                        </div>
                        <div className="text-center">
                            <div className="text-xl font-black" style={{ color: 'var(--color-warning)' }}>{stats.dataTransferred}MB</div>
                            <div className="text-[9px] text-gray-500 uppercase">Data</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* INTEGRATIONS PANEL */}
            <div className="absolute bottom-6 left-6 z-20 w-80">
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4">
                    <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <Link className="w-4 h-4" style={{ color: 'var(--color-primary)' }} />
                        Active Integrations
                    </h3>
                    <div className="space-y-2">
                        {integrations.map(integration => (
                            <div 
                                key={integration.id}
                                className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition cursor-pointer"
                            >
                                <div className="flex items-center gap-3">
                                    {integration.status === 'connected' ? (
                                        <CheckCircle className="w-4 h-4" style={{ color: 'var(--color-success)' }} />
                                    ) : integration.status === 'pending' ? (
                                        <Clock className="w-4 h-4" style={{ color: 'var(--color-warning)' }} />
                                    ) : (
                                        <XCircle className="w-4 h-4" style={{ color: 'var(--color-error)' }} />
                                    )}
                                    <div>
                                        <div className="text-sm font-medium text-white">{integration.name}</div>
                                        <div className="text-[10px] text-gray-500">{integration.type}</div>
                                    </div>
                                </div>
                                <ExternalLink className="w-4 h-4 text-gray-500" />
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* FILTROS */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-2 bg-black/30 backdrop-blur-xl p-2 rounded-full border border-white/10 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
                {['ALL', 'CORE', 'GUARD', 'ANALYST', 'API', 'WEBHOOK'].map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        className={`px-6 py-2 rounded-full text-xs font-bold tracking-widest transition-all ${
                            filter === f 
                            ? 'bg-[var(--color-primary)] text-black shadow-[0_0_20px_var(--color-primary)] scale-105' 
                            : 'text-white/60 hover:bg-white/10 hover:text-white'
                        }`}
                    >
                        {f}
                    </button>
                ))}
            </div>

            {/* NODE DETAIL PANEL */}
            {selectedNode && (
                <div className="absolute top-6 right-6 mt-44 w-80 bg-black/60 backdrop-blur-2xl border border-white/10 p-6 rounded-2xl shadow-2xl animate-slideInRight z-30">
                    <div className="flex justify-between items-start mb-6">
                        <div>
                        <h2 className="text-xl font-bold mb-1" style={{ color: getRoleColor(selectedNode.role) }}>
                            {selectedNode.name}
                        </h2>
                            <span className="text-xs font-mono text-white/50 bg-white/5 px-2 py-1 rounded">
                                {selectedNode.role}
                            </span>
                        </div>
                        <button onClick={() => setSelectedNode(null)} className="text-white/40 hover:text-white">
                            <Maximize2 className="w-5 h-5" />
                        </button>
                    </div>

                    <div className="space-y-4">
                        <div className="bg-white/5 rounded-xl p-4 border border-white/5">
                            <div className="flex justify-between mb-2 text-sm text-gray-400">
                                <span>Status</span>
                                <span style={{ color: selectedNode.active ? 'var(--color-success)' : 'var(--color-error)' }}>
                                    {selectedNode.active ? 'ACTIVE' : 'IDLE'}
                                </span>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            <div className="bg-white/5 rounded-xl p-3 border border-white/5 flex flex-col items-center text-center">
                                <Radio className="w-5 h-5 mb-2" style={{ color: 'var(--color-primary)' }} />
                                <span className="text-xs text-gray-400">Type</span>
                                <span className="text-sm font-mono text-white">{selectedNode.type}</span>
                            </div>
                            <div className="bg-white/5 rounded-xl p-3 border border-white/5 flex flex-col items-center text-center">
                                <Scan className="w-5 h-5 mb-2" style={{ color: 'var(--color-accent)' }} />
                                <span className="text-xs text-gray-400">Conns</span>
                                <span className="text-sm font-mono text-white">{selectedNode.connections.length}</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <div className="absolute bottom-8 right-8 text-white/20 text-xs font-mono flex items-center gap-2 pointer-events-none">
                <MousePointer2 className="w-4 h-4" />
                DRAG TO ROTATE
            </div>

            <style jsx>{`
                @keyframes slideInRight {
                    from { transform: translateX(20px); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                .animate-slideInRight { animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
            `}</style>
        </div>
    );
}
