'use client';

import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricCardProps {
    icon: string;
    value: string | number;
    label: string;
    description: string;
    trend?: string;
    badge?: string;
}

export default function MetricCard({
    icon,
    value,
    label,
    description,
    trend,
    badge
}: MetricCardProps) {
    const isPositiveTrend = trend && trend.includes('+');

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.01 }}
            className="glass-card p-4 rounded-xl border border-[var(--theme-card-border)]/50
                 hover:border-[var(--theme-primary)]/50 transition-all duration-300
                 hover:shadow-lg"
        >
            <div className="flex items-start justify-between mb-2">
                <div className="text-xl opacity-80">{icon}</div>
                {badge && (
                    <span className="px-2 py-0.5 bg-[var(--theme-primary)]/20 border border-[var(--theme-primary)]/30 
                           rounded-full text-[9px] font-bold text-[var(--theme-text-primary)]">
                        {badge}
                    </span>
                )}
            </div>

            <div className="mb-2">
                <div className="font-orbitron text-xl font-bold text-[var(--theme-text-primary)]">
                    {value}
                </div>
                <div className="font-orbitron text-[9px] tracking-wider text-[var(--theme-text-secondary)] uppercase">
                    {label}
                </div>
            </div>

            <div className="flex items-center justify-between">
                <span className="text-[9px] text-[var(--theme-text-secondary)]">
                    {description}
                </span>

                {trend && (
                    <div className={`flex items-center gap-0.5 text-[9px] font-bold ${isPositiveTrend ? 'text-green-400' : 'text-red-400'
                        }`}>
                        {isPositiveTrend ? (
                            <TrendingUp className="w-3 h-3" />
                        ) : (
                            <TrendingDown className="w-3 h-3" />
                        )}
                        <span>{trend}</span>
                    </div>
                )}
            </div>
        </motion.div>
    );
}
