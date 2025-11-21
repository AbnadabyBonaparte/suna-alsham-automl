'use client';

import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

interface MobileMenuProps {
    isOpen: boolean;
    onClose: () => void;
}

const menuItems = [
    { icon: '📊', label: 'Cockpit', href: '/dashboard' },
    { icon: '🤖', label: 'Sentinelas', href: '/dashboard/agents' },
    { icon: '💎', label: 'Valor', href: '/dashboard/value' },
    { icon: '📈', label: 'Matrix', href: '/dashboard/matrix' },
    { icon: '🔮', label: 'Evolution', href: '/dashboard/evolution' },
    { icon: '🌀', label: 'The Void', href: '/dashboard/void' },
];

export default function MobileMenu() {
    const [isOpen, setIsOpen] = useState(false);

    // Close menu on ESC key
    useEffect(() => {
        const handleEsc = (e: KeyboardEvent) => {
            if (e.key === 'Escape') setIsOpen(false);
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, []);

    // Prevent body scroll when menu is open
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
    }, [isOpen]);

    return (
        <>
            {/* Hamburger Button - Only visible on mobile */}
            <button
                onClick={() => setIsOpen(true)}
                className="fixed top-6 right-6 z-[100] md:hidden w-12 h-12 glass-panel rounded-xl
                   flex items-center justify-center border border-[var(--theme-card-border)]
                   hover:border-[var(--theme-primary)] transition-colors"
                aria-label="Abrir menu"
            >
                <Menu className="w-6 h-6 text-[var(--theme-text-primary)]" />
            </button>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsOpen(false)}
                            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-[110] md:hidden"
                        />

                        {/* Slide-in Menu */}
                        <motion.div
                            initial={{ x: '100%' }}
                            animate={{ x: 0 }}
                            exit={{ x: '100%' }}
                            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                            className="fixed top-0 right-0 bottom-0 w-[280px] glass-panel border-l border-[var(--theme-card-border)]
                         z-[120] md:hidden overflow-y-auto"
                        >
                            {/* Close Button */}
                            <button
                                onClick={() => setIsOpen(false)}
                                className="absolute top-6 right-6 w-10 h-10 flex items-center justify-center
                           rounded-lg hover:bg-white/10 transition-colors"
                                aria-label="Fechar menu"
                            >
                                <X className="w-5 h-5 text-[var(--theme-text-primary)]" />
                            </button>

                            {/* Menu Content */}
                            <div className="p-8 pt-20">
                                <h2 className="font-orbitron text-sm tracking-widest text-[var(--theme-text-secondary)] mb-6">
                                    NAVEGAÇÃO
                                </h2>

                                <nav className="space-y-2">
                                    {menuItems.map((item, index) => (
                                        <motion.div
                                            key={item.href}
                                            initial={{ opacity: 0, x: 20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: index * 0.05 }}
                                        >
                                            <Link
                                                href={item.href}
                                                onClick={() => setIsOpen(false)}
                                                className="flex items-center gap-3 px-4 py-3 rounded-lg
                                   hover:bg-[var(--theme-primary)]/10 border border-transparent
                                   hover:border-[var(--theme-primary)]/30 transition-all group"
                                            >
                                                <span className="text-2xl">{item.icon}</span>
                                                <span className="font-medium text-[var(--theme-text-primary)] group-hover:text-[var(--theme-primary)]">
                                                    {item.label}
                                                </span>
                                            </Link>
                                        </motion.div>
                                    ))}
                                </nav>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
}
