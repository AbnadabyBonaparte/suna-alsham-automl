# 🎯 HUNTER X.1 — O Caçador do Santuário

Os OLHOS PARA FORA do Universo Bonaparte. Enquanto o SENTINELA olha para
dentro (universo vs canon), o HUNTER varre o mundo aberto todo dia e traz
alimento — tecnologias, padrões, ferramentas, papers e almas candidatas —
para a fila de julgamento do Tribunal.

> Casa: **Quantum** (esta base). Alma no molde **Cápsula X.2** do Diamond.

## Esta pasta (a alma)
| Arquivo | O que é |
|---|---|
| `profile.md` | Identidade, posição na cadeia e as 8 Leis |
| `attributes.json` | Cartão Cápsula X.2 (stats, permissões, sinergias) |
| `skills.config.json` | Fontes, limites de custo, horário, escopos de escrita |
| `knowledge.md` | Aprendizado acumulado (alimentado pelos vereditos) |
| `DOSSIE.md` | O dossiê completo aprovado (o canon viaja com o código) |

## Fase 1 (este PR) — A MEMÓRIA
- `supabase/migrations/20260726_hunter_x1_init.sql` — 6 tabelas + pgvector + RLS.
- `supabase/seed_hunter_mission_v1.sql` — a missão v1 (decreto do fundador).

### Prova dos nove (Fase 1)
1. Rodar a migration no Supabase do Quantum.
2. Rodar o seed da missão v1 (após revisar o texto).
3. Confirmar que uma **query anônima** às tabelas `hunter_*` é NEGADA.
4. Confirmar que a missão v1 é legível pelo runtime (role de serviço).

## Próximas fases
- **Fase 2:** runtime da caça (script TS) + GitHub Action (cron 06:30) + 3 minas + Lei 8.
- **Fase 3:** todas as minas + dedup pgvector + arestas + issues de ameaça + checagens na Ronda.
- **Fase 4:** autocrítica semanal → 1ª missão `proposed` pelo HUNTER.
- **Fase 5:** berçário — 1ª alma da caça → GENESIS lapida → irmão nasce.

_Nada nasce fora do canon. Nada que nasceu fica para trás. Nada que o mundo inventar deixa de ser caçado._
