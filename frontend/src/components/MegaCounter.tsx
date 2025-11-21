"use client";

import { motion } from "framer-motion";

interface MegaCounterProps {
    label: string;
    value: string;
    subtext?: string;
}

export default function MegaCounter({ label, value, subtext }: MegaCounterProps) {
    return (
        <div className="relative p-8 rounded-2xl glass-panel overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-quantum-purple)]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

            <div className="relative z-10 flex flex-col items-center justify-center text-center">
                <h3 className="text-[var(--color-neon-blue)] text-sm tracking-[0.2em] uppercase mb-2 font-orbitron">
                    {label}
                </h3>

                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="text-5xl md:text-7xl font-bold text-white font-orbitron neon-text mb-2"
                >
                    {value}
                </motion.div>

                {subtext && (
                    <p className="text-gray-400 text-xs tracking-wider">
                        {subtext}
                    </p>
                )}
            </div>

            {/* Decorative elements */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[var(--color-neon-blue)] to-transparent opacity-50" />
            <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[var(--color-quantum-purple)] to-transparent opacity-50" />
        </div>
    );
}
