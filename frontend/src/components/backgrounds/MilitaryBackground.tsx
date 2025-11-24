'use client';
export default function MilitaryBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#020604]">
      {/* Grid Radar */}
      <div 
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: `linear-gradient(0deg, transparent 24%, #10B981 25%, #10B981 26%, transparent 27%, transparent 74%, #10B981 75%, #10B981 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, #10B981 25%, #10B981 26%, transparent 27%, transparent 74%, #10B981 75%, #10B981 76%, transparent 77%, transparent)`,
          backgroundSize: '50px 50px'
        }}
      />
      {/* Scanline Radar */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#10B981]/10 to-transparent w-full h-[20%] animate-scanline" />
      <style jsx>{`
        @keyframes scanline {
          0% { top: -20%; }
          100% { top: 120%; }
        }
        .animate-scanline { animation: scanline 3s linear infinite; }
      `}</style>
    </div>
  );
}
