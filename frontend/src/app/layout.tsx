import type { Metadata } from "next";
import { Orbitron, Inter, Rajdhani } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeProvider } from "@/contexts/ThemeContext";
import { RealityBackground } from "@/components/backgrounds/RealityBackground";

const orbitron = Orbitron({ 
  subsets: ["latin"], 
  variable: "--font-orbitron", 
  display: "swap" 
});

const inter = Inter({ 
  subsets: ["latin"], 
  variable: "--font-inter", 
  display: "swap" 
});

const rajdhani = Rajdhani({ 
  subsets: ["latin"], 
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-rajdhani", 
  display: "swap" 
});

export const metadata: Metadata = {
  title: "ALSHAM QUANTUM v13.3 | Reality Codex",
  description: "Cockpit de Inteligência Suprema - Sistema de Realidades Visuais",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html 
      lang="pt-br" 
      className={`${orbitron.variable} ${inter.variable} ${rajdhani.variable}`}
      data-theme="quantum"
      suppressHydrationWarning
    >
      <body 
        className="antialiased h-screen w-screen overflow-hidden flex"
        style={{
          background: 'var(--bg-core)',
          color: 'var(--text-primary)',
        }}
      >
        <ThemeProvider>
          <AuthProvider>
            {/* Background dinâmico baseado no tema */}
            <RealityBackground />
            
            <aside className="flex-shrink-0 z-50 hidden md:block relative">
              <Sidebar />
            </aside>
            
            <main 
              className="flex-1 relative h-full overflow-y-auto overflow-x-hidden z-10"
            >
              {children}
            </main>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
