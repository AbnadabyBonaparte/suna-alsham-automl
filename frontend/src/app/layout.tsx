import type { Metadata } from 'next';
import { Inter, Orbitron, Rajdhani } from 'next/font/google';
import './globals.css';
import { ThemeHydrator } from '@/components/ThemeHydrator';
import { AuthHydrator } from '@/components/AuthHydrator';
import { GlobalKeyListener } from '@/components/layout/GlobalKeyListener';
import RealityBackground from '@/components/backgrounds/RealityBackground';
import { ThemeSwitcher } from '@/components/ui/ThemeSwitcher';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

const orbitron = Orbitron({
  subsets: ['latin'],
  variable: '--font-orbitron',
});

const rajdhani = Rajdhani({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-rajdhani',
});

export const metadata: Metadata = {
  title: 'ALSHAM QUANTUM - Reality Codex v13.3',
  description: 'A Singularidade Chegou. Sistema de Gestão de Agentes Autônomos com IA.',
  keywords: ['AI', 'Quantum', 'Agents', 'CRM', 'Automation', 'Neural Networks'],
  authors: [{ name: 'ALSHAM GLOBAL' }],
  openGraph: {
    title: 'ALSHAM QUANTUM',
    description: 'A Singularidade Chegou',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="pt-BR"
      className={`${inter.variable} ${orbitron.variable} ${rajdhani.variable}`}
      suppressHydrationWarning
    >
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="antialiased">
        <ThemeHydrator />
        <AuthHydrator />

        <RealityBackground />
        <GlobalKeyListener />

        <main className="relative z-10">
          {children}
        </main>

        <ThemeSwitcher />
      </body>
    </html>
  );
}
