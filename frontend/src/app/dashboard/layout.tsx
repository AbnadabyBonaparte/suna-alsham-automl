import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-black text-white flex">
      <Sidebar />
      <main className="flex-1 ml-64 relative z-0">
        {children}
      </main>
    </div>
  );
}
