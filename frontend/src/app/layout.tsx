import type { Metadata } from "next";
import { Orbitron, Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";

const orbitron = Orbitron({ subsets: ["latin"], variable: "--font-orbitron", display: "swap" });
const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });

export const metadata: Metadata = {
  title: "ALSHAM QUANTUM v12.1",
  description: "Cockpit de Inteligência Suprema",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-br" className={`${orbitron.variable} ${inter.variable} dark`}>
      <body className="bg-[#020C1B] text-white antialiased h-screen w-screen overflow-hidden flex">
        <aside className="flex-shrink-0 z-50 hidden md:block">
          <Sidebar />
        </aside>
        <main className="flex-1 relative h-full overflow-y-auto overflow-x-hidden bg-[url('/grid.svg')]">
          {children}
        </main>
      </body>
    </html>
  );
}
