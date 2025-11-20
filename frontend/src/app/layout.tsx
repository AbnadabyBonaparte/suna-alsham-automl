// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import { Orbitron, Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar"; // Trazendo a navegação de volta

// Configuração das Fontes
const orbitron = Orbitron({ 
  subsets: ["latin"], 
  variable: "--font-orbitron",
  display: "swap",
});

const inter = Inter({ 
  subsets: ["latin"], 
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "ALSHAM QUANTUM v12.1",
  description: "Sistema de Inteligência Suprema - Cockpit Central",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-br" className={`${orbitron.variable} ${inter.variable} dark`}>
      <body className="bg-[#020C1B] text-white antialiased h-screen w-screen overflow-hidden flex selection:bg-[#F4D03F] selection:text-black">
        
        {/* ZONA 1: SIDEBAR (Navegação) */}
        <aside className="flex-shrink-0 z-50">
          <Sidebar />
        </aside>

        {/* ZONA 2: CONTEÚDO PRINCIPAL (Onde os agentes vivem) */}
        <main className="flex-1 relative h-full overflow-y-auto overflow-x-hidden bg-[url('/grid.svg')] bg-fixed">
          
          {/* Efeito de brilho no topo */}
          <div className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#6C3483] via-[#F4D03F] to-[#6C3483] opacity-50 z-40 pointer-events-none" />
          
          {children}
        </main>

      </body>
    </html>
  );
}
