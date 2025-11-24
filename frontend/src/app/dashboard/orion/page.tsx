"use client";

import { useState, useRef, useEffect } from 'react';
import { 
    Brain, 
    Send, 
    Sparkles, 
    Bot,
    User,
    Lightbulb,
    TrendingUp,
    Target,
    Zap,
    MessageSquare,
    RefreshCw,
    Copy,
    Check,
    Settings,
    Maximize2,
    ChevronDown
} from 'lucide-react';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export default function OrionPage() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'assistant',
            content: 'Olá! Sou ORION, sua inteligência artificial quântica. Estou aqui para ajudar com análises, estratégias e otimização de agentes. Como posso ajudar você hoje?',
            timestamp: new Date()
        }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [copiedId, setCopiedId] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const suggestions = [
        { icon: TrendingUp, text: "Analisar performance dos agentes", color: "text-green-400" },
        { icon: Target, text: "Sugerir otimizações para leads", color: "text-blue-400" },
        { icon: Lightbulb, text: "Gerar insights do dashboard", color: "text-yellow-400" },
        { icon: Zap, text: "Prever tendências de conversão", color: "text-purple-400" },
    ];

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Simulate AI response
        await new Promise(resolve => setTimeout(resolve, 1500));

        const responses: Record<string, string> = {
            'performance': `📊 **Análise de Performance dos Agentes**

Baseado nos dados atuais do sistema:

• **Top Performers:**
  - UNIT_24: 92% eficiência (+5% vs média)
  - UNIT_29: 91% eficiência (+4% vs média)
  
• **Áreas de Melhoria:**
  - UNIT_27 está com 87% - recomendo otimização de parâmetros
  
• **Tendência Geral:** 
  A eficiência média subiu 3.2% nas últimas 24h. 
  
🎯 **Recomendação:** Replicar configurações do UNIT_24 para outros agentes.`,
            
            'leads': `🎯 **Otimizações para Leads**

Analisei os 106 leads ativos e identifiquei:

• **Leads Quentes (Score > 80):** 23 leads
  - Taxa de conversão esperada: 45%
  - Ação: Priorizar contato imediato

• **Leads Mornos (Score 50-80):** 58 leads  
  - Recomendação: Nutrir com conteúdo
  
• **Leads Frios (Score < 50):** 25 leads
  - Considerar campanhas de reengajamento

📈 **Insight:** Leads do segmento Tech têm 2x mais conversão.`,

            'insights': `💡 **Insights do Dashboard**

🔬 **Métricas Chave:**
- Agentes ativos: 139 (+2 hoje)
- Taxa de sucesso: 89.2%
- Leads processados: 1,247 este mês

📊 **Padrões Identificados:**
1. Pico de atividade: 14h-17h
2. Melhor dia: Terça-feira
3. Agentes especialistas > Generalistas

⚡ **Ações Recomendadas:**
1. Escalar recursos no horário de pico
2. Criar mais agentes especialistas
3. Implementar automação para leads frios`,

            'default': `Entendi sua pergunta! Com base nos dados do sistema ALSHAM Quantum, posso ajudar com:

• Análise de performance de agentes
• Otimização de leads e conversões
• Insights e métricas do dashboard
• Previsões e tendências

O que você gostaria de explorar especificamente?`
        };

        let responseContent = responses.default;
        const lowerInput = input.toLowerCase();
        
        if (lowerInput.includes('performance') || lowerInput.includes('agente')) {
            responseContent = responses.performance;
        } else if (lowerInput.includes('lead') || lowerInput.includes('otimiz')) {
            responseContent = responses.leads;
        } else if (lowerInput.includes('insight') || lowerInput.includes('dashboard') || lowerInput.includes('analise')) {
            responseContent = responses.insights;
        }

        const aiMessage: Message = {
            id: (Date.now() + 1).toString(),
            role: 'assistant',
            content: responseContent,
            timestamp: new Date()
        };

        setIsTyping(false);
        setMessages(prev => [...prev, aiMessage]);
    };

    const handleSuggestionClick = (text: string) => {
        setInput(text);
    };

    const handleCopy = (id: string, content: string) => {
        navigator.clipboard.writeText(content);
        setCopiedId(id);
        setTimeout(() => setCopiedId(null), 2000);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="min-h-screen flex flex-col">
            {/* Header */}
            <div className="p-6 border-b border-zinc-800">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl border border-purple-500/30 relative">
                            <Brain className="w-8 h-8 text-purple-400" />
                            <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-2">
                                ORION AI
                                <Sparkles className="w-6 h-6 text-yellow-400" />
                            </h1>
                            <p className="text-zinc-400">Quantum Intelligence Assistant</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="px-3 py-1 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-full text-purple-400 text-sm font-medium">
                            GPT-4 Enhanced
                        </span>
                    </div>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex gap-4 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        {/* Avatar */}
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                            message.role === 'assistant' 
                                ? 'bg-gradient-to-br from-purple-500 to-pink-500' 
                                : 'bg-gradient-to-br from-cyan-500 to-blue-500'
                        }`}>
                            {message.role === 'assistant' ? (
                                <Bot className="w-5 h-5 text-white" />
                            ) : (
                                <User className="w-5 h-5 text-white" />
                            )}
                        </div>

                        {/* Message Content */}
                        <div className={`max-w-[70%] ${message.role === 'user' ? 'text-right' : ''}`}>
                            <div className={`rounded-2xl p-4 ${
                                message.role === 'assistant'
                                    ? 'bg-zinc-900/50 border border-zinc-800'
                                    : 'bg-cyan-500/20 border border-cyan-500/30'
                            }`}>
                                <div className="text-white whitespace-pre-wrap">
                                    {message.content}
                                </div>
                            </div>
                            <div className="flex items-center gap-2 mt-2 text-xs text-zinc-500">
                                <span>
                                    {message.timestamp.toLocaleTimeString('pt-BR', { 
                                        hour: '2-digit', 
                                        minute: '2-digit' 
                                    })}
                                </span>
                                {message.role === 'assistant' && (
                                    <button
                                        onClick={() => handleCopy(message.id, message.content)}
                                        className="hover:text-zinc-300 transition-colors"
                                    >
                                        {copiedId === message.id ? (
                                            <Check className="w-3 h-3 text-green-400" />
                                        ) : (
                                            <Copy className="w-3 h-3" />
                                        )}
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                ))}

                {/* Typing Indicator */}
                {isTyping && (
                    <div className="flex gap-4">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                            <Bot className="w-5 h-5 text-white" />
                        </div>
                        <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-4">
                            <div className="flex gap-1">
                                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Suggestions */}
            {messages.length === 1 && (
                <div className="px-6 pb-4">
                    <p className="text-sm text-zinc-500 mb-3">Sugestões para começar:</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {suggestions.map((suggestion, index) => (
                            <button
                                key={index}
                                onClick={() => handleSuggestionClick(suggestion.text)}
                                className="flex items-center gap-2 p-3 bg-zinc-900/50 border border-zinc-800 rounded-xl hover:border-purple-500/30 hover:bg-purple-500/5 transition-all text-left"
                            >
                                <suggestion.icon className={`w-5 h-5 ${suggestion.color}`} />
                                <span className="text-sm text-zinc-300">{suggestion.text}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Input Area */}
            <div className="p-6 border-t border-zinc-800 bg-black/50">
                <div className="flex items-end gap-4">
                    <div className="flex-1 relative">
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Pergunte ao ORION..."
                            rows={1}
                            className="w-full bg-zinc-900/50 border border-zinc-700 rounded-xl px-4 py-3 pr-12 text-white placeholder-zinc-500 focus:border-purple-500 focus:outline-none resize-none"
                            style={{ minHeight: '48px', maxHeight: '120px' }}
                        />
                    </div>
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isTyping}
                        className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-xl text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
                <p className="text-xs text-zinc-600 mt-2 text-center">
                    ORION pode cometer erros. Verifique informações importantes.
                </p>
            </div>
        </div>
    );
}
