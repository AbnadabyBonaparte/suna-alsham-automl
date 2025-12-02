/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - NEURAL NEXUS: CELESTIAL SPHERE EDITION
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/nexus/page.tsx
 * 📋 Visualização Holoesférica 3D com Campo Estelar e UI de Vidro
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef, useMemo } from 'react';
import { 
    Network, Search, Filter, Maximize2, 
    Cpu, Shield, Zap, Database, Activity,
    Globe, Radio, Scan, MousePointer2
} from 'lucide-react';

// --- CONFIGURAÇÕES CÓSMICAS ---
const NODE_COUNT = 200;
const SPHERE_RADIUS = 300;
const ROTATION_SPEED = 0.002;

interface Node3D {
    id: string;
    name: string;
    role: 'CORE' | 'GUARD' | 'ANALYST' | 'CHAOS';
    x: number; y: number; z: number; // Posição 3D original
    px: number; py: number; // Posição 2D projetada
    scale: number; // Escala baseada na profundidade (Z)
    active: boolean;
    connections: number[]; // Índices dos vizinhos
}

interface Star {
    x: number; y: number; z: number;
    size: number;
    speed: number;
}

export default function NexusPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estado
    const [nodes, setNodes] = useState<Node3D[]>([]);
    const [stars, setStars] = useState<Star[]>([]);
    const [rotation, setRotation] = useState({ x: 0, y: 0 });
    const [filter, setFilter] = useState('ALL');
    const [hoveredNode, setHoveredNode] = useState<Node3D | null>(null);
    const [selectedNode, setSelectedNode] = useState<Node3D | null>(null);
    
    const mouseRef = useRef({ x: 0, y: 0, isDown: false });

    // 1. GERAÇÃO DO UNIVERSO (BIG BANG)
    useEffect(() => {
        // Criar Agentes na Esfera (Fibonacci Sphere Algorithm para distribuição perfeita)
        const newNodes: Node3D[] = [];
        const phi = Math.PI * (3 - Math.sqrt(5)); // Golden Angle

        for (let i = 0; i < NODE_COUNT; i++) {
            const y = 1 - (i / (NODE_COUNT - 1)) * 2; // y vai de 1 a -1
            const radius = Math.sqrt(1 - y * y); // raio no y
            const theta = phi * i; // ângulo dourado

            const x = Math.cos(theta) * radius;
            const z = Math.sin(theta) * radius;

            // Definir Role aleatória
            const rand = Math.random();
            let role: Node3D['role'] = 'ANALYST';
            if (rand > 0.9) role = 'CORE';
            else if (rand > 0.7) role = 'GUARD';
            else if (rand > 0.6) role = 'CHAOS';

            newNodes.push({
                id: `agt-${i}`,
                name: `${role}_${String(i).padStart(3, '0')}`,
                role,
                x: x * SPHERE_RADIUS,
                y: y * SPHERE_RADIUS,
                z: z * SPHERE_RADIUS,
                px: 0, py: 0, scale: 0,
                active: Math.random() > 0.1,
                connections: []
            });
        }

        // Criar conexões (Vizinhos mais próximos na esfera 3D)
        newNodes.forEach((node, i) => {
            const neighbors = newNodes
                .map((n, idx) => ({ 
                    idx, 
                    dist: Math.pow(n.x - node.x, 2) + Math.pow(n.y - node.y, 2) + Math.pow(n.z - node.z, 2) 
                }))
                .sort((a, b) => a.dist - b.dist)
                .slice(1, 4); // 3 vizinhos mais próximos
            
            node.connections = neighbors.map(n => n.idx);
        });

        setNodes(newNodes);

        // Criar Campo Estelar de Fundo
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

    }, []);

    // 2. ENGINE DE RENDERIZAÇÃO 3D
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
            // Configuração Básica
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            // Limpar com rastro suave (Motion Blur Cósmico)
            ctx.fillStyle = 'rgba(2, 6, 23, 0.2)'; // Azul muito escuro quase preto
            ctx.fillRect(0, 0, w, h);

            // --- 1. DESENHAR ESTRELAS (FUNDO) ---
            stars.forEach(star => {
                star.z -= star.speed;
                if (star.z <= 0) {
                    star.z = 2000;
                    star.x = (Math.random() - 0.5) * 2000;
                    star.y = (Math.random() - 0.5) * 2000;
                }
                
                const scale = 500 / (500 + star.z); // Perspectiva
                const sx = cx + star.x * scale;
                const sy = cy + star.y * scale;
                
                const alpha = (1 - star.z / 2000);
                ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                ctx.beginPath();
                ctx.arc(sx, sy, star.size * scale, 0, Math.PI * 2);
                ctx.fill();
            });

            // --- 2. CÁLCULO DE ROTAÇÃO 3D DA ESFERA ---
            if (!mouseRef.current.isDown) {
                autoRotateX += ROTATION_SPEED; // Rotação automática lenta
            }
            
            // Matrizes de Rotação
            const rotX = rotation.x + (mouseRef.current.isDown ? 0 : 0); 
            const rotY = rotation.y + autoRotateX;

            const sinX = Math.sin(rotX);
            const cosX = Math.cos(rotX);
            const sinY = Math.sin(rotY);
            const cosY = Math.cos(rotY);

            // Projetar Nós 3D -> 2D
            nodes.forEach(node => {
                // Rotação Y
                const x1 = node.x * cosY - node.z * sinY;
                const z1 = node.z * cosY + node.x * sinY;
                // Rotação X
                const y2 = node.y * cosX - z1 * sinX;
                const z2 = z1 * cosX + node.y * sinX;

                // Perspectiva
                const scale = 600 / (600 + z2); // Fator de profundidade
                node.px = cx + x1 * scale;
                node.py = cy + y2 * scale;
                node.scale = scale;
                node.z = z2; // Salvar Z para ordenação (Z-Index)
            });

            // Ordenar para desenhar o que está atrás primeiro (Z-Buffer fake)
            nodes.sort((a, b) => b.z - a.z);

            // --- 3. DESENHAR CONEXÕES (TEIA NEURAL) ---
            ctx.lineWidth = 1;
            nodes.forEach(node => {
                if (filter !== 'ALL' && node.role !== filter) return;
                if (node.scale < 0.5) return; // Ocultar conexões muito distantes

                node.connections.forEach(targetIdx => {
                    const target = nodes[targetIdx];
                    if (!target) return;
                    if (filter !== 'ALL' && target.role !== filter) return;

                    // Só desenha se o alvo também estiver visível
                    if (target.scale < 0.5) return;

                    // Distância para Alpha (Fade out)
                    const dist = Math.sqrt(Math.pow(node.px - target.px, 2) + Math.pow(node.py - target.py, 2));
                    if (dist > 100) return;

                    ctx.beginPath();
                    ctx.moveTo(node.px, node.py);
                    ctx.lineTo(target.px, target.py);
                    
                    // Cor da conexão baseada na profundidade
                    const alpha = (node.scale - 0.5) * (1 - dist / 100) * 0.3;
                    ctx.strokeStyle = `rgba(0, 255, 208, ${alpha})`; // Ciano padrão
                    ctx.stroke();
                });
            });

            // --- 4. DESENHAR NÓS (AGENTES) ---
            // Configuração de Glow
            ctx.shadowBlur = 15;
            ctx.globalCompositeOperation = 'lighter'; // Adição de luz (Bloom)

            nodes.forEach(node => {
                if (filter !== 'ALL' && node.role !== filter) return;

                // Cor baseada no Role (usando RGB para alpha)
                let color = '0, 255, 208'; // Ciano (Core/Padrão)
                if (node.role === 'GUARD') color = '16, 185, 129'; // Verde Tático
                if (node.role === 'ANALYST') color = '139, 92, 246'; // Roxo
                if (node.role === 'CHAOS') color = '239, 68, 68'; // Vermelho

                // Opacidade baseada na profundidade (Z)
                const alpha = Math.max(0.1, (node.scale - 0.4) * 1.5);
                
                // Desenhar Glow
                ctx.shadowColor = `rgb(${color})`;
                ctx.fillStyle = `rgba(${color}, ${alpha})`;
                
                ctx.beginPath();
                // Tamanho varia com a profundidade e se está selecionado
                const size = node.role === 'CORE' ? 6 : 3;
                const finalSize = size * node.scale * (hoveredNode?.id === node.id ? 1.5 : 1);
                
                ctx.arc(node.px, node.py, finalSize, 0, Math.PI * 2);
                ctx.fill();

                // Desenhar Núcleo Branco
                ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                ctx.beginPath();
                ctx.arc(node.px, node.py, finalSize * 0.5, 0, Math.PI * 2);
                ctx.fill();
            });

            // Resetar configs de contexto
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

    // --- INTERAÇÃO DO MOUSE (ROTAÇÃO) ---
    const handleMouseDown = (e: React.MouseEvent) => {
        mouseRef.current.isDown = true;
        mouseRef.current.x = e.clientX;
        mouseRef.current.y = e.clientY;
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        // 1. Detectar Hover em Nós (Raycasting 2D simplificado)
        const canvas = canvasRef.current;
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        // Encontrar nó mais próximo do mouse (que esteja na frente Z > 0)
        let found: Node3D | null = null;
        // Percorre reverso porque nós desenhados por último estão na frente
        for (let i = nodes.length - 1; i >= 0; i--) {
            const n = nodes[i];
            if (n.scale < 0.8) continue; // Ignora nós muito ao fundo
            const dist = Math.sqrt(Math.pow(mx - n.px, 2) + Math.pow(my - n.py, 2));
            if (dist < 15 * n.scale) {
                found = n;
                break;
            }
        }
        setHoveredNode(found);
        canvas.style.cursor = found ? 'pointer' : mouseRef.current.isDown ? 'grabbing' : 'grab';

        // 2. Rotação da Esfera
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

    // Renderização de Cores para UI (Helper)
    const getRoleColor = (role: string) => {
        switch(role) {
            case 'CORE': return 'text-[var(--color-primary)] border-[var(--color-primary)]';
            case 'GUARD': return 'text-emerald-400 border-emerald-400';
            case 'ANALYST': return 'text-purple-400 border-purple-400';
            case 'CHAOS': return 'text-red-400 border-red-400';
            default: return 'text-white border-white';
        }
    };

    return (
        <div className="relative h-[calc(100vh-6rem)] w-full overflow-hidden rounded-3xl border border-white/10 bg-[#020617] group">

            {/* COMING SOON BADGE */}
            <div className="absolute top-4 right-4 z-50 animate-pulse">
                <div className="bg-gradient-to-r from-[var(--color-primary)]/20 via-[var(--color-accent)]/20 to-[var(--color-secondary)]/20 backdrop-blur-xl border-2 border-[var(--color-primary)]/50 rounded-2xl px-6 py-3 shadow-[0_0_30px_var(--color-primary)]">
                    <div className="flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-ping" />
                        <span className="text-sm font-black text-white uppercase tracking-widest orbitron">
                            Coming Soon
                        </span>
                    </div>
                    <div className="text-[10px] text-gray-400 text-center mt-1 font-mono">
                        Feature in development
                    </div>
                </div>
            </div>

            {/* CANVAS CÓSMICO */}
            <canvas
                ref={canvasRef}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                className="w-full h-full block"
            />

            {/* UI FLUTUANTE: HEADER */}
            <div className="absolute top-6 left-6 pointer-events-none">
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 p-6 rounded-2xl shadow-2xl">
                    <div className="flex items-center gap-3 mb-2">
                        <Globe className="w-6 h-6 text-[var(--color-primary)] animate-pulse" />
                        <h1 className="text-2xl font-black text-white tracking-tight font-display">
                            CELESTIAL NEXUS
                        </h1>
                    </div>
                    <div className="flex items-center gap-4 text-xs font-mono text-[var(--color-text-secondary)]">
                        <span className="flex items-center gap-1"><Activity className="w-3 h-3" /> LIVE FEED</span>
                        <span className="flex items-center gap-1"><Database className="w-3 h-3" /> {nodes.length} NODES</span>
                    </div>
                </div>
            </div>

            {/* UI FLUTUANTE: FILTROS (GLASSMORPHISM) */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-2 bg-black/30 backdrop-blur-xl p-2 rounded-full border border-white/10 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
                {['ALL', 'CORE', 'GUARD', 'ANALYST', 'CHAOS'].map(f => (
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

            {/* UI FLUTUANTE: PAINEL DE DETALHES (SLIDE IN) */}
            {selectedNode && (
                <div className="absolute top-6 right-6 w-80 bg-black/60 backdrop-blur-2xl border border-white/10 p-6 rounded-2xl shadow-2xl animate-slideInRight">
                    <div className="flex justify-between items-start mb-6">
                        <div>
                            <h2 className={`text-xl font-bold mb-1 ${getRoleColor(selectedNode.role).split(' ')[0]}`}>
                                {selectedNode.name}
                            </h2>
                            <span className="text-xs font-mono text-white/50 bg-white/5 px-2 py-1 rounded">
                                ID: {selectedNode.id}
                            </span>
                        </div>
                        <button onClick={() => setSelectedNode(null)} className="text-white/40 hover:text-white">
                            <Maximize2 className="w-5 h-5" />
                        </button>
                    </div>

                    <div className="space-y-4">
                        <div className="bg-white/5 rounded-xl p-4 border border-white/5">
                            <div className="flex justify-between mb-2 text-sm text-gray-400">
                                <span>Neural Load</span>
                                <span>87%</span>
                            </div>
                            <div className="h-1 w-full bg-white/10 rounded-full overflow-hidden">
                                <div className="h-full bg-[var(--color-primary)] w-[87%]" />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            <div className="bg-white/5 rounded-xl p-3 border border-white/5 flex flex-col items-center text-center">
                                <Radio className="w-5 h-5 text-emerald-400 mb-2" />
                                <span className="text-xs text-gray-400">Latency</span>
                                <span className="text-lg font-mono text-white">12ms</span>
                            </div>
                            <div className="bg-white/5 rounded-xl p-3 border border-white/5 flex flex-col items-center text-center">
                                <Scan className="w-5 h-5 text-purple-400 mb-2" />
                                <span className="text-xs text-gray-400">Conns</span>
                                <span className="text-lg font-mono text-white">{selectedNode.connections.length}</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* HINT DE NAVEGAÇÃO */}
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
