// Simple toast notification system for micro-updates
'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

interface Toast {
    id: string;
    message: string;
    type: 'success' | 'error' | 'info' | 'warning';
    icon?: string;
}

interface ToastContextType {
    showToast: (message: string, type?: Toast['type'], icon?: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toasts, setToasts] = useState<Toast[]>([]);

    const showToast = (message: string, type: Toast['type'] = 'info', icon?: string) => {
        const id = Date.now().toString();
        const newToast = { id, message, type, icon };

        setToasts(prev => [...prev, newToast]);

        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            setToasts(prev => prev.filter(t => t.id !== id));
        }, 3000);
    };

    const dismiss = (id: string) => {
        setToasts(prev => prev.filter(t => t.id !== id));
    };

    const getIcon = (type: Toast['type']) => {
        switch (type) {
            case 'success': return <CheckCircle className="w-5 h-5" />;
            case 'error': return <AlertCircle className="w-5 h-5" />;
            case 'warning': return <AlertTriangle className="w-5 h-5" />;
            default: return <Info className="w-5 h-5" />;
        }
    };

    const getColors = (type: Toast['type']) => {
        switch (type) {
            case 'success': return 'border-green-500/50 bg-green-500/10 text-green-400';
            case 'error': return 'border-red-500/50 bg-red-500/10 text-red-400';
            case 'warning': return 'border-yellow-500/50 bg-yellow-500/10 text-yellow-400';
            default: return 'border-blue-500/50 bg-blue-500/10 text-blue-400';
        }
    };

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}

            {/* Toast Container */}
            <div className="fixed bottom-6 right-6 z-[200] flex flex-col gap-2 max-w-sm">
                <AnimatePresence>
                    {toasts.map(toast => (
                        <motion.div
                            key={toast.id}
                            initial={{ opacity: 0, y: 20, scale: 0.9 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, x: 100 }}
                            className={`glass-panel p-4 rounded-xl border flex items-center gap-3 ${getColors(toast.type)}`}
                        >
                            {toast.icon ? (
                                <span className="text-2xl">{toast.icon}</span>
                            ) : (
                                getIcon(toast.type)
                            )}
                            <span className="flex-1 text-sm font-medium">{toast.message}</span>
                            <button
                                onClick={() => dismiss(toast.id)}
                                className="hover:opacity-70 transition-opacity"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </ToastContext.Provider>
    );
}

export function useToast() {
    const context = useContext(ToastContext);
    if (!context) throw new Error('useToast must be used within ToastProvider');
    return context;
}
