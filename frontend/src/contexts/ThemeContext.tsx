"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useTheme as useNextTheme } from "next-themes";
import { RealityConfig, RealityId, REALITY_CONFIGS } from "@/types/reality";

interface ThemeContextType {
    theme: RealityId;
    setTheme: (theme: RealityId) => void;
    isTransitioning: boolean;
    realityConfig: RealityConfig;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
    const { theme: nextTheme, setTheme: setNextTheme } = useNextTheme();
    const [isTransitioning, setIsTransitioning] = useState(false);
    const [mounted, setMounted] = useState(false);

    // Get current reality config
    const currentTheme = (nextTheme as RealityId) || 'quantum';
    const realityConfig = REALITY_CONFIGS[currentTheme];

    // Sound Effect
    const playGlitchSound = () => {
        const audio = new Audio("/sounds/glitch.mp3");
        audio.volume = 0.3;
        audio.play().catch(e => console.log("Audio play failed", e));
    };

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleSetTheme = (newTheme: RealityId) => {
        if (newTheme === nextTheme) return;

        setIsTransitioning(true);
        playGlitchSound();

        // Delay theme switch to match glitch effect
        setTimeout(() => {
            setNextTheme(newTheme);
        }, 200); // Switch halfway through glitch

        setTimeout(() => {
            setIsTransitioning(false);
        }, 600); // End glitch
    };

    return (
        <ThemeContext.Provider value={{
            theme: currentTheme,
            setTheme: handleSetTheme,
            isTransitioning,
            realityConfig
        }}>
            {children}
        </ThemeContext.Provider>
    );
}

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (context === undefined) {
        throw new Error("useTheme must be used within a ThemeProvider");
    }
    return context;
};

/**
 * Hook to access complete reality configuration
 */
export const useReality = () => {
    const { realityConfig } = useTheme();
    return realityConfig;
};
