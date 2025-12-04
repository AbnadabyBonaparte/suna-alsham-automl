# 🧬 Sistema de Processamento de Agents - Suna Alsham AutoML

## 📋 Visão Geral

Este documento explica o sistema de processamento de requests pelos agents, implementado para fazer os 139 agents do banco **REALMENTE** processarem tarefas!

## 🎯 O Problema

- ✅ Existiam 139 agents no banco
- ❌ Nenhum processava tarefas
- ❌ `last_active` estava parado há 10+ dias
- ❌ Requests ficavam em "queued" para sempre

## ✨ A Solução

Implementamos 3 componentes principais:

### 1. API Route: `/api/process-request`

**Localização:** `frontend/src/app/api/process-request/route.ts`

**Funcionalidade:**
- Recebe `request_id` no body
- Busca a request no Supabase
- Seleciona um agent disponível (`status='idle'`)
- Chama OpenAI API (gpt-4o-mini) com o prompt do agent
- Salva resultado no banco
- Atualiza status da request para `completed`
- Atualiza `last_active` do agent

**Exemplo de uso:**
```bash
curl -X POST http://localhost:3000/api/process-request \
  -H "Content-Type: application/json" \
  -d '{"request_id": "uuid-da-request"}'
```

**Resposta de sucesso:**
```json
{
  "success": true,
  "request_id": "uuid-da-request",
  "agent_id": "agent-123",
  "agent_name": "Alhambra-001",
  "result": "Resposta da OpenAI aqui...",
  "message": "Request processada com sucesso"
}
```

### 2. API Route: `/api/agents/heartbeat`

**Localização:** `frontend/src/app/api/agents/heartbeat/route.ts`

**Funcionalidade:**
- **POST:** Atualiza `last_active` de todos agents idle
- **GET:** Retorna estatísticas dos agents (total, idle, processing, etc)

**Exemplo de uso:**
```bash
# Atualizar heartbeat
curl -X POST http://localhost:3000/api/agents/heartbeat

# Consultar status
curl http://localhost:3000/api/agents/heartbeat
```

**Resposta GET:**
```json
{
  "success": true,
  "stats": {
    "total": 139,
    "idle": 135,
    "processing": 4,
    "active": 0,
    "offline": 0
  },
  "agents": [...],
  "timestamp": "2025-12-04T02:00:00.000Z"
}
```

### 3. Interface na Página de Agents

**Localização:** `frontend/src/app/dashboard/agents/page.tsx`

**Funcionalidade:**
- Botão "Processar Request de Teste" em cada agent
- Ao clicar:
  1. Cria uma request de teste no banco
  2. Chama `/api/process-request` para processá-la
  3. Mostra resultado em tempo real
  4. Atualiza a página após 2 segundos

**UI:**
- ⚡ Botão com gradiente animado
- 🔄 Loading spinner durante processamento
- ✅ Banner verde com sucesso
- ❌ Banner vermelho com erro

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `frontend/.env.local` com as seguintes variáveis:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua_anon_key
SUPABASE_SERVICE_ROLE_KEY=sua_service_role_key

# OpenAI
OPENAI_API_KEY=sk-proj-...
```

### Dependências

O OpenAI SDK foi adicionado ao projeto:

```bash
cd frontend
npm install openai
```

## 🚀 Como Usar

### 1. Processar Request Manualmente

1. Acesse `/dashboard/agents`
2. Clique em qualquer agent
3. No modal, clique em "Processar Request de Teste"
4. Aguarde o processamento
5. Veja o resultado!

### 2. Processar Request via API

```javascript
// Criar request
const { data: newRequest } = await supabase
  .from('requests')
  .insert({
    user_id: 'uuid-do-usuario',
    title: 'Minha tarefa',
    description: 'Descrição detalhada',
    status: 'queued',
    priority: 'normal'
  })
  .select()
  .single();

// Processar
const response = await fetch('/api/process-request', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ request_id: newRequest.id })
});

const result = await response.json();
console.log(result);
```

### 3. Atualizar Heartbeat (Automatizado)

Para manter os agents "vivos", você pode configurar um cron job:

```bash
# A cada 5 minutos
*/5 * * * * curl -X POST http://localhost:3000/api/agents/heartbeat
```

Ou usar um serviço como Vercel Cron:

```json
// vercel.json
{
  "crons": [{
    "path": "/api/agents/heartbeat",
    "schedule": "*/5 * * * *"
  }]
}
```

## 📊 Schema do Banco de Dados

### Tabela: `agents`

```sql
- id: uuid (PK)
- name: text
- role: text (GUARD, CORE, ANALYST, SPECIALIST)
- status: text (idle, processing, active, offline)
- efficiency: numeric
- current_task: text
- last_active: timestamp
- created_at: timestamp
```

### Tabela: `requests`

```sql
- id: uuid (PK)
- user_id: uuid (FK)
- title: text
- description: text
- status: text (queued, processing, completed, failed)
- priority: text (low, normal, high)
- created_at: timestamp
- updated_at: timestamp
```

## 🎯 Próximos Passos

1. **Background Queue:** Implementar fila automática para processar requests em background
2. **Worker Process:** Deploy de worker no Railway/Render para processar continuamente
3. **Webhooks:** Notificações quando requests forem completadas
4. **Retry Logic:** Re-tentar requests que falharam
5. **Métricas:** Dashboard com estatísticas de processamento

## 🐛 Debug

Para ver logs do processamento:

```bash
# Terminal 1: Iniciar Next.js
cd frontend
npm run dev

# Terminal 2: Acompanhar logs
tail -f .next/trace
```

Ou veja os logs diretamente no console do navegador (F12).

## ⚠️ Importante

- **Timeout:** As Edge Functions têm timeout de 60 segundos
- **Custo:** Estamos usando `gpt-4o-mini` para economizar ($0.15/1M tokens)
- **Concorrência:** Apenas 1 agent processa por vez (por request)
- **Segurança:** Service Role Key permite bypass de RLS - use com cuidado!

## 🎉 Resultado

Agora os agents estão VIVOS! 🧬

- ✅ Processam requests de verdade
- ✅ `last_active` é atualizado
- ✅ Status muda dinamicamente (idle → processing → idle)
- ✅ Resultados salvos no banco
- ✅ Interface visual mostra tudo em tempo real

---

**Implementado por:** Claude Code
**Data:** 2025-12-04
**Status:** ✅ FUNCIONANDO
