'use client';

import { motion } from 'framer-motion';

interface LoadingStateProps {
  message?: string;
  rows?: number;
}

export function LoadingState({ message = 'Carregando...', rows = 3 }: LoadingStateProps) {
  return (
    <div className="q-panel q-grain q-rise flex flex-col items-center justify-center gap-4 px-6 py-16">
      <div className="relative">
        <div className="q-glow-blob left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2" />
        <motion.div
          className="relative h-11 w-11 rounded-full border-2 border-[var(--color-primary)] border-t-transparent"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
      </div>
      <p className="font-mono text-sm text-[var(--color-text-secondary)]">{message}</p>
      <div className="mt-2 w-full max-w-md space-y-3">
        {Array.from({ length: rows }).map((_, i) => (
          <div
            key={i}
            className="h-4 animate-pulse rounded"
            style={{
              width: `${100 - i * 15}%`,
              background: 'color-mix(in srgb, var(--color-surface) 60%, transparent)',
            }}
          />
        ))}
      </div>
    </div>
  );
}
