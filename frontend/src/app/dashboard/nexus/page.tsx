/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - NEURAL NEXUS: ELASTIC WEB EDITION
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/nexus/page.tsx
 * 📋 Física de molas, sinapses ativas e interação de "puxar"
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    Network, Play, Pause, RefreshCw, 
    Cpu, Zap, Activity, MousePointer2, Expand 
} from 'lucide-react';

// Tipos para o sistema de física avançada
interface Node {
    id: string;
    name: string;
    type: 'core' | 'specialist' | 'observer' | 'chaos';
    x: number;
    y: number;
    vx: number;
    vy: number;
    mass: number;
    radius: number;
    connections: string[]; // IDs dos vizinhos
    efficiency: number;
}

// Partícula de dados que viaja na linha (Sinapse)
interface Synapse {
    fromId: string;
    toId: string;
    progress: number; // 0 a 1
    speed: number;
    color: string;
}

export default function NexusPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estado da simulação (usando Refs para performance máxima 60fps sem re-renders)
    const nodesRef = useRef<Node[]>([]);
    const synapsesRef = useRef<Synapse[]>([]);
    const draggingNodeRef = useRef<Node | null>(null);
    const mouseRef = useRef({ x: 0, y: 0 });
    
    // Estado de UI (React)
    const [isAnimating, setIsAnimating] = useState(true);
    const [stats, setStats] = useState({ active: 0, traffic: 0 });
    const [hoveredNodeName, setHoveredNodeName] = useState<string | null>(null);

    const animationRef = useRef<number>();

    // 1. INICIALIZAÇÃO (O Big Bang Neural)
    useEffect(() => {
        const initNodes = () => {
            const types: Node['type'][] = ['core', 'specialist', 'observer', 'chaos'];
            const newNodes: Node[] = [];
            const width = window.innerWidth;
            const height = window.innerHeight;

            // Criar 80 nós (menos nós para física mais fluida e elástica)
            for (let i = 0; i < 80; i++) {
                const type = types[Math.floor(Math.random() * types.length)];
                newNodes.push({
                    id: `node_${i}`,
                    name: `NEURON_${String(i + 1).padStart(3, '0')}`,
                    type,
                    x: width / 2 + (Math.random() - 0.5) * 400,
                    y: height / 2 + (Math.random() - 0.5) * 400,
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    mass: type === 'core' ? 5 : 2, // Cores são mais pesados
                    radius: type === 'core' ? 12 : type === 'chaos' ? 8 : 5,
                    connections: [],
                    efficiency: Math.random() * 100
                });
            }

            // Criar conexões orgânicas (Vizinhos próximos)
            newNodes.forEach((node, i) => {
                // Conectar com os 3 vizinhos mais próximos iniciais
                const neighbors = newNodes
                    .map((n, idx) => ({ idx, dist: Math.hypot(n.x - node.x, n.y - node.y) }))
                    .sort((a, b) => a.dist - b.dist)
                    .slice(1, 4); // Pula o próprio nó (índice 0)

                neighbors.forEach(neighbor => {
                    const targetId = newNodes[neighbor.idx].id;
                    if (!node.connections.includes(targetId)) {
                        node.connections.push(targetId);
                        // Conexão bidirecional para física estável
                        const target = newNodes[neighbor.idx];
                        if (!target.connections.includes(node.id)) {
                            target.connections.push(node.id);
                        }
                    }
                });
            });

            nodesRef.current = newNodes;
        };

        initNodes();
    }, []);

    // 2. LOOP DE FÍSICA E RENDERIZAÇÃO
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

        // Configurações de Física
        const SPRING_LENGTH = 150;
        const SPRING_STRENGTH = 0.05; // Quão forte a teia puxa de volta
        const REPULSION = 200; // Força de repulsão (evita bolos)
        const DAMPING = 0.95; // Fricção do ar (para parar devagar)
        const MOUSE_INFLUENCE = 0.2; // Suavidade do arrasto

        const animate = () => {
            if (!isAnimating) return;

            // Limpar com rastro (Motion Blur cinematográfico)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.15)'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // --- FÍSICA ---
            nodesRef.current.forEach(node => {
                // Se estiver sendo arrastado, ignora física e segue o mouse
                if (draggingNodeRef.current?.id === node.id) {
                    node.x += (mouseRef.current.x - node.x) * MOUSE_INFLUENCE;
                    node.y += (mouseRef.current.y - node.y) * MOUSE_INFLUENCE;
                    node.vx = 0;
                    node.vy = 0;
                    return;
                }

                let fx = 0;
                let fy = 0;

                // 1. Repulsão (Coulomb) - Nós se odeiam
                nodesRef.current.forEach(other => {
                    if (node.id === other.id) return;
                    const dx = node.x - other.x;
                    const dy = node.y - other.y;
                    const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                    
                    if (dist < 300) {
                        const force = REPULSION / (dist * dist);
                        fx += (dx / dist) * force;
                        fy += (dy / dist) * force;
                    }
                });

                // 2. Atração (Hooke) - Conexões se amam (Molas)
                node.connections.forEach(connId => {
                    const target = nodesRef.current.find(n => n.id === connId);
                    if (!target) return;

                    const dx = target.x - node.x;
                    const dy = target.y - node.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    // Força elástica
                    const force = (dist - SPRING_LENGTH) * SPRING_STRENGTH;
                    fx += (dx / dist) * force;
                    fy += (dy / dist) * force;
                });

                // 3. Gravidade Central (Para não sumirem da tela)
                const dxCenter = (canvas.width / 2) - node.x;
                const dyCenter = (canvas.height / 2) - node.y;
                fx += dxCenter * 0.0005;
                fy += dyCenter * 0.0005;

                // Aplicar forças
                node.vx = (node.vx + fx / node.mass) * DAMPING;
                node.vy = (node.vy + fy / node.mass) * DAMPING;
                node.x += node.vx;
                node.y += node.vy;

                // Bordas
                const margin = 50;
                if (node.x < margin) node.vx += 1;
                if (node.x > canvas.width - margin) node.vx -= 1;
                if (node.y < margin) node.vy += 1;
                if (node.y > canvas.height - margin) node.vy -= 1;
            });

            // --- GERAÇÃO DE SINAPSES (DADOS) ---
            // Chance aleatória de disparar um dado entre conexões
            if (Math.random() > 0.85) {
                const sourceNode = nodesRef.current[Math.floor(Math.random() * nodesRef.current.length)];
                if (sourceNode.connections.length > 0) {
                    const targetId = sourceNode.connections[Math.floor(Math.random() * sourceNode.connections.length)];
                    synapsesRef.current.push({
                        fromId: sourceNode.id,
                        toId: targetId,
                        progress: 0,
                        speed: 0.02 + Math.random() * 0.03, // Velocidade variável
                        color: sourceNode.type === 'chaos' ? '#EF4444' : '#00FFD0'
                    });
                }
            }

            // --- RENDERIZAÇÃO ---
            
            // A. Desenhar Conexões (Teia)
            ctx.lineWidth = 1;
            nodesRef.current.forEach(node => {
                node.connections.forEach(connId => {
                    const target = nodesRef.current.find(n => n.id === connId);
                    if (!target) return;

                    // Desenhar linha apenas uma vez por par
                    if (node.id < target.id) {
                        const dist = Math.hypot(target.x - node.x, target.y - node.y);
                        const opacity = Math.max(0.05, 1 - dist / 400); // Mais transparente se longe (esticado)
                        
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 255, 200, ${opacity * 0.5})`;
                        ctx.moveTo(node.x, node.y);
                        ctx.lineTo(target.x, target.y);
                        ctx.stroke();
                    }
                });
            });

            // B. Desenhar e Atualizar Sinapses (Partículas na linha)
            for (let i = synapsesRef.current.length - 1; i >= 0; i--) {
                const synapse = synapsesRef.current[i];
                synapse.progress += synapse.speed;

                const from = nodesRef.current.find(n => n.id === synapse.fromId);
                const to = nodesRef.current.find(n => n.id === synapse.toId);

                if (!from || !to || synapse.progress >= 1) {
                    synapsesRef.current.splice(i, 1); // Remover se chegou ou nó sumiu
                    continue;
                }

                const x = from.x + (to.x - from.x) * synapse.progress;
                const y = from.y + (to.y - from.y) * synapse.progress;

                // Desenhar "Pacote de Dados"
                ctx.beginPath();
                ctx.fillStyle = synapse.color;
                ctx.shadowBlur = 10;
                ctx.shadowColor = synapse.color;
                ctx.arc(x, y, 3, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0; // Reset
            }

            // C. Desenhar Nós
            nodesRef.current.forEach(node => {
                const isHovered = hoveredNodeName === node.name;
                const isDragging = draggingNodeRef.current?.id === node.id;

                // Cor baseada no tipo
                let color = '#374151';
                if (node.type === 'core') color = '#00FFD0';
                else if (node.type === 'specialist') color = '#A855F7';
                else if (node.type === 'observer') color = '#F59E0B';
                else if (node.type === 'chaos') color = '#EF4444';

                // Glow
                ctx.beginPath();
                const glowSize = isDragging ? 30 : isHovered ? 20 : 0;
                if (glowSize > 0) {
                    const glow = ctx.createRadialGradient(node.x, node.y, node.radius, node.x, node.y, node.radius + glowSize);
                    glow.addColorStop(0, color);
                    glow.addColorStop(1, 'transparent');
                    ctx.fillStyle = glow;
                    ctx.arc(node.x, node.y, node.radius + glowSize, 0, Math.PI * 2);
                    ctx.fill();
                }

                // Corpo do Nó
                ctx.beginPath();
                ctx.fillStyle = isDragging ? '#FFFFFF' : color;
                ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
                ctx.fill();

                // Label (só se hover ou drag)
                if (isHovered || isDragging) {
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 12px monospace';
                    ctx.fillText(node.name, node.x + 15, node.y - 5);
                    ctx.fillStyle = '#AAAAAA';
                    ctx.font = '10px monospace';
                    ctx.fillText(node.type.toUpperCase(), node.x + 15, node.y + 8);
                }
            });

            // Atualizar Stats UI
            setStats({
                active: nodesRef.current.length,
                traffic: synapsesRef.current.length
            });

            animationRef.current = requestAnimationFrame(animate);
        };

        animate();

        return () => {
            window.removeEventListener('resize', resize);
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
        };
    }, [isAnimating, hoveredNodeName]);

    // 3. CONTROLES DO MOUSE (INTERAÇÃO FÍSICA)
    const handleMouseDown = (e: React.MouseEvent) => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Encontrar nó clicado (Hit Test)
        const clickedNode = nodesRef.current.find(n => {
            const dist = Math.hypot(n.x - mouseX, n.y - mouseY);
            return dist < n.radius * 2; // Área de clique generosa
        });

        if (clickedNode) {
            draggingNodeRef.current = clickedNode;
            mouseRef.current = { x: mouseX, y: mouseY };
        }
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        mouseRef.current = { x: mouseX, y: mouseY };

        // Lógica de Hover (apenas visual)
        if (!draggingNodeRef.current) {
            const node = nodesRef.current.find(n => Math.hypot(n.x - mouseX, n.y - mouseY) < n.radius + 5);
            setHoveredNodeName(node ? node.name : null);
            canvas.style.cursor = node ? 'grab' : 'default';
        } else {
            canvas.style.cursor = 'grabbing';
        }
    };

    const handleMouseUp = () => {
        draggingNodeRef.current = null;
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col rounded-3xl overflow-hidden border border-[var(--color-border)]/20 bg-black relative">
            
            {/* OVERLAY DE INFORMAÇÕES */}
            <div className="absolute top-6 left-6 z-20 pointer-events-none">
                <div className="bg-black/60 backdrop-blur-md border border-white/10 rounded-2xl p-5 shadow-2xl">
                    <div className="flex items-center gap-3 mb-4">
                        <Activity className="w-5 h-5 text-[var(--color-primary)] animate-pulse" />
                        <h2 className="text-white font-bold tracking-widest">NEURAL TRAFFIC</h2>
                    </div>
                    <div className="flex gap-6">
                        <div>
                            <div className="text-[10px] text-gray-500 uppercase font-mono">Nodes Online</div>
                            <div className="text-2xl font-mono text-white">{stats.active}</div>
                        </div>
                        <div>
                            <div className="text-[10px] text-gray-500 uppercase font-mono">Synapses/Sec</div>
                            <div className="text-2xl font-mono text-[var(--color-accent)]">{stats.traffic * 12}</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* CANVAS PRINCIPAL */}
            <canvas
                ref={canvasRef}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                className="w-full h-full cursor-crosshair active:cursor-grabbing"
            />

            {/* DICA DE INTERAÇÃO */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                <div className="px-4 py-2 rounded-full bg-black/40 border border-white/10 backdrop-blur text-xs text-gray-400 font-mono flex items-center gap-2">
                    <MousePointer2 className="w-3 h-3" />
                    <span>CLIQUE E ARRASTE PARA INTERAGIR COM A TEIA</span>
                </div>
            </div>

            {/* CONTROLES DE REFRESH */}
            <button 
                onClick={() => window.location.reload()} // Maneira preguiçosa mas eficaz de resetar o big bang
                className="absolute top-6 right-6 z-20 p-3 rounded-xl bg-black/60 border border-white/10 hover:bg-white/10 transition-colors text-white"
            >
                <RefreshCw className="w-5 h-5" />
            </button>
        </div>
    );
}
