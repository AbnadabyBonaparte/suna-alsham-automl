"use client";

import { Button } from "@/components/ui/button";
import { Shield, Brain, Server, MessageSquare, LayoutDashboard, Settings, Zap } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  { name: "Cockpit", icon: LayoutDashboard, path: "/dashboard", color: "text-white" },
  { name: "Sentinelas", icon: Shield, path: "/dashboard/sentinels", color: "text-red-400" },
  { name: "Inteligência", icon: Brain, path: "/dashboard/intelligence", color: "text-blue-400" },
  { name: "Infraestrutura", icon: Server, path: "/dashboard/infrastructure", color: "text-green-400" },
  { name: "Comunicação", icon: MessageSquare, path: "/dashboard/communication", color: "text-purple-400" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="h-screen w-64 bg-black/90 border-r border-white/10 flex flex-col p-4 fixed left-0 top-0 backdrop-blur-xl z-50">
      {/* Logo Area */}
      <div className="mb-8 flex items-center gap-3 px-2">
        <div className="h-8 w-8 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 animate-pulse" />
        <div>
            <h2 className="font-bold text-white tracking-wider">ALSHAM</h2>
            <p className="text-[10px] text-white/50 tracking-[0.2em]">QUANTUM v11</p>
        </div>
      </div>

      {/* Menu Items */}
      <nav className="space-y-2 flex-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link key={item.path} href={item.path}>
              <Button
                variant="ghost"
                className={`w-full justify-start gap-3 mb-1 transition-all duration-300 ${
                  isActive 
                    ? "bg-white/10 border border-white/5 text-white shadow-[0_0_15px_rgba(255,255,255,0.1)]" 
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <item.icon className={`h-4 w-4 ${isActive ? item.color : "text-gray-500"}`} />
                <span className="font-light tracking-wide">{item.name}</span>
              </Button>
            </Link>
          );
        })}
      </nav>

      {/* Footer Actions */}
      <div className="mt-auto space-y-2 pt-4 border-t border-white/10">
         <Button variant="outline" className="w-full justify-start gap-2 border-purple-500/30 text-purple-400 hover:bg-purple-500/10">
            <Zap className="h-4 w-4" />
            Turbo Mode
         </Button>
         <Button variant="ghost" className="w-full justify-start gap-2 text-gray-500 hover:text-white">
            <Settings className="h-4 w-4" />
            Settings
         </Button>
      </div>
    </div>
  );
}
