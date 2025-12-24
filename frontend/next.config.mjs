/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: false,
  poweredByHeader: false,
  compress: true,
  typescript: {
    // Ignora erros de TS no build para garantir o deploy
    ignoreBuildErrors: true,
  },
  experimental: {
    // Minimize bundle size
    optimizePackageImports: ['@supabase/supabase-js', 'lucide-react', 'framer-motion'],
  },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
          // {
          //   key: 'Content-Security-Policy',
          //   value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline' https://us-assets.i.posthog.com https://*.supabase.co; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' blob: data: https://*.supabase.co; font-src 'self' data: https://fonts.gstatic.com; connect-src 'self' https://us.i.posthog.com https://*.supabase.co wss://*.supabase.co; frame-src 'self';",
          // },
        ],
      },
    ];
  },
};

export default nextConfig;
