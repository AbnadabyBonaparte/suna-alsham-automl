/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - PLAN BADGE COMPONENT
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { Crown, Rocket, Zap } from 'lucide-react';
import { useSubscription } from '@/hooks/useSubscription';

export function PlanBadge() {
    const { isLoading, isSubscribed, plan, planName, isEnterprise, isPro } = useSubscription();

    if (isLoading) {
        return (
            <div className="animate-pulse h-7 w-24 bg-white/10 rounded-full" />
        );
    }

    if (!isSubscribed || !plan) {
        return (
            <a
                href="/pricing"
                className="flex items-center gap-1.5 px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-xs font-medium text-gray-400 hover:text-white transition-all"
            >
                <Zap className="w-3 h-3" />
                Fazer Upgrade
            </a>
        );
    }

    if (isEnterprise) {
        return (
            <div className="relative group">
                <div className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/50 rounded-full shadow-[0_0_15px_rgba(250,204,21,0.3)] animate-pulse-slow">
                    <Crown className="w-3.5 h-3.5 text-yellow-400" />
                    <span className="text-xs font-black tracking-wider text-yellow-300">
                        ENTERPRISE
                    </span>
                </div>
                
                {/* Tooltip */}
                <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
                    <div className="bg-black/90 border border-yellow-500/30 rounded-lg px-3 py-2 text-xs text-center whitespace-nowrap">
                        <p className="text-yellow-400 font-bold">Plano Enterprise</p>
                        <p className="text-gray-400">Acesso ilimitado a todos os recursos</p>
                    </div>
                </div>
            </div>
        );
    }

    if (isPro) {
        return (
            <div className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/50 rounded-full">
                <Rocket className="w-3.5 h-3.5 text-purple-400" />
                <span className="text-xs font-bold tracking-wider text-purple-300">
                    PRO
                </span>
            </div>
        );
    }

    return (
        <div className="flex items-center gap-1.5 px-3 py-1 bg-blue-500/10 border border-blue-500/30 rounded-full">
            <Zap className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-xs font-bold tracking-wider text-blue-300">
                STARTER
            </span>
        </div>
    );
}

// Componente para exibir em tela cheia (header do dashboard)
export function PlanBadgeLarge() {
    const { isLoading, isSubscribed, plan, isEnterprise, isPro } = useSubscription();

    if (isLoading || !isSubscribed || !plan) return null;

    if (isEnterprise) {
        return (
            <div className="fixed top-4 right-20 z-[100]">
                <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-yellow-500/30 to-orange-500/30 backdrop-blur-xl border-2 border-yellow-500/60 rounded-xl shadow-[0_0_30px_rgba(250,204,21,0.4)]">
                    <Crown className="w-5 h-5 text-yellow-400 animate-bounce" />
                    <div>
                        <span className="text-sm font-black tracking-widest text-yellow-300 block">
                            ENTERPRISE
                        </span>
                        <span className="text-[9px] text-yellow-500/80 font-mono">
                            GOD MODE ATIVO
                        </span>
                    </div>
                </div>
            </div>
        );
    }

    return null;
}

