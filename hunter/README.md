# 🎯 HUNTER X.1 — Runtime da Caça (Fase 2)

O corpo do caçador: um script TypeScript, sem framework de agente, que roda a liturgia diária do dossiê e deixa a fila de julgamento pronta pro tribunal.

## Liturgia (ordem exata)
1. Lê a missão `active` do Supabase. Sem missão = aborta + abre issue (nunca improvisa mandato).
2. Esvazia a quarentena (`hunter_raw_queue` não processada) **antes** de coletar o novo (Lei 8).
3. Coleta as 3 minas habilitadas na missão v1 (últimas 24h): arXiv, GitHub Search, Hacker News (Algolia). Retry com backoff (3 tentativas); fonte fora = `sources_fail+1` e "NÃO VERIFICADO".
4. Triagem barata contra as `scoring_rules`. Teto de custo v1: **300 itens/caça**; excedente vai pra quarentena com `queued_reason='rate'`.
5. Dedup semântica (pgvector, similaridade > 0.92 = já visto).
6. Análise profunda dos finalistas: resumo **próprio**, `relevance` + `relevance_why`, `single_source`, `license`, `kind`, arestas do grafo, e rascunho de Cápsula X.2 se `kind='soul'`.
7. Fecha `hunter_hunts` com números honestos + `cost_usd` real dos tokens.
8. Escreve `cacas/caca-AAAA-MM-DD.md` (formato do dossiê). O workflow abre o PR da caça = fila do tribunal.

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

## Fora de escopo (Fase 3+)
Cron 06:30, minas além das 3, auto-crítica da missão. Nada disso aqui.
