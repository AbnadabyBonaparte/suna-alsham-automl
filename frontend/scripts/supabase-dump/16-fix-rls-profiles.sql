-- ═══════════════════════════════════════════════════════════════
-- 🔧 FIX: CORRIGIR RLS RECURSÃO INFINITA NA TABELA PROFILES
-- ═══════════════════════════════════════════════════════════════
-- EXECUTE ESTE SCRIPT PRIMEIRO SE VOCÊ ESTIVER TENDO O ERRO:
-- "infinite recursion detected in policy for relation profiles"
-- ═══════════════════════════════════════════════════════════════

-- PASSO 1: Ver policies atuais (diagnóstico)
SELECT 
  policyname, 
  cmd, 
  permissive,
  qual as using_clause,
  with_check
FROM pg_policies 
WHERE tablename = 'profiles';

-- ═══════════════════════════════════════════════════════════════
-- PASSO 2: Dropar TODAS as policies problemáticas
-- (Descomente e execute se necessário)
-- ═══════════════════════════════════════════════════════════════

-- DROP POLICY IF EXISTS "Users can view their own profile" ON profiles;
-- DROP POLICY IF EXISTS "Users can update their own profile" ON profiles;
-- DROP POLICY IF EXISTS "Users can insert their own profile" ON profiles;
-- DROP POLICY IF EXISTS "Enable read access for users based on auth id" ON profiles;
-- DROP POLICY IF EXISTS "Enable update for users based on auth id" ON profiles;
-- DROP POLICY IF EXISTS "Enable insert for authenticated users" ON profiles;
-- DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON profiles;
-- DROP POLICY IF EXISTS "profiles_select_policy" ON profiles;
-- DROP POLICY IF EXISTS "profiles_update_policy" ON profiles;
-- DROP POLICY IF EXISTS "profiles_insert_policy" ON profiles;

-- ═══════════════════════════════════════════════════════════════
-- PASSO 3: Criar policies CORRETAS (sem recursão)
-- ═══════════════════════════════════════════════════════════════

-- Policy para SELECT - Usuário pode ver APENAS seu próprio profile
-- IMPORTANTE: Usa auth.uid() diretamente, SEM subquery na tabela profiles
CREATE POLICY "profiles_select_own"
ON profiles FOR SELECT
USING (id = auth.uid());

-- Policy para UPDATE - Usuário pode atualizar APENAS seu próprio profile
CREATE POLICY "profiles_update_own"
ON profiles FOR UPDATE
USING (id = auth.uid())
WITH CHECK (id = auth.uid());

-- Policy para INSERT - Usuário pode inserir APENAS com seu próprio ID
CREATE POLICY "profiles_insert_own"
ON profiles FOR INSERT
WITH CHECK (id = auth.uid());

-- Policy para DELETE - Usuário pode deletar APENAS seu próprio profile
CREATE POLICY "profiles_delete_own"
ON profiles FOR DELETE
USING (id = auth.uid());

-- ═══════════════════════════════════════════════════════════════
-- PASSO 4: Verificar se as policies foram criadas corretamente
-- ═══════════════════════════════════════════════════════════════

SELECT 
  policyname, 
  cmd, 
  permissive,
  qual as using_clause,
  with_check
FROM pg_policies 
WHERE tablename = 'profiles';

-- ═══════════════════════════════════════════════════════════════
-- PASSO 5: Testar acesso (substitua pelo ID de um usuário real)
-- ═══════════════════════════════════════════════════════════════

-- SELECT * FROM profiles LIMIT 5;

-- ═══════════════════════════════════════════════════════════════
-- 📝 NOTAS IMPORTANTES:
-- ═══════════════════════════════════════════════════════════════
-- 
-- ❌ ERRADO - Causa recursão infinita:
--    USING (id = (SELECT id FROM profiles WHERE auth_user_id = auth.uid()))
--    USING (id IN (SELECT id FROM profiles WHERE ...))
--    USING (EXISTS (SELECT 1 FROM profiles WHERE ...))
--
-- ✅ CORRETO - Sem recursão:
--    USING (id = auth.uid())
--    USING (auth.uid() = id)
--
-- O erro 42P17 acontece quando a policy de SELECT faz uma subquery
-- na própria tabela profiles, criando um loop infinito.
-- ═══════════════════════════════════════════════════════════════

