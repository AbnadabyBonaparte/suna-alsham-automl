/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - REQUESTS
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/requests/page.tsx
 * 📋 ROTA: /dashboard/requests
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect } from 'react';
import { 
    Inbox,
    Send,
    Clock,
    CheckCircle,
    XCircle,
    AlertCircle,
    Filter,
    Search,
    Plus,
    Eye,
    MessageSquare,
    User,
    Calendar,
    Tag,
    ChevronDown,
    MoreHorizontal,
    RefreshCw,
    Archive,
    Trash2,
    Reply,
    Forward
} from 'lucide-react';

interface Request {
    id: string;
    title: string;
    description: string;
    requester: string;
    assignedTo: string;
    status: 'pending' | 'in_progress' | 'completed' | 'rejected' | 'archived';
    priority: 'low' | 'medium' | 'high' | 'critical';
    category: string;
    createdAt: string;
    updatedAt: string;
    comments: number;
}

const mockRequests: Request[] = [
    {
        id: 'REQ-001',
        title: 'Novo agente para análise de mercado',
        description: 'Requisição para criação de um agente especializado em análise de tendências de mercado.',
        requester: 'casamondestore@gmail.com',
        assignedTo: 'UNIT_24',
        status: 'in_progress',
        priority: 'high',
        category: 'Criação de Agente',
        createdAt: '2025-11-24T10:30:00Z',
        updatedAt: '2025-11-24T14:45:00Z',
        comments: 5
    },
    {
        id: 'REQ-002',
        title: 'Integração com API externa',
        description: 'Conectar o sistema com a API do HubSpot para sincronização de leads.',
        requester: 'operator@alsham.quantum',
        assignedTo: 'UNIT_29',
        status: 'pending',
        priority: 'medium',
        category: 'Integração',
        createdAt: '2025-11-24T09:15:00Z',
        updatedAt: '2025-11-24T09:15:00Z',
        comments: 2
    },
    {
        id: 'REQ-003',
        title: 'Relatório de performance mensal',
        description: 'Gerar relatório detalhado de performance dos agentes no último mês.',
        requester: 'casamondestore@gmail.com',
        assignedTo: 'ORION',
        status: 'completed',
        priority: 'low',
        category: 'Relatório',
        createdAt: '2025-11-23T16:00:00Z',
        updatedAt: '2025-11-24T08:30:00Z',
        comments: 8
    },
    {
        id: 'REQ-004',
        title: 'Correção de bug no Evolution Lab',
        description: 'Bug identificado na visualização de ondas de evolução.',
        requester: 'agent.handler@system',
        assignedTo: 'UNIT_15',
        status: 'in_progress',
        priority: 'critical',
        category: 'Bug Fix',
        createdAt: '2025-11-24T11:00:00Z',
        updatedAt: '2025-11-24T13:20:00Z',
        comments: 12
    },
    {
        id: 'REQ-005',
        title: 'Atualização de segurança',
        description: 'Implementar novas políticas de segurança no módulo de autenticação.',
        requester: 'operator@alsham.quantum',
        assignedTo: 'UNIT_08',
        status: 'pending',
        priority: 'high',
        category: 'Segurança',
        createdAt: '2025-11-24T08:00:00Z',
        updatedAt: '2025-11-24T08:00:00Z',
        comments: 1
    },
    {
        id: 'REQ-006',
        title: 'Novo tema visual: Cyber Noir',
        description: 'Criar um novo tema visual inspirado em cyberpunk noir.',
        requester: 'casamondestore@gmail.com',
        assignedTo: 'UNIT_42',
        status: 'rejected',
        priority: 'low',
        category: 'Design',
        createdAt: '2025-11-22T14:30:00Z',
        updatedAt: '2025-11-23T10:00:00Z',
        comments: 4
    },
    {
        id: 'REQ-007',
        title: 'Otimização de queries do banco',
        description: 'Melhorar performance das queries mais utilizadas no sistema.',
        requester: 'agent.handler@system',
        assignedTo: 'UNIT_31',
        status: 'completed',
        priority: 'medium',
        category: 'Performance',
        createdAt: '2025-11-21T09:00:00Z',
        updatedAt: '2025-11-23T17:45:00Z',
        comments: 6
    },
];

