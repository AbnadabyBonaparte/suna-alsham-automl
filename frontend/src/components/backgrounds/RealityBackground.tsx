"use client";

import { useTheme } from "@/contexts/ThemeContext";
import QuantumParticles from "./QuantumParticles";
import TacticalGrid from "./TacticalGrid";
import NeuralPulse from "./NeuralPulse";
import PremiumNoise from "./PremiumNoise";
import GodRays from "./GodRays";

/**
 * Conditional Background Renderer
 * Renders the correct background component based on active reality
 */
export default function RealityBackground() {
    const { realityConfig } = useTheme();

    if (realityConfig.assets.particles) {
        return <QuantumParticles />;
    }

    if (realityConfig.assets.tacticalGrid) {
        return <TacticalGrid />;
    }

    if (realityConfig.assets.neuralPulse) {
        return <NeuralPulse />;
    }

    if (realityConfig.assets.noiseTexture) {
        return <PremiumNoise />;
    }

    if (realityConfig.assets.volumetricLight) {
        return <GodRays />;
    }

    // Fallback to simple gradient
    return (
        <div
            className="fixed inset-0 z-0 pointer-events-none"
            style={{ background: realityConfig.colors.bgCore }}
        />
    );
}
