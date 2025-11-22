"use client";

import { useTheme } from "@/contexts/ThemeContext";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { Settings, Monitor, Shield, Cpu, Briefcase, Sun } from "lucide-react";

const themes = [
    { id: "quantum", name: "QUANTUM LAB", icon: <Monitor className="w-4 h-4" />, color: "#00FFC8" },
    { id: "military", name: "MILITARY OPS", icon: <Shield className="w-4 h-4" />, color: "#F4D03F" },
    { id: "neural", name: "NEURAL SINGULARITY", icon: <Cpu className="w-4 h-4" />, color: "#D022FF" },
    { id: "titanium", name: "TITANIUM EXECUTIVE", icon: <Briefcase className="w-4 h-4" />, color: "#38BDF8" },
    { id: "ascension", name: "LUMINOUS ASCENSION", icon: <Sun className="w-4 h-4" />, color: "#D97706" },
];

export default function ThemeSwitcher() {
    const { theme, setTheme } = useTheme();
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="fixed bottom-6 left-6 z-50">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.9 }}
                        className="absolute bottom-16 left-0 mb-2 glass-panel p-2 rounded-xl border border-[var(--border)] min-w-[200px] flex flex-col gap-1"
                    >
                        <div className="px-3 py-2 text-xs font-bold text-[var(--text-primary)] opacity-50 tracking-widest border-b border-[var(--border)] mb-1">
                            SELECT REALITY
                        </div>
                        {themes.map((t) => (
                            <button
                                key={t.id}
                                onClick={() => {
                                    setTheme(t.id as any);
                                    setIsOpen(false);
                                }}
                                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-mono transition-all ${theme === t.id
                                        ? "bg-[var(--accent)] text-black font-bold"
                                        : "text-[var(--text-primary)] hover:bg-[var(--bg-panel)] hover:border hover:border-[var(--border)]"
                                    }`}
                            >
                                {t.icon}
                                {t.name}
                            </button>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>

            <button
                onClick={() => setIsOpen(!isOpen)}
                className="p-3 rounded-full bg-[var(--bg-panel)] border border-[var(--border)] text-[var(--accent)] shadow-[var(--effect-glow)] hover:scale-110 transition-transform"
            >
                <Settings className={`w-6 h-6 ${isOpen ? "animate-spin" : ""}`} />
            </button>
        </div>
    );
}
