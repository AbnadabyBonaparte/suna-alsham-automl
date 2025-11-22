import type { Metadata } from "next";
import { Orbitron, Inter, IBM_Plex_Mono, Cinzel } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { GamificationProvider } from "@/contexts/GamificationProvider";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { ThemeProvider } from "@/contexts/ThemeContext";
import RealityGlitch from "@/components/ui/RealityGlitch";
import ThemeSwitcher from "@/components/ui/ThemeSwitcher";
import RealityBackground from "@/components/backgrounds/RealityBackground";
import ConditionalScanlines from "@/components/effects/ConditionalScanlines";
import OrionCopilot from "@/components/OrionCopilot";
import { ToastProvider } from "@/contexts/ToastProvider";

const orbitron = Orbitron({ subsets: ["latin"], variable: "--font-orbitron" });
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const ibmPlexMono = IBM_Plex_Mono({
  weight: ['400', '700'],
  subsets: ["latin"],
  variable: "--font-ibm-plex-mono"
});
const cinzel = Cinzel({ subsets: ["latin"], variable: "--font-cinzel" });

export const metadata: Metadata = {
  title: "Alsham Quantum | v13.3 Codex",
  description: "The First Self-Evolving Digital Organism - Reality Shifter Engine",
};



export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${orbitron.variable} ${inter.variable} ${ibmPlexMono.variable} ${cinzel.variable} font-sans overflow-hidden`}>
        <NextThemesProvider attribute="data-theme" defaultTheme="quantum" enableSystem={false}>
          <ThemeProvider>
            <AuthProvider>
              <GamificationProvider>
                <ToastProvider>
                  <div className="relative min-h-screen">
                    {/* Conditional Reality Background */}
                    <RealityBackground />

                    {/* Reality Glitch Transition Effect */}
                    <RealityGlitch />

                    {/* Conditional Scanlines (Military theme only) */}
                    <ConditionalScanlines />

                    {/* Theme Switcher */}
                    <ThemeSwitcher />

                    {/* Main Content */}
                    <div className="relative z-10">
                      {children}
                    </div>

                    {/* Orion Copilot */}
                    <OrionCopilot />
                  </div>
                </ToastProvider>
              </GamificationProvider>
            </AuthProvider>
          </ThemeProvider>
        </NextThemesProvider>
      </body>
    </html>
  );
}
