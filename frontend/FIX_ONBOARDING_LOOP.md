# 🔧 CORREÇÃO - LOOP NO ONBOARDING

**Data:** 2025-12-23  
**Problema:** Usuário fica preso na página de onboarding mesmo após completar

---

## 🔍 PROBLEMA IDENTIFICADO

O middleware **NÃO estava verificando** `onboarding_completed` antes de permitir acesso ao dashboard. Ele só verificava subscription/pagamento.

**Fluxo quebrado:**
1. Usuário completa onboarding → `onboarding_completed: true` salvo no banco
2. Onboarding tenta redirecionar para `/dashboard` usando `window.location.href`
3. Middleware intercepta requisição → **NÃO verifica onboarding_completed**
4. Middleware verifica apenas subscription → pode redirecionar para `/pricing` ou bloquear
5. **LOOP ou TRAVAMENTO**

---

## ✅ CORREÇÕES APLICADAS

### 1. **Middleware agora verifica onboarding_completed**

**Arquivo:** `suna-alsham-automl/frontend/src/middleware.ts`

**Mudanças:**
- ✅ Adicionado `onboarding_completed` na query do perfil
- ✅ Verificação de onboarding_completed **ANTES** de verificar subscription
- ✅ Se `onboarding_completed === false`, redireciona para `/onboarding`
- ✅ Se perfil não existe (erro PGRST116), redireciona para `/onboarding`
- ✅ Adicionada verificação na rota `/onboarding` para redirecionar se já completo

**Antes:**
```typescript
const { data: userData } = await supabase
    .from('profiles')
    .select('subscription_plan, subscription_status, founder_access')
    .eq('id', userId)
    .single();
// Não verificava onboarding_completed
```

**Depois:**
```typescript
const { data: userData } = await supabase
    .from('profiles')
    .select('subscription_plan, subscription_status, founder_access, onboarding_completed')
    .eq('id', userId)
    .single();

// Verificar onboarding ANTES de subscription
if (userData && userData.onboarding_completed === false) {
    return NextResponse.redirect('/onboarding');
}
```

---

### 2. **Onboarding usa router.push() ao invés de window.location.href**

**Arquivo:** `frontend/src/app/onboarding/page.tsx`

**Mudanças:**
- ✅ Trocado `window.location.href` por `router.push()`
- ✅ Middleware agora garante redirecionamento correto
- ✅ Evita reload completo desnecessário

**Antes:**
```typescript
window.location.href = '/dashboard';
```

**Depois:**
```typescript
router.push('/dashboard');
```

---

## 📊 FLUXO CORRIGIDO

```
1. Usuário completa onboarding → Salva onboarding_completed: true
2. Onboarding chama router.push('/dashboard')
3. Middleware intercepta requisição → Verifica onboarding_completed ✅
4. Se onboarding_completed === true → Verifica subscription
5. Se tem subscription ou founder_access → Permite acesso ao dashboard ✅
6. Dashboard carrega normalmente ✅
```

---

## 🧪 TESTES NECESSÁRIOS

1. ✅ Completar onboarding e verificar redirecionamento para dashboard
2. ✅ Verificar que usuário não fica preso na página de onboarding
3. ✅ Verificar que middleware redireciona corretamente se onboarding não completo
4. ✅ Verificar que middleware redireciona de /onboarding para /dashboard se já completo

---

## 📝 NOTAS

- O middleware agora tem verificação completa de onboarding
- A ordem de verificação é: onboarding → subscription → acesso
- O router.push() é mais eficiente que window.location.href
- O middleware garante que não há loops de redirecionamento

