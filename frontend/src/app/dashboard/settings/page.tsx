/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SETTINGS
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/settings/page.tsx
 * 📋 ROTA: /dashboard/settings
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState } from 'react';
import { 
    Settings, 
    Bell, 
    Moon, 
    Sun,
    Globe,
    Lock,
    User,
    Palette,
    Volume2,
    VolumeX,
    Monitor,
    Smartphone,
    Mail,
    Shield,
    Key,
    Save,
    RotateCcw,
    Zap,
    Eye,
    Languages
} from 'lucide-react';

export default function SettingsPage() {
    const [notifications, setNotifications] = useState({
        email: true,
        push: true,
        agentAlerts: true,
        systemUpdates: false,
        weeklyReport: true,
    });

    const [appearance, setAppearance] = useState({
        theme: 'quantum',
        reducedMotion: false,
        soundEffects: true,
        compactMode: false,
    });

    const [privacy, setPrivacy] = useState({
        analytics: true,
        crashReports: true,
        showActivity: true,
    });

    const [language, setLanguage] = useState('pt-BR');

    const themes = [
        { id: 'quantum', name: 'Quantum Lab', color: 'from-cyan-500 to-teal-500', description: 'Ciano futurista' },
        { id: 'ascension', name: 'Ascension Protocol', color: 'from-amber-500 to-orange-500', description: 'Dourado celestial' },
        { id: 'military', name: 'Military Ops', color: 'from-green-600 to-emerald-600', description: 'Verde tático' },
        { id: 'neural', name: 'Neural Singularity', color: 'from-purple-500 to-pink-500', description: 'Roxo neural' },
        { id: 'titanium', name: 'Titanium Executive', color: 'from-zinc-400 to-zinc-600', description: 'Cinza premium' },
    ];

    const ToggleSwitch = ({ enabled, onChange }: { enabled: boolean; onChange: () => void }) => (
        <button
            onClick={onChange}
            className={`relative w-12 h-6 rounded-full transition-colors ${
                enabled ? 'bg-cyan-500' : 'bg-zinc-700'
            }`}
        >
            <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                enabled ? 'left-7' : 'left-1'
            }`} />
        </button>
    );

    return (
        <div className="min-h-screen p-6 space-y-6 max-w-4xl mx-auto">
            {/* Header */}
            <div className="flex items-center gap-4">
                <div className="p-3 bg-zinc-800 rounded-xl border border-zinc-700">
                    <Settings className="w-8 h-8 text-zinc-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">
                        Settings
                    </h1>
                    <p className="text-zinc-400">Configure your quantum experience</p>
                </div>
            </div>

            {/* Profile Section */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
                    <User className="w-5 h-5 text-cyan-400" />
                    Profile
                </h2>
                <div className="flex items-start gap-6">
                    <div className="w-20 h-20 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                        C
                    </div>
                    <div className="flex-1 space-y-4">
                        <div>
                            <label className="block text-sm text-zinc-400 mb-1">Display Name</label>
                            <input 
                                type="text" 
                                defaultValue="ALSHAM Operator"
                                className="w-full bg-black/50 border border-zinc-700 rounded-lg px-4 py-2 text-white focus:border-cyan-500 focus:outline-none transition-colors"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-zinc-400 mb-1">Email</label>
                            <input 
                                type="email" 
                                defaultValue="casamondestore@gmail.com"
                                disabled
                                className="w-full bg-black/50 border border-zinc-700 rounded-lg px-4 py-2 text-zinc-500 cursor-not-allowed"
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Appearance */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
                    <Palette className="w-5 h-5 text-purple-400" />
                    Appearance
                </h2>
                
                {/* Theme Selection */}
                <div className="mb-6">
                    <label className="block text-sm text-zinc-400 mb-3">Visual Reality Theme</label>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {themes.map((theme) => (
                            <button
                                key={theme.id}
                                onClick={() => setAppearance({ ...appearance, theme: theme.id })}
                                className={`p-4 rounded-xl border transition-all ${
                                    appearance.theme === theme.id 
                                        ? 'border-cyan-500 bg-cyan-500/10' 
                                        : 'border-zinc-700 hover:border-zinc-600'
                                }`}
                            >
                                <div className={`w-full h-3 rounded-full bg-gradient-to-r ${theme.color} mb-3`} />
                                <p className="text-white font-medium text-left">{theme.name}</p>
                                <p className="text-sm text-zinc-500 text-left">{theme.description}</p>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Other appearance settings */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between py-3 border-t border-zinc-800">
                        <div className="flex items-center gap-3">
                            <Eye className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Reduced Motion</p>
                                <p className="text-sm text-zinc-500">Disable animations for accessibility</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={appearance.reducedMotion}
                            onChange={() => setAppearance({ ...appearance, reducedMotion: !appearance.reducedMotion })}
                        />
                    </div>

                    <div className="flex items-center justify-between py-3 border-t border-zinc-800">
                        <div className="flex items-center gap-3">
                            {appearance.soundEffects ? (
                                <Volume2 className="w-5 h-5 text-zinc-400" />
                            ) : (
                                <VolumeX className="w-5 h-5 text-zinc-400" />
                            )}
                            <div>
                                <p className="text-white">Sound Effects</p>
                                <p className="text-sm text-zinc-500">Enable quantum interface sounds</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={appearance.soundEffects}
                            onChange={() => setAppearance({ ...appearance, soundEffects: !appearance.soundEffects })}
                        />
                    </div>

                    <div className="flex items-center justify-between py-3 border-t border-zinc-800">
                        <div className="flex items-center gap-3">
                            <Monitor className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Compact Mode</p>
                                <p className="text-sm text-zinc-500">Reduce spacing and padding</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={appearance.compactMode}
                            onChange={() => setAppearance({ ...appearance, compactMode: !appearance.compactMode })}
                        />
                    </div>
                </div>
            </div>

            {/* Notifications */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
                    <Bell className="w-5 h-5 text-yellow-400" />
                    Notifications
                </h2>
                <div className="space-y-4">
                    <div className="flex items-center justify-between py-3">
                        <div className="flex items-center gap-3">
                            <Mail className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Email Notifications</p>
                                <p className="text-sm text-zinc-500">Receive updates via email</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={notifications.email}
                            onChange={() => setNotifications({ ...notifications, email: !notifications.email })}
                        />
                    </div>

                    <div className="flex items-center justify-between py-3 border-t border-zinc-800">
                        <div className="flex items-center gap-3">
                            <Smartphone className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Push Notifications</p>
                                <p className="text-sm text-zinc-500">Browser push notifications</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={notifications.push}
                            onChange={() => setNotifications({ ...notifications, push: !notifications.push })}
                        />
                    </div>

                    <div className="flex items-center justify-between py-3 border-t border-zinc-800">
                        <div className="flex items-center gap-3">
                            <Zap className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Agent Alerts</p>
                                <p className="text-sm text-zinc-500">Critical agent status updates</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={notifications.agentAlerts}
                            onChange={() => setNotifications({ ...notifications, agentAlerts: !notifications.agentAlerts })}
                        />
                    </div>
                </div>
            </div>

            {/* Privacy & Security */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
                    <Shield className="w-5 h-5 text-green-400" />
                    Privacy & Security
                </h2>
                <div className="space-y-4">
                    <div className="flex items-center justify-between py-3">
                        <div className="flex items-center gap-3">
                            <Key className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Change Password</p>
                                <p className="text-sm text-zinc-500">Update your access credentials</p>
                            </div>
                        </div>
                        <button className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-white text-sm transition-colors">
                            Update
                        </button>
                    </div>

                    <div className="flex items-center justify-between py-3 border-t border-zinc-800">
                        <div className="flex items-center gap-3">
                            <Globe className="w-5 h-5 text-zinc-400" />
                            <div>
                                <p className="text-white">Usage Analytics</p>
                                <p className="text-sm text-zinc-500">Help improve ALSHAM Quantum</p>
                            </div>
                        </div>
                        <ToggleSwitch 
                            enabled={privacy.analytics}
                            onChange={() => setPrivacy({ ...privacy, analytics: !privacy.analytics })}
                        />
                    </div>
                </div>
            </div>

            {/* Language */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
                    <Languages className="w-5 h-5 text-blue-400" />
                    Language & Region
                </h2>
                <div>
                    <label className="block text-sm text-zinc-400 mb-2">Interface Language</label>
                    <select 
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-full md:w-64 bg-black/50 border border-zinc-700 rounded-lg px-4 py-2 text-white focus:border-cyan-500 focus:outline-none"
                    >
                        <option value="pt-BR">Português (Brasil)</option>
                        <option value="en-US">English (US)</option>
                        <option value="es">Español</option>
                    </select>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center justify-between pt-4">
                <button className="flex items-center gap-2 px-4 py-2 text-zinc-400 hover:text-white transition-colors">
                    <RotateCcw className="w-4 h-4" />
                    Reset to Defaults
                </button>
                <button className="flex items-center gap-2 px-6 py-2 bg-cyan-500 hover:bg-cyan-600 text-black font-medium rounded-lg transition-colors">
                    <Save className="w-4 h-4" />
                    Save Changes
                </button>
            </div>
        </div>
    );
}
