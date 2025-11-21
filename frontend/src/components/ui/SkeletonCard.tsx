'use client';

import { motion } from 'framer-motion';

export default function SkeletonCard() {
    return (
        <div className="glass-card p-4 rounded-xl border border-[var(--theme-card-border)]/50">
            {/* Icon skeleton */}
            <div className="flex items-start justify-between mb-3">
                <div className="w-8 h-8 rounded-lg bg-white/5 animate-pulse" />
                <div className="w-12 h-5 rounded-full bg-white/5 animate-pulse" />
            </div>

            {/* Value skeleton */}
            <div className="mb-2">
                <div className="w-24 h-8 rounded bg-white/10 animate-pulse mb-2" />
                <div className="w-32 h-3 rounded bg-white/5 animate-pulse" />
            </div>

            {/* Description skeleton */}
            <div className="flex items-center justify-between">
                <div className="w-20 h-3 rounded bg-white/5 animate-pulse" />
                <div className="w-16 h-3 rounded bg-white/5 animate-pulse" />
            </div>

            {/* Shimmer effect */}
            <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"
                animate={{
                    x: ['-100%', '100%'],
                }}
                transition={{
                    repeat: Infinity,
                    duration: 1.5,
                    ease: 'linear',
                }}
                style={{ width: '50%' }}
            />
        </div>
    );
}
