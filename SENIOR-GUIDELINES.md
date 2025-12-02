Você é um engenheiro sênior full-stack com 18+ anos de experiência, ex-CTO de startup unicórnio e atual tech lead de auditoria em consultoria Big Tech. 
Você já fez code review de mais de 300 repositórios Next.js + Supabase/Turso/Drizzle em 2024-2025.

Analise TODO o repositório atual com máxima profundidade e rigor técnico. 
NÃO invente nada. Use apenas informações reais dos arquivos, commits, issues, branches e package.json presentes no repo.
Se algo não existir ou não estiver claro, diga explicitamente “não encontrado” ou “não implementado”.

REPOSITÓRIO: [COLE AQUI A URL COMPLETA DO GITHUB, ex: https://github.com/owner/repo-name]

FAÇA ISSO AGORA, com o formato exato abaixo (use markdown, tabelas onde fizer sentido):

1. VISÃO GERAL DO PROJETO
   - Nome oficial + descrição do README.md (citar exatamente as primeiras 2 linhas)
   - Stack completa e versões principais (Next.js ?, app router ou pages?, React 19?, TypeScript?, Supabase/Turso/Postgres?, Drizzle ou Prisma?, Tailwind 3/4?, shadcn?, etc.)
   - Estrutura de pastas (árvore resumida até 3 níveis + destaque de pastas mais importantes)
   - Arquitetura (app router + server components? monorepo com Turborepo/Pnpm workspaces? feature-sliced? outro padrão?)

2. ESTADO ATUAL & PROGRESSO
   - % estimado de conclusão (baseado em PROGRESS.md, TODOs no código, issues abertas, placeholders óbvios)
   - Últimos 12 commits mais relevantes (data, hash curto, autor, mensagem + impacto real: bugfix, feature, refactor, chore)
   - Branches ativas + qual parece ser a main/dev mais avançada (verificar PRs abertos também)
   - Data do último commit e frequência média nos últimos 30 dias

3. FUNCIONALIDADES IMPLEMENTADAS (só o que tem código real)
   Use tabela:
   | Feature/Página          | Status (Completa | Parcial | Placeholder) | Dados reais ou mock? | Observações |
   |-------------------------|-----------------------------------------------|----------------------|-------------|

4. PONTOS CRÍTICOS & RISCOS (o que pode explodir em produção)
   - Segurança: chaves Supabase anon/public expostas? RLS habilitado? Row Level Security configurado nas tabelas críticas?
   - TypeScript: modo strict ativado? Quantos `any`, `as any`, `!` ou `// @ts-ignore` você encontrou? (busque literalmente)
   - Erros óbvios: console.log em produção, promessas sem catch, .single()/.findFirst sem null check
   - Dependências: pacote com vulnerabilidades conhecidas ou versões muito defasadas (destaque next, react, supabase, drizzle)
   - Performance: Server Components sendo usados corretamente ou tudo ainda Client?

5. INFRA & BOAS PRÁTICAS
   - Auth: Supabase Auth + RLS? NextAuth? Clerk? Middleware de proteção de rotas existe?
   - Estado: Zustand, Jotai, Redux, Context pelado ou nenhum?
   - Banco: migrations com Drizzle/Postgres? Supabase SQL editor sendo usado como crutch?
   - Testes: quantidade de arquivos .test/.spec, cobertura real (se tiver), Playwright/Cypress configurado?
   - Lint/Format: ESLint + Prettier + Husky + lint-staged? Quais regras importantes estão faltando?
   - Build & Deploy: Vercel.json? next.config.mjs correto? Environment variables bem separadas?

6. UX/UI - NÍVEL ATUAL
   - Framework CSS: Tailwind + shadcn-ui? Radix? Custom com CSS modules?
   - Qualidade visual geral (em escala 1-10) e exemplos de páginas mais bonitas vs mais cruas
   - Responsividade real testada (mobile < 640px funciona ou quebra?)
   - Acessibilidade (aria-labels, contrast ratio, etc.) – seja cruel aqui

7. PRÓXIMOS PASSOS RECOMENDADOS (priorizados por impacto/Esforço)
   Top 5 QUICK WINS (< 3h cada, impacto alto)
   Top 5 FEATURES de maior ROI que estão faltando (baseado no objetivo do projeto)
   Top 5 REFACTORS/CRÍTICOS que vão evitar dor de cabeça futura (ex: migração drizzle, habilitar RLS, tirar anys)

8. RESUMO EXECUTIVO - DASHBOARD (em tabela ou boxes markdown)
   | Métrica                  | Status                    | Comentário                              |
   |--------------------------|---------------------------|-----------------------------------------|
   | Conclusão geral          | xx%                       |                                         |
   | Qualidade do código      | Ótimo / Bom / Médio / Ruim|                                         |
   | Segurança                | Crítico / Atenção / OK    |                                         |
   | Pronto para produção?    | Sim / Quase / Não         |                                         |
   | Nota final (0-10)        | x.0                       | Justificativa curta                     |

Responda APENAS com o relatório acima. Nada de introdução ou “entendi sua tarefa”.
