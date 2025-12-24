# 🚀 DUMP COMPLETO DO SUPABASE - INSTRUÇÕES

## Como usar estes scripts

### Passo 1: Acesse o SQL Editor do Supabase
1. Vá para https://supabase.com/dashboard
2. Selecione seu projeto `vktzdrsigrdnemdshcdp`
3. Clique em **SQL Editor** no menu lateral

### Passo 2: Execute cada script em ordem
1. Abra cada arquivo `.sql` desta pasta
2. Copie o conteúdo
3. Cole no SQL Editor
4. Clique em **Run**
5. Clique em **Download** para salvar o resultado como CSV

### Passo 3: Salve os resultados
Organize os resultados assim:
```
resultados/
├── 01-schema-completo.csv
├── 02-indices.csv
├── 03-foreign-keys.csv
├── 04-rls-policies.csv
├── 05-triggers.csv
├── 06-funcoes.csv
├── 07-storage-buckets.csv
├── 08-profiles-dados.csv
├── 09-auth-users.csv
├── 10-agents-dados.csv
├── 11-estatisticas.csv
├── 12-views.csv
├── 13-sequencias.csv
└── supabase-dump-visual.html
```

### ⚠️ IMPORTANTE: Favoritos do SQL Editor
Para salvar nos favoritos:
1. No SQL Editor, cole o script
2. Clique no ícone de estrela ⭐
3. Dê um nome como "DUMP 01 - Schema Completo"
4. Repita para cada script

---

## Scripts incluídos

| Arquivo | Descrição |
|---------|-----------|
| `02-schema-completo.sql` | Todas as tabelas, colunas, tipos |
| `03-indices.sql` | Chaves primárias, índices |
| `04-foreign-keys.sql` | Relacionamentos entre tabelas |
| `05-rls-policies.sql` | Políticas de segurança RLS |
| `06-triggers.sql` | Triggers automáticos |
| `07-funcoes.sql` | Funções customizadas |
| `08-storage-buckets.sql` | Buckets de storage |
| `09-dados-profiles.sql` | Dados da tabela profiles |
| `10-dados-auth-users.sql` | Dados dos usuários |
| `11-dados-agents.sql` | Dados dos agents |
| `12-estatisticas.sql` | Estatísticas gerais |
| `13-views.sql` | Views customizadas |
| `14-sequencias.sql` | Sequências auto-increment |
| `15-dump-visual-html.sql` | Gera HTML visual completo |

---

## Nota sobre identificadores de usuário
- O identificador canônico de usuário é `profiles.id = auth.users.id`.
- A coluna `auth_user_id` é legado e **não deve ser usada** em novas policies.

---

## 🔧 Para corrigir o erro de RLS na tabela profiles

Antes de fazer o dump, você precisa corrigir a recursão infinita. Execute primeiro:

```sql
-- Ver policies atuais
SELECT policyname, cmd, qual FROM pg_policies WHERE tablename = 'profiles';

-- Se houver policies com recursão, drope e recrie
-- DROP POLICY "nome_da_policy" ON profiles;
```

Depois crie policies simples:

```sql
-- Policy segura para SELECT
CREATE POLICY "Users can view own profile"
ON profiles FOR SELECT
USING (id = auth.uid());

-- Policy segura para UPDATE
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (id = auth.uid());

-- Policy segura para INSERT
CREATE POLICY "Users can insert own profile"
ON profiles FOR INSERT
WITH CHECK (id = auth.uid());
```

---

Gerado em: 2025-12-07
Projeto: ALSHAM QUANTUM AutoML

