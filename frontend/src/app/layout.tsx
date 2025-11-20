import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ALSHAM QUANTUM v12.1",
  description: "Cockpit de Inteligência Suprema",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-br" className="dark">
      <body className="bg-[#020C1B] text-white antialiased min-h-screen overflow-x-hidden selection:bg-[#F4D03F] selection:text-black">
        {/* Layout Simplificado para Garantir o Build */}
        <main className="relative w-full h-full">
          {children}
        </main>
      </body>
    </html>
  );
}
