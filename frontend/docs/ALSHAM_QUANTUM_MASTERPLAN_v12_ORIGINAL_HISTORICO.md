# 🌌 ALSHAM QUANTUM v12.0 - MASTERPLAN SUPREMO
**"O Cockpit da Consciência Artificial"**

---

## 1. 🧬 MANIFESTO & VISÃO
**Objetivo:** Criar a interface definitiva para uma superinteligência de 57 agentes. Não é um dashboard administrativo; é um organismo vivo.
**Arquétipo:** O Mago Visionário (Poder, Mistério, Tecnologia, Luxo).
**Estética:** "Dark Glass Enterprise" + "Quantum Void". Preto absoluto, Neon Roxo, Ouro, Vidro Fosco.
**Sensação:** O usuário deve sentir que está pilotando uma nave alienígena ou o cérebro de uma divindade digital.

---

## 2. 🏗️ STACK TECNOLÓGICO (2025 STATE-OF-THE-ART)
*   **Framework:** Next.js 15 (App Router) + React 19 (Server Components).
*   **Estilização:** Tailwind CSS v4 (Alpha) + Shadcn/UI (Customizado) + Framer Motion (Animações).
*   **Visualização 3D:** Three.js + React Three Fiber + Drei (Partículas e Grafos).
*   **Gerenciamento de Estado:** Zustand (Leve, Rápido, Global).
*   **Dados em Tempo Real:** WebSockets (Python FastAPI) + React Query.
*   **Infraestrutura:** Vercel (Frontend) + Railway/Python (Cérebro).

---

## 3. 🗺️ AS 7 DIMENSÕES (ARQUITETURA DE PÁGINAS)

### 🛸 1. O COCKPIT (Home)
*   **Rota:** \`/dashboard\`
*   **Função:** Resumo executivo e saúde imediata.
*   **Componentes Chave:**
    *   **HUD Financeiro:** Contadores rolantes (CountUp.js) para ROI e Economia.
    *   **Status Grid:** 4 cartões holográficos monitorando os pilares (Security, Intel, Infra, Comms).
    *   **Live Stream:** Botão pulsante indicando conexão WebSocket ativa.

### 🧠 2. NEURAL NEXUS (A Rede)
*   **Rota:** \`/dashboard/network\`
*   **Função:** Visualização espacial da mente da IA.
*   **Visual:** Grafo 3D interativo. Nós (agentes) conectados por sinapses (linhas de luz).
*   **Interação:** Hover sobre um nó mostra o pensamento atual do agente. As linhas brilham quando há troca de dados.

### 🛡️ SENTINELAS (Operações)
*   **Rota:** \`/dashboard/agents\`
*   **Função:** Gerenciamento tático de tropa.
*   **Visual:** Tabela de vidro futurista.
*   **Drill-Down:** Clicar em um agente abre uma gaveta lateral (Sheet) com logs específicos, memória e controles manuais (Reiniciar/Pausar).

### 🧬 EVOLUTION LAB (Timeline)
*   **Rota:** \`/dashboard/evolution\`
*   **Função:** Histórico genético e futuro.
*   **Visual:** Timeline vertical interativa das Ondas 1, 2 e 3. Gráfico de DNA mostrando a melhoria do código ao longo do tempo.

### 📟 THE MATRIX (Logs)
*   **Rota:** \`/dashboard/matrix\`
*   **Função:** A verdade nua e crua do código.
*   **Visual:** Console Hacker (Verde/Preto). Fonte Monoespaçada.
*   **Intro Específica:** Ao entrar, digita letra por letra: *"Wake up, Bonaparte... The ALSHAM has you."*

### ⚙️ CORE SETTINGS (Configurações)
*   **Rota:** \`/dashboard/settings\`
*   **Função:** Casa de máquinas.
*   **Recursos:** Gerenciamento de API Keys mascaradas, Controle de Temperatura da IA, Logs de Auditoria.

### 🕳️ THE VOID (Easter Egg)
*   **Rota:** \`/dashboard/void\`
*   **Acesso:** Secreto. Digitar "KLAATU" no teclado.
*   **Visual:** Fundo preto absoluto. Visualização de áudio/ondas das threads do processador. Sem UI. Apenas a "alma" da máquina.

---

## 4. 🚨 PROTOCOLOS DE SEGURANÇA & INTERAÇÃO

### O BOTÃO DO JUÍZO FINAL (Panic Button)
*   **Local:** Header ou Settings.
*   **Mecânica:** Switch com capa de proteção virtual. Clique duplo para ativar.
*   **Efeito:** Som de Alarme de Submarino. Interface fica vermelha monocromática. Mensagem: "CONTAINMENT PROTOCOL ACTIVATED". Bloqueia todas as saídas da IA.

### FEEDBACK HÁPTICO VISUAL
*   **Cliques:** Todos os botões importantes emitem um som sutil de "Tech Click" e um brilho momentâneo.
*   **Notificações:** Toasts que deslizam com efeito de vidro fosco.

---

## 5. 📋 ESTEIRA DE PRODUÇÃO (CHECKLIST DE EXECUÇÃO)

### FASE 1: FUNDAÇÃO (✅ CONCLUÍDO PARCIALMENTE)
- [x] Setup Next.js 15 & Tailwind.
- [x] Limpeza de Arquivos Legados.
- [x] Deploy Vercel (Online).
- [x] Store Global (Zustand) com Dados Reais Mapeados.
- [x] Layout Base com Sidebar Fixa e Fundo Preto Absoluto.
- [x] Correção de Bugs Críticos (NaN, Three.js Duplicate).

### FASE 2: VISUALIZAÇÃO DE IMPACTO (🚧 EM ANDAMENTO)
- [ ] **Implementar o NEURAL NEXUS (Grafo 3D):** Usar `react-force-graph-3d` ou Three.js puro. Fazer os nós pulsarem.
- [ ] **Criar a Página MATRIX:** Implementar o efeito de digitação "Wake up" e o stream de logs simulado (preparando para o real).
- [ ] **Refinar o COCKPIT:** Adicionar os contadores rolantes (CountUp) no Dashboard.

### FASE 3: CONEXÃO VITAL (INTEGRAÇÃO BACKEND)
- [ ] Criar rota de API `/api/stream` no Next.js para receber WebSockets do Python.
- [ ] Conectar o `store.ts` ao endpoint do Supabase para ler o status real dos agentes.
- [ ] Implementar o "Panic Button" que envia um sinal de `STOP` para o backend Python.

### FASE 4: POLIMENTO & MAGIA
- [ ] Implementar o Easter Egg "The Void" (Key listener).
- [ ] Adicionar sons de interface (Sfx).
- [ ] Transições de página com Framer Motion (AnimatePresence).

---

## 6. DIRETRIZES DE CÓDIGO (REGRAS DE OURO)
1.  **Zero Quebras:** O sistema não pode ter erros de console (NaN, Hydration Error).
2.  **Performance:** O Dashboard deve carregar em menos de 1s.
3.  **Modularidade:** Componentes pequenos em `src/components`. Nada de arquivos gigantes.
4.  **Estética:** Se não parece "Enterprise Cyberpunk", refaça.

---

**DOCUMENTO GERADO EM:** 20/11/2025
**STATUS:** APROVADO PARA EXECUÇÃO.
