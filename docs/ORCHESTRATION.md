# ALSHAM QUANTUM — Orquestração Multi-Agente

> ORCHESTRATOR ALPHA deixou de ser genérico: agora é o orquestrador real
> que faz os agentes especialistas trabalharem JUNTOS. Módulo:
> `frontend/src/lib/quantum-brain/orchestrator.ts`. Skills:
> `frontend/src/lib/quantum-brain/skills.ts`.

## Arquitetura: plano → delegação → encadeamento → síntese

```
Objetivo (alto nível)
   │
   ▼  decomposeObjective()  (PURO/determinístico)
Plan { steps: [{ skill, agentId, dependsOn }] }
   │
   ▼  orchestrate()  (executa em ordem)
para cada passo:
   • resolve skill → agente especialista tipado
   • monta input = objetivo + { upstream: saídas das dependências }
   • executeTask(agent) → persiste em requests/quantum_tasks/agent_logs
   • guarda a saída para alimentar o próximo passo
   │
   ▼
PlanResult { plan, steps[], trace[], configured, summary }
```

1. **Plano (decomposição).** `decomposeObjective(objective)` é determinístico:
   casa palavras-chave do objetivo com skills e monta os passos na ordem
   canônica do pipeline, encadeando `dependsOn` de forma linear. Sem match →
   pipeline de crescimento completo (papel padrão do ORCHESTRATOR ALPHA).
2. **Delegação por skill.** Cada passo resolve `skill → agente` via o registro
   de skills. O agente é executado pelo seu contrato tipado (`agent-behaviors.ts`).
3. **Encadeamento (saída → input).** A saída de um passo entra no `data.upstream`
   do passo seguinte (chaveado pela skill de origem). Como o `buildUserPrompt`
   do agente serializa `data`, o LLM do passo N enxerga o resultado do passo N-1.
4. **Síntese + rastro.** `PlanResult` agrega as saídas tipadas, o `trace`
   (qual agente fez cada passo e com que status) e um `summary` honesto.

## Fluxo-exemplo (ponta a ponta)

`aggregate-stats` → `score-leads` → `generate-copy` → `build-sequence`

| # | Skill | Agente | Faz |
|---|-------|--------|-----|
| 1 | aggregate-stats | DATA MINER | agrega métricas REAIS da frota (determinístico) |
| 2 | score-leads | LEAD MAGNET | pontua leads (usa contexto do passo 1) |
| 3 | generate-copy | CONTENT CREATOR | gera copy para o segmento quente (passo 2) |
| 4 | build-sequence | EMAIL SEQUENCE BOT | monta a cadência de e-mails (passo 3) |

O teste `orchestrator.test.ts` prova o encadeamento: o prompt do LEAD MAGNET
contém as métricas do DATA MINER; o do CONTENT CREATOR contém o lead quente
(`ACME_HOT`); o do EMAIL SEQUENCE BOT contém o tópico do CONTENT CREATOR.

## Modelo de Skills

Uma **skill** é uma capacidade nomeada e reutilizável provida por um agente
(SSOT do mapeamento em `skills.ts`). Cada behavior declara `provides: SkillId[]`,
e um teste garante que não há drift entre `provides` e o registro `SKILLS`.

| Skill | Agente | requiresLLM |
|-------|--------|-------------|
| aggregate-stats | data-miner | **false** (determinística) |
| score-leads | lead-magnet | true |
| generate-copy | content-creator | true |
| build-sequence | email-sequence-bot | true |

## Determinístico vs. precisa de LLM

- **Determinístico (roda sempre, sem chave):** decomposição do plano, resolução
  skill→agente, agregação real do DATA MINER (`aggregate-stats`), derivação de
  tier/soma de duração/normalização nos contratos.
- **Precisa de LLM:** a geração de conteúdo textual (leads sugeridos, copy,
  assuntos de e-mail, insights).

## Degradação honesta (Lei da Honestidade)

Sem `OPENAI_API_KEY`, `orchestrate()` **ainda devolve o plano completo**. Cada
passo é marcado:
- `partial` — skill determinística que produziu saída real (ex.: DATA MINER
  devolve as métricas reais; `insights: []`, sem nada inventado);
- `requires_configuration` — passo que precisa de LLM e ficou pendente;
- `completed` — executado com LLM;
- `failed` — erro.

Nunca há saída falsa. O `summary` reporta a contagem por status.

## Persistência (rastro auditável)

- Plano e conclusão: `agent_logs` (`event_type` `orchestration_plan` /
  `orchestration_complete`) sob `orchestrator-alpha`.
- Cada passo: `executeTask` grava `requests` + `quantum_tasks` + `agent_logs`
  (via service role), com `task_id` referenciado em cada `StepResult`.

## Como acionar (API)

`POST /api/quantum/brain/execute` com um objetivo de alto nível:

```json
{ "objective": "Lançar campanha de crescimento" }
```

Também aciona a orquestração `agent_id: "orchestrator-alpha"` ou
`mode: "orchestrate"`. Requer usuário autenticado (FK `requests.user_id`).
A resposta traz `plan`, `steps`, `trace`, `configured` e `summary`.
