'use client';
export default function TitaniumBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 bg-[#020617]">
      {/* Textura de Couro Sutil */}
      <div className="absolute inset-0 opacity-10 bg-[url('/grid.svg')] mix-blend-overlay" />
      {/* Glow Dourado de Luxo */}
      <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-[#D4AF37] rounded-full blur-[120px] opacity-10" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[600px] h-[600px] bg-[#1E293B] rounded-full blur-[100px] opacity-20" />
    </div>
  );
}
