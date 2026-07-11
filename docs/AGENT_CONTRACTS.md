# ALSHAM QUANTUM — Agentes e Contratos

> 10 agentes reais executados server-side pelo motor em
> `frontend/src/lib/quantum-brain/` via `POST /api/quantum/brain/execute`.
> Sem chave de LLM, cada agente **degrada com honestidade**: devolve um
> resultado claro pedindo configuração — nunca dados fake (Lei da Honestidade).

## Como funciona

- `executeTask()` (`task-executor.ts`) cria `requests` + `quantum_tasks`,
  roteia para um agente, chama o LLM (OpenAI `gpt-4o-mini`) com um
  **system prompt específico do agente** e persiste o resultado via service role.
- Roteamento (`agent-router.ts`): `resolveAgentName()` casa palavras-chave →
  agente especialista; senão `resolveRole()` escolhe o role e pega o agente
  ativo de maior eficiência / menor carga.
- 4 agentes têm **comportamento tipado** (contratos em `agent-behaviors.ts`):
  system prompt próprio, `buildUserPrompt`, e `parse()` que mapeia a resposta
  do LLM para uma saída **estruturada e normalizada de forma determinística**.
  Os outros 6 usam o prompt genérico por role (fallback `DEFAULT_PROMPTS`).

## Agentes com contrato tipado

### LEAD MAGNET (`lead-magnet`, SPECIALIST)
Qualifica e pontua leads. Saída `lead_scoring`:
`{ leads: [{ name, score (0-100), tier: hot|warm|cold, rationale, suggested_action }], summary, next_actions }`.
`tier` é **derivado do score** de forma determinística (≥70 hot, ≥40 warm, senão cold); scores são clampados a 0-100.

### CONTENT CREATOR (`content-creator`, SPECIALIST)
Gera conteúdo multi-formato. Saída `content`:
`{ topic, pieces: [{ format: blog|social|email|ad, title, body, hashtags[], cta }], next_actions }`.
Formato inválido cai para `social`.

### EMAIL SEQUENCE BOT (`email-sequence-bot`, SPECIALIST)
Monta cadência de e-mails. Saída `email_sequence`:
`{ audience, steps: [{ step, delay_days (≥0), subject, body, goal }], total_duration_days, next_actions }`.
`step` é reindexado (1..n) e `total_duration_days` é a **soma** dos `delay_days` (determinístico).

### DATA MINER (`data-miner`, ANALYST)
Agrega métricas **REAIS** da frota (não do LLM) e gera insights sobre elas. Saída `data_mining`:
`{ metrics: { total_agents, active_agents, by_role, average_efficiency }, insights[], recommendations[] }`.
`metrics` vem de `aggregateAgentStats()` sobre a tabela `agents` — mesmo sem LLM as métricas reais são preservadas.

## Agentes genéricos (prompt por role)

`ORCHESTRATOR ALPHA` (CORE), `SECURITY GUARDIAN` (GUARD), `REVENUE HUNTER`,
`SOCIAL ENGAGER`, `ADS OPTIMIZER` (SPECIALIST) e `BACKUP KEEPER` (GUARD)
executam com o system prompt do `metadata.system_prompt` (seed) ou o default
do role, retornando JSON livre. São candidatos naturais a ganhar contrato tipado.

## Testes

`frontend/src/__tests__/lib/quantum-brain/`:
- `agent-router.test.ts` — roteamento por keyword → agente/role.
- `agent-behaviors.test.ts` — parse/normalização dos 4 contratos + agregação real.
- `task-executor.test.ts` — transições IDLE→PROCESSING→IDLE, custo, degradação sem chave.
