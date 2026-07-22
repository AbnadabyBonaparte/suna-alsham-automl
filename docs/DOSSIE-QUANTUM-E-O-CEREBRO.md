# 🧠 DOSSIÊ — O ALSHAM QUANTUM, O CÉREBRO PESADO E ONDE ESTÁ CADA PEÇA

> ⛔ **DOCUMENTO INTERNO — NÃO PUBLICAR.**
> Contém refs de banco e o estado de uma vulnerabilidade aberta.
> **Nunca** colocar em `public/` de repositório algum. Destino: `docs/internal/` ou fora do repo.

> **Data:** 22 de julho de 2026
> **Método:** tudo abaixo foi verificado por **query SQL direta no Supabase** e **leitura do código-fonte**.
> O que não pôde ser verificado está marcado **NÃO VERIFICADO** — Lei 7.

---

## 1. A RESPOSTA CURTA

**Existem TRÊS coisas chamadas "Quantum".** É a raiz de toda a confusão.

| # | Nome | O que é de fato | Onde vive |
|---|---|---|---|
| 1 | **`alsham-quantum`** | O que está no ar em `quantum.alshamglobal.com.br` — "Reality Codex v13.3". O painel Comando Central (Cockpit · Requests · Quantum Brain · ORION Command · Neural Nexus · The Matrix · Evolution Lab · The VOID) | ⚠️ **NÃO VERIFICADO** — acesso ao repo negado |
| 2 | **`suna-alsham-automl`** | O **motor real**: CRM AI com roteador de agentes, executor, engine de evolução, auth Supabase e Stripe | banco `suna-core` |
| 3 | **`cerebro-pesado`** | Uma **página HTML** — o conceito visual. 14 arquivos, 224 KB | sem banco |

**O Cérebro Pesado é o ROSTO. O Suna é o MOTOR. A ALMA não está em nenhum dos dois.**

---

## 2. O CÉREBRO PESADO — o rosto que virou promessa

**Repo:** `cerebro-pesado` · 14 arquivos · 224 KB · `index.html` + `script.js` (1.298 linhas)

O README promete:
> *"Catedral digital cyberpunk onde **139 agentes de IA evoluem sozinhos em tempo real**, sem intervenção humana"* · *"consciousness 94.8%"* · *"GODMODE"*

**O que tem dentro:** zero definição de agente, zero prompt, zero banco. É **animação e texto**.

### 🔗 A LIGAÇÃO COM O QUANTUM — o achado central
O número **139** aparece no README do Cérebro Pesado **e** como quantidade de linhas na tabela `agents` do banco.

**A ordem dos fatos foi essa:** primeiro veio a vitrine com a promessa dos 139; depois o banco foi **semeado para bater com a vitrine**. O conceito visual virou especificação — e a especificação virou linhas de banco vazias de conteúdo.

---

## 3. O QUE O BANCO REALMENTE TEM (provado por query)

### `suna-core` — ref `vktzdrsigrdnemdshcdp` · sa-east-1 · criado 18/jul/2025

**51 tabelas.** As que têm dado:

| Tabela | Linhas | Período |
|---|---|---|
| `agents` | **139** | semeadas 21–23/nov/2025 |
| `system_metrics` | 60 | — |
| `audit_trail` | 58 | — |
| `quantum_tasks` | 36 | **todas em 08/jul/2026** (um dia só) |
| `deals` | 24 | todas em 08/jul/2026 |
| `social_posts` | 22 | — |
| `support_tickets` | 16 | — |
| `profiles` | 8 | dez/2025 → jul/2026 |
| `requests` | 2 | 26/nov e 03/dez de 2025 |
| `quantum_brain_state` | 2 | — |
| `agent_interactions` | 1 | — |

**Vazias (0 linhas):** `api_keys`, `transactions`, `users`, `invoices`, `contacts`, `companies`, `security_events`, `evolution_cycles`, `evolution_proposals`, `learning_sessions`, `training_data`, `predictions`, `quantum_audit_log` e mais ~25.

