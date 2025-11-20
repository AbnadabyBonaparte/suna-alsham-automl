// frontend/src/app/not-found/page.tsx — MATA O ERRO DO BUILD PRA SEMPRE
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center text-white">
      <h1 className="text-9xl font-black text-yellow-500 orbitron mb-8 animate-pulse">
        404
      </h1>
      <p className="text-4xl text-gray-400 mb-12 font-mono">
        Página perdida no vazio quântico
      </p>
      <Link 
        href="/dashboard" 
        className="px-16 py-8 bg-gradient-to-r from-purple-600 to-yellow-500 text-black text-3xl font-black rounded-2xl hover:scale-110 transition-all shadow-[0_0_50px_rgba(244,208,63,0.6)]"
      >
        VOLTAR AO COCKPIT
      </Link>
    </div>
  );
}
