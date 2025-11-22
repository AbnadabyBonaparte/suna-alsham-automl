"use client";

import { useTheme } from "@/contexts/ThemeContext";
import Scanlines from "./Scanlines";

/**
 * Client-side conditional wrapper for Scanlines effect
 * Only renders for Military theme
 */
export default function ConditionalScanlines() {
    const { realityConfig } = useTheme();

    if (realityConfig.assets.scanlines) {
        return <Scanlines />;
    }

    return null;
}
