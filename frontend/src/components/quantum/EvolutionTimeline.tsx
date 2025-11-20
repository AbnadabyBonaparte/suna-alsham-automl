"use client";

import { CheckCircle2, Circle, Lock, ArrowDown } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const WAVES = [
  {
    id: 1,
    name: "ONDA 1: GÊNESE",
    status: "COMPLETED",
    date: "Q4 2025",
    desc: "Estabelecimento do Núcleo (Core, Guard, Learn). Validação científica inicial e primeiros 20 agentes.",
    roi: "+320%",
    color: "text-green-500",
    border: "border-green-500"
  },
  {
    id: 2,
    name: "ONDA 2: EXPANSÃO",
    status: "IN_PROGRESS",
    date: "CURRENT",
    desc: "Especialização Tática. Implementação de agentes de Vendas, Analytics e Infraestrutura. Integração total com Stripe.",
    roi: "+1.200% (Proj)",
    color: "text-blue-500",
    border: "border-blue-500"
  },
  {
    id: 3,
    name: "ONDA 3: SINGULARIDADE",
    status: "LOCKED",
    date: "Q2 2026",
    desc: "Transcendência. O sistema opera em clusters autônomos sem supervisão humana direta.",
    roi: "???",
    color: "text-purple-500",
    border: "border-zinc-800"
  }
];

export default function EvolutionTimeline() {
  return (
    <div className="space-y-8 relative">
      <div className="absolute left-[19px] top-8 bottom-8 w-0.5 bg-gradient-to-b from-green-500 via-blue-500 to-zinc-800 opacity-50" />

      {WAVES.map((wave, index) => (
        <div key={wave.id} className="relative pl-12 group">
          <div className={`absolute left-0 top-1 w-10 h-10 rounded-full bg-black border-2 flex items-center justify-center z-10 transition-all duration-500 ${
            wave.status === 'COMPLETED' ? 'border-green-500 shadow-[0_0_15px_rgba(34,197,94,0.3)]' :
            wave.status === 'IN_PROGRESS' ? 'border-blue-500 animate-pulse shadow-[0_0_20px_rgba(59,130,246,0.4)]' :
            'border-zinc-800 opacity-50'
          }`}>
            {wave.status === 'COMPLETED' ? <CheckCircle2 className="w-5 h-5 text-green-500" /> :
             wave.status === 'IN_PROGRESS' ? <div className="w-3 h-3 bg-blue-500 rounded-full animate-ping" /> :
             <Lock className="w-4 h-4 text-zinc-600" />}
          </div>

          <Card className={`bg-zinc-900/40 backdrop-blur-sm border p-6 transition-all duration-300 hover:bg-zinc-900/60 ${
             wave.status === 'LOCKED' ? 'border-white/5 opacity-60' : 'border-white/10 hover:border-white/20'
          }`}>
            <div className="flex justify-between items-start mb-2">
                <div>
                    <h3 className={`text-xl font-bold tracking-widest ${wave.color}`}>{wave.name}</h3>
                    <span className="text-xs font-mono text-zinc-500">{wave.date}</span>
                </div>
                <Badge variant="outline" className={`${wave.border} ${wave.color} bg-transparent`}>
                    ROI: {wave.roi}
                </Badge>
            </div>
            <p className="text-zinc-400 text-sm leading-relaxed mb-4">
                {wave.desc}
            </p>
            
            {wave.status !== 'LOCKED' && (
                <div className="w-full bg-black/50 h-1.5 rounded-full overflow-hidden">
                    <div 
                        className={`h-full ${wave.status === 'COMPLETED' ? 'bg-green-500' : 'bg-blue-500 animate-pulse'}`} 
                        style={{ width: wave.status === 'COMPLETED' ? '100%' : '42%' }}
                    />
                </div>
            )}
          </Card>
        </div>
      ))}
    </div>
  );
}