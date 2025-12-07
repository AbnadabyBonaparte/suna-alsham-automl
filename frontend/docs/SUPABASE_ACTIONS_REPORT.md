# 📊 RELATÓRIO DE AÇÕES NO SUPABASE
## ALSHAM QUANTUM AutoML - suna-core

**Data:** 07/12/2025  
**Projeto:** `vktzdrsigrdnemdshcdp` (suna-core)  
**Região:** sa-east-1  
**Status:** ACTIVE_HEALTHY  

---

## 🔑 Credenciais Utilizadas

| Tipo | Prefixo | Uso |
|------|---------|-----|
| Anon Key | `W5n4H...` | Queries públicas (respeita RLS) |
| Service Role Key | `GFiIP...` | Queries administrativas (bypassa RLS) |
| Personal Access Token | `sbp_2de...` | Management API (DDL, criar funções) |

---

## 🔍 Diagnóstico Inicial

### Problema Encontrado
```
Erro: 42P17 - infinite recursion detected in policy for relation "profiles"
```

### Causa Raiz
A policy **"Founders can read all profiles"** continha uma subquery na própria tabela `profiles`:

```sql
-- ❌ POLICY PROBLEMÁTICA (causava recursão infinita)
CREATE POLICY "Founders can read all profiles" ON profiles FOR SELECT
USING (
  auth.uid() IN (
    SELECT profiles_1.id
    FROM profiles profiles_1
    WHERE (profiles_1.founder_access = true)
  )
);
```

**Por que causava recursão:**
1. Usuário tenta ler `profiles`
2. RLS verifica policy de SELECT
3. Policy executa `SELECT ... FROM profiles`
4. Esse SELECT interno também precisa verificar RLS
5. Volta ao passo 2 → **LOOP INFINITO**

---

## ✅ Ações Executadas

### 1. Verificação de Acesso (service_role key)

**Query executada:**
```sql
SELECT id, username, subscription_plan, subscription_status, founder_access
FROM profiles LIMIT 5;
```

**Resultado:**
| username | subscription_plan | subscription_status | founder_access |
|----------|------------------|---------------------|----------------|
| casamonde | enterprise | active | ✅ true |
| alsham-demo | enterprise | active | false |
| (null) | enterprise | active | false |
| (null) | free | inactive | false |
| (null) | free | inactive | false |

**Observação:** Usuário `casamonde` é o founder com acesso total.

---

### 2. Análise das Policies Existentes

**Query executada:**
```sql
SELECT policyname, cmd, qual FROM pg_policies WHERE tablename = 'profiles';
```

**Resultado (ANTES da correção):**
| policyname | cmd | qual |
|------------|-----|------|
| Allow authenticated users to update own profile | UPDATE | `(auth.uid() = auth_user_id)` |
| Founders can read all profiles | SELECT | ❌ `(auth.uid() IN (SELECT profiles_1.id FROM profiles profiles_1 WHERE ...))` |
| Users can read own profile | SELECT | `(auth.uid() = id)` |

---

### 3. Remoção da Policy Problemática

**Query executada:**
```sql
DROP POLICY IF EXISTS "Founders can read all profiles" ON profiles;
```

**Status:** ✅ Executado com sucesso

---

### 4. Criação de Função SECURITY DEFINER

**Query executada:**
```sql
CREATE OR REPLACE FUNCTION public.is_founder()
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
STABLE
AS $$
  SELECT COALESCE(
    (SELECT founder_access FROM profiles WHERE id = auth.uid()),
    false
  )
$$;
```

**Por que SECURITY DEFINER:**
- Executa com privilégios do **owner da função** (superuser)
- **Bypassa RLS** durante a verificação
- Não causa recursão porque não passa pela verificação de policies

**Status:** ✅ Executado com sucesso

---

### 5. Criação da Nova Policy (Corrigida)

**Query executada:**
```sql
CREATE POLICY "Founders can read all profiles" ON profiles FOR SELECT
USING (public.is_founder() = true);
```

**Status:** ✅ Executado com sucesso

---

### 6. Verificação Final das Policies

**Query executada:**
```sql
SELECT policyname, cmd, qual FROM pg_policies WHERE tablename = 'profiles';
```

**Resultado (DEPOIS da correção):**
| policyname | cmd | qual |
|------------|-----|------|
| Allow authenticated users to update own profile | UPDATE | `(auth.uid() = auth_user_id)` |
| Founders can read all profiles | SELECT | ✅ `(is_founder() = true)` |
| Users can read own profile | SELECT | `(auth.uid() = id)` |

---

### 7. Teste de Funcionamento