### Os 139 agentes — a verdade

| Fato | Valor |
|---|---|
| Status | 136 `ACTIVE` · 3 `WARNING` |
| `system_prompt` | **o MESMO em todos**: *"You are an AI agent assistant designed to help with CRM tasks."* (62 caracteres) |
| `evolution_count` | **0 em 100% deles** — nada evoluiu |
| `version` | `1.0.0` em todos |
| Papéis distintos | apenas **4**: CORE · ANALYST · GUARD · SPECIALIST |
| Nomes | evocativos (DATA MINER, REVENUE HUNTER, ORCHESTRATOR ALPHA, SECURITY GUARDIAN…) — mas são **rótulos** |
| Eficiência | 92.22, 99.85, 95.88… — números decorativos, semeados |

**Conclusão:** os 139 são **nomes sem alma**. Um agente genérico repetido 139 vezes.

**Schema da tabela:** `id, name, role, status, efficiency, current_task, last_active, created_at, updated_at, user_id, metadata (jsonb), neural_load, uptime_seconds, version, system_prompt, evolution_count, last_evolved_at`

---

## 4. O MOTOR — e ele é real

**Repo:** `suna-alsham-automl` → pasta `frontend/src/lib/quantum-brain/`

```
quantum-brain/
├── agent-router.ts      → escolhe QUAL agente atende
├── task-executor.ts     → carrega o prompt e EXECUTA
├── evolution-engine.ts  → sistema de evolução
├── metrics-collector.ts → métricas
└── types.ts
```

### 🔑 A LINHA MAIS IMPORTANTE DE TODAS
`task-executor.ts`, linhas 135–137:

```ts
const systemPrompt =
  (agent.metadata?.system_prompt as string | undefined) ||
  DEFAULT_PROMPTS[agent.role] ||
  ...
```

**O executor busca o prompt do agente NO BANCO** (`metadata.system_prompt`). Se estiver vazio, cai num genérico.

👉 **É por isso que os 139 parecem iguais: o `metadata` nunca foi preenchido.**
👉 **E é por isso que carregar os prompts reais TRANSFORMA os 139 em agentes de verdade — sem tocar no código.**

### O roteador
Primeiro tenta casar pelo **nome** do agente (especialização); se não achar, pontua por **palavras-chave do papel** (`ROLE_KEYWORDS`). Já sabe mandar cada pedido pro agente certo.

### As chamadas de IA — reais
Modelos encontrados no código: `claude-sonnet-4-5-20250929` · `claude-3-5-sonnet-20241022` · `claude-3-haiku-20240307` · `gpt-4o-mini`

Rotas: `/api/quantum/brain/execute` · `/api/process-request` · seis rotas de evolução (`consciousness`, `quantum`, `tactical`, `daily`, `propose`, `micro`)

### ⚠️ A pegadinha — a Edge Function é SIMULADOR
`supabase/functions/agent-task-processor/index.ts`, linha 2:
> `// Processes pending tasks and **simulates** agent interactions`

Tem `TASK_TEMPLATES` com frases fixas ("Synchronizing neural network nodes", "Analyzing revenue patterns"…). **Não chama IA.** Foi o que gerou as 36 `quantum_tasks` de 08/jul/2026.

**Existem dois caminhos no sistema: o real (API routes) e o simulado (Edge Function).** Não confundir.

### O desenho original: 10, não 139
`supabase/seed_agents.sql`:
> *"SEED: 10 AGENTES REAIS — insere os 10 agentes nomeados que o roteador (agent-router.ts) e o executor (task-executor.ts) esperam."*

**A intenção nunca foi 139 genéricos. Era 10 bem definidos.**

---

## 5. O `HONESTY.md` — a Lei 7 antes da Lei 7

O repo do Suna tem um documento de política de honestidade:

