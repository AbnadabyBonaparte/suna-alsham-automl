/** @type {import('next').NextConfig} */
const nextConfig = {
  // Garante que imagens externas funcionem
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  // Força a saída correta para o servidor Vercel
  distDir: '.next',
};

export default nextConfig;
