'use client';

import { useGamification, BADGES } from '@/contexts/GamificationProvider';
import { motion } from 'framer-motion';
import { Trophy, Award, TrendingUp } from 'lucide-react';

export default function GamificationPage() {
    const { points, level, badges, streak, addPoints, unlockBadge } = useGamification();

    const pointsToNextLevel = (level * 1000) - points;
    const progressPercent = ((points % 1000) / 1000) * 100;

    return (
        <div className="min-h-screen p-6 md:p-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="font-orbitron text-4xl font-bold text-[var(--theme-text-primary)] mb-2">
                    Gamificação
                </h1>
                <p className="text-[var(--theme-text-secondary)]">
                    Acompanhe seu progresso e conquistas
                </p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {/* Level Card */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)]"
                >
                    <div className="flex items-center gap-3 mb-4">
                        <Trophy className="w-6 h-6 text-[var(--theme-accent)]" />
                        <h3 className="font-orbitron text-sm tracking-wider text-[var(--theme-text-secondary)]">
                            NÍVEL ATUAL
                        </h3>
                    </div>
                    <div className="text-4xl font-bold text-[var(--theme-text-primary)] mb-2">
                        {level}
                    </div>
                    <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden mb-2">
                        <div
                            className="h-full bg-gradient-to-r from-[var(--theme-primary)] to-[var(--theme-accent)]"
                            style={{ width: `${progressPercent}%` }}
                        />
                    </div>
                    <p className="text-xs text-[var(--theme-text-secondary)]">
                        {pointsToNextLevel} XP para próximo nível
                    </p>
                </motion.div>

                {/* Points Card */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)]"
                >
                    <div className="flex items-center gap-3 mb-4">
                        <Award className="w-6 h-6 text-[var(--theme-accent)]" />
                        <h3 className="font-orbitron text-sm tracking-wider text-[var(--theme-text-secondary)]">
                            PONTOS TOTAIS
                        </h3>
                    </div>
                    <div className="text-4xl font-bold text-[var(--theme-text-primary)]">
                        {points.toLocaleString()}
                    </div>
                    <p className="text-xs text-[var(--theme-text-secondary)] mt-2">
                        XP acumulado
                    </p>
                </motion.div>

                {/* Streak Card */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)]"
                >
                    <div className="flex items-center gap-3 mb-4">
                        <TrendingUp className="w-6 h-6 text-[var(--theme-accent)]" />
                        <h3 className="font-orbitron text-sm tracking-wider text-[var(--theme-text-secondary)]">
                            STREAK ATUAL
                        </h3>
                    </div>
                    <div className="text-4xl font-bold text-[var(--theme-text-primary)]">
                        {streak}
                    </div>
                    <p className="text-xs text-[var(--theme-text-secondary)] mt-2">
                        dias consecutivos
                    </p>
                </motion.div>
            </div>

            {/* Badges */}
            <div className="mb-8">
                <h2 className="font-orbitron text-2xl font-bold text-[var(--theme-text-primary)] mb-4">
                    Conquistas
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    {Object.values(BADGES).map((badge, index) => {
                        const unlocked = badges.includes(badge.id);
                        return (
                            <motion.div
                                key={badge.id}
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: index * 0.05 }}
                                className={`glass-card p-4 rounded-xl border text-center ${unlocked
                                        ? 'border-[var(--theme-primary)] bg-[var(--theme-primary)]/10'
                                        : 'border-[var(--theme-card-border)] opacity-50'
                                    }`}
                            >
                                <div className="text-4xl mb-2">{badge.icon}</div>
                                <div className="font-medium text-xs text-[var(--theme-text-primary)] mb-1">
                                    {badge.name}
                                </div>
                                <div className="text-[9px] text-[var(--theme-text-secondary)]">
                                    {badge.requirement}
                                </div>
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* Test Buttons */}
            <div className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)]">
                <h3 className="font-orbitron text-sm tracking-wider text-[var(--theme-text-secondary)] mb-4">
                    TESTE DE GAMIFICAÇÃO
                </h3>
                <div className="flex flex-wrap gap-3">
                    <button
                        onClick={() => addPoints(10, 'Teste manual')}
                        className="px-4 py-2 bg-[var(--theme-primary)] hover:bg-[var(--theme-primary)]/80
                       text-white text-sm rounded-lg transition-colors"
                    >
                        +10 XP
                    </button>
                    <button
                        onClick={() => addPoints(100, 'Teste grande')}
                        className="px-4 py-2 bg-[var(--theme-primary)] hover:bg-[var(--theme-primary)]/80
                       text-white text-sm rounded-lg transition-colors"
                    >
                        +100 XP
                    </button>
                    <button
                        onClick={() => unlockBadge('iniciante')}
                        className="px-4 py-2 bg-green-600 hover:bg-green-700
                       text-white text-sm rounded-lg transition-colors"
                    >
                        Desbloquear Iniciante
                    </button>
                </div>
            </div>
        </div>
    );
}
