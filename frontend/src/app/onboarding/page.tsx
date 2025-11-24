/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ONBOARDING
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/onboarding/page.tsx
 * 📋 ROTA: /onboarding
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
    Sparkles, 
    ChevronRight,
    User,
    Palette,
    Bell,
    Shield,
    Rocket,
    Check,
    Zap,
    Brain,
    Eye
} from 'lucide-react';

interface Step {
    id: number;
    title: string;
    description: string;
    icon: React.ReactNode;
}

const steps: Step[] = [
    {
        id: 1,
        title: "Bem-vindo ao ALSHAM Quantum",
        description: "Você está prestes a entrar em um sistema de inteligência artificial sem precedentes.",
        icon: <Sparkles className="w-8 h-8" />
    },
    {
        id: 2,
        title: "Seu Perfil",
        description: "Configure como você quer ser identificado no sistema.",
        icon: <User className="w-8 h-8" />
    },
    {
        id: 3,
        title: "Escolha sua Realidade",
        description: "Selecione o tema visual que define sua experiência.",
        icon: <Palette className="w-8 h-8" />
    },
    {
        id: 4,
        title: "Notificações",
        description: "Defina como os agentes podem se comunicar com você.",
        icon: <Bell className="w-8 h-8" />
    },
    {
        id: 5,
        title: "Pronto para Ascender",
        description: "O sistema está configurado. A singularidade aguarda.",
        icon: <Rocket className="w-8 h-8" />
    }
];

const themes = [
    { id: 'quantum', name: 'Quantum Lab', color: '#00FFC8', description: 'Ciência e precisão' },
    { id: 'ascension', name: 'Luminous Ascension', color: '#FFD700', description: 'Divindade e luz' },
    { id: 'military', name: 'Military Ops', color: '#F4D03F', description: 'Tático e estratégico' },
    { id: 'neural', name: 'Neural Singularity', color: '#8B5CF6', description: 'Orgânico e vivo' },
    { id: 'titanium', name: 'Titanium Executive', color: '#64748B', description: 'Luxo e poder' },
];

