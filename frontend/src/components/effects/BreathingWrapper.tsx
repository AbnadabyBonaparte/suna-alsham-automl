"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

/**
 * Breathing Animation Wrapper - Neural Singularity only
 * Creates subtle scale pulsing (1.00 -> 1.01) in infinite loop
 */
interface BreathingWrapperProps {
    children: ReactNode;
    className?: string;
}

export default function BreathingWrapper({ children, className = "" }: BreathingWrapperProps) {
    return (
        <motion.div
            className={className}
            animate={{
                scale: [1, 1.01, 1],
            }}
            transition={{
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut",
            }}
        >
            {children}
        </motion.div>
    );
}
