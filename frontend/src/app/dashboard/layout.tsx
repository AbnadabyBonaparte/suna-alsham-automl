import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-black">
      {/* Sidebar Fixa */}
      <div className="fixed inset-y-0 z-50 w-64 hidden md:flex flex-col">
        <Sidebar />
      </div>

      {/* Conteúdo Principal (com margem para não ficar embaixo da sidebar) */}
      <main className="flex-1 md:pl-64 relative overflow-y-auto h-screen">
        {children}
      </main>
    </div>
  );
}
