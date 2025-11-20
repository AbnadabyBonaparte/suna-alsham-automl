// frontend/src/app/_not-found/page.tsx — MATA O ERRO DO BUILD PRA SEMPRE
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center text-white">
      <div className="text-center">
        <h1 className="text-9xl font-black text-photon-gold orbitron">404</h1>
        <p className="text-4xl mt-8 text-gray-400">Página não encontrada no vazio quântico</p>
        <Link href="/dashboard" className="mt-12 inline-block px-12 py-6 bg-photon-gold/20 border border-photon-gold text-photon-gold text-2xl rounded-2xl hover:bg-photon-gold/40 transition-all">
          Voltar ao Cockpit
        </Link>
      </div>
    </div>
  );
}
