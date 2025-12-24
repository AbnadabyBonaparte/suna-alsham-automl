# 🔍 FORENSE COMPLETA - PROBLEMAS DE LOGIN

**Data:** 2025-12-23  
**Status:** 🔴 CRÍTICO - Login trava ou cai em tela branca

---

## 📋 PROBLEMAS IDENTIFICADOS

### 1. ⚠️ **MIDDLEWARE PROCURANDO COOKIES ERRADOS**

**Arquivo:** `frontend/src/middleware.ts` (linhas 86-87)

**Problema:**
```typescript
const authToken = req.cookies.get('sb-access-token')?.value ||
                  req.cookies.get('supabase-auth-token')?.value;
```

O Supabase SSR usa cookies com formato diferente: `sb-<project-ref>-auth-token` e `sb-<project-ref>-auth-token-code-verifier`.

**Impacto:** Middleware nunca encontra o token, sempre redireciona para login mesmo após login bem-sucedido.

---

### 2. ⚠️ **MIDDLEWARE NÃO USA CLIENTE SSR CORRETO**

**Arquivo:** `frontend/src/middleware.ts` (linhas 105-109)

**Problema:**
```typescript
const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        persistSession: false
    }
});
```

Está usando `createClient` do `@supabase/supabase-js` diretamente, sem passar cookies. Deveria usar `createServerClient` do `@supabase/ssr`.

**Impacto:** Middleware não consegue ler a sessão dos cookies, sempre retorna sessão null.

---

### 3. ⚠️ **CLIENTE BROWSER USA LOCALSTORAGE**

**Arquivo:** `frontend/src/lib/supabase/client.ts`

**Problema:**
```typescript
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
```

O `createBrowserClient` do `@supabase/ssr` por padrão usa cookies, mas precisa ser configurado corretamente para funcionar com o middleware.

**Impacto:** Sessão pode não estar sendo sincronizada entre cliente e servidor.

---

### 4. ⚠️ **REDIRECIONAMENTO COM WINDOW.LOCATION**

**Arquivo:** `frontend/src/contexts/AuthContext.tsx` (linhas 173, 176)

**Problema:**
```typescript
window.location.href = '/dashboard';
window.location.href = '/onboarding';
```

Usar `window.location.href` causa reload completo da página, o que pode causar problemas com o middleware que roda antes do JavaScript carregar.

**Impacto:** Pode causar tela branca ou loop de redirecionamento.

---

### 5. ⚠️ **ERRO DE REFRESH TOKEN NO SUPABASE**

**Logs do Supabase:**
```
error finding session from refresh token: error finding session: unable to fetch records: context canceled
status: 500
```

**Problema:** O Supabase está tentando renovar o token mas não consegue encontrar a sessão no banco.

**Possíveis causas:**
- Sessão não está sendo persistida corretamente
- Cookies não estão sendo enviados nas requisições
- Timeout na conexão com o banco

---

### 6. ⚠️ **AUTHCONTEXT NÃO SINCRONIZA COM MIDDLEWARE**

**Arquivo:** `frontend/src/contexts/AuthContext.tsx`

**Problema:** O AuthContext usa `createBrowserClient` que pode não estar sincronizado com os cookies que o middleware espera.

**Impacto:** Usuário pode estar logado no cliente mas não no servidor/middleware.

---

## 🔧 SOLUÇÕES NECESSÁRIAS

### ✅ **SOLUÇÃO 1: Corrigir Middleware para usar SSR Client**

O middleware precisa usar `createServerClient` do `@supabase/ssr` com acesso aos cookies da requisição.

### ✅ **SOLUÇÃO 2: Corrigir Cliente Browser**

O cliente browser precisa usar `createBrowserClient` do `@supabase/ssr` com configuração de cookies.

### ✅ **SOLUÇÃO 3: Usar Router.push ao invés de window.location**

Trocar `window.location.href` por `router.push()` para evitar reload completo.

### ✅ **SOLUÇÃO 4: Garantir Sincronização de Cookies**

Garantir que os cookies estão sendo configurados corretamente tanto no cliente quanto no servidor.

---

## 📊 FLUXO ATUAL (QUEBRADO)

```
1. Usuário faz login → AuthContext.signIn()
2. Supabase retorna sessão → Salva em localStorage (via createBrowserClient)
3. AuthContext redireciona com window.location.href → '/dashboard'
4. Middleware intercepta requisição → Procura cookies 'sb-access-token' (NÃO EXISTE)
5. Middleware não encontra token → Redireciona para '/login'
6. LOOP ou TELA BRANCA
```

---

## 📊 FLUXO CORRETO (DEVE SER)

```
1. Usuário faz login → AuthContext.signIn()
2. Supabase retorna sessão → Salva em cookies (via createBrowserClient SSR)
3. AuthContext redireciona com router.push() → '/dashboard'
4. Middleware intercepta requisição → Usa createServerClient para ler cookies
5. Middleware encontra sessão → Verifica permissões
6. Middleware permite acesso → Dashboard carrega
```

---

## 🎯 PRIORIDADE

1. **CRÍTICO:** Corrigir middleware para usar SSR client
2. **CRÍTICO:** Corrigir cliente browser para usar cookies
3. **ALTO:** Trocar window.location por router.push
4. **MÉDIO:** Adicionar logs para debug
5. **BAIXO:** Melhorar tratamento de erros

---

## 📝 NOTAS

- O projeto já tem `@supabase/ssr` instalado
- O arquivo `server.ts` já está correto
- O problema está principalmente no middleware e no cliente browser
- Os logs do Supabase mostram que há problemas com refresh token

