/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - TOAST CONTAINER
 * ═══════════════════════════════════════════════════════════════
 * Global toast notification UI with glassmorphism + animations
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle, XCircle, AlertTriangle, Info, X
} from 'lucide-react';
import { useNotificationStore, type NotificationType } from '@/stores/useNotificationStore';

const ICON_MAP: Record<NotificationType, React.ElementType> = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertTriangle,
  info: Info,
};

const COLOR_MAP: Record<NotificationType, { bg: string; border: string; icon: string; text: string }> = {
  success: {
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/30',
    icon: 'text-emerald-400',
    text: 'text-emerald-100',
  },
  error: {
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    icon: 'text-red-400',
    text: 'text-red-100',
  },
  warning: {
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500/30',
    icon: 'text-yellow-400',
    text: 'text-yellow-100',
  },
  info: {
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/30',
    icon: 'text-blue-400',
    text: 'text-blue-100',
  },
};

export function ToastContainer() {
  const { notifications, removeNotification } = useNotificationStore();

  return (
    <div className="fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none max-w-md w-full">
      <AnimatePresence mode="popLayout">
        {notifications.map((notification) => {
          const Icon = ICON_MAP[notification.type];
          const colors = COLOR_MAP[notification.type];

          return (
            <motion.div
              key={notification.id}
              layout
              initial={{ opacity: 0, x: 100, scale: 0.8 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 100, scale: 0.8 }}
              transition={{
                type: "spring",
                stiffness: 300,
                damping: 25
              }}
              className={`
                relative pointer-events-auto
                ${colors.bg} backdrop-blur-xl
                border ${colors.border}
                rounded-2xl p-4 shadow-2xl
                flex items-start gap-3
                overflow-hidden
              `}
            >
              {/* Glow Effect */}
              <div className={`absolute inset-0 ${colors.bg} blur-xl opacity-50 pointer-events-none`} />

              {/* Icon */}
              <div className={`relative z-10 ${colors.icon} flex-shrink-0 mt-0.5`}>
                <Icon className="w-5 h-5" />
              </div>

              {/* Content */}
              <div className="relative z-10 flex-1 min-w-0">
                <h4 className={`font-bold text-sm ${colors.text} mb-0.5`}>
                  {notification.title}
                </h4>
                {notification.message && (
                  <p className="text-xs text-gray-300 leading-relaxed">
                    {notification.message}
                  </p>
                )}
              </div>

              {/* Close Button */}
              <button
                onClick={() => removeNotification(notification.id)}
                className={`
                  relative z-10 flex-shrink-0
                  ${colors.icon} hover:text-white
                  transition-colors
                `}
                aria-label="Close notification"
              >
                <X className="w-4 h-4" />
              </button>

              {/* Progress Bar (if duration is set) */}
              {notification.duration && notification.duration > 0 && (
                <motion.div
                  className={`absolute bottom-0 left-0 h-0.5 ${colors.icon.replace('text-', 'bg-')}`}
                  initial={{ width: '100%' }}
                  animate={{ width: '0%' }}
                  transition={{
                    duration: notification.duration / 1000,
                    ease: 'linear'
                  }}
                />
              )}

              {/* Scan Line Effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"
                initial={{ x: '-100%' }}
                animate={{ x: '100%' }}
                transition={{
                  duration: 1.5,
                  ease: 'easeInOut',
                  repeat: Infinity,
                  repeatDelay: 3
                }}
              />
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
