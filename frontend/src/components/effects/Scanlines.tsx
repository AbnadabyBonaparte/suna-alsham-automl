"use client";

import { useEffect, useState } from "react";

/**
 * CRT Scanlines Effect - Military Ops only
 * Based on Códice Visual Oficial - REALIDADE 2
 */
export default function Scanlines() {
    const [position, setPosition] = useState(-100);

    useEffect(() => {
        const interval = setInterval(() => {
            setPosition(prev => {
                if (prev >= 100) return -100;
                return prev + 0.5;
            });
        }, 16); // ~60fps

        return () => clearInterval(interval);
    }, []);

    return (
        <>
            {/* Horizontal scanline sweep */}
            <div
                className="fixed left-0 right-0 h-0.5 bg-[#F4D03F] opacity-20 z-50 pointer-events-none blur-sm"
                style={{
                    top: `${position}%`,
                    transition: 'top 0.016s linear',
                }}
            />

            {/* Static scanlines overlay */}
            <div className="fixed inset-0 z-50 pointer-events-none">
                <div
                    className="w-full h-full opacity-5"
                    style={{
                        backgroundImage: `repeating-linear-gradient(
              0deg,
              rgba(244, 208, 63, 0.1) 0px,
              transparent 1px,
              transparent 2px
            )`,
                    }}
                />
            </div>
        </>
    );
}
