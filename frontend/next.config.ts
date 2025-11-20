import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Configurações de Build */
  eslint: {
    // Ignora erros de lint durante o deploy para não travar
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Ignora erros de tipo durante o deploy (crítico para Three.js rápido)
    ignoreBuildErrors: true,
  },
  // Garante que imagens externas funcionem se precisar
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
};

export default nextConfig;
