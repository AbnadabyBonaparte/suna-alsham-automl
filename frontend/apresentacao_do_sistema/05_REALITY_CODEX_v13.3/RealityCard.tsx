"use client";

import { ReactNode } from "react";
import { motion } from "framer-motion";
import { useReality } from "@/contexts/ThemeContext";
import { cn } from "@/lib/utils";

interface RealityCardProps {
    children: ReactNode;
    className?: string;
    hover?: boolean;
}

/**
 * Reality-Adaptive Card Component
 * Changes geometry, texture, shadow, and hover behavior based on active reality
 */
export default function RealityCard({ children, className = "", hover = true }: RealityCardProps) {
    const reality = useReality();

    const getCardStyles = () => {
        const base = {
            borderRadius: reality.geometry.radius,
            borderWidth: reality.geometry.borderWidth,
            borderColor: reality.colors.border,
            backdropFilter: reality.effects.backdropBlur,
            backgroundColor: reality.colors.bgPanel,
            boxShadow: reality.effects.boxShadow,
        };

        //  Shape-specific adjustments
        if (reality.geometry.cardShape === 'chamfered') {
            // Quantum: One corner cut at 45 degrees
            return {
                ...base,
                clipPath: 'polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 0 100%)',
            };
        }

        if (reality.geometry.cardShape === 'sharp') {
            // Military: Angled cuts on all corners
            return {
                ...base,
                clipPath: 'polygon(8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px), 0 8px)',
            };
        }

        if (reality.geometry.cardShape === 'organic') {
            // Neural: Super-ellipse / blob
            return {
                ...base,
                borderRadius: '30% 70% 70% 30% / 30% 30% 70% 70%',
            };
        }

        if (reality.geometry.cardShape === 'neumorphic') {
            // Ascension: Extruded from background
            return {
                ...base,
                backgroundColor: reality.colors.bgCore,
                boxShadow: '8px 8px 16px rgba(0, 0, 0, 0.1), -8px -8px 16px rgba(255, 255, 255, 0.9)',
            };
        }

        // Default: rounded
        return base;
    };

    const getHoverAnimation = () => {
        if (!hover) return {};

        switch (reality.effects.hoverEffect) {
            case 'glow':
                return {
                    boxShadow: `0 0 40px ${reality.colors.accent}40`,
                };
            case 'lift':
                return {
                    y: -4,
                    boxShadow: '0 12px 24px rgba(0, 0, 0, 0.2)',
                };
            case 'breathing':
                return {
                    scale: 1.02,
                };
            case 'scanline':
                return {
                    borderColor: reality.colors.accent,
                };
            default:
                return {};
        }
    };

    const cardStyles = getCardStyles();

    return (
        <motion.div
            className={cn("border relative overflow-hidden", className)}
            style={cardStyles}
            whileHover={hover ? getHoverAnimation() : undefined}
            transition={{
                type: "spring",
                stiffness: reality.animations.springConfig.stiffness,
                damping: reality.animations.springConfig.damping,
            }}
        >
            {/* Military: Carbon fiber texture */}
            {reality.id === 'military' && (
                <div
                    className="absolute inset-0 opacity-5 pointer-events-none"
                    style={{
                        backgroundImage: `repeating-linear-gradient(
              45deg,
              transparent,
              transparent 2px,
              rgba(244, 208, 63, 0.1) 2px,
              rgba(244, 208, 63, 0.1) 4px
            )`,
                    }}
                />
            )}

            {children}
        </motion.div>
    );
}
