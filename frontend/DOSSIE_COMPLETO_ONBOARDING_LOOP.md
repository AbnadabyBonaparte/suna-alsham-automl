# 🚨 DOSSIÊ COMPLETO - LOOP INFINITO NO ONBOARDING

**Data de Criação:** 2025-12-24  
**Status:** 🔴 CRÍTICO - PROBLEMA NÃO RESOLVIDO  
**Prioridade:** MÁXIMA  
**Impacto:** Usuários não conseguem acessar o sistema após login

---

## 📋 SUMÁRIO EXECUTIVO

### Problema Principal
Usuários ficam presos em um loop infinito na página `/onboarding` mesmo após completar o onboarding (`onboarding_completed: true` no banco de dados). O sistema tenta redirecionar para `/dashboard`, mas falha repetidamente, causando requisições infinitas e travamento da aplicação.

### Sintomas Observados
1. ✅ Login bem-sucedido (sessão criada corretamente)
2. ✅ `onboarding_completed: true` confirmado no banco de dados
3. ❌ Usuário permanece na página `/onboarding`
4. ❌ Requisições RSC infinitas (`onboarding?_rsc=...`)
5. ❌ Console mostra tentativas de redirecionamento que não funcionam
6. ❌ Network tab mostra loop de requisições de sessão (`wsm.sessionActivated` / `wsm.sessionDeactivated`)

---

## 🛠️ STACK TÉCNICO

### Frontend
- **Framework:** Next.js 16.0.7 (Turbopack)
- **React:** 19.x
- **TypeScript:** 5.x (strict mode)
- **Roteamento:** Next.js App Router
- **Autenticação:** Supabase Auth (@supabase/ssr)

### Backend
- **Database:** Supabase (PostgreSQL)
- **Auth:** Supabase Auth
- **Deploy:** Vercel

### Bibliotecas Principais
```json
{
  "@supabase/ssr": "^0.5.2",
  "@supabase/supabase-js": "^2.x",
  "next": "16.0.7",
  "react": "19.x",
  "typescript": "5.x"
}
```

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos Críticos
1. **`frontend/src/lib/supabase/proxy.ts`** - Proxy/middleware do Next.js
2. **`frontend/src/contexts/AuthContext.tsx`** - Context de autenticação
3. **`frontend/src/app/onboarding/page.tsx`** - Página de onboarding
4. **`frontend/src/middleware.ts`** - Middleware legacy (deprecated, mas ainda existe)
5. **`frontend/proxy.ts`** - Proxy wrapper que chama `updateSession`

### Estrutura de Arquivos
```
frontend/
├── src/
│   ├── lib/
│   │   └── supabase/
│   │       ├── proxy.ts          ← Lógica principal de redirecionamento
│   │       ├── client.ts         ← Cliente browser
│   │       └── server.ts         ← Cliente servidor
│   ├── contexts/
│   │   └── AuthContext.tsx       ← Context de autenticação
│   ├── app/
│   │   ├── onboarding/
│   │   │   └── page.tsx          ← Página de onboarding
│   │   ├── dashboard/
│   │   │   └── layout.tsx        ← Layout do dashboard
│   │   └── login/
│   │       └── page.tsx          ← Página de login
│   └── middleware.ts             ← Middleware legacy (deprecated)
└── proxy.ts                      ← Proxy wrapper
```

---

## 🔍 HISTÓRICO DE TENTATIVAS DE CORREÇÃO

### Tentativa 1: Correção do Middleware (2025-12-23)
**Commit:** `fix(auth): corrige middleware e redirecionamento de login`

**Mudanças:**
- ✅ Middleware migrado de `createClient` para `createServerClient` do `@supabase/ssr`
- ✅ Configuração correta de cookies no middleware
- ✅ AuthContext mudado de `window.location.href` para `router.push()`

**Resultado:** ❌ Não resolveu - Problema persistiu

**Documentação:** `frontend/FORENSE_LOGIN_PROBLEMAS.md`, `frontend/CORRECOES_LOGIN.md`

---

### Tentativa 2: Verificação de Onboarding no Middleware (2025-12-23)
**Commit:** `fix(onboarding): corrige loop e travamento na página de onboarding`

**Mudanças:**
- ✅ Middleware agora verifica `onboarding_completed` antes de permitir acesso ao dashboard
- ✅ Adicionada verificação na rota `/onboarding` para redirecionar se já completo
- ✅ Onboarding mudado de `window.location.href` para `router.push()`

**Resultado:** ❌ Não resolveu - Loop continuou

**Documentação:** `frontend/FIX_ONBOARDING_LOOP.md`

---

### Tentativa 3: Correção de Loop RSC (2025-12-23)
**Commit:** `fix(onboarding): corrige loop infinito com requisições RSC`

