import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-black text-white">
      <h1 className="text-6xl font-bold text-yellow-500">404</h1>
      <p className="mt-4 text-xl">Página não encontrada no Vazio.</p>
      <Link href="/" className="mt-8 px-6 py-3 bg-purple-600 rounded hover:bg-purple-700">
        Voltar ao Início
      </Link>
    </div>
  );
}
