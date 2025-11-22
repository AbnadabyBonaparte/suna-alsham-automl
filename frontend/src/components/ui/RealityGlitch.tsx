"use client";

import { useTheme } from "@/contexts/ThemeContext";
import { useEffect, useState } from "react";

export default function RealityGlitch() {
    const { isTransitioning } = useTheme();
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        if (isTransitioning) {
            setVisible(true);
            const timer = setTimeout(() => setVisible(false), 600);
            return () => clearTimeout(timer);
        }
    }, [isTransitioning]);

    if (!visible) return null;

    return (
        <div className="fixed inset-0 z-[9999] pointer-events-none overflow-hidden">
            {/* Noise Layer */}
            <div className="absolute inset-0 bg-black opacity-90 animate-pulse"></div>

            {/* Glitch Bars */}
            <div className="absolute top-0 left-0 w-full h-2 bg-white opacity-50 animate-ping" style={{ top: '20%' }}></div>
            <div className="absolute top-0 left-0 w-full h-4 bg-[var(--accent)] opacity-30 animate-pulse" style={{ top: '60%' }}></div>

            {/* Static Effect (CSS based) */}
            <div className="absolute inset-0 mix-blend-overlay opacity-20"
                style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
                }}
            ></div>

            {/* Text Flash */}
            <div className="absolute inset-0 flex items-center justify-center">
                <h1 className="text-6xl font-black text-white tracking-widest glitch-text">
                    SHIFTING REALITY...
                </h1>
            </div>
        </div>
    );
}