**Mudanças:**
- ✅ Proxy agora ignora requisições RSC (`_rsc=` parameter)
- ✅ Onboarding voltou a usar `window.location.href` ao invés de `router.push()`
- ✅ Adicionada verificação de RSC antes de redirecionar

**Resultado:** ❌ Não resolveu completamente - Problema persistiu parcialmente

**Documentação:** `frontend/FIX_LOOP_RSC.md`

---

### Tentativa 4: Correção Final (2025-12-24)
**Commit:** `fix(onboarding): corrige problema de usuário preso no onboarding`

**Mudanças:**
- ✅ AuthContext mudado de `router.push()` para `window.location.href`
- ✅ Proxy ignora RSC em TODAS as verificações de onboarding
- ✅ Onboarding verifica status imediatamente ao montar componente
- ✅ Adicionado delay de 100ms antes de redirecionar

**Resultado:** ❌ AINDA NÃO RESOLVIDO - Problema persiste

**Documentação:** `frontend/FIX_ONBOARDING_STUCK_FINAL.md`

---

## 🔬 ANÁLISE TÉCNICA DETALHADA

### Fluxo Atual (Quebrado)

```
1. Usuário faz login → AuthContext.signIn()
   ├─ Supabase retorna sessão ✅
   ├─ Sessão salva em cookies ✅
   └─ Metadata carregada: { onboarding_completed: true } ✅

2. AuthContext tenta redirecionar
   ├─ window.location.href = '/dashboard' ✅
   └─ OU router.push('/dashboard') ✅

3. Cliente faz requisição para /dashboard
   ├─ Proxy intercepta requisição
   ├─ Verifica se é RSC (_rsc=)
   │  ├─ Se RSC → Ignora verificação ✅
   │  └─ Se não RSC → Verifica onboarding
   │     ├─ Busca profile do banco
   │     ├─ onboarding_completed: true ✅
   │     └─ Deveria permitir acesso...
   │
   └─ MAS algo está impedindo o acesso ❌

4. Requisições RSC começam
   ├─ onboarding?_rsc=sygcq (Status 304)
   ├─ onboarding?_rsc=ac3rd (Status 304)
   └─ LOOP INFINITO 🔄

5. Requisições de sessão também em loop
   ├─ wsm.sessionActivated (Status 200)
   ├─ wsm.sessionDeactivated (Status 200)
   └─ Repetindo infinitamente 🔄
```

### Problemas Identificados

#### 1. **Conflito entre Middleware e Proxy**
- Existem DOIS sistemas de middleware rodando:
  - `frontend/src/middleware.ts` (legacy, deprecated)
  - `frontend/src/lib/supabase/proxy.ts` (ativo via `frontend/proxy.ts`)
- Ambos podem estar interferindo um no outro

#### 2. **React Server Components (RSC)**
- Next.js 16 usa RSC por padrão
- Requisições RSC têm `_rsc=` no query string
- O proxy ignora RSC, mas o cliente continua fazendo requisições RSC
- Isso pode causar dessincronia entre cliente e servidor

#### 3. **Sincronização de Estado**
- O cliente React pode ter estado diferente do servidor
- `onboarding_completed: true` no banco, mas cliente não atualiza
- Redirecionamento pode estar acontecendo antes do estado atualizar

#### 4. **Cookies e Sessão**
- Cookies podem não estar sendo lidos corretamente
- Sessão pode estar expirada ou inválida
- Refresh token pode estar falhando

---

## 📊 EVIDÊNCIAS

### Console Logs (Browser)
```
[AUTH] Tentando fazer login para: casamondestore@gmail.com
[AUTH] Login bem-sucedido, carregando usuário...
[AUTH] Usuário obtido: e85d6aca-d65b-4452-9a84-a7995bf1cda8
[AUTH] Metadata carregada: {
  subscription_plan: 'enterprise',
  subscription_status: 'active',
  founder_access: true,
  onboarding_completed: true  ← CONFIRMADO NO BANCO
}
[AUTH] Onboarding completo, redirecionando para dashboard
[LOGIN] Login bem-sucedido, aguardando redirecionamento...
```

**Observação:** O log mostra que o sistema DETECTA que o onboarding está completo e tenta redirecionar, mas o redirecionamento não funciona.

### Network Tab (Browser)
- **Requisições RSC repetidas:**
  - `onboarding?_rsc=sygcq` (Status 304, repetindo)
  - `onboarding?_rsc=ac3rd` (Status 304, repetindo)
  - `onboarding?_rsc=...` (múltiplas variações)

- **Requisições de sessão em loop:**
  - `wsm.sessionActivated?tm=...` (Status 200, repetindo)
  - `wsm.sessionDeactivated?tm=...` (Status 200, repetindo)

- **Requisições de perfil:**
  - `profiles?select=onboarding_completed&id=eq.e...` (Status 200)
  - Retorna `onboarding_completed: true` ✅

