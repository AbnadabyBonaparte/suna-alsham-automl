/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - GLOBAL NETWORK (THE PANOPTICON)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/network/page.tsx
 * 🌍 Mapa de conexões - Agents ↔ Banco ↔ OpenAI
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/lib/supabase';
import { Globe, Server, Wifi, Radio, MapPin, Activity, Zap, X, TrendingUp, Clock, Database, Cpu, Brain } from 'lucide-react';

interface NetworkServer {
    id: string;
    lat: number;
    lon: number;
    name: string;
    type: 'database' | 'api' | 'agent' | 'user';
    load: number;
    status: 'online' | 'offline' | 'warning';
    requests: number;
}

export default function NetworkPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [selectedServer, setSelectedServer] = useState<NetworkServer | null>(null);
    const [rotation, setRotation] = useState(0);
    const [servers, setServers] = useState<NetworkServer[]>([]);
    const [stats, setStats] = useState({ 
        packets: 0, 
        latency: 24,
        totalAgents: 0,
        totalRequests: 0,
        activeConnections: 0,
    });
    const [supabaseLatency, setSupabaseLatency] = useState<number>(0);

    // Carregar dados reais e criar servers
    useEffect(() => {
        async function loadNetworkData() {
            try {
                // Medir latência real do Supabase
                const start = performance.now();
                const { count: agentsCount } = await supabase
                    .from('agents')
                    .select('*', { count: 'exact', head: true });
                const end = performance.now();
                const latency = Math.round(end - start);
                setSupabaseLatency(latency);

                // Total requests
                const { count: requestsCount } = await supabase
                    .from('requests')
                    .select('*', { count: 'exact', head: true });

                // Criar servers baseados em dados reais
                const networkServers: NetworkServer[] = [
                    { id: 'SUPABASE', lat: -23, lon: -46, name: 'Supabase Database', type: 'database', load: Math.floor(Math.random() * 30 + 40), status: 'online', requests: agentsCount || 0 },
                    { id: 'OPENAI', lat: 37, lon: -122, name: 'OpenAI API', type: 'api', load: Math.floor(Math.random() * 40 + 50), status: 'online', requests: requestsCount || 0 },
                    { id: 'VERCEL', lat: 37, lon: -122, name: 'Vercel Edge', type: 'api', load: Math.floor(Math.random() * 20 + 30), status: 'online', requests: 0 },
                    { id: 'ORION', lat: 40, lon: -74, name: 'ORION Core', type: 'agent', load: Math.floor(Math.random() * 50 + 40), status: 'online', requests: Math.floor((requestsCount || 0) * 0.3) },
                    { id: 'VOID-HUB', lat: 51, lon: -0.1, name: 'VOID Squad Hub', type: 'agent', load: Math.floor(Math.random() * 30 + 20), status: 'online', requests: Math.floor((requestsCount || 0) * 0.2) },
                    { id: 'NEXUS-CORE', lat: 35, lon: 139, name: 'NEXUS Core', type: 'agent', load: Math.floor(Math.random() * 40 + 30), status: 'online', requests: Math.floor((requestsCount || 0) * 0.25) },
                    { id: 'USER-PORTAL', lat: -23, lon: -46, name: 'User Portal', type: 'user', load: Math.floor(Math.random() * 60 + 30), status: 'online', requests: requestsCount || 0 },
                ];

                setServers(networkServers);

                setStats({
                    packets: Math.floor(Math.random() * 100000),
                    latency,
                    totalAgents: agentsCount || 139,
                    totalRequests: requestsCount || 0,
                    activeConnections: networkServers.filter(s => s.status === 'online').length,
                });

            } catch (err) {
                console.error('Failed to load network data:', err);
            }
        }

        loadNetworkData();
        const interval = setInterval(loadNetworkData, 30000);
        return () => clearInterval(interval);
    }, []);

    // ENGINE VISUAL (HOLO-GLOBE)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let time = 0;
        const GLOBE_RADIUS = 220;
        const DOT_DENSITY = 1000;

        const dots: {theta: number, phi: number, alt: number}[] = [];
        for(let i=0; i<DOT_DENSITY; i++) {
            dots.push({
                theta: Math.random() * 2 * Math.PI,
                phi: Math.acos((Math.random() * 2) - 1),
                alt: 1
            });
        }

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

            ctx.fillStyle = 'rgba(2, 6, 23, 0.3)';
            ctx.fillRect(0, 0, w, h);

            time += 0.005;
            setRotation(time);

            const themeColor = '#0EA5E9';

            // Desenhar globo de pontos
            dots.forEach(dot => {
                const rotTheta = dot.theta + time;

                const x = GLOBE_RADIUS * Math.sin(dot.phi) * Math.cos(rotTheta);
                const y = GLOBE_RADIUS * Math.cos(dot.phi);
                const z = GLOBE_RADIUS * Math.sin(dot.phi) * Math.sin(rotTheta);

                const scale = 400 / (400 + z);
                const px = cx + x * scale;
                const py = cy + y * scale;
                const alpha = (z + GLOBE_RADIUS) / (2 * GLOBE_RADIUS);

                if (z > -100) {
                    ctx.fillStyle = themeColor;
                    ctx.globalAlpha = alpha * 0.6;
                    ctx.beginPath();
                    ctx.arc(px, py, 1.5 * scale, 0, Math.PI * 2);
                    ctx.fill();
                }
            });

            // Desenhar servers
            servers.forEach(server => {
                const phi = (90 - server.lat) * (Math.PI / 180);
                const theta = (server.lon + 180) * (Math.PI / 180) + time;

                const x = GLOBE_RADIUS * Math.sin(phi) * Math.cos(theta);
                const y = GLOBE_RADIUS * Math.cos(phi);
                const z = GLOBE_RADIUS * Math.sin(phi) * Math.sin(theta);

                const scale = 400 / (400 + z);
                const px = cx + x * scale;
                const py = cy + y * scale;

                if (z > 0) {
                    // Ping wave
                    const wave = (Date.now() / 20) % 50;
                    ctx.strokeStyle = server.type === 'database' ? '#10B981' : 
                                     server.type === 'api' ? '#8B5CF6' : 
                                     server.type === 'agent' ? '#FFD700' : themeColor;
                    ctx.globalAlpha = 1 - (wave / 50);
                    ctx.beginPath();
                    ctx.arc(px, py, wave * scale, 0, Math.PI * 2);
                    ctx.stroke();

                    // Ponto central
                    ctx.fillStyle = '#FFFFFF';
                    ctx.globalAlpha = 1;
                    ctx.beginPath();
                    ctx.arc(px, py, 4 * scale, 0, Math.PI * 2);
                    ctx.fill();

                    // Haste
                    ctx.strokeStyle = ctx.strokeStyle;
                    ctx.globalAlpha = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(px, py);
                    ctx.lineTo(px, py - 20 * scale);
                    ctx.stroke();

                    // Label
                    ctx.font = `bold ${10 * scale}px monospace`;
                    ctx.fillStyle = '#FFFFFF';
                    ctx.globalAlpha = 1;
                    ctx.fillText(server.id, px + 5, py - 25 * scale);
                }
            });

            // Satélites
            ctx.globalAlpha = 0.1;
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 1;
            
            ctx.beginPath();
            ctx.ellipse(cx, cy, GLOBE_RADIUS + 20, (GLOBE_RADIUS + 20) * 0.3, 0, 0, Math.PI * 2);
            ctx.stroke();

            ctx.globalAlpha = 1;
            satellites.forEach(sat => {
                sat.angle += sat.speed;
                const sx = cx + Math.cos(sat.angle) * sat.radius;
                const sy = cy + Math.sin(sat.angle) * (sat.radius * 0.3);
                
                if (Math.sin(sat.angle) > 0) {
                    ctx.fillStyle = '#FCD34D';
                    ctx.shadowColor = '#FCD34D';
                    ctx.shadowBlur = 10;
                    ctx.beginPath();
                    ctx.arc(sx, sy, sat.size, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }
            });

            // Conexões entre servers (data flow)
            ctx.globalAlpha = 0.3;
            ctx.strokeStyle = themeColor;
            ctx.lineWidth = 1;
            ctx.setLineDash([5, 5]);
            
            for (let i = 0; i < servers.length; i++) {
                for (let j = i + 1; j < servers.length; j++) {
                    const s1 = servers[i];
                    const s2 = servers[j];
                    
                    const phi1 = (90 - s1.lat) * (Math.PI / 180);
                    const theta1 = (s1.lon + 180) * (Math.PI / 180) + time;
                    const x1 = GLOBE_RADIUS * Math.sin(phi1) * Math.cos(theta1);
                    const y1 = GLOBE_RADIUS * Math.cos(phi1);
                    const z1 = GLOBE_RADIUS * Math.sin(phi1) * Math.sin(theta1);
                    
                    const phi2 = (90 - s2.lat) * (Math.PI / 180);
                    const theta2 = (s2.lon + 180) * (Math.PI / 180) + time;
                    const x2 = GLOBE_RADIUS * Math.sin(phi2) * Math.cos(theta2);
                    const y2 = GLOBE_RADIUS * Math.cos(phi2);
                    const z2 = GLOBE_RADIUS * Math.sin(phi2) * Math.sin(theta2);
                    
                    if (z1 > 0 && z2 > 0) {
                        const scale1 = 400 / (400 + z1);
                        const scale2 = 400 / (400 + z2);
                        
                        ctx.beginPath();
                        ctx.moveTo(cx + x1 * scale1, cy + y1 * scale1);
                        ctx.lineTo(cx + x2 * scale2, cy + y2 * scale2);
                        ctx.stroke();
                    }
                }
            }
            ctx.setLineDash([]);

            requestAnimationFrame(render);
        };

        render();

        return () => window.removeEventListener('resize', resize);
    }, [servers]);

    // Simulador de tráfego
    useEffect(() => {
        const interval = setInterval(() => {
            setStats(prev => ({
                ...prev,
                packets: prev.packets + Math.floor(Math.random() * 500),
            }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* CANVAS */}
            <div className="absolute inset-0 bg-[#020617] -z-10">
                <canvas ref={canvasRef} className="w-full h-full" />
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                <div className="absolute inset-0 bg-radial-gradient from-transparent via-transparent to-black/90 pointer-events-none" />
            </div>

            {/* ESQUERDA: LISTA DE SERVIDORES */}
            <div className="w-full lg:w-80 flex flex-col gap-4 z-10 h-full pointer-events-none">
                <div className="bg-black/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 pointer-events-auto shadow-2xl">
                    <div className="flex items-center gap-3 mb-6">
                        <Globe className="w-6 h-6 animate-spin" style={{ animationDuration: '10s', color: 'var(--color-primary)' }} />
                        <div>
                            <h1 className="text-xl font-black text-white tracking-tight font-display">GLOBAL NET</h1>
                            <p className="text-xs text-gray-400 font-mono">Active Nodes: {servers.length}</p>
                        </div>
                    </div>

                    <div className="space-y-3 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-white/10">
                        {servers.map((server) => (
                            <div
                                key={server.id}
                                onClick={() => setSelectedServer(server)}
                                className="group p-3 rounded-lg border border-white/5 bg-white/5 hover:bg-white/10 hover:border-cyan-500/50 transition-all cursor-pointer hover:scale-105"
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center gap-2">
                                        {server.type === 'database' ? <Database className="w-3 h-3" style={{ color: 'var(--color-success)' }} /> :
                                         server.type === 'api' ? <Cpu className="w-3 h-3" style={{ color: 'var(--color-accent)' }} /> :
                                         server.type === 'agent' ? <Brain className="w-3 h-3" style={{ color: 'var(--color-warning)' }} /> :
                                         <MapPin className="w-3 h-3" style={{ color: 'var(--color-primary)' }} />}
                                        <span className="text-sm font-bold text-white">{server.id}</span>
                                    </div>
                                    <span className="text-xs font-mono" style={{ color: server.load > 80 ? 'var(--color-error)' : 'var(--color-success)' }}>
                                        {server.load}% LOAD
                                    </span>
                                </div>
                                <div className="text-xs text-gray-400 font-mono pl-5">{server.name}</div>
                                <div className="mt-3 h-1 w-full bg-black/50 rounded-full overflow-hidden">
                                    <div 
                                        className="h-full transition-all duration-1000" 
                                        style={{ width: `${server.load}%`, background: server.load > 80 ? 'var(--color-error)' : 'var(--color-primary)' }} 
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* DIREITA: STATS */}
            <div className="absolute top-6 right-6 z-10 flex flex-col gap-3 w-64">
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Supabase Latency</span>
                        <Wifi className="w-4 h-4" style={{ color: 'var(--color-success)' }} />
                    </div>
                    <div className="text-3xl font-mono text-white">{supabaseLatency} <span className="text-sm text-gray-500">ms</span></div>
                </div>

                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Total Requests</span>
                        <Activity className="w-4 h-4" style={{ color: 'var(--color-primary)' }} />
                    </div>
                    <div className="text-2xl font-mono text-white">{stats.totalRequests.toLocaleString()}</div>
                </div>

                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Active Agents</span>
                        <Brain className="w-4 h-4" style={{ color: 'var(--color-warning)' }} />
                    </div>
                    <div className="text-2xl font-mono text-white">{stats.totalAgents}</div>
                </div>

                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-gray-400 uppercase font-mono">Network Status</span>
                        <Radio className="w-4 h-4 animate-pulse" style={{ color: 'var(--color-success)' }} />
                    </div>
                    <div className="text-sm font-bold tracking-widest" style={{ color: 'var(--color-success)' }}>ENCRYPTED</div>
                </div>
            </div>

            {/* RODAPÉ */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 bg-black/40 backdrop-blur-md border border-white/10 px-6 py-2 rounded-full text-xs font-mono text-gray-400 flex items-center gap-3">
                <div className="w-2 h-2 rounded-full animate-ping" style={{ background: 'var(--color-primary)' }} />
                <span>SCANNING SECTOR {Math.floor(rotation * 100 % 360)}°</span>
            </div>

            {/* MODAL */}
            {selectedServer && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
                    onClick={() => setSelectedServer(null)}
                >
                    <div
                        className="relative bg-black/95 border-2 border-cyan-500/50 backdrop-blur-xl rounded-2xl p-8 max-w-2xl w-full shadow-[0_0_80px_rgba(6,182,212,0.3)]"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            onClick={() => setSelectedServer(null)}
                            className="absolute top-4 right-4 p-2 rounded-lg bg-black/40 hover:bg-black/60 text-gray-400 hover:text-white transition-all"
                        >
                            <X className="w-6 h-6" />
                        </button>

                        <div className="flex items-center gap-6 mb-8">
                            <div className="p-6 rounded-2xl bg-black/80 border border-[var(--color-primary)]/30 shadow-[0_0_20px_var(--color-primary)/30]" style={{ color: 'var(--color-primary)' }}>
                                {selectedServer.type === 'database' ? <Database className="w-8 h-8" /> :
                                 selectedServer.type === 'api' ? <Cpu className="w-8 h-8" /> :
                                 selectedServer.type === 'agent' ? <Brain className="w-8 h-8" /> :
                                 <Server className="w-8 h-8" />}
                            </div>
                            <div>
                                <h2 className="text-4xl font-black text-white tracking-wide mb-2">
                                    {selectedServer.id}
                                </h2>
                                <p className="text-gray-400 font-mono">{selectedServer.name}</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6 mb-6">
                            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <Activity className="w-5 h-5" style={{ color: 'var(--color-primary)' }} />
                                    <span className="text-sm text-gray-400 uppercase font-mono">Server Load</span>
                                </div>
                                <div className="text-3xl font-bold" style={{ color: selectedServer.load > 80 ? 'var(--color-error)' : 'var(--color-success)' }}>
                                    {selectedServer.load}%
                                </div>
                            </div>

                            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <TrendingUp className="w-5 h-5" style={{ color: 'var(--color-success)' }} />
                                    <span className="text-sm text-gray-400 uppercase font-mono">Requests</span>
                                </div>
                                <div className="text-3xl font-bold text-white">
                                    {selectedServer.requests.toLocaleString()}
                                </div>
                            </div>

                            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <MapPin className="w-5 h-5" style={{ color: 'var(--color-warning)' }} />
                                    <span className="text-sm text-gray-400 uppercase font-mono">Location</span>
                                </div>
                                <div className="text-xl font-mono text-white">
                                    {selectedServer.lat}°, {selectedServer.lon}°
                                </div>
                            </div>

                            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <Zap className="w-5 h-5" style={{ color: 'var(--color-success)' }} />
                                    <span className="text-sm text-gray-400 uppercase font-mono">Status</span>
                                </div>
                                <div className="text-xl font-bold" style={{ color: selectedServer.status === 'online' ? 'var(--color-success)' : 'var(--color-error)' }}>
                                    {selectedServer.status.toUpperCase()}
                                </div>
                            </div>
                        </div>

                        <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                            <h3 className="text-xs text-gray-500 uppercase tracking-widest mb-3 font-mono">
                                Resource Usage
                            </h3>
                            <div className="space-y-3">
                                <div>
                                    <div className="flex justify-between text-sm mb-2 font-mono">
                                        <span className="text-gray-400">CPU</span>
                                        <span className="font-bold" style={{ color: selectedServer.load > 80 ? 'var(--color-error)' : 'var(--color-primary)' }}>
                                            {selectedServer.load}%
                                        </span>
                                    </div>
                                    <div className="w-full bg-white/5 h-3 rounded-full overflow-hidden">
                                        <div
                                            className="h-full transition-all duration-1000"
                                            style={{
                                                width: `${selectedServer.load}%`,
                                                background: selectedServer.load > 80 ? 'var(--color-error)' : 'linear-gradient(to right, var(--color-primary), var(--color-accent))'
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
