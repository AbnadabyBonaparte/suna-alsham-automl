"use client";

/**
 * Luminous Ascension Background - God Rays (Volumetric Light)
 * Based on Códice Visual Oficial - REALIDADE 5
 */
export default function GodRays() {
    return (
        <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
            {/* Diagonal light rays */}
            <div className="absolute inset-0 opacity-10">
                {[...Array(8)].map((_, i) => (
                    <div
                        key={i}
                        className="absolute h-[200%] w-32 bg-gradient-to-r from-transparent via-[#D97706] to-transparent blur-2xl animate-god-ray"
                        style={{
                            left: `${i * 15}%`,
                            top: '-50%',
                            transform: `rotate(25deg) translateY(${i * 10}px)`,
                            animationDelay: `${i * 0.5}s`,
                        }}
                    />
                ))}
            </div>

            {/* Subtle ambient glow */}
            <div className="absolute inset-0 bg-gradient-to-b from-[#F59E0B]/5 via-transparent to-transparent" />
        </div>
    );
}