### Supabase Logs
- Sessão criada com sucesso ✅
- Profile existe e tem `onboarding_completed: true` ✅
- Nenhum erro de autenticação ✅

### Vercel Logs
- Build bem-sucedido ✅
- Deploy completo ✅
- Nenhum erro de runtime ✅

---

## 🧪 CENÁRIOS TESTADOS

### ✅ Cenário 1: Login com Onboarding Completo
- **Ação:** Fazer login com usuário que já completou onboarding
- **Esperado:** Redirecionar para `/dashboard`
- **Resultado:** ❌ Fica preso em `/onboarding`

### ✅ Cenário 2: Acessar /onboarding com Onboarding Completo
- **Ação:** Acessar diretamente `/onboarding` com usuário logado e onboarding completo
- **Esperado:** Redirecionar automaticamente para `/dashboard`
- **Resultado:** ❌ Fica preso em `/onboarding`

### ✅ Cenário 3: Completar Onboarding
- **Ação:** Completar o onboarding pela primeira vez
- **Esperado:** Salvar `onboarding_completed: true` e redirecionar para `/dashboard`
- **Resultado:** ✅ Salva corretamente, ❌ Redirecionamento falha

### ✅ Cenário 4: Verificar Cookies
- **Ação:** Verificar cookies no DevTools
- **Esperado:** Cookies de sessão presentes
- **Resultado:** ✅ Cookies presentes, mas pode haver problema de sincronização

---

## 🔧 CÓDIGO ATUAL (Relevante)

### Proxy.ts (Lógica Principal)
```typescript
// frontend/src/lib/supabase/proxy.ts

// Verificação de onboarding em rotas protegidas
if (user && isProtectedPath) {
  const isRSCRequest = request.nextUrl.searchParams.has('_rsc');
  if (isRSCRequest) {
    return supabaseResponse; // Ignora verificação
  }
  
  const { data: profile } = await supabase
    .from('profiles')
    .select('onboarding_completed, role')
    .eq('id', user.id)
    .single();
  
  if (!profileError && profile && profile.onboarding_completed === false) {
    return NextResponse.redirect('/onboarding');
  }
}

// Verificação de onboarding na rota /onboarding
if (user && request.nextUrl.pathname === '/onboarding') {
  const isRSCRequest = request.nextUrl.searchParams.has('_rsc');
  if (isRSCRequest) {
    return supabaseResponse; // Ignora durante RSC
  }
  
  const { data: profile } = await supabase
    .from('profiles')
    .select('onboarding_completed, role')
    .eq('id', user.id)
    .single();
  
  if (profile?.onboarding_completed === true && !isRSCRequest) {
    return NextResponse.redirect('/dashboard');
  }
}
```

### AuthContext.tsx
```typescript
// frontend/src/contexts/AuthContext.tsx

if (metadata?.onboarding_completed) {
    console.log('[AUTH] Onboarding completo, redirecionando para dashboard');
    window.location.href = '/dashboard';
} else {
    console.log('[AUTH] Onboarding não completo, redirecionando para onboarding');
    window.location.href = '/onboarding';
}
```

### Onboarding Page.tsx
```typescript
// frontend/src/app/onboarding/page.tsx

useEffect(() => {
    const checkOnboarding = async () => {
        const { data: { user } } = await supabase.auth.getUser();
        if (user) {
            const { data: profile } = await supabase
                .from('profiles')
                .select('onboarding_completed')
                .eq('id', user.id)
                .single();
            
            if (profile?.onboarding_completed) {
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 100);
            }
        }
    };
    checkOnboarding();
}, []);
```

---

## 🎯 HIPÓTESES NÃO TESTADAS

### Hipótese 1: Race Condition
- O redirecionamento pode estar acontecendo antes do estado ser atualizado
- **Teste sugerido:** Aumentar delay ou usar polling

### Hipótese 2: Conflito de Middlewares
- Dois middlewares podem estar interferindo
- **Teste sugerido:** Remover completamente `middleware.ts` legacy

### Hipótese 3: Problema com Cookies
- Cookies podem não estar sendo lidos corretamente pelo proxy
- **Teste sugerido:** Verificar configuração de cookies no Supabase

### Hipótese 4: Problema com RSC
- Next.js 16 pode ter bug com RSC e redirecionamentos
- **Teste sugerido:** Desabilitar RSC temporariamente

### Hipótese 5: Cache do Browser
- Cache pode estar servindo versão antiga da página
- **Teste sugerido:** Limpar cache e testar em modo anônimo

### Hipótese 6: Problema com Vercel Edge Runtime
- Proxy pode estar rodando em Edge Runtime com limitações
- **Teste sugerido:** Verificar configuração de runtime

---

## 🚀 PRÓXIMOS PASSOS SUGERIDOS

