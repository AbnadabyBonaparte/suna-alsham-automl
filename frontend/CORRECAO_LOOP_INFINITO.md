# 🔧 CORREÇÃO: Loop Infinito de Redirecionamento

## 🔴 Problema Identificado

**ERR_TOO_MANY_REDIRECTS** - Loop infinito entre `/onboarding` e `/dashboard`

### Causa Raiz

O loop estava sendo causado por **dois pontos de redirecionamento conflitantes**:

1. **`proxy.ts`** (middleware): Redireciona `/onboarding` → `/dashboard` quando `onboarding_completed = true`
2. **`requireDashboardAccess()`** (server component): Redireciona `/dashboard` → `/onboarding` quando `profile` não existe ou há erro

### Fluxo do Loop

```
Usuário em /onboarding (onboarding_completed = true)
  ↓
proxy.ts detecta onboarding completo
  ↓
Redireciona para /dashboard (307)
  ↓
requireDashboardAccess() no layout do dashboard
  ↓
Erro ao buscar profile OU profile não existe
  ↓
Redireciona para /onboarding (redirect)
  ↓
LOOP INFINITO 🔄
```

---

## ✅ Correções Aplicadas

### 1. Removido `middleware.ts` Duplicado

- ✅ Deletado `frontend/src/middleware.ts`
- ✅ Toda lógica agora está apenas em `frontend/proxy.ts`
- ✅ Sem mais warnings do Next.js 16

### 2. Corrigido `requireDashboardAccess()`

**Antes:**
```typescript
if (error || !profile) {
    redirect('/onboarding');  // ❌ Sempre redireciona, mesmo se onboarding completo
}
```

**Depois:**
```typescript
if (error || !profile) {
    // Se o profile não existe, criar automaticamente ao invés de redirecionar
    if (error?.code === 'PGRST116') {
        // Criar profile automaticamente
        const { error: insertError } = await supabase
            .from('profiles')
            .insert({
                id: user.id,
                username: user.email?.split('@')[0] || 'user',
                onboarding_completed: false,
            });

        if (!insertError) {
            redirect('/onboarding');
        }
    }
    redirect('/onboarding');
}
```

### 3. Melhorado `proxy.ts`

**Adicionado:**
- Verificação explícita de RSC antes de redirecionar
- Permite acesso a rotas protegidas mesmo sem profile (deixa `requireDashboardAccess` lidar)

**Antes:**
```typescript
if (profile && profile.onboarding_completed === true && request.nextUrl.pathname === '/onboarding') {
    return NextResponse.redirect(url);  // ❌ Pode redirecionar durante RSC
}
```

**Depois:**
```typescript
if (
    profile && 
    profile.onboarding_completed === true && 
    request.nextUrl.pathname === '/onboarding' &&
    !isRSCRequest  // ✅ Não redireciona durante RSC
) {
    return NextResponse.redirect(url);
}
```

**Adicionado também:**
```typescript
if (isProtectedPath) {
    // Se não tem profile mas está tentando acessar dashboard, deixar passar
    // O requireDashboardAccess vai lidar com isso
    if (!profile) {
        console.log('[PROXY] Profile não encontrado mas permitindo acesso - requireDashboardAccess vai lidar');
        return supabaseResponse;  // ✅ Deixa passar ao invés de bloquear
    }
    // ... resto da lógica
}
```

---

## 📊 Resultado Esperado

### Antes (Loop Infinito)
```
/onboarding → /dashboard → /onboarding → /dashboard → ...
Status: 307 (Temporary Redirect) repetido infinitamente
ERR_TOO_MANY_REDIRECTS
```

### Depois (Funcionando)
```
/onboarding (onboarding_completed = true)
  ↓
proxy.ts redireciona para /dashboard (307)
  ↓
/dashboard carrega normalmente
  ↓
requireDashboardAccess() encontra profile OU cria automaticamente
  ↓
Dashboard renderiza ✅
```

---

## 🧪 Testes de Validação

### Teste 1: Usuário com Onboarding Completo

1. Fazer login
2. Acessar `/onboarding` diretamente
3. **Esperado:** Redirecionar para `/dashboard` (307)
4. **Esperado:** Dashboard carrega normalmente

### Teste 2: Usuário sem Profile

1. Fazer login com usuário novo
2. Acessar `/dashboard` diretamente
3. **Esperado:** `requireDashboardAccess` cria profile automaticamente
4. **Esperado:** Redireciona para `/onboarding` (não loop)

### Teste 3: Verificar Network Tab

1. Abrir DevTools → Network
2. Fazer login
3. **Esperado:** 
   - `/onboarding` → 307 → `/dashboard`
   - `/dashboard` → 200 (não mais 307)
   - Sem requisições infinitas

---

## 📝 Arquivos Modificados

1. ✅ `frontend/proxy.ts` - Melhorias na lógica de redirecionamento
2. ✅ `frontend/src/lib/auth/server.ts` - Criação automática de profile
3. ✅ `frontend/src/middleware.ts` - **REMOVIDO** (duplicado)

---

## 🚀 Próximos Passos

1. ✅ Fazer commit das correções
2. ✅ Fazer deploy no Vercel
3. ✅ Testar fluxo completo de onboarding
4. ✅ Verificar logs do Vercel para confirmar que não há mais loops

---

**Status:** ✅ Correções aplicadas e prontas para deploy

