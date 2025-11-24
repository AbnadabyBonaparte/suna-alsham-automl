"use client";

import { useState } from 'react';
import { 
    Code, 
    Play, 
    Copy, 
    Check,
    ChevronDown,
    ChevronRight,
    Terminal,
    Zap,
    Clock,
    FileJson,
    Send,
    RefreshCw,
    Key,
    Globe,
    Box
} from 'lucide-react';

export default function ApiPlaygroundPage() {
    const [selectedEndpoint, setSelectedEndpoint] = useState('agents');
    const [method, setMethod] = useState('GET');
    const [response, setResponse] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [copied, setCopied] = useState(false);
    const [activeTab, setActiveTab] = useState<'response' | 'headers'>('response');

    const endpoints = [
        { id: 'agents', name: 'Agents', path: '/rest/v1/agents', methods: ['GET', 'POST', 'PATCH', 'DELETE'] },
        { id: 'leads', name: 'Leads', path: '/rest/v1/leads', methods: ['GET', 'POST', 'PATCH', 'DELETE'] },
        { id: 'tasks', name: 'Tasks', path: '/rest/v1/tasks', methods: ['GET', 'POST', 'PATCH', 'DELETE'] },
        { id: 'analytics', name: 'Analytics', path: '/rest/v1/analytics', methods: ['GET'] },
        { id: 'evolution', name: 'Evolution', path: '/rest/v1/evolution_waves', methods: ['GET'] },
        { id: 'gamification', name: 'Gamification', path: '/rest/v1/gamification_points', methods: ['GET', 'POST'] },
    ];

    const sampleResponses: Record<string, any> = {
        agents: {
            data: [
                { id: 'unit_24', name: 'UNIT_24', type: 'SPECIALIST', efficiency: 92, status: 'active' },
                { id: 'unit_25', name: 'UNIT_25', type: 'SPECIALIST', efficiency: 87, status: 'active' },
                { id: 'unit_26', name: 'UNIT_26', type: 'SPECIALIST', efficiency: 88, status: 'active' },
            ],
            count: 139,
            status: 200
        },
        leads: {
            data: [
                { id: 1, name: 'Empresa ABC', status: 'qualified', score: 85 },
                { id: 2, name: 'Tech Corp', status: 'new', score: 72 },
            ],
            count: 106,
            status: 200
        },
        analytics: {
            data: {
                total_agents: 139,
                active_agents: 127,
                total_leads: 106,
                conversion_rate: 34.5,
                avg_efficiency: 89.2
            },
            status: 200
        }
    };

    const handleExecute = async () => {
        setLoading(true);
        setResponse(null);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 800));
        
        const result = sampleResponses[selectedEndpoint] || { 
            data: [], 
            message: 'Endpoint response', 
            status: 200 
        };
        
        setResponse(JSON.stringify(result, null, 2));
        setLoading(false);
    };

    const handleCopy = () => {
        if (response) {
            navigator.clipboard.writeText(response);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    const getMethodColor = (m: string) => {
        switch (m) {
            case 'GET': return 'text-green-400 bg-green-400/10';
            case 'POST': return 'text-blue-400 bg-blue-400/10';
            case 'PATCH': return 'text-yellow-400 bg-yellow-400/10';
            case 'DELETE': return 'text-red-400 bg-red-400/10';
            default: return 'text-zinc-400 bg-zinc-400/10';
        }
    };

    const currentEndpoint = endpoints.find(e => e.id === selectedEndpoint);

    return (
        <div className="min-h-screen p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-emerald-500/20 rounded-xl border border-emerald-500/30">
                        <Code className="w-8 h-8 text-emerald-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            API Playground
                        </h1>
                        <p className="text-zinc-400">Test and explore the Quantum API</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-emerald-500/20 border border-emerald-500/30 rounded-full text-emerald-400 text-sm font-medium flex items-center gap-2">
                        <Globe className="w-3 h-3" />
                        v1.0
                    </span>
                </div>
            </div>

            {/* API Info */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center gap-2 text-zinc-400 mb-2">
                        <Globe className="w-4 h-4" />
                        <span className="text-sm">Base URL</span>
                    </div>
                    <p className="text-cyan-400 font-mono text-sm break-all">
                        https://vktzdrsigrdnemdshcdp.supabase.co
                    </p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center gap-2 text-zinc-400 mb-2">
                        <Key className="w-4 h-4" />
                        <span className="text-sm">Auth Type</span>
                    </div>
                    <p className="text-white font-medium">Bearer Token (JWT)</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="flex items-center gap-2 text-zinc-400 mb-2">
                        <Box className="w-4 h-4" />
                        <span className="text-sm">Response Format</span>
                    </div>
                    <p className="text-white font-medium">JSON</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Endpoints List */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">
                        Endpoints
                    </h3>
                    <div className="space-y-2">
                        {endpoints.map((endpoint) => (
                            <button
                                key={endpoint.id}
                                onClick={() => setSelectedEndpoint(endpoint.id)}
                                className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                                    selectedEndpoint === endpoint.id
                                        ? 'bg-cyan-500/20 border border-cyan-500/30 text-cyan-400'
                                        : 'hover:bg-zinc-800 text-zinc-300'
                                }`}
                            >
                                <div className="flex items-center gap-2">
                                    <FileJson className="w-4 h-4" />
                                    <span>{endpoint.name}</span>
                                </div>
                                <ChevronRight className="w-4 h-4" />
                            </button>
                        ))}
                    </div>
                </div>

                {/* Request Builder & Response */}
                <div className="lg:col-span-3 space-y-4">
                    {/* Request Builder */}
                    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                        <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">
                            Request
                        </h3>
                        
                        <div className="flex flex-wrap gap-3 mb-4">
                            {/* Method Selector */}
                            <div className="flex gap-1 bg-black/30 rounded-lg p-1">
                                {currentEndpoint?.methods.map((m) => (
                                    <button
                                        key={m}
                                        onClick={() => setMethod(m)}
                                        className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                                            method === m ? getMethodColor(m) : 'text-zinc-500 hover:text-zinc-300'
                                        }`}
                                    >
                                        {m}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* URL Preview */}
                        <div className="flex items-center gap-2 bg-black/50 rounded-lg p-3 font-mono text-sm mb-4">
                            <span className={`px-2 py-0.5 rounded ${getMethodColor(method)} font-bold`}>
                                {method}
                            </span>
                            <span className="text-zinc-500">https://...supabase.co</span>
                            <span className="text-cyan-400">{currentEndpoint?.path}</span>
                        </div>

                        {/* Headers Preview */}
                        <div className="bg-black/30 rounded-lg p-4 mb-4">
                            <p className="text-xs text-zinc-500 mb-2">Headers</p>
                            <div className="font-mono text-xs space-y-1">
                                <p><span className="text-purple-400">Authorization:</span> <span className="text-zinc-400">Bearer eyJhbGciOiJIUzI1NiIs...</span></p>
                                <p><span className="text-purple-400">Content-Type:</span> <span className="text-zinc-400">application/json</span></p>
                                <p><span className="text-purple-400">apikey:</span> <span className="text-zinc-400">eyJhbGciOiJIUzI1NiIs...</span></p>
                            </div>
                        </div>

                        {/* Execute Button */}
                        <button
                            onClick={handleExecute}
                            disabled={loading}
                            className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-black font-medium rounded-lg transition-all disabled:opacity-50"
                        >
                            {loading ? (
                                <>
                                    <RefreshCw className="w-4 h-4 animate-spin" />
                                    Executing...
                                </>
                            ) : (
                                <>
                                    <Play className="w-4 h-4" />
                                    Execute Request
                                </>
                            )}
                        </button>
                    </div>

                    {/* Response */}
                    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-4">
                                <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">
                                    Response
                                </h3>
                                {response && (
                                    <div className="flex items-center gap-2">
                                        <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded text-xs font-medium">
                                            200 OK
                                        </span>
                                        <span className="text-xs text-zinc-500 flex items-center gap-1">
                                            <Clock className="w-3 h-3" />
                                            124ms
                                        </span>
                                    </div>
                                )}
                            </div>
                            {response && (
                                <button
                                    onClick={handleCopy}
                                    className="flex items-center gap-2 px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-sm text-zinc-300 transition-colors"
                                >
                                    {copied ? (
                                        <>
                                            <Check className="w-4 h-4 text-green-400" />
                                            Copied!
                                        </>
                                    ) : (
                                        <>
                                            <Copy className="w-4 h-4" />
                                            Copy
                                        </>
                                    )}
                                </button>
                            )}
                        </div>

                        <div className="bg-black/50 rounded-lg p-4 font-mono text-sm min-h-[300px] max-h-[500px] overflow-auto">
                            {loading ? (
                                <div className="flex items-center justify-center h-full text-zinc-500">
                                    <RefreshCw className="w-6 h-6 animate-spin mr-2" />
                                    Loading...
                                </div>
                            ) : response ? (
                                <pre className="text-green-400 whitespace-pre-wrap">{response}</pre>
                            ) : (
                                <div className="flex flex-col items-center justify-center h-full text-zinc-500">
                                    <Terminal className="w-12 h-12 mb-4 opacity-30" />
                                    <p>Click "Execute Request" to see the response</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Code Examples */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Code className="w-5 h-5 text-purple-400" />
                    Code Examples
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-black/50 rounded-lg p-4">
                        <p className="text-xs text-zinc-500 mb-2">JavaScript / fetch</p>
                        <pre className="text-sm text-cyan-400 overflow-x-auto">
{`const response = await fetch(
  'https://...supabase.co${currentEndpoint?.path}',
  {
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'apikey': 'YOUR_API_KEY'
    }
  }
);
const data = await response.json();`}
                        </pre>
                    </div>
                    <div className="bg-black/50 rounded-lg p-4">
                        <p className="text-xs text-zinc-500 mb-2">cURL</p>
                        <pre className="text-sm text-yellow-400 overflow-x-auto">
{`curl -X ${method} \\
  'https://...supabase.co${currentEndpoint?.path}' \\
  -H 'Authorization: Bearer YOUR_TOKEN' \\
  -H 'apikey: YOUR_API_KEY'`}
                        </pre>
                    </div>
                </div>
            </div>
        </div>
    );
}
