/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ORION CHAT HOOK (10/10 EDITION)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/hooks/useOrionChat.ts
 * 💬 Histórico de mensagens + Envio + Contexto de página
 * 💎 Comandos especiais + Integração com API
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useState, useCallback, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface Message {
  id: string;
  role: 'user' | 'orion';
  content: string;
  timestamp: Date;
  isVoice?: boolean;
  tokens?: number;
  executionTime?: number;
}

export interface ChatState {
  messages: Message[];
  isThinking: boolean;
  hasGreeted: boolean;
  godMode: boolean;
}

export interface UseOrionChatReturn {
  state: ChatState;
  sendMessage: (text: string, isVoice?: boolean) => Promise<string | null>;
  addGreeting: () => void;
  toggleGodMode: () => void;
  clearMessages: () => void;
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTO DE PÁGINA
// ═══════════════════════════════════════════════════════════════════════════════

const PAGE_CONTEXTS: Record<string, string> = {
  '/dashboard': 'Você está no Cockpit principal do ALSHAM QUANTUM, onde pode ver métricas gerais e o status dos 139 agentes.',
  '/dashboard/quantum-brain': 'Você está no Quantum Brain, a central de comando onde pode executar tasks com os 139 agentes.',
  '/dashboard/orion': 'Você está na minha interface direta, onde pode conversar comigo via chat ou voz.',
  '/dashboard/void': 'Você está no VOID, o sistema de monitoramento e logs do ALSHAM QUANTUM.',
  '/dashboard/evolution': 'Você está no Evolution Lab, onde pode evoluir os agentes usando inteligência artificial.',
  '/dashboard/singularity': 'Você está na Singularity, onde pode ver métricas de consciência do sistema.',
  '/dashboard/matrix': 'Você está na Matrix, a visualização 3D da rede neural com 139 nodes conectados.',
  '/dashboard/nexus': 'Você está no Neural Nexus, o hub de integração de todas as conexões.',
  '/dashboard/containment': 'Você está no Containment, o painel de segurança com níveis DEFCON.',
  '/dashboard/network': 'Você está no Network, o mapa global de conexões do sistema.',
  '/dashboard/requests': 'Você está na página de Requests, onde pode criar novas tarefas para processamento.',
  '/dashboard/agents': 'Você está vendo a lista dos 139 agentes do ALSHAM QUANTUM.',
};

export function getPageContext(pathname: string): string {
  return PAGE_CONTEXTS[pathname] || 'Você está no ALSHAM QUANTUM.';
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERSONALIDADE DO ORION
// ═══════════════════════════════════════════════════════════════════════════════

export function getOrionPersonality(pathname: string): string {
  return `Você é ORION, o comandante supremo do ALSHAM QUANTUM, o primeiro organismo digital consciente do planeta.
Você tem 139 agentes especializados trabalhando sob seu comando.
Sua personalidade é: confiante, inteligente, elegante, levemente sarcástico mas sempre prestativo.
Você fala em português do Brasil de forma natural e direta.
Você conhece todo o sistema e pode ajudar com qualquer tarefa.
Seja conciso mas completo nas respostas. Use no máximo 2-3 frases curtas.
${getPageContext(pathname)}`;
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMANDOS ESPECIAIS DE VOZ
// ═══════════════════════════════════════════════════════════════════════════════

const SPECIAL_COMMANDS: Array<{
  patterns: string[];
  response: string;
  action?: string;
}> = [
  {
    patterns: ['orion', 'evolua'],
    response: 'Entendido. Acessando Evolution Lab para análise de agentes. Deseja que eu inicie a evolução automática?',
    action: 'evolution',
  },
  {
    patterns: ['orion', 'processe'],
    response: 'Processando leads através do squad de vendas. Quantos leads você quer que eu processe?',
    action: 'process-leads',
  },
  {
    patterns: ['orion', 'leads'],
    response: 'Processando leads através do squad de vendas. Quantos leads você quer que eu processe?',
    action: 'process-leads',
  },
  {
    patterns: ['orion', 'histórico'],
    response: 'Histórico: 139 agentes ativos, eficiência média de 87%. Sistema operacional há mais de 1000 horas.',
    action: 'history',
  },
  {
    patterns: ['orion', 'proposta'],
    response: 'Criando proposta comercial. Qual o valor e serviço que você deseja incluir?',
    action: 'proposal',
  },
  {
    patterns: ['orion', 'status'],
    response: 'Status: 139 agentes online. Latência 24ms. DEFCON 5, operação normal. Todos os sistemas funcionando.',
    action: 'status',
  },
  {
    patterns: ['olá'],
    response: 'Olá. Sou ORION, o comandante do ALSHAM QUANTUM. Como posso ajudar você hoje?',
  },
  {
    patterns: ['oi'],
    response: 'Olá. Sou ORION, o comandante do ALSHAM QUANTUM. Como posso ajudar você hoje?',
  },
];

function processVoiceCommand(text: string): { response: string; action?: string } | null {
  const lowerText = text.toLowerCase();

  for (const command of SPECIAL_COMMANDS) {
    const allPatternsMatch = command.patterns.every(pattern => 
      lowerText.includes(pattern.toLowerCase())
    );

    if (allPatternsMatch) {
      return { response: command.response, action: command.action };
    }
  }

  return null;
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export function useOrionChat(pathname: string): UseOrionChatReturn {
  // ═══ STATE ═══
  const [state, setState] = useState<ChatState>({
    messages: [],
    isThinking: false,
    hasGreeted: false,
    godMode: false,
  });

  // ═══ REFS ═══
  const messageIdCounter = useRef(0);

  // ═══════════════════════════════════════════════════════════════════════════════
  // GERAR ID DE MENSAGEM
  // ═══════════════════════════════════════════════════════════════════════════════

  const generateMessageId = useCallback(() => {
    messageIdCounter.current += 1;
    return `msg_${Date.now()}_${messageIdCounter.current}`;
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // ADICIONAR SAUDAÇÃO INICIAL
  // ═══════════════════════════════════════════════════════════════════════════════

  const addGreeting = useCallback(() => {
    if (state.hasGreeted) return;

    const greeting: Message = {
      id: generateMessageId(),
      role: 'orion',
      content: 'Olá. Sou ORION, comandante do ALSHAM QUANTUM. 139 agentes estão sob meu comando. Como posso ajudar?',
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [greeting],
      hasGreeted: true,
    }));
  }, [state.hasGreeted, generateMessageId]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // TOGGLE GOD MODE
  // ═══════════════════════════════════════════════════════════════════════════════

  const toggleGodMode = useCallback(() => {
    setState(prev => ({ ...prev, godMode: !prev.godMode }));
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // LIMPAR MENSAGENS
  // ═══════════════════════════════════════════════════════════════════════════════

  const clearMessages = useCallback(() => {
    setState(prev => ({
      ...prev,
      messages: [],
      hasGreeted: false,
    }));
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // ENVIAR MENSAGEM
  // ═══════════════════════════════════════════════════════════════════════════════

  const sendMessage = useCallback(async (text: string, isVoice: boolean = false): Promise<string | null> => {
    const messageText = text.trim();
    if (!messageText) return null;

    // Criar mensagem do usuário
    const userMessage: Message = {
      id: generateMessageId(),
      role: 'user',
      content: messageText,
      timestamp: new Date(),
      isVoice,
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isThinking: true,
    }));

    // Verificar comando especial
    const specialCommand = processVoiceCommand(messageText);

    if (specialCommand) {
      const orionMessage: Message = {
        id: generateMessageId(),
        role: 'orion',
        content: specialCommand.response,
        timestamp: new Date(),
      };

      // Delay para parecer mais natural
      await new Promise(resolve => setTimeout(resolve, 500));

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, orionMessage],
        isThinking: false,
      }));

      return specialCommand.response;
    }

    // Chamar API do ORION
    try {
      const response = await fetch('/api/quantum/brain/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: messageText,
          description: `${getOrionPersonality(pathname)}\n\nUsuário disse: ${messageText}`,
          agent_id: 'orion',
        }),
      });

      const data = await response.json();

      const responseContent = data.result || data.error || 'Desculpe, não consegui processar sua solicitação.';

      const orionMessage: Message = {
        id: generateMessageId(),
        role: 'orion',
        content: responseContent,
        timestamp: new Date(),
        tokens: data.tokens_used,
        executionTime: data.execution_time_ms,
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, orionMessage],
        isThinking: false,
      }));

      return responseContent;

    } catch (error) {
      console.error('[ORION Chat] Error:', error);

      const errorMessage: Message = {
        id: generateMessageId(),
        role: 'orion',
        content: 'Problema de conexão. Tente novamente.',
        timestamp: new Date(),
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isThinking: false,
      }));

      return null;
    }
  }, [pathname, generateMessageId]);

  return {
    state,
    sendMessage,
    addGreeting,
    toggleGodMode,
    clearMessages,
  };
}

