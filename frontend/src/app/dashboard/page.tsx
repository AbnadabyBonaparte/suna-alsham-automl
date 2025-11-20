// src/app/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Activity, Shield, Zap, Database, Terminal, Cpu, PauseOctagon } from "lucide-react";
import { useQuantumStore } from "@/lib/store";
import { toggleSystemMode } from "@/lib/actions";
import { useSfx } from "@/hooks/use-sfx";

export default function DashboardPage() {
  const { agents, metrics, isLive, simulatePulse, toggleLiveMode } = useQuantumStore();
  const { play } = useSfx();
  const [isPending, setIsPending] = useState(false);
  const [panicMode, setPanicMode] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => simulatePulse(), 2000);
    return () => clearInterval(interval);
  }, [simulatePulse]);

  const handleCommand = async (mode: 'TURBO' | 'STOP') => {
    setIsPending(true);
    play(mode === 'STOP' ? 'alert' : 'click');

    if (mode === 'STOP') {
      // ==== JUÍZO FINAL ATIVADO ====
      setPanicMode(true);
      play('alert');

      // Alarme de submarino contínuo por 12 segundos
      const submarineAlarm = setInterval(() => play('alert'), 900);
      
      setTimeout(() => {
        clearInterval(submarineAlarm);
        setPanicMode(false);
      }, 12000);
    }

    try {
      const result = await toggleSystemMode(mode);
      if (result.success) play('ambient');
    } catch (error) {
      console.error("Erro crítico:", error);
      play('alert');
    } finally {
      setIsPending(false);
    }
  };

  return (
    <>
      <div className={`p-8 space-y-8 w-full max-w-[1600px] mx-auto transition-all duration-500 ${panicMode ? 'blur-sm' : ''}`}>
        {/* Header + Botões */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/10 pb-6 bg-black/20 backdrop-blur-sm sticky top-0 z-40">
          <div>
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-fuchsia-300 to-white tracking-tight">
              Cockpit de Deus
            </h1>
            <p className="text-zinc-400 mt-1 font-light tracking-wide flex items-center gap-2">
              <span className={`inline-block w-2 h-2 rounded-full ${isLive ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
              ALSHAM QUANTUM v12.0 <span className="text-zinc-600">|</span> Operacional
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              disabled={isPending || panicMode}
              onClick={() => handleCommand('TURBO')}
              className="bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30"
            >
              <Zap className="mr-2 h-4 w-4" /> TURBO MODE
            </Button>

            <Button
              variant="destructive"
              disabled={isPending || panicMode}
              onClick={() => handleCommand('STOP')}
              className="bg-red-900/20 hover:bg-red-900/40 text-red-400 border border-red-500/30 font-bold relative overflow-hidden"
            >
              <span className="relative z-10 flex items-center">
                <PauseOctagon className="mr-2 h-4 w-4" /> CONTAINMENT
              </span>
              {panicMode && (
                <div className="absolute inset-0 bg-red-600 animate-ping opacity-75"></div>
              )}
            </Button>

            <Button
              variant="outline"
              onClick={() => { play('click'); toggleLiveMode(); }}
              className={`border-purple-500/30 bg-purple-500/10 hover:bg-purple-500/20 ${isLive ? 'text-green-400 border-green-500/30' : 'text-gray-400'}`}
            >
              <Activity className="mr-2 h-4 w-4" />
              {isLive ? "LIVE STREAM" : "PAUSED"}
            </Button>
          </div>
        </div>

        {/* KPI Grid + Agents Grid (seu código antigo continua aqui embaixo, sem alteração) */}
        {/* ... todo o resto do seu dashboard que já estava perfeito ... */}
        {/* Cole aqui tudo que já tinha abaixo do header (KPI, Agents Grid, etc.) */}
        {/* Eu não repeti pra não ficar gigante, mas você mantém exatamente como está */}

      </div>

      {/* ==== OVERLAY DO JUÍZO FINAL ==== */}
      {panicMode && (
        <div className="fixed inset-0 bg-red-900/98 z-[99999] flex items-center justify-center pointer-events-none">
          <div className="text-center animate-pulse">
            <h1 className="text-8xl md:text-9xl font-black text-red-500 drop-shadow-[0_0_80px_red] tracking-tighter">
              CONTAINMENT
            </h1>
            <h2 className="text-6xl md:text-8xl font-black text-red-300 mt-4 drop-shadow-[0_0_60px_red]">
              PROTOCOL ACTIVATED
            </h2>
            <p className="text-2xl text-red-200 mt-12 font-mono tracking-widest">
              ALL SYSTEMS FROZEN • 57 AGENTS CONTAINED
            </p>
          </div>
        </div>
      )}
    </>
  );
}

// Mantenha todas as funções KpiCard, StatusBadge, getBarColor no final do arquivo exatamente como estavam
