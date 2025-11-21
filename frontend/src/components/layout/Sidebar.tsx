"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const menuItems = [
    { name: "COCKPIT", path: "/dashboard", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" },
    { name: "SENTINELAS", path: "/dashboard/agents", icon: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" },
    { name: "NEXUS 3D", path: "/dashboard/network", icon: "M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" },
    { name: "MATRIX", path: "/dashboard/matrix", icon: "M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" },
    { name: "EVOLUTION", path: "/dashboard/evolution", icon: "M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" },
    { name: "THE VOID", path: "/dashboard/void", icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" },
  ];

  return (
    <div className="h-screen w-64 bg-[#020C1B] border-r border-[#1F618D]/30 flex flex-col z-50 shadow-[4px_0_24px_rgba(0,0,0,0.5)]">
      {/* Logo */}
      <div className="p-6 border-b border-[#1F618D]/20">
        <h1 className="text-2xl font-bold tracking-tighter text-white orbitron">
          ALSHAM <span className="text-[#F4D03F]">Q</span>
        </h1>
        <p className="text-[10px] text-[#1F618D] mt-1 tracking-[0.2em]">SYSTEM v12.1</p>
      </div>

      {/* Menu */}
      <nav className="flex-1 py-6 space-y-2 overflow-y-auto">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.path}
              href={item.path}
              className={`relative flex items-center px-6 py-3 transition-all duration-300 group ${
                isActive 
                  ? "bg-[#6C3483]/20 text-[#F4D03F] border-r-4 border-[#F4D03F]" 
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <svg 
                className={`w-5 h-5 mr-3 transition-transform duration-300 ${isActive ? "scale-110 shadow-glow" : "group-hover:scale-110"}`} 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
              </svg>
              <span className="text-sm font-bold tracking-wider orbitron">{item.name}</span>
              
              {/* Glow Effect on Active */}
              {isActive && (
                <div className="absolute inset-0 bg-[#F4D03F] opacity-5 blur-md"></div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-[#1F618D]/20">
        <div className="flex items-center space-x-3">
          <div className="w-2 h-2 bg-[#2ECC71] rounded-full animate-pulse shadow-[0_0_10px_#2ECC71]"></div>
          <span className="text-xs font-mono text-[#2ECC71]">SYSTEM ONLINE</span>
        </div>
      </div>
    </div>
  );
}
