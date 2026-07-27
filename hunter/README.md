# 🎯 HUNTER X.1 — Runtime da Caça (Fase 3: O Relógio)

O corpo do caçador: um script TypeScript, sem framework de agente, que roda a liturgia diária do dossiê e deixa a fila de julgamento pronta pro tribunal.

## Liturgia (ordem exata)
1. Lê a missão `active` do Supabase. Sem missão = aborta + abre issue (nunca improvisa mandato).
2. Esvazia a quarentena (`hunter_raw_queue` não processada) **antes** de coletar o novo (Lei 8).
3. Coleta as 3 minas habilitadas na missão v1 (últimas 24h): arXiv, GitHub Search, Hacker News (Algolia). Retry com backoff (3 tentativas); fonte fora = `sources_fail+1` e "NÃO VERIFICADO".
4. Triagem barata contra as `scoring_rules`. Teto de custo v1: **300 itens/caça**; excedente vai pra quarentena com `queued_reason='rate'`.
5. Dedup semântica (pgvector, similaridade > 0.92 = já visto).
6. Análise profunda dos finalistas: resumo **próprio**, `relevance` + `relevance_why`, `single_source`, `license`, `kind`, arestas do grafo, e rascunho de Cápsula X.2 se `kind='soul'`.
7. Fecha `hunter_hunts` com números honestos + `cost_usd` real dos tokens.
8. Escreve `caça/AAAA-MM-DD.md` na raiz do repo (caminho canônico do dossiê). O workflow abre o PR da caça = fila do tribunal.

## Blindagem (Lei 3 — prompt injection)
- Todo conteúdo coletado entra nos prompts como **dado inerte** entre marcas `<<<DADO>>>`, com instrução explícita de ignorar comandos embutidos.
- Saída **sempre** JSON estruturado validado por `zod`. Se a análise falhar: itens pra quarentena, hunt fecha `partial` — nunca silenciosamente.
- O runtime não tem nenhuma ferramenta de ação além de escrever nas tabelas `hunter_*` e no relatório. Mesmo enganado, não alcança nada.

## Motor de IA (vendor-neutral)
O runtime fala com um endpoint **OpenAI-compatível** definido por env (`HUNTER_AI_BASE_URL`, `HUNTER_AI_API_KEY`, `HUNTER_*_MODEL`). O nome do fornecedor não aparece no código (Lei do CLAUDE.md) — é configuração de engenharia.

## Como rodar (local)
```bash
cd hunter
npm install
# exporte as variáveis (ver seção Segredos)
npm run hunt
```
O relatório sai em `caça/AAAA-MM-DD.md` na raiz do repo (um nível acima de `hunter/`). Para mudar, use `HUNTER_REPORT_DIR`.

## Segredos / variáveis necessárias
**Secrets (Actions → Secrets):**
- `HUNTER_SUPABASE_URL` — `https://vktzdrsigrdnemdshcdp.supabase.co`
- `HUNTER_SUPABASE_SERVICE_ROLE_KEY` — service role key do projeto `suna-core`
- `HUNTER_AI_BASE_URL` — endpoint OpenAI-compatível do motor (`.../v1`)
- `HUNTER_AI_API_KEY` — chave do motor de IA

**Variables (Actions → Variables, não-secretas):**
- `HUNTER_TRIAGE_MODEL`, `HUNTER_ANALYSIS_MODEL`, `HUNTER_EMBED_MODEL`
- (opcionais p/ custo real em US$) `HUNTER_PRICE_TRIAGE_IN`, `HUNTER_PRICE_TRIAGE_OUT`, `HUNTER_PRICE_ANALYSIS_IN`, `HUNTER_PRICE_ANALYSIS_OUT`, `HUNTER_PRICE_EMBED` (US$/1M tokens)

**Automático:** `GITHUB_TOKEN` (o Actions injeta) — basta permitir Actions criar PRs.

## Antes da 1ª caça
Aplicar a migration `supabase/migrations/20260726_hunter_x1_dedup_fn.sql` no `suna-core` (função de dedup). O embedding é `vector(1024)`; o `HUNTER_EMBED_MODEL` precisa entregar 1024 dimensões (o runtime pede `dimensions: 1024`).

## Fase 3 — O RELÓGIO

### 1. Cron 06:30 BRT
`.github/workflows/hunter.yml` roda `cron: "30 9 * * *"` — **09:30 UTC = 06:30 America/Sao_Paulo** (BRT é UTC-3 o ano inteiro; o Brasil extinguiu o horário de verão em 2019). Depois da Ronda (06:00 BRT). O `workflow_dispatch` continua valendo.

### 2. Fila pendente ressurge
Todo relatório traz a seção **FILA PENDENTE DE JULGAMENTO**: todos os `hunter_findings` com `verdict='pending'` de caças **anteriores**, ordenados por relevância desc. Sem isso o pendente de ontem some no banco e nunca chega ao tribunal. A query falhar não derruba a caça — vira `NÃO VERIFICADO` no relatório (Lei 7).

### 3. Ameaça abre issue na hora
`kind='threat'` com `relevance >= 90` abre issue `[HUNTER] Ameaça: <title>` **na própria caça**, sem esperar o relatório. Idempotente pelo título exato: o runtime lista as issues com label `hunter` (open+closed) no começo da caça e não reabre o que já existe. Usa a API de **listagem**, não a de busca — busca tem atraso de indexação e deixaria passar duplicata.

### 4. Checagens da Ronda
`npm run ronda` (`src/ronda.ts`) roda as três provas do caçador:

| Checagem | Promessa | Prova |
|---|---|---|
| HUNTER rodou nas últimas 24h | roda todo dia 06:30 | última `hunter_hunts` `done`/`partial` com `finished_at` < 24h |
| RLS nega anônimo | migration declara `anon` NEGADO | query **anônima real** nas 6 tabelas `hunter_*` |
| Quarentena não cresce sem limite | Lei 8: quarentena é transitória | `count` de `raw_queue` não processada ≤ teto (padrão **500**, via `HUNTER_QUARANTINE_MAX`) |

Roda em `.github/workflows/ronda-hunter.yml` às **09:00 UTC = 06:00 BRT**, antes da caça.

**`NÃO VERIFICADO` não é `OK`.** Sem `SUPABASE_ANON_KEY` a prova de RLS sai como não verificada — nunca como aprovada. Se **nenhuma** checagem puder ser provada, a Ronda está cega e **falha** (exit 1): ronda cega não passa por verde.

Read-only por lei: detecta e relata (issue com `RONDA_OPEN_ISSUE=true`). Nunca corrige.

### Prova das peças 2 e 3
```bash
cd hunter && npm run prova
```
Exercita `writeReport` e `openThreatIssue` reais, sem tocar no banco de produção.

### Segredo/variável novos na Fase 3
- `HUNTER_SUPABASE_ANON_KEY` (secret) — chave **anônima** do `suna-core`, só para a prova de RLS. Sem ela a checagem sai `NÃO VERIFICADO`.
- `HUNTER_QUARANTINE_MAX` (variable, opcional) — teto da quarentena. Padrão 500.

## Fora de escopo (Fase 4+)
Minas além das 3, auto-crítica da missão. Nada disso aqui.
