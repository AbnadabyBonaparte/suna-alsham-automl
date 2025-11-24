/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - NEURAL NEXUS 3D (GOD TIER)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/nexus/page.tsx
 * 📋 Grafo neural interativo com física de partículas e zoom
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef, useCallback } from 'react';
import { 
    Network, ZoomIn, ZoomOut, Play, Pause, RefreshCw, 
    Filter, Cpu, Zap, Activity, MousePointer2 
} from 'lucide-react';

// Tipos para o sistema de física
interface Node {
    id: string;
    name: string;
    type: 'core' | 'specialist' | 'observer' | 'chaos';
    x: number;
    y: number;
    vx: number;
    vy: number;
    radius: number;
    connections: string[];
    efficiency: number;
    active: boolean;
    dragged?: boolean;
}

export default function NexusPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [nodes, setNodes] = useState<Node[]>([]);
    const [isAnimating, setIsAnimating] = useState(true);
    const [zoom, setZoom] = useState(1);
    const [offset, setOffset] = useState({ x: 0, y: 0 });
    const [filter, setFilter] = useState<string>('all');
    const [hoveredNode, setHoveredNode] = useState<Node | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
    
    const animationRef = useRef<number>();
    const nodesRef = useRef<Node[]>([]); // Ref para acesso rápido no loop de animação

    // 1. Geração Inicial de Nós (Big Bang)
    useEffect(() => {
        const types: Node['type'][] = ['core', 'specialist', 'observer', 'chaos'];
        const generatedNodes: Node[] = [];
        
        for (let i = 0; i < 139; i++) {
            const type = types[Math.floor(Math.random() * types.length)];
            // Distribuição em espiral (DNA Like)
            const angle = (i * 0.5);
            const radius = 10 * i; 
            
            generatedNodes.push({
                id: `unit_${i + 1}`,
                name: `AGENT_${String(i + 1).padStart(3, '0')}`,
                type,
                x: window.innerWidth / 2 + Math.cos(angle) * radius * 0.5 + (Math.random() - 0.5) * 100,
                y: window.innerHeight / 2 + Math.sin(angle) * radius * 0.5 + (Math.random() - 0.5) * 100,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: type === 'core' ? 8 : type === 'chaos' ? 6 : 4,
                connections: [], // Preenchido depois
                efficiency: 70 + Math.random() * 30,
                active: Math.random() > 0.2
            });
        }

        // Criar conexões inteligentes (Clusters)
        generatedNodes.forEach((node, i) => {
            const numConnections = Math.floor(Math.random() * 3) + 1;
            for(let j=0; j<numConnections; j++) {
                // Conectar com vizinhos próximos na lista
                const targetIndex = (i + j + 1) % generatedNodes.length;
                node.connections.push(generatedNodes[targetIndex].id);
            }
            // Conectar aleatoriamente para criar "atalhos" neurais
            if (Math.random() > 0.8) {
                const randomTarget = generatedNodes[Math.floor(Math.random() * generatedNodes.length)];
                if (randomTarget.id !== node.id) node.connections.push(randomTarget.id);
            }
        });

        setNodes(generatedNodes);
        nodesRef.current = generatedNodes;
        
        // Centralizar
        setOffset({ x: 0, y: 0 });
    }, []);

    // 2. Sistema de Física e Renderização
    useEffect(() => {
        if (!canvasRef.current || !isAnimating) return;
        
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Redimensionar canvas
        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        let time = 0;

        const animate = () => {
            time += 0.01;
            
            // Limpar com rastro suave (Motion Blur)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)'; // Fundo quase preto
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Grid de fundo (Holográfico)
            ctx.strokeStyle = 'rgba(0, 255, 200, 0.03)';
            ctx.lineWidth = 1;
            const gridSize = 50 * zoom;
            const offsetX = offset.x % gridSize;
            const offsetY = offset.y % gridSize;
            
            for(let x = offsetX; x < canvas.width; x += gridSize) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
            }
            for(let y = offsetY; y < canvas.height; y += gridSize) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
            }

            // Atualizar e Desenhar Nós
            const currentNodes = nodesRef.current;
            
            // A. Desenhar Conexões (Camada Traseira)
            ctx.lineWidth = 0.5 * zoom;
            currentNodes.forEach(node => {
                if (filter !== 'all' && node.type !== filter) return;

                node.connections.forEach(connId => {
                    const target = currentNodes.find(n => n.id === connId);
                    if (!target) return;
                    if (filter !== 'all' && target.type !== filter) return;

                    // Posições ajustadas pelo Zoom e Pan
                    const sx = node.x * zoom + offset.x;
                    const sy = node.y * zoom + offset.y;
                    const ex = target.x * zoom + offset.x;
                    const ey = target.y * zoom + offset.y;

                    // Só desenha se estiver na tela
                    if (sx < 0 && ex < 0 || sx > canvas.width && ex > canvas.width) return;

                    const dist = Math.hypot(ex - sx, ey - sy);
                    if (dist > 300 * zoom) return; // Otimização: não desenha linhas muito longas

                    ctx.beginPath();
                    ctx.moveTo(sx, sy);
                    ctx.lineTo(ex, ey);
                    
                    // Cor baseada no tipo
                    const alpha = (1 - dist / (300 * zoom)) * 0.3;
                    ctx.strokeStyle = node.type === 'chaos' 
                        ? `rgba(239, 68, 68, ${alpha})` 
                        : `rgba(0, 255, 200, ${alpha})`;
                    ctx.stroke();
                });
            });

            // B. Desenhar Nós (Camada Frontal)
            currentNodes.forEach(node => {
                if (filter !== 'all' && node.type !== filter) return;

                // Movimento Fluido (Física)
                if (!node.dragged) {
                    node.x += Math.sin(time + node.y * 0.01) * 0.2;
                    node.y += Math.cos(time + node.x * 0.01) * 0.2;
                }

                const screenX = node.x * zoom + offset.x;
                const screenY = node.y * zoom + offset.y;

                // Cores por Tipo
                let color = '#374151';
                let glowColor = 'rgba(55, 65, 81, 0)';
                
                if (node.active) {
                    switch (node.type) {
                        case 'core': color = '#00FFC8'; glowColor = 'rgba(0, 255, 200, 0.4)'; break; // Ciano
                        case 'specialist': color = '#A855F7'; glowColor = 'rgba(168, 85, 247, 0.4)'; break; // Roxo
                        case 'observer': color = '#F59E0B'; glowColor = 'rgba(245, 158, 11, 0.4)'; break; // Amarelo
                        case 'chaos': color = '#EF4444'; glowColor = 'rgba(239, 68, 68, 0.4)'; break; // Vermelho
                    }
                }

                // Efeito Hover
                const isHovered = hoveredNode?.id === node.id;
                const radius = node.radius * zoom * (isHovered ? 1.5 : 1);

                // Glow
                if (node.active || isHovered) {
                    const gradient = ctx.createRadialGradient(screenX, screenY, 0, screenX, screenY, radius * 4);
                    gradient.addColorStop(0, glowColor);
                    gradient.addColorStop(1, 'transparent');
                    ctx.fillStyle = gradient;
                    ctx.beginPath();
                    ctx.arc(screenX, screenY, radius * 4, 0, Math.PI * 2);
                    ctx.fill();
                }

                // Core do Nó
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(screenX, screenY, radius, 0, Math.PI * 2);
                ctx.fill();

                // Nome no Hover
                if (isHovered) {
                    ctx.fillStyle = '#FFF';
                    ctx.font = '12px monospace';
                    ctx.fillText(node.name, screenX + 15, screenY - 15);
                    ctx.fillStyle = '#AAA';
                    ctx.font = '10px monospace';
                    ctx.fillText(`EFFICIENCY: ${node.efficiency.toFixed(1)}%`, screenX + 15, screenY - 3);
                }
            });

            animationRef.current = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            window.removeEventListener('resize', resize);
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
        };
    }, [isAnimating, zoom, offset, filter, hoveredNode]);

    // 3. Controles de Interação (Mouse)
    const handleMouseDown = (e: React.MouseEvent) => {
        setIsDragging(true);
        setDragStart({ x: e.clientX - offset.x, y: e.clientY - offset.y });
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        const rect = canvasRef.current?.getBoundingClientRect();
        if (!rect) return;
        
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Pan (Arrastar Fundo)
        if (isDragging) {
            setOffset({
                x: e.clientX - dragStart.x,
                y: e.clientY - dragStart.y
            });
            return;
        }

        // Detectar Hover em Nós
        const node = nodesRef.current.find(n => {
            const sx = n.x * zoom + offset.x;
            const sy = n.y * zoom + offset.y;
            const dist = Math.hypot(mouseX - sx, mouseY - sy);
            return dist < 20; // Raio de detecção
        });

        setHoveredNode(node || null);
        if (canvasRef.current) {
            canvasRef.current.style.cursor = node ? 'pointer' : isDragging ? 'grabbing' : 'default';
        }
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    const handleWheel = (e: React.WheelEvent) => {
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        setZoom(z => Math.max(0.1, Math.min(5, z * delta)));
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col rounded-3xl overflow-hidden border border-[var(--color-border)]/20 bg-black relative group">
            
            {/* HEADER FLUTUANTE */}
            <div className="absolute top-6 left-6 z-20 bg-black/80 backdrop-blur-md border border-white/10 rounded-2xl p-4 shadow-2xl">
                <div className="flex items-center gap-4 mb-4">
                    <div className="p-3 bg-[var(--color-primary)]/10 rounded-xl border border-[var(--color-primary)]/30">
                        <Network className="w-6 h-6 text-[var(--color-primary)]" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-white tracking-tight">NEURAL NEXUS</h1>
                        <p className="text-xs text-gray-400 font-mono">Visualização da Rede Neural em Tempo Real</p>
                    </div>
                </div>

                {/* Mini Stats */}
                <div className="grid grid-cols-2 gap-2">
                    <div className="bg-white/5 rounded-lg p-2">
                        <div className="text-[10px] text-gray-500 uppercase">Active Nodes</div>
                        <div className="text-lg font-mono text-[var(--color-primary)]">
                            {nodes.filter(n => n.active).length}
                        </div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2">
                        <div className="text-[10px] text-gray-500 uppercase">Connections</div>
                        <div className="text-lg font-mono text-[var(--color-secondary)]">
                            {nodes.reduce((acc, n) => acc + n.connections.length, 0)}
                        </div>
                    </div>
                </div>
            </div>

            {/* CONTROLES FLUTUANTES (Direita) */}
            <div className="absolute top-6 right-6 z-20 flex flex-col gap-2">
                <button onClick={() => setIsAnimating(!isAnimating)} className="p-3 bg-black/80 border border-white/10 rounded-xl text-white hover:text-[var(--color-primary)] hover:border-[var(--color-primary)] transition-all">
                    {isAnimating ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                </button>
                <button onClick={() => setZoom(z => z + 0.2)} className="p-3 bg-black/80 border border-white/10 rounded-xl text-white hover:text-[var(--color-primary)] transition-all">
                    <ZoomIn className="w-5 h-5" />
                </button>
                <button onClick={() => setZoom(z => z - 0.2)} className="p-3 bg-black/80 border border-white/10 rounded-xl text-white hover:text-[var(--color-primary)] transition-all">
                    <ZoomOut className="w-5 h-5" />
                </button>
                <button onClick={() => { setZoom(1); setOffset({x:0, y:0}); }} className="p-3 bg-black/80 border border-white/10 rounded-xl text-white hover:text-[var(--color-primary)] transition-all">
                    <RefreshCw className="w-5 h-5" />
                </button>
            </div>

            {/* FILTROS FLUTUANTES (Inferior) */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex gap-2 bg-black/80 backdrop-blur-md p-2 rounded-2xl border border-white/10">
                {['all', 'core', 'specialist', 'observer', 'chaos'].map((type) => (
                    <button
                        key={type}
                        onClick={() => setFilter(type)}
                        className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
                            filter === type 
                                ? 'bg-[var(--color-primary)] text-black shadow-[0_0_15px_var(--color-primary)]' 
                                : 'text-gray-400 hover:bg-white/10'
                        }`}
                    >
                        {type}
                    </button>
                ))}
            </div>

            {/* CANVAS INTERATIVO */}
            <canvas
                ref={canvasRef}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                onWheel={handleWheel}
                className="w-full h-full cursor-grab active:cursor-grabbing"
            />
            
            {/* Dica de Interação */}
            <div className="absolute bottom-6 right-6 z-10 text-xs text-gray-600 font-mono pointer-events-none opacity-50">
                <div className="flex items-center gap-2">
                    <MousePointer2 className="w-3 h-3" />
                    <span>DRAG TO PAN • SCROLL TO ZOOM</span>
                </div>
            </div>
        </div>
    );
}
