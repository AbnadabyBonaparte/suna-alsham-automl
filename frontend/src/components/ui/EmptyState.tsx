'use client';

import { Inbox } from 'lucide-react';
import { Button } from './button';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  icon,
  title = 'Nada por aqui — ainda',
  description = 'Nenhum registro para exibir no momento. Assim que houver dados, eles aparecem aqui.',
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="q-panel q-grain q-rise flex flex-col items-center justify-center gap-4 px-6 py-16 text-center">
      <div className="relative">
        <div className="q-glow-blob left-1/2 top-1/2 h-32 w-32 -translate-x-1/2 -translate-y-1/2" />
        <div className="q-icon-badge relative h-16 w-16">
          {icon || <Inbox className="h-7 w-7" />}
        </div>
      </div>
      <h3 className="text-lg font-semibold text-[var(--color-text)]">{title}</h3>
      <p className="max-w-md text-sm leading-relaxed text-[var(--color-text-secondary)]">
        {description}
      </p>
      {actionLabel && onAction && (
        <Button variant="outline" onClick={onAction} className="mt-2">
          {actionLabel}
        </Button>
      )}
    </div>
  );
}
