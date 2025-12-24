# 🔧 CORREÇÃO CRÍTICA - LOOP INFINITO COM RSC

**Data:** 2025-12-23  
**Problema:** Loop infinito de requisições RSC (`onboarding?_rsc=...`) causando travamento

---

## 🔍 PROBLEMA IDENTIFICADO

O `proxy.ts` estava redirecionando de `/onboarding` para `/dashboard` **durante requisições RSC** (React Server Components), causando um loop infinito:

1. Cliente faz requisição RSC: `onboarding?_rsc=sygcq`
2. Proxy redireciona para `/dashboard`
3. Cliente tenta carregar dashboard
4. Mas ainda está em `/onboarding` no cliente
5. Cliente faz nova requisição RSC: `onboarding?_rsc=ac3rd`
6. **LOOP INFINITO** 🔄

---

## ✅ CORREÇÕES APLICADAS

### 1. **Proxy.ts ignora requisições RSC**

**Arquivo:** `frontend/src/lib/supabase/proxy.ts`

**Mudança:**
- ✅ Adicionada verificação de requisições RSC (`_rsc` parameter)
- ✅ Se for requisição RSC, **NÃO redireciona** - deixa o cliente fazer o redirect
- ✅ Evita loop infinito de requisições RSC

**Antes:**
```typescript
if (user && request.nextUrl.pathname === '/onboarding') {
  // Sempre redirecionava, mesmo durante RSC requests
  if (profile?.onboarding_completed === true) {
    return NextResponse.redirect('/dashboard');
  }
}
```

**Depois:**
```typescript
if (user && request.nextUrl.pathname === '/onboarding') {
  // Verificar se é requisição RSC
  const isRSCRequest = request.nextUrl.searchParams.has('_rsc');
  if (isRSCRequest) {
    // Durante RSC, não redirecionar - deixa cliente fazer redirect
    return supabaseResponse;
  }
  
  // Só redireciona se NÃO for RSC
  if (profile?.onboarding_completed === true && !isRSCRequest) {
    return NextResponse.redirect('/dashboard');
  }
}
```

---

### 2. **Onboarding usa window.location.href**

**Arquivo:** `frontend/src/app/onboarding/page.tsx`

**Mudança:**
- ✅ Voltou a usar `window.location.href` ao invés de `router.push()`
- ✅ Força reload completo, evitando problemas com RSC
- ✅ Evita loop de requisições RSC

**Razão:** Durante loops de RSC, `router.push()` não funciona bem porque o Next.js está tentando fazer Server Components, causando conflito.

---

## 📊 FLUXO CORRIGIDO

```
1. Usuário completa onboarding → Salva onboarding_completed: true
2. Onboarding chama window.location.href = '/dashboard'
3. Cliente faz requisição para /dashboard
4. Proxy intercepta → Verifica onboarding_completed ✅
5. Se requisição RSC (_rsc=) → NÃO redireciona, deixa passar ✅
6. Se requisição normal → Redireciona se necessário ✅
7. Dashboard carrega normalmente ✅
```

---

## 🧪 TESTES NECESSÁRIOS

1. ✅ Completar onboarding e verificar que não há mais loop de requisições RSC
2. ✅ Verificar que não há mais requisições repetidas de `onboarding?_rsc=...`
3. ✅ Verificar que o redirecionamento funciona corretamente
4. ✅ Verificar logs do Vercel para confirmar que não há mais erros

---

## 📝 NOTAS

- O problema era específico com React Server Components (RSC)
- Requisições RSC têm `_rsc=` no query string
- O proxy não deve redirecionar durante RSC - deixa o cliente fazer
- `window.location.href` força reload completo, evitando problemas com RSC

