'use client';

import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from './button';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  message = 'Erro ao carregar dados. Tente novamente.',
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className="w-16 h-16 rounded-full bg-error/10 flex items-center justify-center">
        <AlertTriangle className="w-8 h-8 text-error" />
      </div>
      <p className="text-textSecondary text-sm text-center max-w-md">{message}</p>
      {onRetry && (
        <Button variant="outline" onClick={onRetry} className="mt-2 gap-2">
          <RefreshCw className="w-4 h-4" />
          Tentar novamente
        </Button>
      )}
    </div>
  );
}