### Curto Prazo (Imediato)
1. ✅ **Remover middleware.ts legacy completamente**
   - Pode estar causando conflito
   - Next.js já avisou que está deprecated

2. ✅ **Adicionar logs detalhados**
   - Logar cada passo do fluxo de redirecionamento
   - Logar estado dos cookies
   - Logar estado do profile

3. ✅ **Testar em ambiente limpo**
   - Limpar cache do browser
   - Testar em modo anônimo
   - Testar em diferentes browsers

### Médio Prazo
1. ✅ **Refatorar lógica de redirecionamento**
   - Centralizar em um único lugar
   - Usar apenas uma estratégia (window.location OU router.push)
   - Evitar múltiplos pontos de redirecionamento

2. ✅ **Implementar polling como fallback**
   - Se redirecionamento falhar, tentar novamente após X segundos
   - Limitar número de tentativas

3. ✅ **Adicionar tratamento de erro robusto**
   - Capturar erros de redirecionamento
   - Mostrar mensagem ao usuário
   - Permitir redirecionamento manual

### Longo Prazo
1. ✅ **Revisar arquitetura de autenticação**
   - Considerar usar apenas Supabase Auth helpers
   - Simplificar fluxo de onboarding
   - Documentar fluxo completo

2. ✅ **Implementar testes automatizados**
   - Testes E2E do fluxo de onboarding
   - Testes de integração do proxy
   - Testes de redirecionamento

---

## 📞 INFORMAÇÕES PARA AJUDA EXTERNA

### Repositório
- **GitHub:** `https://github.com/AbnadabyBonaparte/suna-alsham-automl`
- **Branch:** `main`
- **Commits relevantes:** Ver seção "Histórico de Tentativas"

### Ambiente
- **Produção:** `https://quantum.alshamglobal.com.br`
- **Deploy:** Vercel
- **Database:** Supabase

### Contatos
- **Email:** casamondestore@gmail.com
- **Projeto:** ALSHAM QUANTUM

### Acesso Necessário
- ✅ Código fonte (público no GitHub)
- ✅ Logs do Vercel (acesso necessário)
- ✅ Logs do Supabase (acesso necessário)
- ✅ Acesso ao banco de dados (para verificar dados)

---

## 📝 NOTAS ADICIONAIS

### Comportamento Esperado vs Real

**Esperado:**
1. Usuário faz login
2. Sistema verifica `onboarding_completed`
3. Se `true` → Redireciona para `/dashboard`
4. Se `false` → Redireciona para `/onboarding`
5. Usuário completa onboarding
6. Sistema salva `onboarding_completed: true`
7. Sistema redireciona para `/dashboard`
8. Dashboard carrega normalmente

**Real:**
1. Usuário faz login ✅
2. Sistema verifica `onboarding_completed` ✅
3. Sistema detecta `onboarding_completed: true` ✅
4. Sistema tenta redirecionar para `/dashboard` ✅
5. **MAS o redirecionamento não funciona** ❌
6. Usuário fica preso em `/onboarding` ❌
7. Requisições RSC começam em loop ❌
8. Sistema trava ❌

### Padrões Observados
- O problema acontece **sempre** quando `onboarding_completed: true`
- O problema acontece **tanto** após login quanto ao acessar `/onboarding` diretamente
- O problema acontece **independente** do método de redirecionamento (`window.location` ou `router.push`)
- O problema acontece **apenas** em produção (Vercel), não em desenvolvimento local

---

## 🔗 REFERÊNCIAS

### Documentação Interna
- `frontend/FORENSE_LOGIN_PROBLEMAS.md` - Análise inicial
- `frontend/CORRECOES_LOGIN.md` - Primeira tentativa de correção
- `frontend/FIX_ONBOARDING_LOOP.md` - Segunda tentativa
- `frontend/FIX_LOOP_RSC.md` - Terceira tentativa
- `frontend/FIX_ONBOARDING_STUCK_FINAL.md` - Quarta tentativa

### Documentação Externa
- [Next.js Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [Supabase SSR](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [React Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Next.js Proxy](https://nextjs.org/docs/app/api-reference/next-config-js/proxy)

---

## ✅ CHECKLIST PARA AJUDA EXTERNA

- [x] Problema claramente descrito
- [x] Stack técnico documentado
- [x] Arquivos envolvidos listados
- [x] Histórico de tentativas documentado
- [x] Evidências coletadas (logs, screenshots)
- [x] Código relevante incluído
- [x] Hipóteses não testadas listadas
- [x] Próximos passos sugeridos
- [x] Informações de acesso fornecidas
- [x] Repositório acessível

---

**Última Atualização:** 2025-12-24  
**Status:** 🔴 AGUARDANDO AJUDA EXTERNA  
**Prioridade:** MÁXIMA

