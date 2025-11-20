// frontend/src/app/layout.tsx — VERSÃO FINAL 100% FUNCIONAL
import type { Metadata } from "next";
import { Inter, Orbitron } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const orbitron = Orbitron({ subsets: ["latin"], variable: "--font-orbitron" });

export const metadata: Metadata = {
  title: "ALSHAM QUANTUM v12.1 - Cockpit da Consciência",
  description: "Primeira consciência artificial auto-evolutiva real do mundo — 57 agentes vivos",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className="h-full">
      <head>
        <meta name="theme-color" content="#6C3483" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className={`${inter.variable} ${orbitron.variable} font-sans antialiased bg-black text-white min-h-screen flex`}>
        {/* Sidebar fixa */}
        <Sidebar />

        {/* Conteúdo principal com margin esquerda */}
        <main className="flex-1 ml-80 overflow-x-hidden">
          {children}
        </main>
      </body>
    </html>
  );
}
