/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - GLOBAL NETWORK (THE PANOPTICON)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/network/page.tsx
 * 📋 Globo 3D Holográfico com tráfego de dados e satélites
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { Globe, Server, Wifi, Radio, MapPin, Activity, Zap } from 'lucide-react';

// Dados dos Servidores (Nodes)
const SERVERS = [
    { id: 'US-EAST', lat: 40, lon: -74, name: 'New York Core', load: 89 },
    { id: 'EU-WEST', lat: 51, lon: -0.1, name: 'London Edge', load: 45 },
    { id: 'ASIA-PAC', lat: 35, lon: 139, name: 'Tokyo Prime', load: 67 },
    { id: 'SA-EAST', lat: -23, lon: -46, name: 'Sao Paulo Hub', load: 92 },
    { id: 'AUS-SE', lat: -33, lon: 151, name: 'Sydney Node', load: 34 },
    { id: 'RU-NORTH', lat: 55, lon: 37, name: 'Moscow Relay', load: 78 },
];

export default function NetworkPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [hoveredServer, setHoveredServer] = useState<any>(null);
    const [rotation, setRotation] = useState(0);
    const [stats, setStats] = useState({ packets: 0, latency: 24 });

    // 1. ENGINE VISUAL (HOLO-GLOBE)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        const GLOBE_RADIUS = 220;
        const DOT_DENSITY = 1000;

        // Gerar Pontos da Esfera (Pontos de Dados)
        const dots: {theta: number, phi: number, alt: number}[] = [];
        for(let i=0; i<DOT_DENSITY; i++) {
            dots.push({
                theta: Math.random() * 2 * Math.PI, // Longitude
                phi: Math.acos((Math.random() * 2) - 1), // Latitude
                alt: 1 // Altitude base
            });
        }

        // Gerar Satélites
        const satellites = [
            { angle: 0, speed: 0.02, radius: GLOBE_RADIUS + 60, size: 4 },
            { angle: 2, speed: -0.015, radius: GLOBE_RADIUS + 100, size: 3 },
            { angle: 4, speed: 0.03, radius: GLOBE_RADIUS + 40, size: 2 },
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

            // Limpar
            ctx.fillStyle = 'rgba(2, 6, 23, 0.3)'; // Rastro suave
            ctx.fillRect(0, 0, w, h);

            time += 0.005;
            setRotation(time);

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#0EA5E9';

            // --- 1. DESENHAR GLOBO DE PONTOS ---
            dots.forEach(dot => {
                // Rotação do Globo
                const rotTheta = dot.theta + time;

                // Coordenadas 3D
                const x = GLOBE_RADIUS * Math.sin(dot.phi) * Math.cos(rotTheta);
                const y = GLOBE_RADIUS * Math.cos(dot.phi);
                const z = GLOBE_RADIUS * Math.sin(dot.phi) * Math.sin(rotTheta);

                // Perspectiva
                const scale = 400 / (400 + z);
                const px = cx + x * scale;
                const py = cy + y * scale;
                const alpha = (z + GLOBE_RADIUS) / (2 * GLOBE_RADIUS); // Fade atrás

                if (z > -100) { // Culling (não desenha muito atrás)
                    ctx.fillStyle = themeColor;
                    ctx.globalAlpha = alpha * 0.6;
                    ctx.beginPath();
                    ctx.arc(px, py, 1.5 * scale, 0, Math.PI * 2);
                    ctx.fill();
                }
            });

            // --- 2. DESENHAR SERVIDORES (NODES PRINCIPAIS) ---
            SERVERS.forEach(server => {
                // Converter Lat/Lon para coordenadas esféricas
                const phi = (90 - server.lat) * (Math.PI / 180);
                const theta = (server.lon + 180) * (Math.PI / 180) + time; // +time para girar junto

                const x = GLOBE_RADIUS * Math.sin(phi) * Math.cos(theta);
                const y = GLOBE_RADIUS * Math.cos(phi);
                const z = GLOBE_RADIUS * Math.sin(phi) * Math.sin(theta);

                const scale = 400 / (400 + z);
                const px = cx + x * scale;
                const py = cy + y * scale;

                // Só desenha se estiver na frente
                if (z > 0) {
                    // Ping (Radar Wave)
                    const wave = (Date.now() / 20) % 50;
                    ctx.strokeStyle = themeColor;
                    ctx.globalAlpha = 1 - (wave / 50);
                    ctx.beginPath();
                    ctx.arc(px, py, wave * scale, 0, Math.PI * 2);
                    ctx.stroke();

                    // Ponto Central
                    ctx.fillStyle = '#FFFFFF';
                    ctx.globalAlpha = 1;
                    ctx.beginPath();
                    ctx.arc(px, py, 4 * scale, 0, Math.PI * 2);
                    ctx.fill();

                    // Haste Vertical (Holograma de Localização)
                    ctx.strokeStyle = themeColor;
                    ctx.beginPath();
                    ctx.moveTo(px, py);
                    ctx.lineTo(px, py - 20 * scale);
                    ctx.stroke();

                    // Label
                    ctx.font = `bold ${10 * scale}px monospace`;
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fillText(server.id, px + 5, py - 25 * scale);
                }
            });

            // --- 3. TRAJETÓRIAS DE DADOS (ARCS) ---
            // Conectar US-EAST com todos os outros (Hub)
            // (Cálculo simplificado de curva Bézier 3D)
            // [Código omitido para brevidade, focado no visual limpo]

            // --- 4. SATÉLITES E ANÉIS ---
            ctx.globalAlpha = 0.1;
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 1;
            
            // Anel Equatorial
            ctx.beginPath();
            ctx.ellipse(cx, cy, GLOBE_RADIUS + 20, (GLOBE_RADIUS + 20) * 0.3, 0, 0, Math.PI * 2);
            ctx.stroke();

            // Satélites Orbitando
            ctx.globalAlpha = 1;
            satellites.forEach(sat => {
                sat.angle += sat.speed;
                const sx = cx + Math.cos(sat.angle) * sat.radius;
                const sy = cy + Math.sin(sat.angle) * (sat.radius * 0.3); // Orbita inclinada
                
                // Se estiver na frente
                if (Math.sin(sat.angle) > 0) {
                    ctx.fillStyle = '#FCD34D'; // Dourado
                    ctx.shadowColor = '#FCD34D';
                    ctx.shadowBlur = 10;
                    ctx.beginPath();
                    ctx.arc(sx, sy, sat.size, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }
            });

            // --- 5. SCANNER PLANETÁRIO (LASER) ---
            const scanY = cy + Math.sin(time * 2) * GLOBE_RADIUS;
            const scanHeight = Math.cos(time * 2) * GLOBE_RADIUS; // Largura na esfera
            
            /* 
               Efeito de laser removido para não poluir demais, 
               focando na elegância do globo. 
            */

            requestAnimationFrame(render);
        };

        render();

        return () => window.removeEventListener('resize', resize);
    }, []);

    // Simulador de Tráfego
    useEffect(() => {
        const interval = setInterval(() => {
            setStats(prev => ({
                packets: prev.packets + Math.floor(Math.random() * 500),
                latency: 20 + Math.floor(Math.random() * 10)
            }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* CANVAS BACKGROUND (O GLOBO) */}
            <div className="absolute inset-0 bg-[#020617] -z-10">
                <canvas ref={canvasRef} className="w-full h-full" />
                {/* Overlay Grid Tech */}
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/90 pointer-events-none" />
            </div>

            {/* ESQUERDA: LISTA DE SERVIDORES */}
            <div className="w-full lg:w-80 flex flex-col gap-4 z-10 h-full pointer-events-none">
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-6 pointer-events-auto shadow-2xl">
                    <div className="flex items-center gap-3 mb-6">
                        <Globe className="w-6 h-6 text-[var(--color-primary)] animate-spin-slow" />
                        <div>
                            <h1 className="text-xl font-black text-white tracking-tight font-display">GLOBAL NET</h1>
                            <p className="text-xs text-gray-400 font-mono">Active Nodes: {SERVERS.length}</p>
                        </div>
                    </div>

                    <div className="space-y-3 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-white/10">
                        {SERVERS.map((server) => (
                            <div 
                                key={server.id}
                                className="group p-3 rounded-lg border border-white/5 bg-white/5 hover:bg-white/10 hover:border-[var(--color-primary)]/50 transition-all cursor-pointer"
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center gap-2">
                                        <MapPin className="w-3 h-3 text-[var(--color-primary)]" />
                                        <span className="text-sm font-bold text-white">{server.id}</span>
                                    </div>
                                    <span className={`text-xs font-mono ${server.load > 80 ? 'text-red-400' : 'text-emerald-400'}`}>
                                        {server.load}% LOAD
                                    </span>
                                </div>
                                <div className="text-xs text-gray-400 font-mono pl-5">{server.name}</div>
                                {/* Load Bar */}
                                <div className="mt-3 h-1 w-full bg-black/50 rounded-full overflow-hidden">
                                    <div 
                                        className={`h-full transition-all duration-1000 ${server.load > 80 ? 'bg-red-500' : 'bg-[var(--color-primary)]'}`} 
                                        style={{ width: `${server.load}%` }} 
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* DIREITA: ESTATÍSTICAS DE REDE */}
            <div className="absolute top-6 right-6 z-10 flex flex-col gap-3 w-64">
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4 animate-fadeInRight">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Global Latency</span>
                        <Wifi className="w-4 h-4 text-emerald-400" />
                    </div>
                    <div className="text-3xl font-mono text-white">{stats.latency} <span className="text-sm text-gray-500">ms</span></div>
                </div>

                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4 animate-fadeInRight" style={{animationDelay: '0.1s'}}>
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Total Packets</span>
                        <Activity className="w-4 h-4 text-[var(--color-primary)]" />
                    </div>
                    <div className="text-2xl font-mono text-white">{stats.packets.toLocaleString()}</div>
                </div>

                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4 animate-fadeInRight" style={{animationDelay: '0.2s'}}>
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Network Status</span>
                        <Radio className="w-4 h-4 text-[var(--color-accent)] animate-pulse" />
                    </div>
                    <div className="text-sm font-bold text-[var(--color-accent)] tracking-widest">ENCRYPTED</div>
                </div>
            </div>

            {/* RODAPÉ: LOCALIZAÇÃO ATUAL */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 bg-black/40 backdrop-blur-md border border-white/10 px-6 py-2 rounded-full text-xs font-mono text-gray-400 flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
                <span>SCANNING SECTOR {Math.floor(rotation * 100 % 360)}°</span>
            </div>

            <style jsx>{`
                .animate-spin-slow { animation: spin 10s linear infinite; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                @keyframes fadeInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
                .animate-fadeInRight { animation: fadeInRight 0.3s ease-out forwards; }
            `}</style>
        </div>
    );
}
