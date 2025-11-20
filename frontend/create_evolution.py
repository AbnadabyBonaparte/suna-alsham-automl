import os

# 1. COMPONENTE DE TIMELINE
timeline_component = """
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
"""

# 2. PÁGINA PRINCIPAL
page_code = """
"use client";

import EvolutionTimeline from "@/components/quantum/EvolutionTimeline";
import { Dna, TrendingUp, Zap } from "lucide-react";
import { Card } from "@/components/ui/card";

export default function EvolutionPage() {
  return (
    <div className="p-8 space-y-8 min-h-screen bg-black/50">
      
      <div className="flex flex-col md:flex-row justify-between items-end gap-4 border-b border-white/10 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <Dna className="h-8 w-8 text-purple-500" />
            Evolution Lab
          </h1>
          <p className="text-zinc-400 mt-2 font-mono text-sm">
            Rastreamento Genético e Roadmap de Singularidade
          </p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full">
            <Zap className="w-4 h-4 text-purple-400" />
            <span className="text-xs text-purple-200 font-mono">EVOLUTION RATE: 1.4x / CYCLE</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
            <EvolutionTimeline />
        </div>

        <div className="space-y-6">
            <Card className="bg-zinc-900/30 border-white/10 p-6">
                <h3 className="text-sm font-bold text-zinc-300 mb-4 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" />
                    PROJEÇÃO DE CAPACIDADE
                </h3>
                <div className="space-y-6">
                    <div>
                        <div className="flex justify-between text-xs mb-2">
                            <span className="text-zinc-500">Capacidade Cognitiva</span>
                            <span className="text-blue-400">84 TFLOPS</span>
                        </div>
                        <div className="w-full bg-black h-1 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-500 w-[75%]"></div>
                        </div>
                    </div>
                    <div>
                        <div className="flex justify-between text-xs mb-2">
                            <span className="text-zinc-500">Autonomia de Código</span>
                            <span className="text-purple-400">Lvl 3 (Semi-Autônomo)</span>
                        </div>
                        <div className="w-full bg-black h-1 rounded-full overflow-hidden">
                            <div className="h-full bg-purple-500 w-[45%]"></div>
                        </div>
                    </div>
                </div>
            </Card>

            <div className="p-4 rounded-lg border border-dashed border-white/10 bg-white/5">
                <p className="text-xs text-zinc-500 font-mono text-center">
                    PRÓXIMA MUTAÇÃO PREVISTA:<br/>
                    <span className="text-white font-bold text-sm">AGENTE 58 (ORACLE)</span><br/>
                    EM 14:22:10
                </p>
            </div>
        </div>
      </div>
    </div>
  );
}
"""

# FUNÇÃO DE ESCRITA
def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Criado: {path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("🧬 Gerando arquivos de Evolution Lab...")
write_file("src/components/quantum/EvolutionTimeline.tsx", timeline_component)
write_file("src/app/dashboard/evolution/page.tsx", page_code)
print("🏁 Sequenciamento concluído.")
