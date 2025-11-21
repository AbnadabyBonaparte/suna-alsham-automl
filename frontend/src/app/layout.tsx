import type { Metadata } from "next";
import { Orbitron, Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";
import { AuthProvider } from "@/contexts/AuthContext";
import QuantumBackground from "@/components/QuantumBackground";
import OrionCopilot from "@/components/OrionCopilot";

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

export const metadata: Metadata = {
  title: "ALSHAM QUANTUM v12.1",
  description: "Cockpit de Inteligência Suprema",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={`${orbitron.variable} ${inter.variable} dark`}>
      <body className="bg-[#020C1B] text-white antialiased min-h-screen relative overflow-hidden flex">
        <AuthProvider>
          <div className="fixed inset-0 z-0">
            <QuantumBackground />
          </div>

          <aside className="flex-shrink-0 z-50 hidden md:block relative">
            <Sidebar />
          </aside>

          <main className="flex-1 relative z-10 h-full overflow-y-auto overflow-x-hidden">
            {children}
          </main>

          <OrionCopilot />
        </AuthProvider>
      </body>
    </html>
  );
}