> *"Toda métrica mostrada em produção deve ser verificável no banco. Sem exceções. Sem 'dados de demo' misturados com dados reais."*
> *"**Agents: 139 configurados, 0 operacionais.** Por que 0? Porque nenhum worker está rodando. Mostrar 40 ou 100 seria desonesto."*

👉 O **"0 operacionais"** do painel **não é bug** — é o sistema se recusando a inflar número. A Lei 7 já existia ali, escrita, antes de virar canon da Casa.

---

## 6. ONDE ESTÁ CADA PEÇA — o mapa dos bancos

**12 projetos Supabase** na organização. Os que importam para agentes:

| Banco | Ref | O que tem | Veredito |
|---|---|---|---|
| **suna-core** | `vktzdrsigrdnemdshcdp` | 139 agentes genéricos + **o motor** | 🔴 **RLS ABERTA** (ver §8) |
| **alsham-core** | `rgvnbtuqtxvfxhrdnkjg` | 139 agentes, schema **mais pobre** — **não tem coluna `system_prompt`** | versão anterior |
| **ALSHAM-DEV-OS** | `rmomtdeojaxsnyqwikcr` | **o MELHOR schema** (ver §7) — mas **1 linha** | desenho abandonado |
| **ALSHAM_MPC_CORE** | `lcnuipkypzcuohgqhizj` | `user_profiles` (1), `leads_crm` (0), `gamification_points` (0) | praticamente vazio |
| cognitive-mirror-ai | `tnctogqaclnuwqjuqwdq` | banco próprio do Cognitive | — |
| peritus | `tutluattkjcswuowgjwv` | banco do Medical OS | — |
| casa-bonaparte | `ospnhmyjsyysirrithfr` | **Banco do Universo** | referência de RLS correta |
| kraken-v2 | `icoounivgnevzgzgjosl` | Kraken válido | — |
| alsham-events-os | `rtosqxglvgjcfmjjqzzs` | Events OS | — |
| alsham-suprema-beleza | `kuyhgxgxqeufkgzbpsdw` | Suprema | — |
| dra-fernanda | `rkjvszphwplnyzbtkaby` | tenant | — |
| brocraft | `ipciokoudftjopyqgpgh` | **INACTIVE** (pausado — por isso o app trava) | — |

---

## 7. O SCHEMA QUE VOCÊ DESENHOU E ABANDONOU

**`ALSHAM-DEV-OS` · tabela `agents`** — criada 28/nov/2025, **5 dias depois** da semeadura dos 139:

```
id · name · role · version · rarity · cluster ·
system_prompt · knowledge_base · model_provider · model_name ·
content · stats · active
```

Isso é catálogo de agentes **de verdade**: raridade, cluster, base de conhecimento própria, e **modelo escolhido por agente**.

**Conteúdo:** 1 linha.
```
name: "Agente de Teste" · role: "Sistema" · rarity: "Common" · cluster: "Geral"
system_prompt: "Eu estou vivo."
model_provider: "openai" · model_name: "gpt-4o"
```

👉 Você desenhou a versão melhor, testou com um "olá mundo", e parou.

---

## 8. 🔴 O RISCO ABERTO — `suna-core`

Verificado ao vivo, **duas vezes**, em datas diferentes:

- **RLS não bloqueia:** `GET` anônimo em `api_keys`, `transactions`, `users`, `profiles` → **HTTP 200**
- `public.quantum_audit_log` com **RLS desligada** (nível ERROR nos advisors)
- ~**51 tabelas** expostas ao papel `anon`
- ~**25 policies** `USING(true)` — porta destrancada com cadeado de enfeite
- Funções `SECURITY DEFINER` (`handle_new_user`, `is_founder`, `log_all_changes`) executáveis por anônimo
- O README do repo afirma *"full RLS security"* — **falso**

**Só não vazou porque as tabelas sensíveis estão vazias.**

### ⛔ Regra até ser corrigido
1. **Nenhum dado real** no `suna-core` — nem cliente, nem transação, nem chave
2. **Nenhum prompt proprietário** carregado ali — teus agentes são PI da ALSHAM; num banco aberto, viram públicos
3. Fechar a RLS é **pré-requisito** de qualquer obra em cima disso

