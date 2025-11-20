import os

layout_code = """
import { Sidebar } from "@/components/layout/Sidebar";
import { GlobalKeyListener } from "@/components/layout/GlobalKeyListener";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-black">
      {/* O Ouvido do Sistema (Easter Egg) */}
      <GlobalKeyListener />

      {/* Sidebar Fixa */}
      <div className="fixed inset-y-0 z-50 w-64 hidden md:flex flex-col">
        <Sidebar />
      </div>

      {/* Conteúdo Principal */}
      <main className="flex-1 md:pl-64 relative overflow-y-auto h-screen">
        {children}
      </main>
    </div>
  );
}
"""

def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Arquivo RECRIADO com sucesso: {path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("🛠️ Reparando Layout do Dashboard...")
write_file("src/app/dashboard/layout.tsx", layout_code)
