/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — LEGAL SHELL
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/legal/LegalShell.tsx
 * ⚖️ Casca comum das páginas jurídicas (/terms /privacy /refund).
 *    Pele do mundo ALSHAM/Quantum via tokens — zero cor hardcoded.
 * ═══════════════════════════════════════════════════════════════
 */

import Link from 'next/link';
import { Hexagon } from 'lucide-react';
import type { ReactNode } from 'react';

interface LegalShellProps {
  title: string;
  updatedAt: string;
  children: ReactNode;
}

const LINKS = [
  { href: '/terms', label: 'Termos de Assinatura' },
  { href: '/privacy', label: 'Política de Privacidade' },
  { href: '/refund', label: 'Política de Reembolso' },
];

export default function LegalShell({ title, updatedAt, children }: LegalShellProps) {
  return (
    <div className="min-h-screen bg-background text-text relative overflow-hidden">
      {/* Gradientes sutis da pele Quantum */}
      <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-[var(--color-primary)]/5 to-transparent pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-full h-96 bg-gradient-to-t from-[var(--color-surface)] to-transparent pointer-events-none" />

      {/* Header */}
      <header className="relative z-10 pt-8 pb-4 px-6 border-b border-border/10">
        <nav className="max-w-4xl mx-auto flex justify-between items-center">
          <Link href="/" className="flex items-center gap-3 group">
            <Hexagon className="w-7 h-7 text-[var(--color-primary)] group-hover:rotate-180 transition-transform duration-700" />
            <span className="text-lg font-black tracking-tight">ALSHAM QUANTUM</span>
          </Link>
          <Link href="/pricing" className="text-sm text-textSecondary hover:text-text transition-colors">
            Ver planos
          </Link>
        </nav>
      </header>

      {/* Conteúdo */}
      <main className="relative z-10 max-w-3xl mx-auto px-6 py-16">
        <h1 className="text-3xl md:text-4xl font-black tracking-tight mb-2">{title}</h1>
        <p className="text-sm text-textSecondary mb-4">Última atualização: {updatedAt}</p>

        {/* Identificação do controlador/fornecedor */}
        <div className="mb-10 p-4 rounded-2xl bg-surface/40 border border-border/10 text-sm text-textSecondary leading-relaxed">
          <span className="text-text font-semibold">ALSHAM Global Commerce Ltda.</span> — CNPJ 59.332.265/0001-30.
          Contato: <a href="mailto:comercial@alshamglobal.com.br" className="text-[var(--color-primary)] hover:underline">comercial@alshamglobal.com.br</a>.
        </div>

        <article className="legal-prose space-y-6 text-[15px] leading-relaxed text-text/90">
          {children}
        </article>

        {/* Aviso honesto */}
        <div className="mt-12 p-4 rounded-2xl bg-[var(--color-warning)]/10 border border-[var(--color-warning)]/30 text-sm text-textSecondary leading-relaxed">
          Este documento é um instrumento contratual da ALSHAM Global. Em caso de dúvida sobre seus
          direitos, procure orientação jurídica independente. O Código de Defesa do Consumidor (Lei
          8.078/1990) e a LGPD (Lei 13.709/2018) prevalecem sobre qualquer cláusula que os contrarie.
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-border/10 py-10 px-6">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3">
            <Hexagon className="w-5 h-5 text-[var(--color-primary)]" />
            <span className="text-sm font-bold">ALSHAM QUANTUM</span>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-textSecondary">
            {LINKS.map((l) => (
              <Link key={l.href} href={l.href} className="hover:text-text transition-colors">
                {l.label}
              </Link>
            ))}
          </div>
          <div className="text-xs text-textSecondary">© 2026 ALSHAM Global. Todos os direitos reservados.</div>
        </div>
      </footer>
    </div>
  );
}

/** Subtítulo de seção — usado pelas páginas jurídicas. */
export function LegalSection({ n, title, children }: { n: string; title: string; children: ReactNode }) {
  return (
    <section className="space-y-3">
      <h2 className="text-lg font-bold text-text flex items-baseline gap-2">
        <span className="text-[var(--color-primary)] font-mono text-sm">{n}</span>
        {title}
      </h2>
      <div className="space-y-3 text-text/80">{children}</div>
    </section>
  );
}

/** Marca uma decisão pendente do fundador (Lei 7 — não inventar). */
export function Pendente({ children }: { children: ReactNode }) {
  return (
    <mark className="bg-[var(--color-warning)]/20 text-[var(--color-warning)] px-1.5 py-0.5 rounded font-medium not-italic">
      ({children})
    </mark>
  );
}
