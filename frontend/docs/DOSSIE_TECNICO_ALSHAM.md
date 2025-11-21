DOSSIÊ TÉCNICO: ALSHAM QUANTUM v12
Data: 21/11/2025 Assunto: Incidente de Content Security Policy (CSP), Bloqueio de Estilos (Tailwind) e Assets (SVG) em Produção (Vercel).

1. Visão Geral do Sistema
Projeto: ALSHAM QUANTUM (Frontend)
Framework: Next.js 16.0.3 (Turbopack ativado)
Linguagem: TypeScript / React 19.2.0
Estilização: Tailwind CSS (com plugins tailwindcss-animate)
Hospedagem: Vercel
Integrações: Supabase, PostHog (Analytics)
2. O Problema (Sintomas)
Após o deploy na Vercel, a aplicação apresenta os seguintes comportamentos críticos:

Perda Total de Estilo: A aplicação carrega o HTML cru, sem o CSS do Tailwind (Tela branca/texto preto).
Bloqueio por CSP (Content Security Policy): O console do navegador exibe múltiplos erros indicando que scripts (PostHog) e estilos foram bloqueados por uma diretiva CSP restritiva (script-src 'self' ...).
Erro 404 em Assets: O arquivo 
/grid.svg
 (background) retorna 404, mesmo existindo na pasta public.
Interferência de Extensão: Logs indicaram explicitamente a injeção de CSP por uma extensão de navegador (chrome-extension://...), identificada como "Disable-CSP" ou similar.
3. Histórico de Alterações e Tentativas de Solução
Fase 1: Implementação de Funcionalidades (Sucesso)
Novas Páginas: Implementadas /dashboard/agents/[id] (Detalhes do Agente), /dashboard/containment (Contenção) e refinamento de /dashboard/evolution.
Correções de Build:
Correção de sintaxe JSX (>) na página de Agentes.
Correção de importação do 
Sidebar
 em 
layout.tsx
.
Criação do arquivo 
grid.svg
 faltante.
Fase 2: Combate ao CSP e Estilização (Em Andamento)
Tentativa A: Configuração via 
vercel.json
Ação: Adicionados headers de segurança (CSP) permissivos no 
vercel.json
.
Resultado: FALHA. A Vercel ou o Next.js parecem ignorar esses headers em favor de uma política padrão mais rígida ou injetada.
Tentativa B: Configuração via 
next.config.mjs
Ação: Movida a configuração de 
headers()
 para dentro do 
next.config.mjs
 (método recomendado para Next.js).
Liberados domínios: us-assets.i.posthog.com, *.supabase.co, fonts.googleapis.com.
Liberados métodos: 'unsafe-inline', 'unsafe-eval'.
Resultado: FALHA PARCIAL. Os erros persistiram.
Tentativa C: Identificação de Interferência Externa
Diagnóstico: O erro violates ... directive ... chrome-extension://... confirmou que uma extensão do usuário estava sobrescrevendo o CSP do servidor.
Ação: Usuário instruído a desativar a extensão "Disable-CSP" e testar em Aba Anônima.
Resultado: O problema persistiu mesmo na aba anônima, sugerindo que:
O cache do navegador/Vercel manteve a versão quebrada.
Ou o build do CSS (Tailwind) está falhando silenciosamente, gerando um arquivo CSS vazio ou inválido, independentemente do CSP.
Tentativa D: Isolamento (Estado Atual)
Ação: Comentado/Desativado temporariamente o bloco Content-Security-Policy no 
next.config.mjs
.
Objetivo: Verificar se o bloqueio visual é causado puramente pelo CSP ou se há um erro estrutural no carregamento do CSS.
4. Arquivos de Configuração Relevantes
next.config.mjs
 (Atual)
const nextConfig = {
  reactStrictMode: false,
  typescript: { ignoreBuildErrors: true },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          // CSP DESATIVADO TEMPORARIAMENTE PARA DEBUG
          // { key: 'Content-Security-Policy', value: "..." }
        ],
      },
    ];
  },
};
tailwind.config.ts
Configurado para escanear:

./src/pages/**/*.{js,ts,jsx,tsx,mdx}
./src/components/**/*.{js,ts,jsx,tsx,mdx}
./src/app/**/*.{js,ts,jsx,tsx,mdx}
5. Solicitação para Suporte (Vercel / Devs)
Para o Suporte:

Build Logs: O build na Vercel completa com sucesso ("Compiled successfully"), mas os arquivos estáticos gerados parecem não estar sendo servidos com os MIME types corretos ou estão sendo bloqueados.
CSP Injection: Existe alguma configuração na Vercel (aba "Security" ou "Deployment Protection") que injeta um CSP padrão forçado, ignorando o 
next.config.mjs
?
Tailwind/PostCSS: Há relatos de incompatibilidade do Turbopack (next dev --turbo ou build) com certas configurações de PostCSS que resultam em CSS vazio em produção?
Autor: Antigravity (AI Agent) Status: Aguardando validação do deploy sem CSP.
