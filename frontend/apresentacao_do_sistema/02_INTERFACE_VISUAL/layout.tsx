import type { Metadata } from "next";
import { Orbitron, Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeProvider } from "@/contexts/ThemeProvider";
import { GamificationProvider } from "@/contexts/GamificationProvider";
import { ToastProvider } from "@/contexts/ToastProvider";
import QuantumBackground from "@/components/QuantumBackground";
import OrionCopilot from "@/components/OrionCopilot";
import ThemeSwitcher from "@/components/ThemeSwitcher";

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
      <body className="bg-[#020C1B] text-white antialiased min-h-screen relative">
        <ThemeProvider>
          <GamificationProvider>
            <ToastProvider>
              <AuthProvider>
                <div className="fixed inset-0 z-0">
                  <QuantumBackground />
                </div>

                <div className="relative z-10 min-h-screen">
                  {children}
                </div>

                <ThemeSwitcher />
                <OrionCopilot />
              </AuthProvider>
            </ToastProvider>
          </GamificationProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
