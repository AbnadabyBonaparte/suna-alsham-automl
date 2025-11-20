import Link from "next/link";
import ParticleField from "@/components/quantum/ParticleField";
import { Button } from "@/components/ui/button";
import { Activity, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden font-sans">
      <ParticleField />
      <div className="z-10 flex flex-col items-center text-center px-4 animate-in fade-in zoom-in duration-1000">
        
        <div className="mb-6 inline-flex items-center rounded-full border border-[#F4D03F]/30 bg-[#F4D03F]/10 px-3 py-1 text-xs font-medium text-[#F4D03F] backdrop-blur-md">
          <span className="mr-2 flex h-1.5 w-1.5 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#F4D03F] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-[#F4D03F]"></span>
          </span>
          SISTEMA ONLINE • v11.0 ENTERPRISE
        </div>

        <h1 className="text-5xl md:text-8xl font-bold tracking-tighter text-white mb-6 text-glow">
          ALSHAM <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#6C3483] to-[#F4D03F]">QUANTUM</span>
        </h1>

        <p className="max-w-[600px] text-lg text-gray-400 mb-8 leading-relaxed">
          O Primeiro Organismo Digital Auto-Evolutivo.
          <br/>
          <span className="text-white">57 Agentes Reais. ROI de 2.847%.</span>
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Link href="/dashboard">
            <Button className="bg-[#F4D03F] text-[#020C1B] hover:bg-[#F4D03F]/80 text-lg px-8 py-6 font-bold shadow-[0_0_20px_rgba(244,208,63,0.3)] transition-all hover:scale-105">
              ACESSAR COCKPIT
            </Button>
          </Link>
          <Button variant="outline" className="border-[#6C3483] text-[#6C3483] hover:bg-[#6C3483]/10 text-lg px-8 py-6 backdrop-blur-sm bg-black/40">
            DOCUMENTAÇÃO
          </Button>
        </div>

        <div className="mt-16 grid grid-cols-3 gap-8 text-gray-500 text-sm glass-panel p-6 rounded-xl w-full max-w-2xl border-t border-white/10">
          <div className="flex flex-col items-center gap-2">
            <Activity className="h-5 w-5 text-[#2ECC71]" />
            <span className="font-mono font-bold text-white">R$ 4.7B</span>
            <span className="text-xs">ECONOMIA</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Zap className="h-5 w-5 text-[#F4D03F]" />
            <span className="font-mono font-bold text-white">99.98%</span>
            <span className="text-xs">UPTIME</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-[#6C3483]" />
            <span className="font-mono font-bold text-white">57</span>
            <span className="text-xs">AGENTES</span>
          </div>
        </div>
      </div>
    </main>
  );
}
