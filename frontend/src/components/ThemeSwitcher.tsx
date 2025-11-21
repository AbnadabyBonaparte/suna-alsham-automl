"use client";

import { useTheme, themes } from '@/contexts/ThemeProvider';
import { motion, AnimatePresence } from 'framer-motion';
import { Palette } from 'lucide-react';
import { useState } from 'react';

export default function ThemeSwitcher() {
    const { currentTheme, setTheme, availableThemes } = useTheme();
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="fixed bottom-24 right-6 z-[99]">
            {/* Compact Floating Button */}
            <motion.button
                onClick={() => setIsOpen(!isOpen)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="w-11 h-11 rounded-full glass-panel border border-[var(--theme-card-border)]
                   flex items-center justify-center shadow-lg backdrop-blur-xl
                   hover:border-[var(--theme-primary)] transition-all duration-300"
                style={{
                    boxShadow: isOpen ? `0 0 20px ${themes[currentTheme].primary}40` : '0 4px 12px rgba(0,0,0,0.2)'
                }}
            >
                <Palette className="w-4 h-4 text-[var(--theme-accent)]" />
            </motion.button>

            {/* Compact Dropdown */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8, y: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.8, y: 10 }}
                        className="absolute bottom-14 right-0 glass-panel rounded-xl p-2 border border-[var(--theme-card-border)]
                       shadow-2xl backdrop-blur-xl min-w-[140px]"
                    >
                        {availableThemes.map((themeName) => {
                            const theme = themes[themeName];
                            const isActive = currentTheme === themeName;

                            return (
                                <motion.button
                                    key={themeName}
                                    onClick={() => {
                                        setTheme(themeName);
                                        setIsOpen(false);
                                    }}
                                    whileHover={{ x: 4 }}
                                    className={`
                    w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-left
                    transition-all duration-200 group
                    ${isActive
                                            ? 'bg-[var(--theme-primary)]/20 border border-[var(--theme-primary)]'
                                            : 'hover:bg-white/5 border border-transparent'
                                        }
                  `}
                                >
                                    {/* Tiny Color Indicator */}
                                    <div
                                        className="w-2 h-2 rounded-full"
                                        style={{
                                            backgroundColor: theme.primary,
                                            boxShadow: isActive ? `0 0 8px ${theme.primary}` : 'none'
                                        }}
                                    />

                                    {/* Theme Name */}
                                    <span className={`
                    text-[10px] font-medium tracking-wide transition-colors
                    ${isActive
                                            ? 'text-[var(--theme-text-primary)]'
                                            : 'text-[var(--theme-text-secondary)] group-hover:text-[var(--theme-text-primary)]'
                                        }
                  `}>
                                        {theme.name}
                                    </span>
                                </motion.button>
                            );
                        })}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
