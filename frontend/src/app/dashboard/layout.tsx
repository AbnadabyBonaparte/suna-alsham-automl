"use client";

import Sidebar from "@/components/layout/Sidebar";
import MobileMenu from "@/components/layout/MobileMenu";
import SkipToContent from "@/components/layout/SkipToContent";
import ErrorBoundary from "@/components/ErrorBoundary";
import { GlobalKeyListener } from "@/components/layout/GlobalKeyListener";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ErrorBoundary>
      <SkipToContent />
      <div className="flex h-screen overflow-hidden bg-[#020C1B]">
        {/* Listener Secreto */}
        <GlobalKeyListener />

        {/* Sidebar - Always visible on desktop */}
        <Sidebar />

        {/* Mobile Menu */}
        <MobileMenu />

        {/* Main Content Area - Scrollable */}
        <main id="main-content" className="flex-1 overflow-y-auto overflow-x-hidden relative">
          {children}
        </main>
      </div>
    </ErrorBoundary>
  );
}
