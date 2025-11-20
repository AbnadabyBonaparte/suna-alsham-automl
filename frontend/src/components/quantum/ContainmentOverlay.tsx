// src/components/quantum/ContainmentOverlay.tsx
interface Props {
  active: boolean;
}

export default function ContainmentOverlay({ active }: Props) {
  if (!active) return null;

  return (
    <div className="fixed inset-0 bg-red-900/98 z-[99999] flex items-center justify-center pointer-events-none">
      <div className="text-center animate-pulse">
        <h1 className="text-9xl font-black text-red-500 drop-shadow-[0_0_100px_red] tracking-tighter orbitron">
          CONTAINMENT
        </h1>
        <h2 className="text-7xl font-black text-red-300 mt-8 drop-shadow-[0_0_80px_red]">
          PROTOCOL ACTIVATED
        </h2>
        <p className="text-3xl text-red-200 mt-16 font-mono tracking-widest">
          ALL SYSTEMS FROZEN • 57 AGENTS CONTAINED
        </p>
      </div>
    </div>
  );
}
