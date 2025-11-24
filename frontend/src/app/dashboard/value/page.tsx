/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - VALUE DASH
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/value/page.tsx
 * 📋 ROTA: /dashboard/value
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState } from 'react';
import { 
    TrendingUp, 
    TrendingDown,
    DollarSign, 
    Users, 
    Target,
    Award,
    ArrowUpRight,
    ArrowDownRight,
    BarChart3,
    PieChart,
    Activity,
    Calendar,
    Filter,
    Download,
    RefreshCw,
    Zap,
    Clock,
    CheckCircle
} from 'lucide-react';

interface MetricCard {
    title: string;
    value: string;
    change: number;
    changeLabel: string;
    icon: any;
    color: string;
}

export default function ValueDashPage() {
    const [timeRange, setTimeRange] = useState('30d');
    const [isRefreshing, setIsRefreshing] = useState(false);

    const metrics: MetricCard[] = [
        {
            title: 'Revenue Total',
            value: 'R$ 847.520',
            change: 12.5,
            changeLabel: 'vs mês anterior',
            icon: DollarSign,
            color: 'from-green-500 to-emerald-500'
        },
        {
            title: 'Leads Convertidos',
            value: '1,247',
            change: 8.3,
            changeLabel: 'vs mês anterior',
            icon: Target,
            color: 'from-blue-500 to-cyan-500'
        },
        {
            title: 'Ticket Médio',
            value: 'R$ 2.840',
            change: -3.2,
            changeLabel: 'vs mês anterior',
            icon: BarChart3,
            color: 'from-purple-500 to-pink-500'
        },
        {
            title: 'ROI Marketing',
            value: '342%',
            change: 28.7,
            changeLabel: 'vs mês anterior',
            icon: TrendingUp,
            color: 'from-orange-500 to-amber-500'
        }
    ];

    const topPerformers = [
        { name: 'UNIT_24', value: 'R$ 127.840', deals: 47, efficiency: 92 },
        { name: 'UNIT_29', value: 'R$ 98.520', deals: 38, efficiency: 91 },
        { name: 'UNIT_25', value: 'R$ 89.340', deals: 35, efficiency: 87 },
        { name: 'UNIT_26', value: 'R$ 78.120', deals: 31, efficiency: 88 },
        { name: 'UNIT_28', value: 'R$ 72.450', deals: 29, efficiency: 87 },
    ];

    const conversionFunnel = [
        { stage: 'Leads Totais', value: 2847, percentage: 100 },
        { stage: 'Leads Qualificados', value: 1423, percentage: 50 },
        { stage: 'Propostas Enviadas', value: 712, percentage: 25 },
        { stage: 'Em Negociação', value: 356, percentage: 12.5 },
        { stage: 'Fechados', value: 178, percentage: 6.25 },
    ];

    const recentDeals = [
        { company: 'Tech Solutions Ltda', value: 'R$ 45.000', status: 'closed', date: '23/11' },
        { company: 'Inovação Digital', value: 'R$ 28.500', status: 'closed', date: '22/11' },
        { company: 'Global Enterprises', value: 'R$ 72.000', status: 'negotiating', date: '22/11' },
        { company: 'StartUp Labs', value: 'R$ 15.800', status: 'closed', date: '21/11' },
        { company: 'Corp Systems', value: 'R$ 38.200', status: 'proposal', date: '21/11' },
    ];

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await new Promise(resolve => setTimeout(resolve, 1000));
        setIsRefreshing(false);
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'closed': return 'text-green-400 bg-green-400/10';
            case 'negotiating': return 'text-yellow-400 bg-yellow-400/10';
            case 'proposal': return 'text-blue-400 bg-blue-400/10';
            default: return 'text-zinc-400 bg-zinc-400/10';
        }
    };

    const getStatusLabel = (status: string) => {
        switch (status) {
            case 'closed': return 'Fechado';
            case 'negotiating': return 'Negociando';
            case 'proposal': return 'Proposta';
            default: return status;
        }
    };

    return (
        <div className="min-h-screen p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl border border-green-500/30">
                        <DollarSign className="w-8 h-8 text-green-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            Value Dash
                        </h1>
                        <p className="text-zinc-400">Financial Intelligence & ROI Analytics</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    {/* Time Range Selector */}
                    <div className="flex bg-zinc-900/50 border border-zinc-800 rounded-lg p-1">
                        {['7d', '30d', '90d', '1y'].map((range) => (
                            <button
                                key={range}
                                onClick={() => setTimeRange(range)}
                                className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
                                    timeRange === range
                                        ? 'bg-green-500/20 text-green-400'
                                        : 'text-zinc-400 hover:text-white'
                                }`}
                            >
                                {range}
                            </button>
                        ))}
                    </div>
                    <button
                        onClick={handleRefresh}
                        disabled={isRefreshing}
                        className="p-2 bg-zinc-900/50 border border-zinc-800 rounded-lg hover:bg-zinc-800 transition-colors"
                    >
                        <RefreshCw className={`w-5 h-5 text-zinc-400 ${isRefreshing ? 'animate-spin' : ''}`} />
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-green-500/20 border border-green-500/30 rounded-lg text-green-400 hover:bg-green-500/30 transition-colors">
                        <Download className="w-4 h-4" />
                        Export
                    </button>
                </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {metrics.map((metric, index) => (
                    <div 
                        key={index}
                        className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-5 hover:border-zinc-700 transition-colors"
                    >
                        <div className="flex items-start justify-between mb-4">
                            <div className={`p-2 rounded-lg bg-gradient-to-br ${metric.color} bg-opacity-20`}>
                                <metric.icon className="w-5 h-5 text-white" />
                            </div>
                            <div className={`flex items-center gap-1 text-sm ${
                                metric.change >= 0 ? 'text-green-400' : 'text-red-400'
                            }`}>
                                {metric.change >= 0 ? (
                                    <ArrowUpRight className="w-4 h-4" />
                                ) : (
                                    <ArrowDownRight className="w-4 h-4" />
                                )}
                                {Math.abs(metric.change)}%
                            </div>
                        </div>
                        <p className="text-2xl font-bold text-white mb-1">{metric.value}</p>
                        <p className="text-sm text-zinc-500">{metric.title}</p>
                        <p className="text-xs text-zinc-600 mt-1">{metric.changeLabel}</p>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Conversion Funnel */}
                <div className="lg:col-span-2 bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                            <Activity className="w-5 h-5 text-cyan-400" />
                            Funil de Conversão
                        </h2>
                    </div>
                    <div className="space-y-4">
                        {conversionFunnel.map((stage, index) => (
                            <div key={index} className="relative">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-zinc-300">{stage.stage}</span>
                                    <div className="flex items-center gap-3">
                                        <span className="text-white font-medium">{stage.value.toLocaleString()}</span>
                                        <span className="text-sm text-zinc-500">{stage.percentage}%</span>
                                    </div>
                                </div>
                                <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
                                    <div 
                                        className="h-full bg-gradient-to-r from-cyan-500 to-green-500 rounded-full transition-all duration-500"
                                        style={{ width: `${stage.percentage}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Top Performers */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                            <Award className="w-5 h-5 text-yellow-400" />
                            Top Performers
                        </h2>
                    </div>
                    <div className="space-y-3">
                        {topPerformers.map((performer, index) => (
                            <div 
                                key={index}
                                className="flex items-center justify-between p-3 bg-black/30 rounded-lg border border-zinc-800"
                            >
                                <div className="flex items-center gap-3">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                                        index === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                                        index === 1 ? 'bg-zinc-400/20 text-zinc-300' :
                                        index === 2 ? 'bg-orange-500/20 text-orange-400' :
                                        'bg-zinc-800 text-zinc-500'
                                    }`}>
                                        {index + 1}
                                    </div>
                                    <div>
                                        <p className="text-white font-medium">{performer.name}</p>
                                        <p className="text-xs text-zinc-500">{performer.deals} deals</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="text-green-400 font-medium">{performer.value}</p>
                                    <p className="text-xs text-zinc-500">{performer.efficiency}% eff</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Recent Deals */}
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                        <Clock className="w-5 h-5 text-blue-400" />
                        Deals Recentes
                    </h2>
                    <button className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors">
                        Ver todos →
                    </button>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-zinc-800">
                                <th className="text-left py-3 px-4 text-sm text-zinc-500 font-medium">Empresa</th>
                                <th className="text-left py-3 px-4 text-sm text-zinc-500 font-medium">Valor</th>
                                <th className="text-left py-3 px-4 text-sm text-zinc-500 font-medium">Status</th>
                                <th className="text-left py-3 px-4 text-sm text-zinc-500 font-medium">Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentDeals.map((deal, index) => (
                                <tr key={index} className="border-b border-zinc-800/50 hover:bg-zinc-800/20">
                                    <td className="py-3 px-4">
                                        <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center text-white text-sm font-bold">
                                                {deal.company[0]}
                                            </div>
                                            <span className="text-white">{deal.company}</span>
                                        </div>
                                    </td>
                                    <td className="py-3 px-4 text-green-400 font-medium">{deal.value}</td>
                                    <td className="py-3 px-4">
                                        <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(deal.status)}`}>
                                            {getStatusLabel(deal.status)}
                                        </span>
                                    </td>
                                    <td className="py-3 px-4 text-zinc-400">{deal.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 text-center">
                    <Zap className="w-6 h-6 text-yellow-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">89.2%</p>
                    <p className="text-sm text-zinc-500">Taxa de Sucesso</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 text-center">
                    <Clock className="w-6 h-6 text-blue-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">4.2 dias</p>
                    <p className="text-sm text-zinc-500">Ciclo Médio</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 text-center">
                    <CheckCircle className="w-6 h-6 text-green-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">178</p>
                    <p className="text-sm text-zinc-500">Deals Fechados</p>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 text-center">
                    <Users className="w-6 h-6 text-purple-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">127</p>
                    <p className="text-sm text-zinc-500">Clientes Ativos</p>
                </div>
            </div>
        </div>
    );
}
