/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - NEXUS 3D
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/nexus/page.tsx
 * 📋 ROTA: /dashboard/nexus
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    Network, 
    ZoomIn, 
    ZoomOut, 
    Maximize2,
    RotateCcw,
    Play,
    Pause,
    Eye,
    Settings,
    Filter,
    Download,
    Cpu,
    Activity,
    Zap
} from 'lucide-react';

interface Node {
    id: string;
    name: string;
    type: 'core' | 'specialist' | 'observer' | 'chaos';
    x: number;
    y: number;
    connections: string[];
    efficiency: number;
    active: boolean;
}

export default function NexusPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [nodes, setNodes] = useState<Node[]>([]);
    const [selectedNode, setSelectedNode] = useState<Node | null>(null);
    const [isAnimating, setIsAnimating] = useState(true);
    const [zoom, setZoom] = useState(1);
    const [filter, setFilter] = useState<string>('all');
    const animationRef = useRef<number>();

    // Generate nodes
    useEffect(() => {
        const types: Node['type'][] = ['core', 'specialist', 'observer', 'chaos'];
        const generatedNodes: Node[] = [];
        
        for (let i = 0; i < 139; i++) {
            const angle = (i / 139) * Math.PI * 2;
            const radius = 150 + Math.random() * 100;
            generatedNodes.push({
                id: `unit_${i + 1}`,
                name: `UNIT_${String(i + 1).padStart(2, '0')}`,
                type: types[Math.floor(Math.random() * types.length)],
                x: 400 + Math.cos(angle) * radius + (Math.random() - 0.5) * 50,
                y: 300 + Math.sin(angle) * radius + (Math.random() - 0.5) * 50,
                connections: Array.from({ length: Math.floor(Math.random() * 5) + 1 }, () => 
                    `unit_${Math.floor(Math.random() * 139) + 1}`
                ),
                efficiency: 70 + Math.random() * 30,
                active: Math.random() > 0.1
            });
        }
        setNodes(generatedNodes);
    }, []);

    // Animation loop
    useEffect(() => {
        if (!canvasRef.current || !isAnimating) return;
        
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;

        const animate = () => {
            time += 0.01;
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw connections
            nodes.forEach(node => {
                if (filter !== 'all' && node.type !== filter) return;
                
                node.connections.forEach(connId => {
                    const connNode = nodes.find(n => n.id === connId);
                    if (!connNode) return;
                    if (filter !== 'all' && connNode.type !== filter) return;

                    ctx.beginPath();
                    ctx.moveTo(node.x * zoom, node.y * zoom);
                    ctx.lineTo(connNode.x * zoom, connNode.y * zoom);
                    
                    const gradient = ctx.createLinearGradient(
                        node.x * zoom, node.y * zoom,
                        connNode.x * zoom, connNode.y * zoom
                    );
                    gradient.addColorStop(0, 'rgba(0, 255, 200, 0.1)');
                    gradient.addColorStop(0.5, `rgba(0, 255, 200, ${0.2 + Math.sin(time * 2) * 0.1})`);
                    gradient.addColorStop(1, 'rgba(0, 255, 200, 0.1)');
                    
                    ctx.strokeStyle = gradient;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                });
            });

            // Draw nodes
            nodes.forEach(node => {
                if (filter !== 'all' && node.type !== filter) return;

                const pulse = Math.sin(time * 3 + node.x * 0.01) * 2;
                const size = (4 + pulse) * zoom;
                
                ctx.beginPath();
                ctx.arc(node.x * zoom, node.y * zoom, size, 0, Math.PI * 2);
                
                let color;
                switch (node.type) {
                    case 'core': color = '#00FFC8'; break;
                    case 'specialist': color = '#8B5CF6'; break;
                    case 'observer': color = '#F59E0B'; break;
                    case 'chaos': color = '#EF4444'; break;
                    default: color = '#00FFC8';
                }
                
                ctx.fillStyle = node.active ? color : '#374151';
                ctx.fill();
                
                // Glow effect
                if (node.active) {
                    ctx.beginPath();
                    ctx.arc(node.x * zoom, node.y * zoom, size * 2, 0, Math.PI * 2);
                    const glow = ctx.createRadialGradient(
                        node.x * zoom, node.y * zoom, 0,
                        node.x * zoom, node.y * zoom, size * 2
                    );
                    glow.addColorStop(0, `${color}40`);
                    glow.addColorStop(1, 'transparent');
                    ctx.fillStyle = glow;
                    ctx.fill();
                }
            });

            animationRef.current = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [nodes, isAnimating, zoom, filter]);

    const getTypeColor = (type: string) => {
        switch (type) {
            case 'core': return 'text-cyan-400 bg-cyan-400/10';
            case 'specialist': return 'text-purple-400 bg-purple-400/10';
            case 'observer': return 'text-yellow-400 bg-yellow-400/10';
            case 'chaos': return 'text-red-400 bg-red-400/10';
            default: return 'text-zinc-400 bg-zinc-400/10';
        }
    };

    const stats = {
        total: nodes.length,
        active: nodes.filter(n => n.active).length,
        connections: nodes.reduce((acc, n) => acc + n.connections.length, 0),
        avgEfficiency: (nodes.reduce((acc, n) => acc + n.efficiency, 0) / nodes.length).toFixed(1)
    };

    return (
        <div className="min-h-screen flex flex-col">
            {/* Header */}
            <div className="p-6 border-b border-zinc-800">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-xl border border-cyan-500/30">
                            <Network className="w-8 h-8 text-cyan-400" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-white tracking-tight">
                                Neural Nexus 3D
                            </h1>
                            <p className="text-zinc-400">Agent Network Visualization • {stats.total} Nodes</p>
                        </div>
                    </div>
                    
                    {/* Controls */}
                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => setIsAnimating(!isAnimating)}
                            className={`p-2 rounded-lg border transition-colors ${
                                isAnimating 
                                    ? 'bg-cyan-500/20 border-cyan-500/30 text-cyan-400' 
                                    : 'bg-zinc-800 border-zinc-700 text-zinc-400'
                            }`}
                        >
                            {isAnimating ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                        </button>
                        <button
                            onClick={() => setZoom(z => Math.max(0.5, z - 0.1))}
                            className="p-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-400 hover:text-white"
                        >
                            <ZoomOut className="w-5 h-5" />
                        </button>
                        <span className="px-3 py-1 bg-zinc-900 rounded text-zinc-400 text-sm">
                            {(zoom * 100).toFixed(0)}%
                        </span>
                        <button
                            onClick={() => setZoom(z => Math.min(2, z + 0.1))}
                            className="p-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-400 hover:text-white"
                        >
                            <ZoomIn className="w-5 h-5" />
                        </button>
                        <button
                            onClick={() => setZoom(1)}
                            className="p-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-400 hover:text-white"
                        >
                            <RotateCcw className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>

            <div className="flex-1 flex">
                {/* Canvas */}
                <div className="flex-1 relative bg-black">
                    <canvas
                        ref={canvasRef}
                        width={800}
                        height={600}
                        className="w-full h-full"
                        style={{ background: 'radial-gradient(circle at center, #051015 0%, #000 70%)' }}
                    />
                    
                    {/* Overlay Stats */}
                    <div className="absolute top-4 left-4 space-y-2">
                        <div className="bg-black/80 backdrop-blur border border-zinc-800 rounded-lg p-3">
                            <div className="flex items-center gap-2 text-sm">
                                <Activity className="w-4 h-4 text-green-400" />
                                <span className="text-zinc-400">Active:</span>
                                <span className="text-white font-medium">{stats.active}/{stats.total}</span>
                            </div>
                        </div>
                        <div className="bg-black/80 backdrop-blur border border-zinc-800 rounded-lg p-3">
                            <div className="flex items-center gap-2 text-sm">
                                <Zap className="w-4 h-4 text-cyan-400" />
                                <span className="text-zinc-400">Connections:</span>
                                <span className="text-white font-medium">{stats.connections}</span>
                            </div>
                        </div>
                        <div className="bg-black/80 backdrop-blur border border-zinc-800 rounded-lg p-3">
                            <div className="flex items-center gap-2 text-sm">
                                <Cpu className="w-4 h-4 text-purple-400" />
                                <span className="text-zinc-400">Avg Efficiency:</span>
                                <span className="text-white font-medium">{stats.avgEfficiency}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Sidebar */}
                <div className="w-80 bg-zinc-900/50 border-l border-zinc-800 p-4 space-y-4 overflow-y-auto">
                    {/* Filter */}
                    <div>
                        <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-3">
                            Filter by Type
                        </h3>
                        <div className="space-y-2">
                            {['all', 'core', 'specialist', 'observer', 'chaos'].map((type) => (
                                <button
                                    key={type}
                                    onClick={() => setFilter(type)}
                                    className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                                        filter === type
                                            ? 'bg-cyan-500/20 border border-cyan-500/30 text-cyan-400'
                                            : 'bg-zinc-800/50 border border-zinc-700 text-zinc-400 hover:text-white'
                                    }`}
                                >
                                    <span className="capitalize">{type === 'all' ? 'All Nodes' : type}</span>
                                    <span className="text-xs">
                                        {type === 'all' 
                                            ? nodes.length 
                                            : nodes.filter(n => n.type === type).length
                                        }
                                    </span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Legend */}
                    <div>
                        <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-3">
                            Node Types
                        </h3>
                        <div className="space-y-2">
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-3 h-3 rounded-full bg-cyan-400" />
                                <span className="text-zinc-300 text-sm">Core Agents</span>
                            </div>
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-3 h-3 rounded-full bg-purple-400" />
                                <span className="text-zinc-300 text-sm">Specialists</span>
                            </div>
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                                <span className="text-zinc-300 text-sm">Observers</span>
                            </div>
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-3 h-3 rounded-full bg-red-400" />
                                <span className="text-zinc-300 text-sm">Chaos Agents</span>
                            </div>
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-3 h-3 rounded-full bg-zinc-600" />
                                <span className="text-zinc-300 text-sm">Inactive</span>
                            </div>
                        </div>
                    </div>

                    {/* Top Connections */}
                    <div>
                        <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-3">
                            Most Connected
                        </h3>
                        <div className="space-y-2">
                            {nodes
                                .sort((a, b) => b.connections.length - a.connections.length)
                                .slice(0, 5)
                                .map((node) => (
                                    <div 
                                        key={node.id}
                                        className="flex items-center justify-between p-3 bg-black/30 rounded-lg border border-zinc-800"
                                    >
                                        <div className="flex items-center gap-2">
                                            <div className={`w-2 h-2 rounded-full ${
                                                node.type === 'core' ? 'bg-cyan-400' :
                                                node.type === 'specialist' ? 'bg-purple-400' :
                                                node.type === 'observer' ? 'bg-yellow-400' :
                                                'bg-red-400'
                                            }`} />
                                            <span className="text-white text-sm">{node.name}</span>
                                        </div>
                                        <span className="text-cyan-400 text-sm">{node.connections.length} conn</span>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