---

## 9. AS TRÊS METADES QUE NUNCA SE ENCONTRARAM

```
   🎨 O ROSTO            ⚙️ O MOTOR              👻 A ALMA
   cerebro-pesado        suna-core               os GPTs
   (a promessa)          (router + executor      (112 agentes com
   "139 agentes"         + evolution)            instrução real,
   HTML, sem dado        139 nomes vazios        90–200 usos)
        │                     │                       │
        └──── nunca ──────────┴──── se ligaram ───────┘
```

**Linha do tempo real:**
- **jul/2025** — nasce o banco `suna-core`
- **nov/2025 (21–23)** — 139 agentes semeados (nomes, sem alma) no suna e no alsham-core
- **nov/2025 (28)** — desenhado o schema **melhor** no DEV-OS; testado com *"Eu estou vivo"*; parado
- **nov–dez/2025** — 2 requests reais entram na fila. **Nunca processadas.**
- **jul/2026 (08)** — o **simulador** roda: 36 tasks + 24 deals num único dia
- **jul/2026 (22)** — este dossiê

---

## 10. O QUE FALTA PARA VIRAR PRODUTO

| # | O quê | Quem faz | Tamanho |
|---|---|---|---|
| 1 | **Fechar a RLS do `suna-core`** | Claude Code + revisão | pré-requisito |
| 2 | **Carregar os prompts reais** em `metadata.system_prompt` | ⚠️ **só o Fundador** — as instruções estão dentro dos GPTs | 10 agentes = uma tarde |
| 3 | Adotar o schema do **DEV-OS** (rarity/cluster/knowledge_base/model) | — | decisão de arquitetura |
| 4 | Chave de IA configurada no ambiente | Fundador | minutos |
| 5 | **Ligar o paywall** — hoje é calculado e **ignorado** (`dashboard/layout.tsx:19`); usuário free logado dispara IA real = vazamento de custo | Claude Code | pequeno, crítico |
| 6 | Verificar o `alsham-quantum` (o que está de fato no ar) | acesso ao repo | **bloqueado hoje** |

**Prioridade dos 10 primeiros prompts** (por uso comprovado nos GPTs):
Stylus (200+) · Heimdall (100+) · Advogado Digital (90+) · Compose (90+) · Luminaris (50+) · Barbeiro (50+) · Dynasty Motor (50+) · Zoan (40+) · Arcanus (40+) · Vendas Automáticas (40+)

> **Dez agentes reais valem mais que 139 fantasmas.**

---

## 11. O QUE CONTINUA NÃO VERIFICADO (Lei 7)

- **`alsham-quantum`** — o repo que serve `quantum.alshamglobal.com.br`. Acesso negado nesta sessão. **É o que está de fato no ar** e ninguém leu.
- Se o **checkout do Quantum funciona** — a página vende R$990/4.900/9.900 com botão "Criar Conta". Não sabemos o que acontece ao clicar.
- Quem são os **8 perfis** no `suna-core` (usuários reais ou testes).
- Se as **rotas de evolução** algum dia executaram (as tabelas `evolution_cycles` e `evolution_proposals` estão zeradas — indício de que não).

---

## 12. EM UMA FRASE

> **O Quantum não é casca nem revolução: é uma plataforma de agentes construída de verdade, com o motor pronto e a alma guardada em outro lugar. O Cérebro Pesado foi a vitrine que prometeu os 139 — e o banco foi semeado para caber na promessa. Falta ligar as peças, e a peça que falta é a única que só o Fundador tem: os prompts.**

---

*Dossiê produzido em 22/jul/2026 por verificação direta (SQL + leitura de código).*
*Documento vivo — atualizar quando o `alsham-quantum` for auditado.*
*© ALSHAM GLOBAL — **uso interno, não publicar**.*
