"use client";

import { motion } from "framer-motion";
import CountUp from "react-countup";

interface MegaCounterProps {
    label: string;
    value: string;
    subtext?: string;
}

export default function MegaCounter({ label, value, subtext }: MegaCounterProps) {
    // Extract numeric part and suffix/prefix if possible, or just use raw value if complex
    // Simple heuristic: if value is "8,492", we want 8492. If "R$ 1.2M", we might want to just show it or parse it.
    // For this specific component, let's try to be smart but safe.

    const numericValue = parseFloat(value.replace(/[^0-9.-]+/g, ""));
    const isNumber = !isNaN(numericValue);

    // Determine prefix/suffix based on value structure (simplified)
    let prefix = "";
    let suffix = "";

    if (value.includes("R$")) prefix = "R$ ";
    if (value.includes("%")) suffix = "%";
    if (value.includes("M")) suffix = "M";

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
                    {isNumber ? (
                        <CountUp
                            end={numericValue}
                            duration={2.5}
                            separator=","
                            decimals={value.includes(".") ? 1 : 0}
                            prefix={prefix}
                            suffix={suffix}
                        />
                    ) : (
                        value
                    )}
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
