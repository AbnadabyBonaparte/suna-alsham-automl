/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SETTINGS (SYSTEM BIOS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/settings/page.tsx
 * 📋 Painel de configuração com ID Holográfico e controles táteis
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useNotificationStore } from '@/stores/useNotificationStore';
import {
    User, Volume2, Monitor, Cpu, Shield,
    Bell, Eye, Zap, Save, RefreshCw,
    Power, Fingerprint, CreditCard, BrainCircuit
} from 'lucide-react';
import { useProfile } from '@/hooks/useProfile';

const TABS = [
    { id: 'profile', label: 'Identity', icon: User },
    { id: 'system', label: 'System', icon: Cpu },
    { id: 'neural', label: 'Neural Net', icon: Zap },
    { id: 'notifications', label: 'Signals', icon: Bell },
];

export default function SettingsPage() {
    const [activeTab, setActiveTab] = useState('profile');
    const [isSaving, setIsSaving] = useState(false);
    const [saveSuccess, setSaveSuccess] = useState(false);
    const [saveError, setSaveError] = useState<string | null>(null);

    // Profile Hook & Notifications
    const { profile, loading, error, updateProfile } = useProfile();
    const { addNotification } = useNotificationStore();

    // Estados de edição do profile
    const [username, setUsername] = useState('');
    const [fullName, setFullName] = useState('');

    // Estados de Configuração
    const [volume, setVolume] = useState(75);
    const [performance, setPerformance] = useState(90);
    const [notifications, setNotifications] = useState(true);
    const [stealthMode, setStealthMode] = useState(false);

    // Estados de Notifications Tab
    const [emailNotifs, setEmailNotifs] = useState(true);
    const [pushNotifs, setPushNotifs] = useState(true);
    const [agentAlerts, setAgentAlerts] = useState(true);
    const [securityAlerts, setSecurityAlerts] = useState(true);

    // Refs para Canvas (Audio Viz)
    const audioCanvasRef = useRef<HTMLCanvasElement>(null);

    // Sincronizar profile com estados locais
    useEffect(() => {
        if (profile) {
            setUsername(profile.username || '');
            setFullName(profile.full_name || '');
        }
    }, [profile]);

    // 1. ENGINE VISUAL (AUDIO SPECTRUM)
    useEffect(() => {
        const canvas = audioCanvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        let time = 0;

        const render = () => {
            const w = canvas.width = canvas.clientWidth;
            const h = canvas.height = canvas.clientHeight;
            
            ctx.clearRect(0, 0, w, h);
            time += 0.1;

            const bars = 20;
            const barWidth = w / bars;
            const themeColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';

            for (let i = 0; i < bars; i++) {
                // Simular onda baseada no volume
                const height = (Math.sin(time + i * 0.5) * 0.5 + 0.5) * h * (volume / 100);
                
                const x = i * barWidth;
                const y = h - height;

                // Gradiente
                const gradient = ctx.createLinearGradient(0, h, 0, y);
                gradient.addColorStop(0, themeColor + '20');
                gradient.addColorStop(1, themeColor);

                ctx.fillStyle = gradient;
                ctx.fillRect(x + 2, y, barWidth - 4, height);
            }

            animationId = requestAnimationFrame(render);
        };
        render();

        return () => cancelAnimationFrame(animationId);
    }, [volume]);

    const handleSave = async () => {
        if (activeTab !== 'profile') {
            // Mock save para outras tabs
            setIsSaving(true);
            setTimeout(() => {
                setIsSaving(false);
                setSaveSuccess(true);
                addNotification({
                    type: 'success',
                    title: 'Settings Saved',
                    message: `${activeTab} preferences have been updated.`,
                });
                setTimeout(() => setSaveSuccess(false), 3000);
            }, 1500);
            return;
        }

        // Save real para profile
        try {
            setIsSaving(true);
            setSaveError(null);
            setSaveSuccess(false);

            await updateProfile({
                username: username || null,
                full_name: fullName || null,
            });

            setSaveSuccess(true);
            addNotification({
                type: 'success',
                title: 'Profile Updated',
                message: 'Your identity has been successfully updated.',
            });
            setTimeout(() => setSaveSuccess(false), 3000);
        } catch (err: any) {
            setSaveError(err.message || 'Failed to save profile');
            addNotification({
                type: 'error',
                title: 'Save Failed',
                message: err.message || 'Failed to update profile.',
            });
            setTimeout(() => setSaveError(null), 5000);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-8 p-4 overflow-hidden relative">
            
            {/* ESQUERDA: NAVEGAÇÃO (RACK) */}
            <div className="w-full lg:w-64 flex flex-col gap-2">
                <div className="mb-6 px-4">
                    <h1 className="text-2xl font-black text-white tracking-tight font-display">CONFIG</h1>
                    <p className="text-xs text-gray-500 font-mono uppercase tracking-widest">Bios v13.3</p>
                </div>

                {TABS.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`
                            group relative flex items-center gap-4 px-4 py-4 rounded-xl transition-all duration-300 overflow-hidden
                            ${activeTab === tab.id 
                                ? 'bg-[var(--color-primary)]/10 text-white shadow-[inset_4px_0_0_0_var(--color-primary)]' 
                                : 'text-gray-500 hover:bg-white/5 hover:text-gray-300'}
                        `}
                    >
                        <tab.icon className={`w-5 h-5 transition-colors ${activeTab === tab.id ? 'text-[var(--color-primary)]' : 'group-hover:text-white'}`} />
                        <span className="font-bold text-sm tracking-wide">{tab.label}</span>
                        
                        {/* Hover Light */}
                        <div className="absolute inset-0 bg-gradient-to-r from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                    </button>
                ))}
            </div>

            {/* DIREITA: CONTEÚDO (PAINEL DE CONTROLE) */}
            <div className="flex-1 bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-8 relative overflow-hidden shadow-2xl flex flex-col">
                
                {/* Header da Tab */}
                <div className="flex justify-between items-center mb-8 border-b border-white/5 pb-4">
                    <h2 className="text-xl font-bold text-white flex items-center gap-3 uppercase tracking-widest">
                        {activeTab === 'profile' && <User className="w-6 h-6 text-[var(--color-primary)]" />}
                        {activeTab === 'system' && <Cpu className="w-6 h-6 text-[var(--color-primary)]" />}
                        {activeTab === 'neural' && <Zap className="w-6 h-6 text-[var(--color-primary)]" />}
                        {activeTab === 'notifications' && <Bell className="w-6 h-6 text-[var(--color-primary)]" />}
                        {activeTab} SETTINGS
                    </h2>
                    <div className="flex items-center gap-4">
                        {/* Feedback Messages */}
                        {saveSuccess && (
                            <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/20 border border-emerald-500/50 rounded-full animate-fade-in">
                                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                                <span className="text-xs font-bold text-emerald-400">SAVED SUCCESSFULLY</span>
                            </div>
                        )}
                        {saveError && (
                            <div className="flex items-center gap-2 px-4 py-2 bg-red-500/20 border border-red-500/50 rounded-full animate-fade-in">
                                <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                                <span className="text-xs font-bold text-red-400">ERROR: {saveError}</span>
                            </div>
                        )}
                        <button
                            onClick={handleSave}
                            disabled={isSaving || loading}
                            className="flex items-center gap-2 px-6 py-2 bg-[var(--color-primary)] hover:bg-[var(--color-accent)] text-black font-bold rounded-full transition-all disabled:opacity-50"
                        >
                            {isSaving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                            {isSaving ? 'OVERWRITING...' : 'SAVE CHANGES'}
                        </button>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto pr-4 space-y-8 scrollbar-thin scrollbar-thumb-white/10">
                    
                    {/* --- CONTEÚDO: PROFILE --- */}
                    {activeTab === 'profile' && (
                        <div className="flex flex-col md:flex-row gap-8">
                            {/* ID CARD HOLOGRÁFICO */}
                            <div className="w-full md:w-80 h-48 rounded-2xl bg-gradient-to-br from-[#1a1a1a] to-black border border-white/10 relative overflow-hidden group shadow-2xl transform transition-transform hover:scale-[1.02]">
                                {/* Efeito Holográfico (CSS Gradient) */}
                                <div className="absolute inset-0 bg-[url('/noise.png')] opacity-10 mix-blend-overlay" />
                                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-30 transition-opacity duration-700" />

                                {loading ? (
                                    // Loading State
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <RefreshCw className="w-8 h-8 text-[var(--color-primary)] animate-spin" />
                                    </div>
                                ) : (
                                    <>
                                        <div className="absolute top-6 left-6">
                                            <div className="w-16 h-16 rounded-xl bg-[var(--color-primary)]/20 border border-[var(--color-primary)] flex items-center justify-center mb-4">
                                                <Fingerprint className="w-8 h-8 text-[var(--color-primary)]" />
                                            </div>
                                            <h3 className="text-lg font-bold text-white">
                                                {profile?.full_name || profile?.username || 'Agent'}
                                            </h3>
                                            <p className="text-xs text-gray-500 font-mono uppercase tracking-widest">
                                                {profile?.username ? `@${profile.username}` : 'Quantum Operative'}
                                            </p>
                                        </div>

                                        <div className="absolute bottom-6 right-6 text-right">
                                            <div className="text-[10px] text-gray-600 font-mono">
                                                ID: {profile?.id.slice(0, 8).toUpperCase() || 'UNKNOWN'}
                                            </div>
                                            <div className="flex items-center justify-end gap-1 mt-1">
                                                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                                                <span className="text-xs text-emerald-500 font-bold">AUTHORIZED</span>
                                            </div>
                                        </div>
                                    </>
                                )}

                                {/* Scanline */}
                                <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[var(--color-primary)]/10 to-transparent h-[200%] w-full animate-scanline pointer-events-none" />
                            </div>

                            {/* Campos de Edição */}
                            <div className="flex-1 space-y-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-gray-500 uppercase tracking-widest">Username</label>
                                    <input
                                        type="text"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        placeholder="Enter username"
                                        disabled={loading}
                                        className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white focus:border-[var(--color-primary)] outline-none transition-all font-mono disabled:opacity-50"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-gray-500 uppercase tracking-widest">Full Name</label>
                                    <input
                                        type="text"
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                        placeholder="Enter full name"
                                        disabled={loading}
                                        className="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white focus:border-[var(--color-primary)] outline-none transition-all font-mono disabled:opacity-50"
                                    />
                                </div>
                                {error && (
                                    <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl">
                                        <p className="text-xs text-red-400 font-mono">{error}</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* --- CONTEÚDO: SYSTEM --- */}
                    {activeTab === 'system' && (
                        <div className="space-y-8">
                            {/* Audio Calibration */}
                            <div className="bg-black/20 rounded-2xl p-6 border border-white/5">
                                <div className="flex justify-between items-center mb-4">
                                    <div className="flex items-center gap-3">
                                        <Volume2 className="w-5 h-5 text-gray-400" />
                                        <span className="text-sm font-bold text-white">Audio Output Level</span>
                                    </div>
                                    <span className="text-xs font-mono text-[var(--color-primary)]">{volume}%</span>
                                </div>
                                <div className="h-24 bg-black/40 rounded-xl border border-white/5 overflow-hidden mb-4 relative">
                                    <canvas ref={audioCanvasRef} className="w-full h-full" />
                                </div>
                                <input 
                                    type="range" min="0" max="100" value={volume} onChange={(e) => setVolume(Number(e.target.value))}
                                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-[var(--color-primary)]"
                                />
                            </div>

                            {/* Performance Mode */}
                            <div className="bg-black/20 rounded-2xl p-6 border border-white/5">
                                <div className="flex justify-between items-center mb-4">
                                    <div className="flex items-center gap-3">
                                        <Monitor className="w-5 h-5 text-gray-400" />
                                        <span className="text-sm font-bold text-white">Graphics Quality</span>
                                    </div>
                                    <span className="text-xs font-mono text-yellow-400">ULTRA</span>
                                </div>
                                <div className="flex gap-2 mb-2">
                                    {[20, 40, 60, 80, 100].map((val) => (
                                        <div 
                                            key={val} 
                                            className={`h-2 flex-1 rounded-full transition-all ${performance >= val ? 'bg-[var(--color-primary)] shadow-[0_0_10px_var(--color-primary)]' : 'bg-gray-800'}`}
                                        />
                                    ))}
                                </div>
                                <input 
                                    type="range" min="0" max="100" step="20" value={performance} onChange={(e) => setPerformance(Number(e.target.value))}
                                    className="w-full h-2 bg-transparent rounded-lg appearance-none cursor-pointer accent-transparent relative z-10 opacity-0"
                                />
                            </div>
                        </div>
                    )}

                    {/* --- CONTEÚDO: NEURAL NET --- */}
                    {activeTab === 'neural' && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* Switches Industriais */}
                            {[
                                { label: 'Stealth Mode', state: stealthMode, set: setStealthMode, icon: Eye, color: 'text-red-400' },
                                { label: 'Auto-Training', state: true, set: () => {}, icon: BrainCircuit, color: 'text-purple-400' },
                                { label: 'Quantum Sync', state: true, set: () => {}, icon: RefreshCw, color: 'text-cyan-400' },
                                { label: 'Firewall Guard', state: true, set: () => {}, icon: Shield, color: 'text-emerald-400' },
                            ].map((opt, i) => (
                                <div
                                    key={i}
                                    onClick={() => opt.set(!opt.state)}
                                    className={`
                                        cursor-pointer p-5 rounded-2xl border transition-all duration-300 flex items-center justify-between group
                                        ${opt.state
                                            ? 'bg-white/5 border-[var(--color-primary)]/30'
                                            : 'bg-black/40 border-white/5 opacity-60'}
                                    `}
                                >
                                    <div className="flex items-center gap-3">
                                        <opt.icon className={`w-5 h-5 ${opt.color}`} />
                                        <span className={`font-bold text-sm ${opt.state ? 'text-white' : 'text-gray-500'}`}>{opt.label}</span>
                                    </div>

                                    {/* Toggle Switch Visual */}
                                    <div className={`w-12 h-6 rounded-full p-1 transition-colors ${opt.state ? 'bg-[var(--color-primary)]' : 'bg-gray-700'}`}>
                                        <div className={`w-4 h-4 bg-white rounded-full shadow-md transition-transform ${opt.state ? 'translate-x-6' : 'translate-x-0'}`} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* --- CONTEÚDO: NOTIFICATIONS --- */}
                    {activeTab === 'notifications' && (
                        <div className="space-y-6">
                            <p className="text-sm text-gray-400 font-mono">
                                Configure how you receive alerts and updates from the Alsham Quantum system.
                            </p>

                            <div className="grid grid-cols-1 gap-4">
                                {[
                                    { label: 'Email Notifications', desc: 'Receive updates via email', state: emailNotifs, set: setEmailNotifs, icon: Bell },
                                    { label: 'Push Notifications', desc: 'Browser push notifications', state: pushNotifs, set: setPushNotifs, icon: Zap },
                                    { label: 'Agent Alerts', desc: 'Notifications when agents complete tasks', state: agentAlerts, set: setAgentAlerts, icon: User },
                                    { label: 'Security Alerts', desc: 'Critical security warnings', state: securityAlerts, set: setSecurityAlerts, icon: Shield },
                                ].map((opt, i) => (
                                    <div
                                        key={i}
                                        onClick={() => opt.set(!opt.state)}
                                        className={`
                                            cursor-pointer p-6 rounded-2xl border transition-all duration-300 group
                                            ${opt.state
                                                ? 'bg-white/5 border-[var(--color-primary)]/30 shadow-[0_0_20px_rgba(var(--color-primary-rgb),0.1)]'
                                                : 'bg-black/40 border-white/5 hover:border-white/10'}
                                        `}
                                    >
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-4">
                                                <div className={`p-3 rounded-xl transition-colors ${opt.state ? 'bg-[var(--color-primary)]/20 text-[var(--color-primary)]' : 'bg-white/5 text-gray-500'}`}>
                                                    <opt.icon className="w-5 h-5" />
                                                </div>
                                                <div>
                                                    <h4 className={`font-bold text-sm ${opt.state ? 'text-white' : 'text-gray-500'}`}>
                                                        {opt.label}
                                                    </h4>
                                                    <p className="text-xs text-gray-600 mt-0.5">
                                                        {opt.desc}
                                                    </p>
                                                </div>
                                            </div>

                                            {/* Toggle Switch Visual */}
                                            <div className={`w-14 h-7 rounded-full p-1 transition-all ${opt.state ? 'bg-[var(--color-primary)] shadow-[0_0_15px_var(--color-primary)]' : 'bg-gray-700'}`}>
                                                <div className={`w-5 h-5 bg-white rounded-full shadow-md transition-transform ${opt.state ? 'translate-x-7' : 'translate-x-0'}`} />
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                </div>
            </div>

            <style jsx>{`
                @keyframes scanline {
                    0% { transform: translateY(-100%); }
                    100% { transform: translateY(100%); }
                }
                .animate-scanline { animation: scanline 3s linear infinite; }

                @keyframes fade-in {
                    from { opacity: 0; transform: translateY(-10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in { animation: fade-in 0.3s ease-out; }
            `}</style>
        </div>
    );
}
