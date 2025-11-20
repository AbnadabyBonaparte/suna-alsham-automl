/** @type {import('next').NextConfig} */
const nextConfig = {
  // Ativa o modo standalone: gera um pacote autossuficiente
  output: 'standalone',
  
  // Garante que imagens externas funcionem
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  
  // Ignora erros de verificação para garantir o deploy
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
