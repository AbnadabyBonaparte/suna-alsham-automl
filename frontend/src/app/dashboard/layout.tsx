import { Sidebar } from "@/components/layout/Sidebar";
import { GlobalKeyListener } from "@/components/layout/GlobalKeyListener";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-black w-full">
      {/* Listener Secreto */}
      <GlobalKeyListener />

      {/* Sidebar Fixa - Desktop */}
      <div className="hidden md:flex h-screen w-64 flex-col fixed left-0 top-0 z-50 border-r border-white/10 bg-black/90 backdrop-blur-xl">
        <Sidebar />
      </div>

      {/* Conteúdo Principal - Com Margem para Sidebar */}
      <main className="flex-1 md:pl-64 relative w-full">
        {children}
      </main>
    </div>
  );
}