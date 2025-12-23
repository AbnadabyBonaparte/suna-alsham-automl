# Suna Alsham AutoML — Auditoria de Segurança (07/02/2025)

## Sumário Executivo
- Escopo: revisão rápida de rotas críticas no frontend (`/api`), focando uso de Supabase e chaves sensíveis.
- Risco principal: rotas públicas usando **Service Role** sem autenticação ou validação de escopo, permitindo escrita arbitrária em tabelas protegidas.

## Achados Prioritários

### 1) API `/api/process-request` exposta sem autenticação (Service Role)
- **Local**: `frontend/src/app/api/process-request/route.ts`
- **Problema**: qualquer caller pode enviar `request_id` e o handler, usando `SUPABASE_SERVICE_ROLE_KEY`, atualiza tabelas `requests` e `agents`, executa OpenAI e grava resultados. Não há autenticação, autorização ou validação de ownership da request.
- **Gravidade**: Crítica — bypass total de RLS e possibilidade de corrupção de estado/abuso de billing OpenAI.
- **Evidência**: Uso direto de `getSupabaseAdmin()` e updates em `requests`/`agents` sem checks de sessão ou permissão.
- **Correção sugerida**:
  - Exigir sessão autenticada (middleware NextAuth/Supabase) e validar que `request_id` pertence ao usuário.
  - Substituir Service Role por client com RLS ou stored procedure segura.
  - Adicionar validação de input (Zod) e rate limiting.

### 2) API `/api/agents/heartbeat` pública atualiza todos os agents
- **Local**: `frontend/src/app/api/agents/heartbeat/route.ts`
- **Problema**: tanto `GET` quanto `POST` usam Service Role e permitem ler/alterar `agents` sem autenticação. Um atacante pode falsificar estados, derrubar monitoramento ou mapear a base completa.
- **Gravidade**: Alta — exposição de inventário e integridade dos agents.
- **Correção sugerida**:
  - Proteger com autenticação de serviço (cron com token secreto) ou mover para job interno.
  - Usar policies RLS e role mínimo; evitar Service Role em handlers públicos.
  - Registrar auditoria e limitar frequência (rate limit/cron only).

### 3) API `/api/evolution/daily` (GET/POST) permite mutação ampla de dados
- **Local**: `frontend/src/app/api/evolution/daily/route.ts`
- **Problema**: rota GET, pública, executa ciclo completo de evolução: lê `agents/requests`, atualiza múltiplos agents, e insere em `evolution_cycles` com Service Role (via `getSupabase`). Nenhum controle de acesso ou limitação de execução.
- **Gravidade**: Crítica — qualquer pessoa pode reescrever prompts/capacidades de agents e inflar métricas.
- **Correção sugerida**:
  - Restringir a job interna autenticada; exigir chave de serviço privada ou cron com assinatura.
  - Validar parâmetros e limitar quantas evoluções podem ocorrer por execução.
  - Registrar quem/por que acionou o ciclo e proteger com RLS.

## Recomendações Gerais
- Remover Service Role de rotas públicas; usar client auth com RLS e policies explícitas.
- Criar middleware de autenticação/autorization para todas as rotas `app/api/**` sensíveis.
- Implementar validação de entrada (Zod) e rate limiting (ex.: Upstash/Redis) nos handlers expostos.
- Adicionar monitoramento/auditoria de chamadas e falhas de autorização.

## Dívidas Técnicas Observadas
- Ausência de testes de segurança/regressão para rotas críticas (prioridade: **alta**).
- Falta de documentação de requisitos de autorização por rota (prioridade: **média**).
