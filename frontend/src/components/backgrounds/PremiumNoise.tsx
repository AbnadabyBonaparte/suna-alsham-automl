"use client";

/**
 * Titanium Executive Background - Premium Noise Texture
 * Based on Códice Visual Oficial - REALIDADE 4
 */
export default function PremiumNoise() {
    return (
        <div className="fixed inset-0 z-0 pointer-events-none">
            {/* Brushed steel / currency paper texture */}
            <svg className="absolute inset-0 w-full h-full opacity-[0.015]">
                <filter id="noise">
                    <feTurbulence
                        type="fractalNoise"
                        baseFrequency="0.65"
                        numOctaves="3"
                        stitchTiles="stitch"
                    />
                </filter>
                <rect width="100%" height="100%" filter="url(#noise)" />
            </svg>
        </div>
    );
}
