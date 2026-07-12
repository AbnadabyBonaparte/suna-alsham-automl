'use client';

/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — PAGE HEADER (padrão único de cabeçalho)
 * ═══════════════════════════════════════════════════════════════
 * Cabeçalho editorial coerente para TODAS as rotas do dashboard:
 * eyebrow + título com gradiente + subtítulo + chips/ações à direita.
 * ═══════════════════════════════════════════════════════════════
 */

import React from 'react';
import type { LucideIcon } from 'lucide-react';

export interface PageHeaderChip {
  label: string;
  value: React.ReactNode;
  tone?: 'primary' | 'success' | 'accent' | 'warning' | 'error';
}

const TONE_VAR: Record<NonNullable<PageHeaderChip['tone']>, string> = {
  primary: 'var(--color-primary)',
  success: 'var(--color-success)',
  accent: 'var(--color-accent)',
  warning: 'var(--color-warning)',
  error: 'var(--color-error)',
};

export interface PageHeaderProps {
  /** Texto curto acima do título (kicker). */
  eyebrow?: string;
  /** Título — a última palavra pode receber destaque via `titleAccent`. */
  title: string;
  /** Trecho do título renderizado em gradiente da marca. */
  titleAccent?: string;
  /** Subtítulo / proposta de valor em uma frase. */
  subtitle?: string;
  /** Ícone de marca ao lado do título. */
  icon?: LucideIcon;
  /** Mostra o ponto pulsante "ao vivo" no eyebrow. */
  live?: boolean;
  /** Chips de métrica à direita (dados reais — nunca inventar). */
  chips?: PageHeaderChip[];
  /** Ações (botões) à direita. */
  actions?: React.ReactNode;
}

export function PageHeader({
  eyebrow,
  title,
  titleAccent,
  subtitle,
  icon: Icon,
  live = false,
  chips,
  actions,
}: PageHeaderProps) {
  return (
    <header className="q-panel-hero q-grain q-rise p-6 md:p-8">
      <div className="q-glow-blob -right-24 -top-24 h-96 w-96" />
      <div className="relative z-10 flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div className="min-w-0">
          {eyebrow && (
            <span className="q-eyebrow mb-3">
              {live && (
                <span className="relative flex h-2.5 w-2.5">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[var(--color-primary)] opacity-75" />
                  <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-[var(--color-primary)]" />
                </span>
              )}
              {eyebrow}
            </span>
          )}
          <div className="flex items-center gap-4">
            {Icon && (
              <span className="q-icon-badge h-12 w-12 shrink-0">
                <Icon className="h-6 w-6" />
              </span>
            )}
            <h1 className="text-3xl font-bold tracking-tight text-[var(--color-text)] md:text-4xl">
              {title}
              {titleAccent && (
                <>
                  {' '}
                  <span className="q-title-gradient">{titleAccent}</span>
                </>
              )}
            </h1>
          </div>
          {subtitle && (
            <p className="mt-3 max-w-2xl text-sm leading-relaxed text-[var(--color-text-secondary)] md:text-base">
              {subtitle}
            </p>
          )}
        </div>

        {(chips?.length || actions) && (
          <div className="flex flex-wrap items-center gap-3">
            {chips?.map((chip, i) => (
              <div key={i} className="q-chip flex-col items-start gap-0.5 px-4 py-2 text-center">
                <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-secondary)]">
                  {chip.label}
                </span>
                <span
                  className="font-mono text-lg font-bold"
                  style={{ color: TONE_VAR[chip.tone ?? 'primary'] }}
                >
                  {chip.value}
                </span>
              </div>
            ))}
            {actions}
          </div>
        )}
      </div>
    </header>
  );
}

export default PageHeader;
