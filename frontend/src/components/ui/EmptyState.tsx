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
  title = 'Nenhum dado encontrado',
  description = 'Não há registros para exibir no momento.',
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className="w-16 h-16 rounded-full bg-surface flex items-center justify-center">
        {icon || <Inbox className="w-8 h-8 text-textSecondary" />}
      </div>
      <h3 className="text-text font-medium text-lg">{title}</h3>
      <p className="text-textSecondary text-sm text-center max-w-md">{description}</p>
      {actionLabel && onAction && (
        <Button variant="outline" onClick={onAction} className="mt-2">
          {actionLabel}
        </Button>
      )}
    </div>
  );
}
