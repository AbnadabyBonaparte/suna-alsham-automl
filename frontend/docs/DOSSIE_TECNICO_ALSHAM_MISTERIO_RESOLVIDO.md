DOSSIÊ TÉCNICO: ALSHAM QUANTUM v12 (RESOLVIDO)
Data: 21/11/2025 Status: ✅ RESOLVIDO Assunto: Incidente de Content Security Policy (CSP), Bloqueio de Estilos (Tailwind) e Assets (SVG) em Produção (Vercel).

1. Visão Geral do Sistema
Projeto: ALSHAM QUANTUM (Frontend)
Framework: Next.js 16.0.3 (Turbopack ativado)
Linguagem: TypeScript / React 19.2.0
Estilização: Tailwind CSS v3.4.1 (Anteriormente v4 Beta - Causa do erro)
Hospedagem: Vercel
2. O Problema (Sintomas)
Após o deploy na Vercel, a aplicação apresentava:

Tela Branca (Falta de CSS): O HTML carregava, mas sem nenhum estilo.
Erros de CSP: O console acusava bloqueios de segurança, mascarando o problema real do CSS.
Erro 404 em Assets: Arquivos estáticos não eram encontrados.
3. A Causa Raiz (Diagnóstico Final)
O problema NÃO era o CSP (Content Security Policy), embora ele estivesse alertando sobre extensões. O problema real era uma Incompatibilidade de Versão do Tailwind CSS.

O Erro: O 
package.json
 continha dependências do Tailwind CSS v4 (Beta) (@tailwindcss/postcss), que é uma reescrita completa da engine.
O Conflito: Os arquivos de configuração do projeto (
tailwind.config.ts
, 
globals.css
) estavam escritos na sintaxe do Tailwind v3.
O Resultado: O processo de build não quebrava (silencioso), mas o PostCSS não conseguia processar os estilos corretamente, gerando um arquivo CSS final vazio ou inválido. O navegador, por sua vez, não aplicava nada.
4. A Solução (Passo a Passo)
Para corrigir, realizamos um "Downgrade" controlado para a versão estável (v3):

Passo 1: Ajuste de Dependências (
package.json
)
Removemos o pacote experimental v4 e instalamos a stack padrão v3.

Removido:

@tailwindcss/postcss (v4)
tailwindcss (v4)
Adicionado:

tailwindcss: ^3.4.1
postcss: ^8.4.38
autoprefixer: ^10.4.19 (Essencial para v3)
Passo 2: Correção do PostCSS (
postcss.config.mjs
)
O arquivo estava configurado para o plugin v4. Revertemos para o padrão v3.

De (v4):

plugins: {
  "@tailwindcss/postcss": {},
}
Para (v3):

plugins: {
  tailwindcss: {},
  autoprefixer: {},
}
Passo 3: Validação
Após essas alterações, o build na Vercel gerou o CSS corretamente e a aplicação voltou a funcionar com todo o visual "ALSHAM QUANTUM".

5. Lições Aprendidas (Post-Mortem)
Cuidado com Betas: O Tailwind v4 muda drasticamente a forma de configuração. Não misture dependências v4 com configs v3.
Erros Mascarados: Um erro de build de CSS pode parecer um erro de segurança (CSP) se o navegador bloquear scripts/estilos por outros motivos simultâneos (como extensões).
Verifique o 
package.json
: Sempre confira se as versões instaladas batem com a documentação que você está seguindo.
Autor: Antigravity (AI Agent) Aprovado por: Imperador Abnadaby
