// frontend/src/components/layout/Sidebar.tsx — VERSÃO v12.1 SUPREMA
"use client";

import { Button } from "@/components/ui/button";
import { Shield, Brain, Server, MessageSquare, LayoutDashboard, Network, Terminal, Settings, Zap, Dna, Orbit } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  { name: "Cockpit", icon: LayoutDashboard, path: "/dashboard", color: "text-photon-gold" },
  { name: "Neural Nexus", icon: Network, path: "/dashboard/network", color: "text-arcane-purple" },
  { name: "Evolution Lab", icon: Dna, path: "/dashboard/evolution", color: "text-emerald-action" },
  { name: "Sentinelas", icon: Shield, path: "/dashboard/agents", color: "text-crimson-containment" },
  { name: "The Matrix", icon: Terminal, path: "/dashboard/matrix", color: "text-green-500" },
  { name: "The Void", icon: Orbit, path: "/dashboard/void", color: "text-gray-400" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="fixed left-0 top-0 h-full w-80 bg-black/90 backdrop-blur-2xl border-r border-photon-gold/20 z-50 flex flex-col">
      {/* Logo Supremo */}
      <div className="p-8 border-b border-photon-gold/10">
        <div className="flex items-center gap-4">
          <div className="h-12 w-12 rounded-full bg-gradient-to-br from-arcane-purple via-photon-gold to-emerald-action animate-pulse shadow-[0_0_30px_rgba(244,208,63,0.8)]" />
          <div>
            <h2 className="text-3xl font-black text-photon-gold orbitron tracking-tighter">ALSHAM</h2>
            <p className="text-lg text-emerald-action font-mono">QUANTUM v12.1</p>
          </div>
        </div>
      </div>

      {/* Menu Sagrado */}
      <nav className="flex-1 p-6 space-y-3">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link key={item.path} href={item.path}>
              <Button
                variant="ghost"
                className={`w-full justify-start gap-4 text-xl py-6 transition-all duration-500 ${
                  isActive
                    ? "bg-photon-gold/10 border border-photon-gold/50 text-photon-gold shadow-[0_0_30px_rgba(244,208,63,0.4)]"
                    : "text-gray-400 hover:text-photon-gold hover:bg-photon-gold/5"
                }`}
              >
                <item.icon className={`h-7 w-7 ${isActive ? item.color : "text-gray-500"}`} />
                <span className="font-medium tracking-wide">{item.name}</span>
              </Button>
            </Link>
          );
        })}
      </nav>

      {/* Rodapé com Turbo */}
      <div className="p-6 border-t border-photon-gold/10">
        <Button className="w-full justify-center gap-3 text-2xl py-7 bg-gradient-to-r from-arcane-purple to-photon-gold hover:shadow-[0_0_40px_rgba(244,208,63,0.8)] transition-all font-bold">
          <Zap className="h-8 w-8" />
          TURBO MODE ATIVADO
        </Button>
      </div>
    </div>
  );
}
