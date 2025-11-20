import os

# 1. CONFIGURAÇÃO DO TAILWIND (Garantir que ele veja os arquivos)
tailwind_config = """
import type { Config } from "next";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
};
export default config;
"""

# 2. CSS GLOBAL (Cores e Reset)
global_css = """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 263.4 70% 50.4%;
    --primary-foreground: 210 40% 98%;
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
    --radius: 0.5rem;
  }
}

@layer base {
  * {
    border-color: hsl(var(--border));
  }
  body {
    background-color: #000000;
    color: #ffffff;
  }
}
"""

# 3. LAYOUT DO DASHBOARD (Forçar Sidebar)
dashboard_layout = """
import { Sidebar } from "@/components/layout/Sidebar";
import { GlobalKeyListener } from "@/components/layout/GlobalKeyListener";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-black w-full">
      {/* Listener Secreto */}
      <GlobalKeyListener />

      {/* Sidebar Fixa - Desktop */}
      <div className="hidden md:flex h-screen w-64 flex-col fixed left-0 top-0 z-50 border-r border-white/10 bg-black/90 backdrop-blur-xl">
        <Sidebar />
      </div>

      {/* Conteúdo Principal - Com Margem para Sidebar */}
      <main className="flex-1 md:pl-64 relative w-full">
        {children}
      </main>
    </div>
  );
}
"""

# 4. SIDEBAR (Menu)
sidebar_component = """
"use client";

import { Button } from "@/components/ui/button";
import { Shield, Brain, Server, MessageSquare, LayoutDashboard, Network, Terminal, Settings, Zap, Dna } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  { name: "Cockpit", icon: LayoutDashboard, path: "/dashboard", color: "text-white" },
  { name: "Neural Nexus", icon: Network, path: "/dashboard/network", color: "text-pink-500" },
  { name: "Evolution Lab", icon: Dna, path: "/dashboard/evolution", color: "text-purple-500" },
  { name: "Sentinelas", icon: Shield, path: "/dashboard/agents", color: "text-red-400" },
  { name: "Matrix / Logs", icon: Terminal, path: "/dashboard/matrix", color: "text-green-500" },
  { name: "Inteligência", icon: Brain, path: "/dashboard/intelligence", color: "text-blue-400" },
  { name: "Infraestrutura", icon: Server, path: "/dashboard/infrastructure", color: "text-green-400" },
  { name: "Comunicação", icon: MessageSquare, path: "/dashboard/communication", color: "text-purple-400" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex flex-col h-full p-4">
      <div className="mb-8 flex items-center gap-3 px-2 pt-2">
        <div className="h-8 w-8 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 animate-pulse shadow-[0_0_15px_rgba(168,85,247,0.5)]" />
        <div>
            <h2 className="font-bold text-white tracking-wider">ALSHAM</h2>
            <p className="text-[10px] text-white/50 tracking-[0.2em]">QUANTUM v11</p>
        </div>
      </div>

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

      <div className="mt-auto space-y-2 pt-4 border-t border-white/10">
         <Button variant="outline" className="w-full justify-start gap-2 border-purple-500/30 text-purple-400 hover:bg-purple-500/10 hover:text-purple-200 transition-colors">
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
"""

