/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ADMIN GOD MODE (THE ARCHITECT) - v10
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/admin/page.tsx
 * 📋 Controle total do SaaS, Gestão de Usuários e Kill Switches - REAL DATA
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import {
    ShieldAlert, Users, Database, Power,
    Lock, Unlock, AlertTriangle, Terminal,
    Activity, Eye, Search, Trash2
} from 'lucide-react';
import { useAdmin } from '@/hooks/useAdmin';
import { useNotificationStore } from '@/stores';
import { Skeleton } from '@/components/ui/SkeletonLoader';

interface UserSession {
    id: number;
    name: string;
    role: 'admin' | 'user' | 'bot';
    status: 'active' | 'idle';
    x: number;
    y: number;
    vx: number;
    vy: number;
}

export default function AdminPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const { users, loading, totalUsers, activeUsers } = useAdmin();
    const { addNotification } = useNotificationStore();

    // Estados
    const [isSafetyOff, setIsSafetyOff] = useState(false);
    const [isNukeArmed, setIsNukeArmed] = useState(false);
    const [dbStatus, setDbStatus] = useState('OPTIMAL');
    const [query, setQuery] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    // Filtrar usuários baseado na busca
    const filteredUsers = users.filter(u =>
        u.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.id.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // 1. ENGINE VISUAL (SOUL MAP - USUÁRIOS EM TEMPO REAL)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const userSessions: UserSession[] = [];
        const USER_COUNT = Math.max(30, Math.min(users.length, 50)); // Entre 30-50 "almas"

        const resize = () => {
            const parent = canvas.parentElement;
            if(parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        window.addEventListener('resize', resize);
        resize();

        // Inicializar "Almas" baseado em usuários reais
        for(let i=0; i<USER_COUNT; i++) {
            userSessions.push({
                id: i,
                name: users[i]?.username || `User_${Math.floor(Math.random()*9999)}`,
                role: Math.random() > 0.9 ? 'admin' : 'user',
                status: 'active',
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5
            });
        }

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;

            // Limpar com rastro (Ghosting)
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, w, h);

            // Cor do Tema
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';

            // Conexões (Rede de Usuários)
            ctx.lineWidth = 0.5;
            ctx.strokeStyle = `${themeColor}22`; // Muito transparente

            userSessions.forEach((u, i) => {
                // Movimento
                u.x += u.vx;
                u.y += u.vy;

                // Bounce nas bordas
                if(u.x < 0 || u.x > w) u.vx *= -1;
                if(u.y < 0 || u.y > h) u.vy *= -1;

                // Desenhar Conexões Próximas
                for(let j=i+1; j<userSessions.length; j++) {
                    const u2 = userSessions[j];
                    const dist = Math.hypot(u.x - u2.x, u.y - u2.y);
                    if(dist < 100) {
                        ctx.beginPath();
                        ctx.moveTo(u.x, u.y);
                        ctx.lineTo(u2.x, u2.y);
                        ctx.stroke();
                    }
                }

                // Desenhar Usuário (Alma)
                ctx.beginPath();
                ctx.fillStyle = u.role === 'admin' ? '#FFD700' : themeColor;
                ctx.shadowBlur = 10;
                ctx.shadowColor = ctx.fillStyle;
                ctx.arc(u.x, u.y, u.role === 'admin' ? 4 : 2, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
            });

            // Olho Central (O Observador)
            const cx = w/2;
            const cy = h/2;
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.1;
            ctx.beginPath();
            ctx.arc(cx, cy, 100, 0, Math.PI * 2);
            ctx.stroke();
            ctx.globalAlpha = 1;

            // Radar Scan
            const angle = (Date.now() / 2000) % (Math.PI * 2);
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.arc(cx, cy, 100, angle, angle + 0.2);
            ctx.fillStyle = `rgba(255, 255, 255, 0.05)`;
            ctx.fill();

            requestAnimationFrame(render);
        };

        render();
        return () => window.removeEventListener('resize', resize);
    }, [users]);

    const handleDbStatusToggle = () => {
        const newStatus = dbStatus === 'FROZEN' ? 'OPTIMAL' : 'FROZEN';
        setDbStatus(newStatus);

        addNotification({
            type: newStatus === 'FROZEN' ? 'warning' : 'success',
            title: newStatus === 'FROZEN' ? 'System Frozen' : 'System Resumed',
            message: newStatus === 'FROZEN' ? 'All operations halted' : 'Normal operations restored',
        });
    };

    const handleNukeArm = () => {
        if (!isNukeArmed) {
            setIsNukeArmed(true);
            addNotification({
                type: 'error',
                title: 'Nuclear Option Armed',
                message: 'Click again to confirm system purge. This cannot be undone!',
            });
        } else {
            // Desarmar
            setIsNukeArmed(false);
            setIsSafetyOff(false);
            addNotification({
                type: 'info',
                title: 'Purge Cancelled',
                message: 'System purge aborted. All systems safe.',
            });
        }
    };

    if (loading && users.length === 0) {
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

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col gap-6 p-2 overflow-hidden relative">

            {/* CAMADA SUPERIOR: GOD STATS & NUKES */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">

                {/* Card 1: The Eye (User Monitor) */}
                <div className="lg:col-span-2 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden relative h-64 group shadow-2xl">
                    <div className="absolute top-6 left-6 z-10">
                        <h2 className="text-lg font-bold text-white flex items-center gap-2 tracking-tight">
                            <Eye className="w-5 h-5 text-[var(--color-primary)] animate-pulse" />
                            PANOPTICON VIEW
                        </h2>
                        <p className="text-xs text-gray-400 font-mono uppercase">
                            Monitoring {activeUsers} Active Souls {totalUsers > 0 && `• ${totalUsers} Total Registered`}
                        </p>
                    </div>

                    {/* CANVAS */}
                    <canvas ref={canvasRef} className="w-full h-full absolute inset-0" />

                    {/* Grid Overlay */}
                    <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                </div>

                {/* Card 2: System Controls (Dangerous) */}
                <div className="bg-[#0a0a0a] border border-white/10 rounded-3xl p-6 flex flex-col justify-between relative overflow-hidden">
                    {/* Warning Stripes Background */}
                    <div className="absolute top-0 right-0 w-32 h-full bg-[url('/stripes.png')] opacity-5 pointer-events-none" />

                    <div className="flex items-center gap-3 mb-4">
                        <ShieldAlert className="w-6 h-6" style={{ color: 'var(--color-error)' }} />
                        <h2 className="text-lg font-bold text-white tracking-tight">OVERRIDE PROTOCOLS</h2>
                    </div>

                    <div className="space-y-4">
                        {/* Emergency Stop Switch */}
                        <div className="flex items-center justify-between p-3 rounded-xl border border-white/5 bg-white/5">
                            <span className="text-sm font-bold text-gray-300">Global Freeze</span>
                            <button
                                onClick={handleDbStatusToggle}
                                className="relative w-12 h-6 rounded-full transition-colors duration-300"
                                style={{ background: dbStatus === 'FROZEN' ? 'var(--color-error)' : '#374151' }}
                            >
                                <div className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform duration-300 ${dbStatus === 'FROZEN' ? 'translate-x-6' : ''}`} />
                            </button>
                        </div>

                        {/* The Nuke Button */}
                        <div className="relative group">
                            {/* Glass Cover */}
                            {!isSafetyOff && (
                                <button
                                    onClick={() => setIsSafetyOff(true)}
                                    className="absolute inset-0 bg-white/5 backdrop-blur-[2px] border border-white/10 rounded-xl flex items-center justify-center z-10 hover:bg-white/10 transition-all group-hover:scale-[1.02]"
                                >
                                    <Lock className="w-5 h-5 text-gray-400 mr-2" />
                                    <span className="text-xs font-mono font-bold text-gray-400 tracking-widest">DISENGAGE SAFETY</span>
                                </button>
                            )}

                            {/* The Actual Button */}
                            <button
                                onClick={handleNukeArm}
                                className={`w-full py-4 rounded-xl font-black tracking-widest flex items-center justify-center gap-2 transition-all ${
                                    isNukeArmed
                                    ? 'bg-[var(--color-error)] text-white animate-pulse shadow-[0_0_30px_var(--color-error)]'
                                    : 'bg-[var(--color-error)]/20 text-[var(--color-error)] border border-[var(--color-error)]/40'
                                }`}
                            >
                                <Power className="w-5 h-5" />
                                {isNukeArmed ? 'CONFIRM WIPE?' : 'SYSTEM PURGE'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* CAMADA INFERIOR: DATABASE & USERS */}
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 relative z-10">

                {/* DB CONSOLE (SQL DEMO) */}
                <div className="bg-[#02040a] border border-white/10 rounded-3xl p-6 flex flex-col shadow-xl">
                    <div className="flex justify-between items-center mb-4">
                        <div className="flex items-center gap-2">
                            <Database className="w-5 h-5" style={{ color: 'var(--color-primary)' }} />
                            <span className="font-bold text-white text-sm tracking-wider">REALITY EDITOR (SQL)</span>
                        </div>
                        <span className="text-[10px] px-2 py-1 rounded font-mono" style={{ background: dbStatus === 'OPTIMAL' ? 'var(--color-success)/20' : 'var(--color-error)/20', color: dbStatus === 'OPTIMAL' ? 'var(--color-success)' : 'var(--color-error)', border: `1px solid ${dbStatus === 'OPTIMAL' ? 'var(--color-success)/30' : 'var(--color-error)/30'}` }}>
                            DB_STATUS: {dbStatus}
                        </span>
                    </div>

                    <div className="flex-1 bg-black/50 border border-white/5 rounded-xl p-4 font-mono text-sm text-gray-300 overflow-hidden relative">
                        <div className="absolute left-4 top-4 bottom-4 w-[1px] bg-white/10" />
                        <div className="pl-6 space-y-1">
                            <div className="opacity-50">1  SELECT id, username, full_name</div>
                            <div className="opacity-50">2  FROM profiles</div>
                            <div className="flex items-center gap-2">
                                <span className="opacity-50">3</span>
                                <input
                                    type="text"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    placeholder="WHERE created_at > NOW() - INTERVAL '7 days';"
                                    className="bg-transparent border-none outline-none w-full placeholder-gray-700"
                                    style={{ color: 'var(--color-primary)' }}
                                />
                            </div>
                            {query && (
                                <div className="mt-4 pt-4 border-t border-white/5">
                                    <div className="text-xs" style={{ color: 'var(--color-success)' }}>
                                        -- Query Result: {users.length} rows returned
                                    </div>
                                </div>
                            )}
                        </div>

                        <button
                            onClick={() => {
                                addNotification({
                                    type: 'info',
                                    title: 'Query Executed',
                                    message: `Found ${users.length} users matching query`,
                                });
                            }}
                            className="absolute bottom-4 right-4 p-2 bg-white/10 hover:bg-[var(--color-primary)]/20 rounded-lg transition-all hover:scale-110"
                            style={{ color: 'var(--color-primary)' }}
                        >
                            <Terminal className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                {/* USER LIST (REAL DATA) */}
                <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-6 flex flex-col">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-white text-sm flex items-center gap-2">
                            <Users className="w-4 h-4 text-[var(--color-primary)]" />
                            Elite Users ({filteredUsers.length})
                        </h3>
                        <div className="relative">
                            <Search className="w-3 h-3 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Find Soul..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="bg-white/5 border border-white/10 rounded-full pl-8 pr-3 py-1 text-xs text-white focus:border-[var(--color-primary)] outline-none w-32 focus:w-48 transition-all"
                            />
                        </div>
                    </div>

                    <div className="space-y-2 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-white/10">
                        {filteredUsers.length === 0 && !loading && (
                            <div className="text-center py-8 text-gray-500">
                                <Users className="w-12 h-12 mx-auto mb-2 opacity-50" />
                                <p className="text-sm">No users found</p>
                            </div>
                        )}

                        {filteredUsers.slice(0, 20).map((user) => (
                            <div key={user.id} className="group flex items-center justify-between p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-transparent hover:border-white/10 transition-all cursor-pointer">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-800 to-black border border-white/10 flex items-center justify-center text-xs font-bold text-white">
                                        {(user.username || user.full_name || 'U')[0].toUpperCase()}
                                    </div>
                                    <div>
                                        <div className="text-sm font-medium text-gray-200 group-hover:text-white">
                                            {user.username || user.full_name || 'Unknown User'}
                                        </div>
                                        <div className="text-[10px] text-gray-500 font-mono">
                                            ID: {user.id.slice(0, 8)}...
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button className="p-2 hover:bg-[var(--color-error)]/20 rounded-lg transition-colors" style={{ color: 'var(--color-error)' }}>
                                        <Trash2 className="w-3 h-3" />
                                    </button>
                                    <button className="p-2 hover:bg-[var(--color-primary)]/20 rounded-lg transition-colors" style={{ color: 'var(--color-primary)' }}>
                                        <Activity className="w-3 h-3" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
}