export default function RequestsPage() {
    const [requests, setRequests] = useState<Request[]>(mockRequests);
    const [selectedRequest, setSelectedRequest] = useState<Request | null>(null);
    const [filter, setFilter] = useState<string>('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [showNewModal, setShowNewModal] = useState(false);

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'pending': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/30';
            case 'in_progress': return 'text-blue-400 bg-blue-400/10 border-blue-400/30';
            case 'completed': return 'text-green-400 bg-green-400/10 border-green-400/30';
            case 'rejected': return 'text-red-400 bg-red-400/10 border-red-400/30';
            case 'archived': return 'text-zinc-400 bg-zinc-400/10 border-zinc-400/30';
            default: return 'text-zinc-400 bg-zinc-400/10 border-zinc-400/30';
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'pending': return <Clock className="w-4 h-4" />;
            case 'in_progress': return <RefreshCw className="w-4 h-4 animate-spin" style={{ animationDuration: '3s' }} />;
            case 'completed': return <CheckCircle className="w-4 h-4" />;
            case 'rejected': return <XCircle className="w-4 h-4" />;
            case 'archived': return <Archive className="w-4 h-4" />;
            default: return <AlertCircle className="w-4 h-4" />;
        }
    };

    const getStatusLabel = (status: string) => {
        switch (status) {
            case 'pending': return 'Pendente';
            case 'in_progress': return 'Em Progresso';
            case 'completed': return 'Concluído';
            case 'rejected': return 'Rejeitado';
            case 'archived': return 'Arquivado';
            default: return status;
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'low': return 'text-zinc-400';
            case 'medium': return 'text-yellow-400';
            case 'high': return 'text-orange-400';
            case 'critical': return 'text-red-400';
            default: return 'text-zinc-400';
        }
    };

    const getPriorityLabel = (priority: string) => {
        switch (priority) {
            case 'low': return 'Baixa';
            case 'medium': return 'Média';
            case 'high': return 'Alta';
            case 'critical': return 'Crítica';
            default: return priority;
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR', { 
            day: '2-digit', 
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const filteredRequests = requests.filter(req => {
        if (filter !== 'all' && req.status !== filter) return false;
        if (searchQuery && !req.title.toLowerCase().includes(searchQuery.toLowerCase())) return false;
        return true;
    });

    const stats = {
        total: requests.length,
        pending: requests.filter(r => r.status === 'pending').length,
        inProgress: requests.filter(r => r.status === 'in_progress').length,
        completed: requests.filter(r => r.status === 'completed').length,
    };

    return (
        <div className="min-h-screen flex flex-col">
            {/* Header */}
            <div className="p-6 border-b border-zinc-800">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl border border-purple-500/30">
                            <Inbox className="w-8 h-8 text-purple-400" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-white tracking-tight">
                                Requisições
                            </h1>
                            <p className="text-zinc-400">Gerenciamento de solicitações do sistema</p>
                        </div>
                    </div>
                    
                    <button 
                        onClick={() => setShowNewModal(true)}
                        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-medium rounded-lg hover:opacity-90 transition-opacity"
                    >
                        <Plus className="w-5 h-5" />
                        Nova Requisição
                    </button>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-4 gap-4 mt-6">
                    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                        <p className="text-zinc-400 text-sm">Total</p>
                        <p className="text-2xl font-bold text-white">{stats.total}</p>
                    </div>
                    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                        <p className="text-zinc-400 text-sm">Pendentes</p>
                        <p className="text-2xl font-bold text-yellow-400">{stats.pending}</p>
                    </div>
                    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                        <p className="text-zinc-400 text-sm">Em Progresso</p>
                        <p className="text-2xl font-bold text-blue-400">{stats.inProgress}</p>
                    </div>
                    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                        <p className="text-zinc-400 text-sm">Concluídos</p>
                        <p className="text-2xl font-bold text-green-400">{stats.completed}</p>
                    </div>
                </div>
            </div>

            <div className="flex-1 flex">
                {/* Filters & List */}
                <div className="w-2/3 border-r border-zinc-800 flex flex-col">
                    {/* Search & Filters */}
                    <div className="p-4 border-b border-zinc-800 flex items-center gap-4">
                        <div className="flex-1 relative">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-zinc-500" />
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder="Buscar requisições..."
                                className="w-full pl-10 pr-4 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500"
                            />
                        </div>
                        <div className="flex items-center gap-2">
                            {['all', 'pending', 'in_progress', 'completed', 'rejected'].map((status) => (
                                <button
                                    key={status}
                                    onClick={() => setFilter(status)}
                                    className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                                        filter === status
                                            ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                                            : 'text-zinc-400 hover:text-white'
                                    }`}
                                >
                                    {status === 'all' ? 'Todos' : getStatusLabel(status)}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Request List */}
                    <div className="flex-1 overflow-y-auto">
                        {filteredRequests.map((request) => (
                            <div
                                key={request.id}
                                onClick={() => setSelectedRequest(request)}
                                className={`p-4 border-b border-zinc-800 cursor-pointer transition-colors ${
                                    selectedRequest?.id === request.id
                                        ? 'bg-zinc-800/50'
                                        : 'hover:bg-zinc-900/50'
                                }`}
                            >
                                <div className="flex items-start justify-between gap-4">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="text-zinc-500 text-sm">{request.id}</span>
                                            <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getStatusColor(request.status)}`}>
                                                <span className="flex items-center gap-1">
                                                    {getStatusIcon(request.status)}
                                                    {getStatusLabel(request.status)}
                                                </span>
                                            </span>
                                            <span className={`text-xs ${getPriorityColor(request.priority)}`}>
                                                • {getPriorityLabel(request.priority)}
                                            </span>
                                        </div>
                                        <h3 className="text-white font-medium mb-1">{request.title}</h3>
                                        <p className="text-zinc-500 text-sm line-clamp-1">{request.description}</p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-zinc-500 text-xs">{formatDate(request.updatedAt)}</p>
                                        <div className="flex items-center gap-1 mt-1 text-zinc-500">
                                            <MessageSquare className="w-3 h-3" />
                                            <span className="text-xs">{request.comments}</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4 mt-2 text-xs text-zinc-500">
                                    <span className="flex items-center gap-1">
                                        <User className="w-3 h-3" />
                                        {request.requester.split('@')[0]}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <Tag className="w-3 h-3" />
                                        {request.category}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <Send className="w-3 h-3" />
                                        {request.assignedTo}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Detail Panel */}
                <div className="w-1/3 bg-zinc-900/30">
                    {selectedRequest ? (
                        <div className="p-6">
                            <div className="flex items-center justify-between mb-6">
                                <span className="text-zinc-500">{selectedRequest.id}</span>
                                <button className="p-2 hover:bg-zinc-800 rounded-lg">
                                    <MoreHorizontal className="w-5 h-5 text-zinc-400" />
                                </button>
                            </div>

                            <h2 className="text-xl font-bold text-white mb-2">{selectedRequest.title}</h2>
                            
                            <div className="flex items-center gap-2 mb-4">
                                <span className={`px-2 py-1 rounded text-xs font-medium border ${getStatusColor(selectedRequest.status)}`}>
                                    <span className="flex items-center gap-1">
                                        {getStatusIcon(selectedRequest.status)}
                                        {getStatusLabel(selectedRequest.status)}
                                    </span>
                                </span>
                                <span className={`text-sm ${getPriorityColor(selectedRequest.priority)}`}>
                                    Prioridade: {getPriorityLabel(selectedRequest.priority)}
                                </span>
                            </div>

                            <p className="text-zinc-400 mb-6">{selectedRequest.description}</p>

                            <div className="space-y-4 mb-6">
                                <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                                    <span className="text-zinc-500 text-sm">Solicitante</span>
                                    <span className="text-white text-sm">{selectedRequest.requester}</span>
                                </div>
                                <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                                    <span className="text-zinc-500 text-sm">Atribuído a</span>
                                    <span className="text-cyan-400 text-sm">{selectedRequest.assignedTo}</span>
                                </div>
                                <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                                    <span className="text-zinc-500 text-sm">Categoria</span>
                                    <span className="text-white text-sm">{selectedRequest.category}</span>
                                </div>
                                <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                                    <span className="text-zinc-500 text-sm">Criado em</span>
                                    <span className="text-white text-sm">{formatDate(selectedRequest.createdAt)}</span>
                                </div>
                                <div className="flex items-center justify-between py-2 border-b border-zinc-800">
                                    <span className="text-zinc-500 text-sm">Atualizado em</span>
                                    <span className="text-white text-sm">{formatDate(selectedRequest.updatedAt)}</span>
                                </div>
                            </div>

                            {/* Actions */}
                            <div className="flex items-center gap-2">
                                <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-lg hover:bg-purple-500/30 transition-colors">
                                    <Reply className="w-4 h-4" />
                                    Responder
                                </button>
                                <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-zinc-800 text-zinc-300 border border-zinc-700 rounded-lg hover:bg-zinc-700 transition-colors">
                                    <Forward className="w-4 h-4" />
                                    Encaminhar
                                </button>
                            </div>

                            {/* Comments section */}
                            <div className="mt-6 pt-6 border-t border-zinc-800">
                                <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">
                                    Comentários ({selectedRequest.comments})
                                </h3>
                                <div className="space-y-4">
                                    <div className="bg-black/30 rounded-lg p-3">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-cyan-400 text-sm">{selectedRequest.assignedTo}</span>
                                            <span className="text-zinc-500 text-xs">há 2h</span>
                                        </div>
                                        <p className="text-zinc-300 text-sm">Iniciando análise da requisição. Previsão de conclusão em 24h.</p>
                                    </div>
                                    <div className="bg-black/30 rounded-lg p-3">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-purple-400 text-sm">{selectedRequest.requester.split('@')[0]}</span>
                                            <span className="text-zinc-500 text-xs">há 4h</span>
                                        </div>
                                        <p className="text-zinc-300 text-sm">Por favor, priorizar esta requisição.</p>
                                    </div>
                                </div>

                                {/* Add comment */}
                                <div className="mt-4">
                                    <textarea
                                        placeholder="Adicionar comentário..."
                                        className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500 resize-none"
                                        rows={2}
                                    />
                                    <button className="mt-2 px-4 py-1.5 bg-purple-500 text-white text-sm rounded-lg hover:bg-purple-600 transition-colors">
                                        Enviar
                                    </button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="h-full flex items-center justify-center text-zinc-500">
                            <div className="text-center">
                                <Eye className="w-12 h-12 mx-auto mb-3 opacity-30" />
                                <p>Selecione uma requisição para ver detalhes</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