# 5. DASHBOARD PAGE (Grid Corrigido)
dashboard_page = """
"use client";

import { useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Activity, Shield, Zap, Database, Terminal, Cpu } from "lucide-react";
import { useQuantumStore } from "@/lib/store";

export default function DashboardPage() {
  const { agents, metrics, isLive, simulatePulse, toggleLiveMode } = useQuantumStore();

  useEffect(() => {
    const interval = setInterval(() => simulatePulse(), 2000); 
    return () => clearInterval(interval);
  }, [simulatePulse]);

  return (
    <div className="p-8 space-y-8 w-full max-w-[1600px] mx-auto">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/10 pb-6 bg-black/20 backdrop-blur-sm sticky top-0 z-40">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-fuchsia-300 to-white tracking-tight">
            Cockpit de Deus
          </h1>
          <p className="text-zinc-400 mt-1 font-light tracking-wide flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            ALSHAM QUANTUM v11.0 <span className="text-zinc-600">|</span> Operacional
          </p>
        </div>
        <div className="flex gap-3">
          <Button 
            variant="outline" 
            className={`border-purple-500/30 bg-purple-500/10 hover:bg-purple-500/20 transition-all ${isLive ? 'text-green-400 border-green-500/30' : 'text-gray-400'}`}
            onClick={toggleLiveMode}
          >
            <Activity className="mr-2 h-4 w-4" />
            {isLive ? "LIVE STREAM" : "PAUSED"}
          </Button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard title="ROI Total" value={`${metrics.roi}%`} sub="+12% hoje" icon={Activity} color="text-purple-400" />
        <KpiCard title="Economia" value={`R$ ${metrics.savings}B`} sub="Acumulado Global" icon={Database} color="text-green-400" />
        <KpiCard title="Carga Neural" value={`${metrics.systemLoad.toFixed(1)}%`} sub="Capacidade de CPU" icon={Cpu} color="text-amber-400" />
        <KpiCard title="Agentes" value={metrics.activeAgents.toString()} sub="Rede Ativa" icon={Shield} color="text-blue-400" />
      </div>

      {/* Agents Grid */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <Terminal className="h-6 w-6 text-purple-500" />
            Rede Neural Ativa
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <Card 
              key={agent.id} 
              className="bg-zinc-900/40 border-white/5 backdrop-blur-sm hover:border-purple-500/50 hover:bg-zinc-900/60 transition-all duration-300 group"
            >
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <div className="space-y-1">
                  <CardTitle className="text-sm font-medium text-zinc-200 group-hover:text-purple-300 transition-colors">
                    {agent.name}
                  </CardTitle>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-wider">{agent.role}</p>
                </div>
                <StatusBadge status={agent.status} />
              </CardHeader>
              <CardContent>
                <div className="flex items-end justify-between mb-2">
                   <div className="text-2xl font-bold text-white">
                     {agent.efficiency.toFixed(1)}%
                   </div>
                   <span className="text-xs text-zinc-500 mb-1">Eficiência</span>
                </div>
                
                <div className="w-full bg-black/50 h-1.5 rounded-full overflow-hidden">
                    <div 
                        className={`h-full transition-all duration-1000 ease-in-out ${getBarColor(agent.efficiency)}`}
                        style={{ width: `${agent.efficiency}%` }}
                    />
                </div>
                
                <div className="mt-4 flex items-center gap-2 text-xs text-zinc-400 bg-black/20 p-2 rounded border border-white/5">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-500/50"></span>
                  <span className="truncate font-mono text-purple-200/70">{agent.currentTask}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

function KpiCard({ title, value, sub, icon: Icon, color }: any) {
  return (
    <Card className="bg-zinc-900/40 border-white/5 backdrop-blur-sm">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-zinc-400">{title}</CardTitle>
        <Icon className={`h-4 w-4 ${color}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-white">{value}</div>
        <p className="text-xs text-zinc-500 mt-1">{sub}</p>
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: string }) {
    const colors: Record<string, string> = {
        IDLE: "bg-zinc-500/10 text-zinc-400 border-zinc-500/20",
        PROCESSING: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse",
        LEARNING: "bg-purple-500/10 text-purple-400 border-purple-500/20",
        WARNING: "bg-amber-500/10 text-amber-400 border-amber-500/20",
        ERROR: "bg-red-500/10 text-red-400 border-red-500/20",
    };
    return (
        <Badge variant="outline" className={`${colors[status] || colors.IDLE} border font-mono text-[10px] uppercase`}>
            {status}
        </Badge>
    );
}

function getBarColor(efficiency: number) {
  if (efficiency > 90) return "bg-gradient-to-r from-purple-500 to-blue-500";
  if (efficiency > 70) return "bg-blue-500";
  return "bg-amber-500";
}
"""

def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Restaurado: {path}")
    except Exception as e:
        print(f"❌ Erro em {path}: {e}")

print("🏥 Iniciando Cirurgia Plástica no Frontend...")
write_file("tailwind.config.ts", tailwind_config)
write_file("src/app/globals.css", global_css)
write_file("src/app/dashboard/layout.tsx", dashboard_layout)
write_file("src/components/layout/Sidebar.tsx", sidebar_component)
write_file("src/app/dashboard/page.tsx", dashboard_page)
print("🏁 Procedimento concluído com sucesso.")
