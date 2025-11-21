"use client";

import { motion } from "framer-motion";
import { Activity, Cpu, Zap } from "lucide-react";

interface AgentCardProps {
    name: string;
    role: string;
    status: "active" | "idle" | "processing";
    efficiency: number;
}

export default function AgentCard({ name, role, status, efficiency }: AgentCardProps) {
    const statusColors = {
        active: "text-green-400 border-green-400/50 shadow-[0_0_10px_rgba(74,222,128,0.3)]",
        idle: "text-gray-400 border-gray-400/50",
        processing: "text-[var(--color-photon-gold)] border-[var(--color-photon-gold)]/50 shadow-[0_0_10px_rgba(244,208,63,0.3)]"
    };

    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="glass-card p-6 relative overflow-hidden"
        >
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h4 className="text-lg font-orbitron text-white">{name}</h4>
                    <p className="text-xs text-gray-400 uppercase tracking-wider">{role}</p>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs border ${statusColors[status]} uppercase tracking-widest`}>
                    {status}
                </div>
            </div>

            <div className="grid grid-cols-3 gap-2 mt-4">
                <div className="text-center p-2 bg-white/5 rounded-lg">
                    <Activity className="w-4 h-4 mx-auto mb-1 text-[var(--color-neon-blue)]" />
                    <span className="text-xs text-gray-300">{efficiency}%</span>
                </div>
                <div className="text-center p-2 bg-white/5 rounded-lg">
                    <Cpu className="w-4 h-4 mx-auto mb-1 text-[var(--color-quantum-purple)]" />
                    <span className="text-xs text-gray-300">CPU</span>
                </div>
                <div className="text-center p-2 bg-white/5 rounded-lg">
                    <Zap className="w-4 h-4 mx-auto mb-1 text-[var(--color-photon-gold)]" />
                    <span className="text-xs text-gray-300">PWR</span>
                </div>
            </div>

            {/* Progress Bar */}
            <div className="mt-4 h-1 w-full bg-white/10 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${efficiency}%` }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="h-full bg-gradient-to-r from-[var(--color-neon-blue)] to-[var(--color-quantum-purple)]"
                />
            </div>
        </motion.div>
    );
}