**Query de teste (com anon key):**
```sql
SELECT id, username, founder_access FROM profiles LIMIT 3;
```

**Resultado:**
- ✅ **ANTES:** Erro `42P17 - infinite recursion`
- ✅ **DEPOIS:** Retorna `[]` (array vazio, correto para usuário não autenticado)

---

## 📁 Scripts SQL Criados

Criei uma pasta com scripts organizados para dump completo do Supabase:

```
frontend/scripts/supabase-dump/
├── 01-INSTRUCOES.md              # Guia de uso
├── 02-schema-completo.sql        # Todas tabelas/colunas/tipos
├── 03-indices.sql                # Chaves primárias e índices
├── 04-foreign-keys.sql           # Relacionamentos entre tabelas
├── 05-rls-policies.sql           # Políticas de segurança RLS
├── 06-triggers.sql               # Triggers automáticos
├── 07-funcoes.sql                # Funções customizadas
├── 08-storage-buckets.sql        # Buckets de storage
├── 09-dados-profiles.sql         # Dados da tabela profiles
├── 10-dados-auth-users.sql       # Dados dos usuários auth
├── 11-dados-agents.sql           # Dados dos 139 agents
├── 12-estatisticas.sql           # Estatísticas do banco
├── 13-views.sql                  # Views customizadas
├── 14-sequencias.sql             # Sequências auto-increment
├── 15-dump-visual-html.sql       # Gera HTML visual bonito
├── 16-fix-rls-profiles.sql       # Script de correção de RLS
└── 17-todas-tabelas-contagem.sql # Contagem de linhas
```

---

## 📊 Estado Final do Banco

### Tabela `profiles`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | uuid | PK, FK para auth.users |
| auth_user_id | uuid | FK para auth.users (legacy?) |
| username | text | Nome de usuário |
| full_name | text | Nome completo |
| avatar_url | text | URL do avatar |
| role | text | Role do usuário |
| subscription_plan | text | `free`, `pro`, `enterprise` |
| subscription_status | text | `active`, `inactive`, `canceled` |
| founder_access | boolean | Acesso especial de founder |
| created_at | timestamptz | Data de criação |
| updated_at | timestamptz | Data de atualização |

### Policies Atuais na `profiles`

| Policy | Operação | Condição | Status |
|--------|----------|----------|--------|
| Users can read own profile | SELECT | `auth.uid() = id` | ✅ OK |
| Founders can read all profiles | SELECT | `is_founder() = true` | ✅ CORRIGIDA |
| Allow authenticated users to update own profile | UPDATE | `auth.uid() = auth_user_id` | ✅ OK |

### Funções Criadas

| Função | Tipo | Descrição |
|--------|------|-----------|
| `public.is_founder()` | SECURITY DEFINER | Verifica se usuário é founder (bypassa RLS) |

---

## ⚠️ Observações Importantes

### 1. Discrepância nos campos de ID
A policy de UPDATE usa `auth_user_id`, mas as de SELECT usam `id`. Isso pode indicar:
- Migração incompleta de schema
- Dois campos diferentes apontando para auth.users

**Recomendação:** Verificar se `id` e `auth_user_id` sempre têm o mesmo valor na tabela profiles.

### 2. Usuários sem acesso
Usuários com `subscription_status = 'inactive'` e `founder_access = false` não conseguirão acessar o dashboard (comportamento correto).

### 3. Scripts não salvos em favoritos
Os favoritos do SQL Editor do Supabase são armazenados na conta do usuário no dashboard, não há API pública para gerenciá-los programaticamente. Os scripts precisam ser adicionados manualmente.

---

## 🔒 Segurança

### Tokens Expostos (Rotacionar se necessário)
- Personal Access Token foi usado nesta sessão
- Service Role Key foi usada nesta sessão

**Recomendação:** Se desejar máxima segurança, rotacione o Personal Access Token em:
https://supabase.com/dashboard/account/tokens

---

## ✅ Checklist de Verificação

- [x] Erro 42P17 corrigido
- [x] Função `is_founder()` criada
- [x] Policy "Founders can read all profiles" recriada sem recursão
- [x] Teste de acesso bem-sucedido
- [x] Scripts de dump criados
- [ ] Scripts adicionados aos favoritos (manual)
- [ ] Verificar discrepância `id` vs `auth_user_id`

---

## 📞 Suporte

Se precisar de mais alterações no Supabase, as credenciais necessárias são:
- **Service Role Key** - para queries administrativas
- **Personal Access Token** - para DDL (CREATE/DROP/ALTER)

---

**Relatório gerado automaticamente por Cursor AI**  
**Data:** 07/12/2025  
**Projeto:** ALSHAM QUANTUM AutoML

