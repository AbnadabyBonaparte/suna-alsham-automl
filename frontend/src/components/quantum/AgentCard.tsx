"use client";

import React from "react";

interface AgentProps {
  name: string;
  role: string;
  status: "active" | "idle" | "warning";
  efficiency: number;
}

export default function AgentCard({ name, role, status, efficiency }: AgentProps) {
  // Define cores baseadas no status sem usar bibliotecas externas
  const statusColor = 
    status === "active" ? "bg-[#2ECC71]" : 
    status === "warning" ? "bg-[#E74C3C]" : "bg-[#F4D03F]";

  return (
    <div className="relative group bg-[#020C1B]/80 border border-[#1F618D]/30 p-6 rounded-lg overflow-hidden transition-all duration-300 hover:border-[#F4D03F] hover:shadow-[0_0_20px_rgba(244,208,63,0.2)]">
      
      {/* Header do Card */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-bold text-white tracking-wider orbitron">{name}</h3>
          <p className="text-xs text-[#1F618D] uppercase font-mono mt-1">{role}</p>
        </div>
        <div className={`w-3 h-3 rounded-full ${statusColor} shadow-[0_0_10px_currentColor] animate-pulse`} />
      </div>

      {/* Barra de Eficiência */}
      <div className="mt-4">
        <div className="flex justify-between text-xs font-mono text-gray-400 mb-1">
          <span>EFICIÊNCIA</span>
          <span className="text-white">{efficiency}%</span>
        </div>
        <div className="w-full h-1 bg-[#1F618D]/20 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-[#6C3483] to-[#F4D03F]" 
            style={{ width: `${efficiency}%` }}
          />
        </div>
      </div>

      {/* Grid Decorativo (CSS Puro) */}
      <div className="absolute bottom-0 right-0 p-2 opacity-10">
        <div className="grid grid-cols-3 gap-1">
          {[...Array(9)].map((_, i) => (
            <div key={i} className="w-1 h-1 bg-white rounded-full" />
          ))}
        </div>
      </div>
    </div>
  );
}
