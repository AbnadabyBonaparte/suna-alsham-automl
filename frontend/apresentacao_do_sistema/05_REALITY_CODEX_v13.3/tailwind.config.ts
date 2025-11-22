import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                core: 'var(--bg-core)',
                panel: 'var(--bg-panel)',
                primary: 'var(--text-primary)',
                accent: 'var(--accent)',
                'accent-secondary': 'var(--accent-secondary)',
                border: 'var(--border)',
            },
            borderRadius: {
                theme: 'var(--radius)',
            },
            borderWidth: {
                theme: 'var(--border-width)',
            },
            boxShadow: {
                glow: 'var(--effect-glow)',
            },
            backdropBlur: {
                theme: 'var(--backdrop-blur)',
            },
            fontFamily: {
                display: ['var(--font-display)', 'sans-serif'],
                orbitron: ['var(--font-orbitron)', 'sans-serif'],
                mono: ['var(--font-ibm-plex-mono)', 'monospace'],
                serif: ['var(--font-cinzel)', 'serif'],
                sans: ['var(--font-inter)', 'sans-serif'],
            },
            backgroundImage: {
                "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
                "gradient-conic":
                    "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
            },
            animation: {
                'god-ray': 'god-ray 8s ease-in-out infinite',
            },
        },
    },
    plugins: [],
};
export default config;
