# 🔧 FIX: LOOP ONBOARDING/DASHBOARD

## ✅ PROBLEMA RESOLVIDO

O loop infinito entre `/onboarding` e `/dashboard` foi causado por:
1. A página de onboarding **não salvava** que o usuário completou o processo
2. O middleware **não verificava** se o onboarding foi completado
3. O AuthContext sempre redirecionava para `/dashboard` após login

## 🛠️ CORREÇÕES IMPLEMENTADAS

### 1. Banco de Dados
- ✅ Criado campo `onboarding_completed` na tabela `profiles`
- ✅ Migration SQL em: `supabase/migrations/20231209_add_onboarding_fields.sql`

### 2. Página de Onboarding
- ✅ Adiciona lógica para salvar no banco ao selecionar perfil
- ✅ Atualiza `onboarding_completed = true` e `role` na tabela profiles
- ✅ Arquivo: `src/app/onboarding/page.tsx`

### 3. Middleware
- ✅ Verifica `onboarding_completed` antes de permitir acesso ao dashboard
- ✅ Redireciona para `/onboarding` se não completou
- ✅ Impede volta para `/onboarding` se já completou
- ✅ Arquivo: `src/middleware.ts`

### 4. AuthContext
- ✅ Carrega campo `onboarding_completed` do banco
- ✅ Redireciona para `/onboarding` após login se não completou
- ✅ Redireciona para `/dashboard` se já completou
- ✅ Arquivo: `src/contexts/AuthContext.tsx`

---

## 📋 PASSOS PARA APLICAR

### Passo 1: Executar Migration SQL no Supabase

**⚠️ IMPORTANTE: Execute este SQL no Supabase SQL Editor**

```sql
-- Adicionar campo onboarding_completed (padrão FALSE)
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;

-- Criar índice para otimizar queries
CREATE INDEX IF NOT EXISTS idx_profiles_onboarding_completed
ON public.profiles(onboarding_completed);

-- Atualizar founder para já ter completado onboarding
UPDATE public.profiles
SET onboarding_completed = TRUE
WHERE founder_access = TRUE;
```

**Como executar:**
1. Acesse: https://supabase.com/dashboard/project/YOUR_PROJECT/editor
2. Vá em **SQL Editor**
3. Cole o SQL acima
4. Clique em **RUN**

### Passo 2: Verificar se o campo foi criado

```sql
-- Verificar estrutura da tabela
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'profiles' AND column_name = 'onboarding_completed';

-- Ver dados dos usuários
SELECT id, username, role, onboarding_completed, founder_access
FROM public.profiles;
```

### Passo 3: (Opcional) Marcar usuário específico como completo

Se quiser marcar seu usuário como já tendo completado o onboarding:

```sql
-- Substituir 'SEU_EMAIL' pelo seu email
UPDATE public.profiles
SET onboarding_completed = TRUE
WHERE id = (SELECT id FROM auth.users WHERE email = 'SEU_EMAIL');
```

### Passo 4: Testar o fluxo

1. **Limpar cookies do navegador** (importante!)
2. Fazer logout
3. Fazer login novamente
4. Verificar se vai para `/onboarding`
5. Selecionar um perfil (THE ARCHITECT, THE OBSERVER, etc)
6. Verificar se salva no banco
7. Verificar se redireciona para `/dashboard`
8. Atualizar a página e verificar que **permanece** no dashboard (não volta para onboarding)

---

## 🔍 COMO FUNCIONA AGORA

### Fluxo Correto:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. LOGIN                                                     │
│    ↓                                                         │
│    AuthContext verifica onboarding_completed                │
│    ↓                                                         │
│    ┌─────────────────┬─────────────────┐                   │
│    │ FALSE           │ TRUE            │                   │
│    ↓                 ↓                 │                   │
│ /onboarding      /dashboard           │                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 2. ONBOARDING                                                │
│    ↓                                                         │
│    Usuário seleciona perfil (ARCHITECT/OBSERVER/STRATEGIST) │
│    ↓                                                         │
│    Salva no banco:                                           │
│    - onboarding_completed = TRUE                             │
│    - role = 'architect' | 'observer' | 'strategist'          │
│    ↓                                                         │
│    Animação WARP SPEED (2.5s)                                │
│    ↓                                                         │
│    Redireciona para /dashboard                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 3. MIDDLEWARE (em todas as rotas)                            │
│    ↓                                                         │
│    Verifica se está tentando acessar rota protegida          │
│    ↓                                                         │
│    ┌─────────────────┬─────────────────┐                   │
│    │ Sem onboarding  │ Com onboarding  │                   │
│    ↓                 ↓                 │                   │
│ → /onboarding     → Permite acesso    │                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐛 DEBUGGING

Se o problema persistir, adicione logs no console do navegador:

### Ver estado do onboarding:

**No Browser Console (F12):**

```javascript
// Ver o que está salvo no Supabase
const { createClient } = require('@supabase/supabase-js')
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

// Ver dados do usuário
supabase.auth.getUser().then(({ data: { user } }) => {
  console.log('User ID:', user.id)

  // Ver profile
  supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single()
    .then(({ data }) => console.log('Profile:', data))
})
```

### Logs adicionados no código:

- `[ONBOARDING] Salvando perfil:` - Quando salva no banco
- `[ONBOARDING] Perfil salvo com sucesso!` - Quando salva OK
- `[ONBOARDING] Erro ao salvar perfil:` - Se der erro
- `[ONBOARDING] Redirecionando para dashboard...` - Antes de redirecionar

---

## ✅ CHECKLIST DE VERIFICAÇÃO

```
[ ] 1. Migration SQL executada no Supabase
[ ] 2. Campo onboarding_completed existe na tabela profiles
[ ] 3. Código atualizado (git pull / atualizar arquivos)
[ ] 4. Limpar cookies do navegador
[ ] 5. Fazer logout e login novamente
[ ] 6. Verificar que vai para /onboarding
[ ] 7. Selecionar um perfil
[ ] 8. Verificar que salva no banco (Supabase > Table Editor > profiles)
[ ] 9. Verificar que redireciona para /dashboard
[ ] 10. Atualizar página e verificar que permanece no /dashboard
```

---

## 🚀 PRÓXIMOS PASSOS

Depois que o fluxo estiver funcionando:
1. Remover logs de debug (console.log) se quiser
2. Testar com diferentes usuários
3. Testar signup (novo usuário) → deve ir direto para onboarding

---

## 📞 SUPORTE

Se ainda tiver problemas:
1. Verifique os logs do console do navegador (F12)
2. Verifique se a migration foi executada corretamente
3. Verifique se o campo `onboarding_completed` existe e tem valor correto no banco

---

**Criado por:** Claude Code
**Data:** 2023-12-09
**Issue:** Loop infinito onboarding/dashboard
