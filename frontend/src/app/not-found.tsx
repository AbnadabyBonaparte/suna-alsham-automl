// frontend/src/app/not-found.tsx
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#020C1B] text-white">
      <h1 className="text-9xl font-bold text-[#F4D03F] mb-4 animate-pulse">
        404
      </h1>
      <h2 className="text-2xl font-mono text-[#1F618D] mb-8 uppercase tracking-widest">
        Anomalia Quântica // Página Inexistente
      </h2>
      <p className="text-gray-400 max-w-md text-center mb-12">
        A rota que você tentou acessar colapsou no vazio.
      </p>
      <Link 
        href="/dashboard" 
        className="px-8 py-4 bg-[#6C3483] hover:bg-[#5B2C6F] text-white font-bold rounded shadow-[0_0_20px_rgba(108,52,131,0.5)] transition-all"
      >
        RETORNAR AO COCKPIT
      </Link>
    </div>
  );
}
