"use client";

/**
 * Military Ops Background - Tactical Grid + Crosshairs
 * Based on Códice Visual Oficial - REALIDADE 2
 */
export default function TacticalGrid() {
    return (
        <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
            {/* Milimetric Grid */}
            <svg className="absolute inset-0 w-full h-full opacity-5">
                <defs>
                    <pattern id="tactical-grid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#F4D03F" strokeWidth="0.5" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#tactical-grid)" />
            </svg>

            {/* Crosshairs in corners */}
            <div className="absolute top-8 left-8 w-8 h-8">
                <div className="absolute top-1/2 left-0 w-full h-px bg-[#F4D03F]" />
                <div className="absolute top-0 left-1/2 w-px h-full bg-[#F4D03F]" />
            </div>
            <div className="absolute top-8 right-8 w-8 h-8">
                <div className="absolute top-1/2 left-0 w-full h-px bg-[#F4D03F]" />
                <div className="absolute top-0 left-1/2 w-px h-full bg-[#F4D03F]" />
            </div>
            <div className="absolute bottom-8 left-8 w-8 h-8">
                <div className="absolute top-1/2 left-0 w-full h-px bg-[#F4D03F]" />
                <div className="absolute top-0 left-1/2 w-px h-full bg-[#F4D03F]" />
            </div>
            <div className="absolute bottom-8 right-8 w-8 h-8">
                <div className="absolute top-1/2 left-0 w-full h-px bg-[#F4D03F]" />
                <div className="absolute top-0 left-1/2 w-px h-full bg-[#F4D03F]" />
            </div>

            {/* Digital Camo Pattern */}
            <svg className="absolute inset-0 w-full h-full opacity-3">
                <defs>
                    <pattern id="camo" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
                        <rect x="0" y="0" width="30" height="30" fill="rgba(244, 208, 63, 0.02)" />
                        <rect x="35" y="15" width="25" height="25" fill="rgba(244, 208, 63, 0.01)" />
                        <rect x="10" y="45" width="20" height="35" fill="rgba(244, 208, 63, 0.015)" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#camo)" />
            </svg>
        </div>
    );
}
