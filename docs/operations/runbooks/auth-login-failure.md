# Runbook: Falha de Login/Sessão

**Severidade:** 🔴 Crítico  
**Última Atualização:** 2025-12-23  
**Fonte:** Extraído de `frontend/docs/DOSSIE_LOGIN.md`

---

## Sintomas

- Usuário faz login com sucesso (email/password aceitos)
- Redirecionado para `/dashboard`
- Middleware bloqueia e redireciona de volta para `/login`
- Loop infinito de login
- Nenhum cookie `sb-*-auth-token` no browser

---

## Diagnóstico

### 1. Verificar Cookies no Browser
```
1. Abrir DevTools (F12)
2. Application → Cookies
3. Procurar por cookie começando com 'sb-'
4. Se ausente → problema confirmado
```

### 2. Verificar localStorage
```javascript
// No console do browser
localStorage.getItem('sb-vktzdrsigrdnemdshcdp-auth-token')
// Se existir aqui mas não em cookies → problema de SSR
```

### 3. Verificar Middleware Logs
```
1. Vercel Dashboard → Deployments → Functions
2. Procurar logs de middleware
3. Verificar mensagem "[AUTH] No Supabase cookie found"
```

### 4. Verificar Supabase Auth
```javascript
// No console do browser
const { data } = await supabase.auth.getSession();
console.log(data.session); // Se existir, auth funcionou
```

---

## Causa Raiz

```
PROBLEMA:
├── Cliente usa @supabase/supabase-js (createClient)
│   └── Salva sessão em localStorage
├── Middleware espera cookie sb-*-auth-token
│   └── Não encontra → redireciona para /login
└── Server Components não têm acesso a localStorage
    └── Sessão "perdida" no server-side
```

---

## Solução

### Opção A: Migrar para @supabase/ssr (RECOMENDADO)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();
  
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options });
        },
      },
    }
  );
}
```

### Opção B: Ajustar Middleware para aceitar header

```typescript
// middleware.ts
const authHeader = req.headers.get('authorization');
const hasAuthHeader = authHeader?.startsWith('Bearer ');

if (!hasSupabaseAuthCookie && !hasAuthHeader) {
  // Redirecionar para login
}
```

---

## Verificação Pós-Correção

1. [ ] Fazer login em aba anônima
2. [ ] Verificar cookie `sb-*-auth-token` existe
3. [ ] Navegar para `/dashboard` com sucesso
4. [ ] Refresh da página mantém sessão
5. [ ] Logout remove cookie

---

## Prevenção

1. **Usar @supabase/ssr desde o início** em projetos Next.js com App Router
2. **Testar fluxo de auth** em ambiente de preview antes de produção
3. **Monitorar logs de middleware** para detectar problemas de sessão

---

## Referências

- [Supabase SSR Documentation](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [DOSSIE_LOGIN.md](../../../frontend/docs/DOSSIE_LOGIN.md) - Análise forense completa
- [MAPA_ENVS.md](../../../frontend/docs/MAPA_ENVS.md) - Variáveis de ambiente

