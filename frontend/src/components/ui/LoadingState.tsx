'use client';

import { motion } from 'framer-motion';

interface LoadingStateProps {
  message?: string;
  rows?: number;
}

export function LoadingState({ message = 'Carregando...', rows = 3 }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <motion.div
        className="w-10 h-10 border-2 border-primary border-t-transparent rounded-full"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      />
      <p className="text-textSecondary text-sm">{message}</p>
      <div className="w-full max-w-md space-y-3 mt-4">
        {Array.from({ length: rows }).map((_, i) => (
          <div
            key={i}
            className="h-4 bg-surface rounded animate-pulse"
            style={{ width: `${100 - i * 15}%` }}
          />
        ))}
      </div>
    </div>
  );
}
