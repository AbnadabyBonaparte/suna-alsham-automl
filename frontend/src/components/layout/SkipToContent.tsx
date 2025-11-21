'use client';

export default function SkipToContent() {
    return (
        <a
            href="#main-content"
            className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[1000]
                 px-4 py-2 bg-[var(--theme-primary)] text-white rounded-lg
                 focus:outline-none focus:ring-2 focus:ring-[var(--theme-accent)]"
        >
            Pular para o conteúdo principal
        </a>
    );
}
