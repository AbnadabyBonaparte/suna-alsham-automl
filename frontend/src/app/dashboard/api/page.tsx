/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - API PLAYGROUND (QUANTUM GATE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/api/page.tsx
 * 📋 Console de testes de API com efeitos de fluxo de dados
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { 
    Play, Code, Copy, Check, Server, 
    Globe, Shield, Zap, Database, RefreshCw 
} from 'lucide-react';

const METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];

const ENDPOINTS = [
    { label: 'List Agents', path: '/v1/agents', method: 'GET' },
    { label: 'Create Simulation', path: '/v1/simulations', method: 'POST' },
    { label: 'Neural Health', path: '/v1/neural/status', method: 'GET' },
    { label: 'Purge Memory', path: '/v1/core/purge', method: 'DELETE' },
    { label: 'User Auth', path: '/v1/auth/login', method: 'POST' },
];

export default function ApiPage() {
    // States
    const [method, setMethod] = useState('GET');
    const [url, setUrl] = useState('https://api.alsham.quantum/v1/agents');
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState<string | null>(null);
    const [status, setStatus] = useState<number | null>(null);
    const [latency, setLatency] = useState<number | null>(null);
    const [copied, setCopied] = useState(false);

    const responseRef = useRef<HTMLPreElement>(null);

    // Simulação de Request
    const handleSend = () => {
        setIsLoading(true);
        setResponse(null);
        setStatus(null);
        setLatency(null);

        const startTime = performance.now();

        // Simular delay de rede e resposta
        setTimeout(() => {
            const endTime = performance.now();
            setLatency(Math.round(endTime - startTime));
            
            // Gerar resposta fake baseada no método
            const mockData = generateMockResponse(method, url);
            
            setStatus(mockData.status);
            setResponse(JSON.stringify(mockData.data, null, 2));
            setIsLoading(false);
        }, 800 + Math.random() * 1000);
    };

    const generateMockResponse = (m: string, u: string) => {
        const success = Math.random() > 0.2;
        if (!success) return { status: 500, data: { error: "INTERNAL_QUANTUM_FLUX", code: "Q-500", message: "Neural alignment failed." } };
        
        return {
            status: 200,
            data: {
                success: true,
                timestamp: new Date().toISOString(),
                cluster: "ORION-X7",
                payload: Array.from({length: 5}, (_, i) => ({
                    id: `obj_${Math.random().toString(16).substr(2, 8)}`,
                    type: "entity",
                    integrity: Math.floor(Math.random() * 100),
                    status: "active"
                }))
            }
        };
    };

    const handleCopy = () => {
        if(response) {
            navigator.clipboard.writeText(response);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col lg:flex-row gap-6 p-2 overflow-hidden relative">
            
            {/* ESQUERDA: CONTROLE DE REQUEST */}
            <div className="lg:w-1/2 w-full flex flex-col gap-6 h-full">
                
                {/* Painel Principal */}
                <div className="bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl flex flex-col gap-6 relative overflow-hidden group">
                    
                    {/* Header */}
                    <div className="flex justify-between items-center">
                        <div>
                            <h1 className="text-2xl font-bold text-white tracking-tight font-display flex items-center gap-2">
                                <Globe className="w-6 h-6 text-[var(--color-primary)]" />
                                QUANTUM GATE
                            </h1>
                            <p className="text-xs text-gray-400 font-mono mt-1">Secure API Endpoint Tester v4.0</p>
                        </div>
                        <div className="px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-xs font-bold font-mono flex items-center gap-2">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                            ONLINE
                        </div>
                    </div>

                    {/* URL Bar (Estilo Browser Sci-Fi) */}
                    <div className="flex items-center gap-0 bg-black/40 border border-white/10 rounded-xl p-1 focus-within:border-[var(--color-primary)]/50 transition-all shadow-lg">
                        {/* Method Selector */}
                        <div className="relative group/method">
                            <div className={`px-4 py-3 font-bold font-mono text-sm cursor-pointer hover:text-white transition-colors ${
                                method === 'GET' ? 'text-blue-400' : 
                                method === 'POST' ? 'text-green-400' : 
                                method === 'DELETE' ? 'text-red-400' : 'text-yellow-400'
                            }`}>
                                {method}
                            </div>
                            {/* Dropdown (Hover) */}
                            <div className="absolute top-full left-0 mt-2 w-32 bg-[#0a0a0a] border border-white/10 rounded-lg overflow-hidden shadow-xl opacity-0 pointer-events-none group-hover/method:opacity-100 group-hover/method:pointer-events-auto transition-all z-50">
                                {METHODS.map(m => (
                                    <div 
                                        key={m} 
                                        onClick={() => setMethod(m)}
                                        className="px-4 py-2 text-xs font-mono text-gray-400 hover:bg-white/10 hover:text-white cursor-pointer"
                                    >
                                        {m}
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="w-[1px] h-6 bg-white/10 mx-2" />

                        {/* URL Input */}
                        <input 
                            type="text" 
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            className="flex-1 bg-transparent border-none outline-none text-white font-mono text-sm placeholder-gray-600"
                            placeholder="https://api.endpoint..."
                        />
                    </div>

                    {/* Botão de Disparo */}
                    <button 
                        onClick={handleSend}
                        disabled={isLoading}
                        className={`
                            relative w-full py-4 rounded-xl font-bold text-sm tracking-widest uppercase overflow-hidden group/btn transition-all
                            ${isLoading ? 'bg-gray-800 cursor-not-allowed' : 'bg-[var(--color-primary)] text-black hover:scale-[1.02] shadow-[0_0_30px_rgba(var(--color-primary-rgb),0.4)]'}
                        `}
                    >
                        <div className="relative z-10 flex items-center justify-center gap-2">
                            {isLoading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Zap className="w-5 h-5" />}
                            {isLoading ? 'TRANSMITTING...' : 'EXECUTE REQUEST'}
                        </div>
                        {/* Scanline Effect no Botão */}
                        {!isLoading && <div className="absolute inset-0 bg-white/20 translate-x-[-100%] group-hover/btn:translate-x-[100%] transition-transform duration-500 ease-in-out skew-x-12" />}
                    </button>

                    {/* Presets */}
                    <div className="mt-4">
                        <p className="text-[10px] text-gray-500 uppercase font-bold mb-3 tracking-widest">Quick Access</p>
                        <div className="flex flex-wrap gap-2">
                            {ENDPOINTS.map((ep, i) => (
                                <button
                                    key={i}
                                    onClick={() => { setMethod(ep.method); setUrl(`https://api.alsham.quantum${ep.path}`); }}
                                    className="px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 hover:border-[var(--color-primary)]/30 text-xs text-gray-300 transition-all flex items-center gap-2"
                                >
                                    <span className={`font-mono font-bold ${ep.method === 'GET' ? 'text-blue-400' : ep.method === 'POST' ? 'text-green-400' : 'text-red-400'}`}>
                                        {ep.method.charAt(0)}
                                    </span>
                                    {ep.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Configurações Adicionais (Headers/Body) */}
                <div className="flex-1 bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-6 relative">
                    <div className="flex gap-4 border-b border-white/5 pb-2 mb-4">
                        <button className="text-sm font-bold text-[var(--color-primary)] border-b-2 border-[var(--color-primary)] pb-2">Params</button>
                        <button className="text-sm font-bold text-gray-500 hover:text-white pb-2 transition-colors">Headers</button>
                        <button className="text-sm font-bold text-gray-500 hover:text-white pb-2 transition-colors">Body</button>
                    </div>
                    
                    <div className="font-mono text-xs text-gray-500">
                        <div className="flex items-center gap-2 p-2 bg-black/20 rounded mb-2">
                            <span className="text-yellow-400">Authorization:</span>
                            <span className="truncate">Bearer sk_test_51MxQ...</span>
                        </div>
                        <div className="flex items-center gap-2 p-2 bg-black/20 rounded">
                            <span className="text-purple-400">Content-Type:</span>
                            <span>application/json</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* DIREITA: RESPONSE TERMINAL */}
            <div className="lg:w-1/2 w-full bg-[#050505] border border-white/10 rounded-3xl p-0 overflow-hidden relative flex flex-col shadow-2xl">
                
                {/* Terminal Header */}
                <div className="h-12 bg-white/5 border-b border-white/5 flex items-center justify-between px-4">
                    <div className="flex items-center gap-3">
                        <div className="flex gap-1.5">
                            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50" />
                            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50" />
                            <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50" />
                        </div>
                        <span className="text-xs font-mono text-gray-500">RESPONSE_STREAM</span>
                    </div>
                    <div className="flex items-center gap-3">
                        {status && (
                            <span className={`px-2 py-0.5 rounded text-xs font-bold ${status === 200 ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                {status} {status === 200 ? 'OK' : 'ERR'}
                            </span>
                        )}
                        {latency && (
                            <span className="text-xs font-mono text-gray-500">{latency}ms</span>
                        )}
                    </div>
                </div>

                {/* Terminal Body */}
                <div className="flex-1 relative overflow-hidden bg-black/80">
                    {/* Loading State */}
                    {isLoading && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 z-20 bg-black/50 backdrop-blur-sm">
                            <div className="w-16 h-16 border-4 border-t-[var(--color-primary)] border-white/10 rounded-full animate-spin" />
                            <p className="text-xs font-mono text-[var(--color-primary)] animate-pulse">ESTABLISHING UPLINK...</p>
                        </div>
                    )}

                    {/* Code Display */}
                    <div className="absolute inset-0 overflow-auto p-6 scrollbar-thin scrollbar-thumb-white/10">
                        {response ? (
                            <pre ref={responseRef} className="font-mono text-sm text-blue-300 leading-relaxed">
                                {response}
                            </pre>
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-gray-700 select-none">
                                <Server className="w-16 h-16 mb-4 opacity-20" />
                                <p className="text-xs font-mono uppercase tracking-widest">Awaiting Transmission</p>
                            </div>
                        )}
                    </div>

                    {/* Copy Button */}
                    {response && (
                        <button 
                            onClick={handleCopy}
                            className="absolute top-4 right-4 p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-all z-10"
                        >
                            {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                        </button>
                    )}
                </div>

                {/* Footer do Terminal (Scanline) */}
                <div className="h-1 w-full bg-[var(--color-primary)]/20 relative overflow-hidden">
                    <div className={`absolute inset-0 bg-[var(--color-primary)] w-1/3 animate-loading-bar ${isLoading ? 'opacity-100' : 'opacity-0'}`} />
                </div>
            </div>

            {/* Efeitos Globais */}
            <style jsx>{`
                @keyframes loading-bar {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(300%); }
                }
                .animate-loading-bar { animation: loading-bar 1s linear infinite; }
            `}</style>
        </div>
    );
}