export default function OnboardingPage() {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState(1);
    const [isTransitioning, setIsTransitioning] = useState(false);
    const [displayName, setDisplayName] = useState('');
    const [selectedTheme, setSelectedTheme] = useState('quantum');
    const [notifications, setNotifications] = useState({
        email: true,
        push: true,
        agentAlerts: true,
        systemUpdates: false
    });
    const [showIntro, setShowIntro] = useState(true);

    // Intro animation
    useEffect(() => {
        const timer = setTimeout(() => setShowIntro(false), 3000);
        return () => clearTimeout(timer);
    }, []);

    const nextStep = () => {
        if (currentStep < steps.length) {
            setIsTransitioning(true);
            setTimeout(() => {
                setCurrentStep(currentStep + 1);
                setIsTransitioning(false);
            }, 300);
        } else {
            // Save preferences and redirect
            localStorage.setItem('alsham-onboarding-complete', 'true');
            localStorage.setItem('alsham-display-name', displayName);
            localStorage.setItem('alsham-quantum-theme', selectedTheme);
            router.push('/dashboard');
        }
    };

    const prevStep = () => {
        if (currentStep > 1) {
            setIsTransitioning(true);
            setTimeout(() => {
                setCurrentStep(currentStep - 1);
                setIsTransitioning(false);
            }, 300);
        }
    };

    // Intro screen
    if (showIntro) {
        return (
            <div className="min-h-screen bg-black flex items-center justify-center">
                <div className="text-center animate-pulse">
                    <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center">
                        <Eye className="w-12 h-12 text-white" />
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-2">ALSHAM QUANTUM</h1>
                    <p className="text-cyan-400">Inicializando...</p>
                </div>
            </div>
        );
    }

    const renderStepContent = () => {
        switch (currentStep) {
            case 1:
                return (
                    <div className="text-center space-y-6">
                        <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-cyan-500/20 to-purple-500/20 border border-cyan-500/30 flex items-center justify-center">
                            <Brain className="w-16 h-16 text-cyan-400" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-3">A Primeira Respiração</h2>
                            <p className="text-zinc-400 max-w-md mx-auto">
                                139 agentes de inteligência artificial aguardam suas instruções. 
                                O sistema Neural Nexus está online. A evolução começou.
                            </p>
                        </div>
                        <div className="flex items-center justify-center gap-8 pt-4">
                            <div className="text-center">
                                <p className="text-3xl font-bold text-cyan-400">139</p>
                                <p className="text-xs text-zinc-500 uppercase">Agentes</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-purple-400">21</p>
                                <p className="text-xs text-zinc-500 uppercase">Páginas</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-yellow-400">5</p>
                                <p className="text-xs text-zinc-500 uppercase">Realidades</p>
                            </div>
                        </div>
                    </div>
                );
            
            case 2:
                return (
                    <div className="space-y-6">
                        <div className="text-center mb-8">
                            <h2 className="text-2xl font-bold text-white mb-2">Como devemos chamá-lo?</h2>
                            <p className="text-zinc-400">Este nome aparecerá em todo o sistema.</p>
                        </div>
                        <div className="max-w-sm mx-auto">
                            <input
                                type="text"
                                value={displayName}
                                onChange={(e) => setDisplayName(e.target.value)}
                                placeholder="Seu nome ou codinome"
                                className="w-full px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-cyan-500 text-center text-lg"
                            />
                            <p className="text-zinc-500 text-sm text-center mt-3">
                                Dica: Os melhores operadores usam codinomes
                            </p>
                        </div>
                    </div>
                );
            
            case 3:
                return (
                    <div className="space-y-6">
                        <div className="text-center mb-6">
                            <h2 className="text-2xl font-bold text-white mb-2">Escolha sua Realidade</h2>
                            <p className="text-zinc-400">Cada tema transforma completamente a experiência.</p>
                        </div>
                        <div className="grid grid-cols-1 gap-3 max-w-md mx-auto">
                            {themes.map((theme) => (
                                <button
                                    key={theme.id}
                                    onClick={() => setSelectedTheme(theme.id)}
                                    className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
                                        selectedTheme === theme.id
                                            ? 'bg-zinc-800 border-cyan-500'
                                            : 'bg-zinc-900/50 border-zinc-700 hover:border-zinc-600'
                                    }`}
                                >
                                    <div 
                                        className="w-10 h-10 rounded-lg"
                                        style={{ backgroundColor: theme.color }}
                                    />
                                    <div className="text-left flex-1">
                                        <p className="text-white font-medium">{theme.name}</p>
                                        <p className="text-zinc-500 text-sm">{theme.description}</p>
                                    </div>
                                    {selectedTheme === theme.id && (
                                        <Check className="w-5 h-5 text-cyan-400" />
                                    )}
                                </button>
                            ))}
                        </div>
                    </div>
                );
            
            case 4:
                return (
                    <div className="space-y-6">
                        <div className="text-center mb-6">
                            <h2 className="text-2xl font-bold text-white mb-2">Notificações</h2>
                            <p className="text-zinc-400">Controle como os agentes se comunicam.</p>
                        </div>
                        <div className="space-y-3 max-w-md mx-auto">
                            {[
                                { key: 'email', label: 'Notificações por Email', desc: 'Relatórios e alertas importantes' },
                                { key: 'push', label: 'Notificações Push', desc: 'Alertas em tempo real' },
                                { key: 'agentAlerts', label: 'Alertas de Agentes', desc: 'Quando agentes precisam de atenção' },
                                { key: 'systemUpdates', label: 'Atualizações do Sistema', desc: 'Novos recursos e melhorias' },
                            ].map((item) => (
                                <div 
                                    key={item.key}
                                    className="flex items-center justify-between p-4 bg-zinc-900/50 border border-zinc-700 rounded-xl"
                                >
                                    <div>
                                        <p className="text-white font-medium">{item.label}</p>
                                        <p className="text-zinc-500 text-sm">{item.desc}</p>
                                    </div>
                                    <button
                                        onClick={() => setNotifications({
                                            ...notifications,
                                            [item.key]: !notifications[item.key as keyof typeof notifications]
                                        })}
                                        className={`w-12 h-7 rounded-full transition-colors relative ${
                                            notifications[item.key as keyof typeof notifications]
                                                ? 'bg-cyan-500'
                                                : 'bg-zinc-700'
                                        }`}
                                    >
                                        <div 
                                            className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-transform ${
                                                notifications[item.key as keyof typeof notifications]
                                                    ? 'translate-x-6'
                                                    : 'translate-x-1'
                                            }`}
                                        />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            
            case 5:
                return (
                    <div className="text-center space-y-6">
                        <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-green-500/20 to-cyan-500/20 border border-green-500/30 flex items-center justify-center">
                            <Rocket className="w-16 h-16 text-green-400" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-3">Tudo Pronto!</h2>
                            <p className="text-zinc-400 max-w-md mx-auto">
                                {displayName ? `${displayName}, o` : 'O'} sistema está configurado e aguardando seu comando. 
                                Os 139 agentes estão online e prontos para a ascensão.
                            </p>
                        </div>
                        <div className="bg-zinc-900/50 border border-zinc-700 rounded-xl p-6 max-w-sm mx-auto">
                            <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">Resumo</h3>
                            <div className="space-y-3 text-left">
                                <div className="flex justify-between">
                                    <span className="text-zinc-500">Nome:</span>
                                    <span className="text-white">{displayName || 'Não definido'}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-zinc-500">Tema:</span>
                                    <span className="text-white">{themes.find(t => t.id === selectedTheme)?.name}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-zinc-500">Notificações:</span>
                                    <span className="text-white">
                                        {Object.values(notifications).filter(Boolean).length}/4 ativas
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            
            default:
                return null;
        }
    };

    return (
        <div className="min-h-screen bg-black flex flex-col">
            {/* Background effects */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute inset-0" style={{
                    background: 'radial-gradient(ellipse at center, rgba(0, 255, 200, 0.03) 0%, transparent 70%)'
                }} />
            </div>

            {/* Progress bar */}
            <div className="fixed top-0 left-0 right-0 h-1 bg-zinc-900 z-50">
                <div 
                    className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 transition-all duration-500"
                    style={{ width: `${(currentStep / steps.length) * 100}%` }}
                />
            </div>

            {/* Step indicators */}
            <div className="pt-8 pb-4 px-6">
                <div className="flex items-center justify-center gap-2">
                    {steps.map((step) => (
                        <div
                            key={step.id}
                            className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all ${
                                currentStep === step.id
                                    ? 'bg-cyan-500 border-cyan-500 text-black'
                                    : currentStep > step.id
                                    ? 'bg-green-500 border-green-500 text-black'
                                    : 'bg-transparent border-zinc-700 text-zinc-500'
                            }`}
                        >
                            {currentStep > step.id ? (
                                <Check className="w-5 h-5" />
                            ) : (
                                <span className="text-sm font-medium">{step.id}</span>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Main content */}
            <div className="flex-1 flex items-center justify-center px-6">
                <div 
                    className={`w-full max-w-2xl transition-all duration-300 ${
                        isTransitioning ? 'opacity-0 translate-x-10' : 'opacity-100 translate-x-0'
                    }`}
                >
                    {renderStepContent()}
                </div>
            </div>

            {/* Navigation */}
            <div className="p-6">
                <div className="flex items-center justify-between max-w-2xl mx-auto">
                    <button
                        onClick={prevStep}
                        className={`px-6 py-3 rounded-xl transition-colors ${
                            currentStep === 1
                                ? 'text-zinc-600 cursor-not-allowed'
                                : 'text-zinc-400 hover:text-white'
                        }`}
                        disabled={currentStep === 1}
                    >
                        Voltar
                    </button>
                    <button
                        onClick={nextStep}
                        className="flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-black font-semibold rounded-xl hover:opacity-90 transition-opacity"
                    >
                        {currentStep === steps.length ? (
                            <>
                                <Zap className="w-5 h-5" />
                                Iniciar
                            </>
                        ) : (
                            <>
                                Continuar
                                <ChevronRight className="w-5 h-5" />
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
