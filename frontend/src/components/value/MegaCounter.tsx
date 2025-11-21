'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface MegaCounterProps {
    value: number;
    label: string;
    sublabel: string;
    prefix?: string;
    animated?: boolean;
}

export default function MegaCounter({
    value,
    label,
    sublabel,
    prefix = 'R$',
    animated = true
}: MegaCounterProps) {
    const [displayValue, setDisplayValue] = useState(0);

    useEffect(() => {
        if (!animated) {
            setDisplayValue(value);
            return;
        }

        const duration = 2000;
        const steps = 60;
        const stepValue = value / steps;
        const stepDuration = duration / steps;

        let current = 0;
        const interval = setInterval(() => {
            current += stepValue;
            if (current >= value) {
                setDisplayValue(value);
                clearInterval(interval);
            } else {
                setDisplayValue(Math.floor(current));
            }
        }, stepDuration);

        return () => clearInterval(interval);
    }, [value, animated]);

    const formatValue = (val: number) => {
        return val.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-5 rounded-xl border border-[var(--theme-primary)]/30 
                 shadow-lg relative overflow-hidden"
        >
            {/* Subtle Glow */}
            <div
                className="absolute inset-0 opacity-10"
                style={{
                    background: `radial-gradient(circle at 50% 50%, var(--theme-primary) 0%, transparent 70%)`
                }}
            />

            {/* Content */}
            <div className="relative z-10 text-center">
                <motion.div
                    className="font-orbitron text-3xl md:text-4xl font-bold mb-1"
                    style={{
                        background: `linear-gradient(135deg, var(--theme-primary) 0%, var(--theme-accent) 100%)`,
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text'
                    }}
                >
                    {prefix} {formatValue(displayValue)}
                </motion.div>

                <h2 className="font-orbitron text-xs tracking-widest text-[var(--theme-text-primary)] mb-0.5">
                    {label}
                </h2>

                <p className="text-[10px] text-[var(--theme-text-secondary)]">
                    {sublabel}
                </p>
            </div>
        </motion.div>
    );
}
