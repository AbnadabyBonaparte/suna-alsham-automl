'use client';

import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from './button';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  message = 'Não foi possível carregar os dados. Tente novamente.',
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="q-panel q-grain q-rise flex flex-col items-center justify-center gap-4 px-6 py-16 text-center">
      <div
        className="flex h-16 w-16 items-center justify-center rounded-2xl border"
        style={{
          background: 'color-mix(in srgb, var(--color-error) 12%, transparent)',
          borderColor: 'color-mix(in srgb, var(--color-error) 35%, transparent)',
          color: 'var(--color-error)',
        }}
      >
        <AlertTriangle className="h-7 w-7" />
      </div>
      <h3 className="text-lg font-semibold text-[var(--color-text)]">Algo saiu do eixo</h3>
      <p className="max-w-md text-sm leading-relaxed text-[var(--color-text-secondary)]">
        {message}
      </p>
      {onRetry && (
        <Button variant="outline" onClick={onRetry} className="mt-2 gap-2">
          <RefreshCw className="h-4 w-4" />
          Tentar novamente
        </Button>
      )}
    </div>
  );
}
