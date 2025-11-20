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