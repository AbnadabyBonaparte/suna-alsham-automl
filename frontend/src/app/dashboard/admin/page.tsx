/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ADMIN MODE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/admin/page.tsx
 * 📋 ROTA: /dashboard/admin
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect } from 'react';
import { 
    Shield, 
    Users, 
    Database, 
    Settings, 
    Activity,
    AlertTriangle,
    CheckCircle,
    XCircle,
    RefreshCw,
    Lock,
    Unlock,
    Terminal,
    Cpu,
    HardDrive,
    Wifi,
    Eye,
    EyeOff
} from 'lucide-react';
import { supabase } from '@/lib/supabase';

interface SystemStatus {
    id: string;
    name: string;
    status: 'online' | 'offline' | 'warning';
    uptime: string;
    load: number;
}

interface UserData {
    id: string;
    email: string;
    role: string;
    last_login: string;
    status: 'active' | 'inactive' | 'suspended';
}

export default function AdminPage() {
    const [systemStatus, setSystemStatus] = useState<SystemStatus[]>([
        { id: '1', name: 'Core Neural Engine', status: 'online', uptime: '99.97%', load: 42 },
        { id: '2', name: 'Quantum Database', status: 'online', uptime: '99.99%', load: 28 },
        { id: '3', name: 'Agent Orchestrator', status: 'online', uptime: '99.95%', load: 65 },
        { id: '4', name: 'Reality Processor', status: 'warning', uptime: '98.50%', load: 87 },
        { id: '5', name: 'Containment Grid', status: 'online', uptime: '100%', load: 15 },
    ]);

    const [users, setUsers] = useState<UserData[]>([
        { id: '1', email: 'casamondestore@gmail.com', role: 'ADMIN', last_login: '2025-11-24 01:55', status: 'active' },
        { id: '2', email: 'operator@alsham.quantum', role: 'OPERATOR', last_login: '2025-11-23 18:30', status: 'active' },
        { id: '3', email: 'agent.handler@system', role: 'HANDLER', last_login: '2025-11-22 09:15', status: 'inactive' },
    ]);

    const [logs, setLogs] = useState([
        { time: '01:55:32', type: 'INFO', message: 'User authentication successful' },
        { time: '01:54:18', type: 'WARN', message: 'Reality Processor load exceeding threshold' },
        { time: '01:52:45', type: 'INFO', message: 'Agent UNIT_24 optimization complete' },
        { time: '01:50:00', type: 'INFO', message: 'System backup initiated' },
        { time: '01:48:33', type: 'ERROR', message: 'Connection timeout - auto-recovered' },
    ]);

    const [showSecrets, setShowSecrets] = useState(false);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'online': return <CheckCircle className="w-4 h-4 text-green-400" />;
            case 'offline': return <XCircle className="w-4 h-4 text-red-400" />;
            case 'warning': return <AlertTriangle className="w-4 h-4 text-yellow-400" />;
            default: return null;
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'online': return 'text-green-400 bg-green-400/10 border-green-400/30';
            case 'offline': return 'text-red-400 bg-red-400/10 border-red-400/30';
            case 'warning': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/30';
            case 'active': return 'text-green-400 bg-green-400/10';
            case 'inactive': return 'text-zinc-400 bg-zinc-400/10';
            case 'suspended': return 'text-red-400 bg-red-400/10';
            default: return 'text-zinc-400';
        }
    };

    const getLogColor = (type: string) => {
        switch (type) {
            case 'INFO': return 'text-cyan-400';
            case 'WARN': return 'text-yellow-400';
            case 'ERROR': return 'text-red-400';
            default: return 'text-zinc-400';
        }
    };

    return (
        <div className="min-h-screen p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-red-500/20 rounded-xl border border-red-500/30">
                        <Shield className="w-8 h-8 text-red-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            Admin Mode
                        </h1>
                        <p className="text-zinc-400">System Control & User Management</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-red-500/20 border border-red-500/30 rounded-full text-red-400 text-sm font-medium flex items-center gap-2">
                        <Lock className="w-3 h-3" />
                        RESTRICTED ACCESS
                    </span>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center justify-between">
                        <Users className="w-5 h-5 text-cyan-400" />
                        <span className="text-xs text-green-400">+2 today</span>
                    </div>
                    <p className="text-2xl font-bold text-white mt-2">139</p>
                    <p className="text-sm text-zinc-400">Active Agents</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center justify-between">
                        <Database className="w-5 h-5 text-purple-400" />
                        <span className="text-xs text-zinc-400">21 tables</span>
                    </div>
                    <p className="text-2xl font-bold text-white mt-2">2.4 GB</p>
                    <p className="text-sm text-zinc-400">Database Size</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center justify-between">
                        <Cpu className="w-5 h-5 text-orange-400" />
                        <span className="text-xs text-green-400">Healthy</span>
                    </div>
                    <p className="text-2xl font-bold text-white mt-2">47%</p>
                    <p className="text-sm text-zinc-400">CPU Usage</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center justify-between">
                        <Activity className="w-5 h-5 text-green-400" />
                        <span className="text-xs text-green-400">99.97%</span>
                    </div>
                    <p className="text-2xl font-bold text-white mt-2">Online</p>
                    <p className="text-sm text-zinc-400">System Status</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* System Services */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                            <HardDrive className="w-5 h-5 text-cyan-400" />
                            System Services
                        </h2>
                        <button className="p-2 hover:bg-zinc-800 rounded-lg transition-colors">
                            <RefreshCw className="w-4 h-4 text-zinc-400" />
                        </button>
                    </div>
                    <div className="space-y-3">
                        {systemStatus.map((service) => (
                            <div 
                                key={service.id}
                                className="flex items-center justify-between p-3 bg-black/30 rounded-lg border border-zinc-800"
                            >
                                <div className="flex items-center gap-3">
                                    {getStatusIcon(service.status)}
                                    <span className="text-white">{service.name}</span>
                                </div>
                                <div className="flex items-center gap-4">
                                    <span className="text-sm text-zinc-400">{service.uptime}</span>
                                    <div className="w-24 h-2 bg-zinc-800 rounded-full overflow-hidden">
                                        <div 
                                            className={`h-full rounded-full ${
                                                service.load > 80 ? 'bg-red-500' : 
                                                service.load > 60 ? 'bg-yellow-500' : 'bg-green-500'
                                            }`}
                                            style={{ width: `${service.load}%` }}
                                        />
                                    </div>
                                    <span className="text-sm text-zinc-400 w-12">{service.load}%</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* User Management */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                            <Users className="w-5 h-5 text-purple-400" />
                            User Management
                        </h2>
                        <button className="px-3 py-1.5 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-400 text-sm hover:bg-purple-500/30 transition-colors">
                            + Add User
                        </button>
                    </div>
                    <div className="space-y-3">
                        {users.map((user) => (
                            <div 
                                key={user.id}
                                className="flex items-center justify-between p-3 bg-black/30 rounded-lg border border-zinc-800"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                                        {user.email[0].toUpperCase()}
                                    </div>
                                    <div>
                                        <p className="text-white text-sm">{user.email}</p>
                                        <p className="text-xs text-zinc-500">Last: {user.last_login}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                                        user.role === 'ADMIN' ? 'bg-red-500/20 text-red-400' :
                                        user.role === 'OPERATOR' ? 'bg-cyan-500/20 text-cyan-400' :
                                        'bg-zinc-500/20 text-zinc-400'
                                    }`}>
                                        {user.role}
                                    </span>
                                    <span className={`px-2 py-0.5 rounded text-xs ${getStatusColor(user.status)}`}>
                                        {user.status}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* System Logs */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                        <Terminal className="w-5 h-5 text-green-400" />
                        System Logs
                    </h2>
                    <div className="flex items-center gap-2">
                        <button 
                            onClick={() => setShowSecrets(!showSecrets)}
                            className="p-2 hover:bg-zinc-800 rounded-lg transition-colors"
                        >
                            {showSecrets ? (
                                <EyeOff className="w-4 h-4 text-zinc-400" />
                            ) : (
                                <Eye className="w-4 h-4 text-zinc-400" />
                            )}
                        </button>
                    </div>
                </div>
                <div className="bg-black/50 rounded-lg p-4 font-mono text-sm space-y-2 max-h-64 overflow-y-auto">
                    {logs.map((log, index) => (
                        <div key={index} className="flex items-start gap-4">
                            <span className="text-zinc-500">[{log.time}]</span>
                            <span className={`font-bold ${getLogColor(log.type)}`}>[{log.type}]</span>
                            <span className="text-zinc-300">{log.message}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Environment Variables */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                        <Settings className="w-5 h-5 text-orange-400" />
                        Environment Configuration
                    </h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-3 bg-black/30 rounded-lg border border-zinc-800">
                        <p className="text-xs text-zinc-500 mb-1">SUPABASE_URL</p>
                        <p className="text-sm text-cyan-400 font-mono">
                            {showSecrets ? 'https://vktzdrsigrdnemdshcdp.supabase.co' : '••••••••••••••••'}
                        </p>
                    </div>
                    <div className="p-3 bg-black/30 rounded-lg border border-zinc-800">
                        <p className="text-xs text-zinc-500 mb-1">NEXT_PUBLIC_ENV</p>
                        <p className="text-sm text-green-400 font-mono">production</p>
                    </div>
                    <div className="p-3 bg-black/30 rounded-lg border border-zinc-800">
                        <p className="text-xs text-zinc-500 mb-1">DEPLOY_REGION</p>
                        <p className="text-sm text-purple-400 font-mono">pdx1 (Portland, USA)</p>
                    </div>
                    <div className="p-3 bg-black/30 rounded-lg border border-zinc-800">
                        <p className="text-xs text-zinc-500 mb-1">NODE_ENV</p>
                        <p className="text-sm text-yellow-400 font-mono">production</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
