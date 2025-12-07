-- ═══════════════════════════════════════════════════════════════
-- RLS: PROFILES (estado canônico)
-- ═══════════════════════════════════════════════════════════════
-- Observação:
-- - O identificador canônico de usuário é profiles.id = auth.users.id
-- - auth_user_id é legado e não deve ser usado em novas policies
-- ═══════════════════════════════════════════════════════════════

-- Leitura: usuário lê apenas o próprio profile
CREATE POLICY "Users can read own profile"
  ON public.profiles
  FOR SELECT
  USING (auth.uid() = id);

-- Leitura: founders podem ler todos os profiles
CREATE POLICY "Founders can read all profiles"
  ON public.profiles
  FOR SELECT
  USING (is_founder() = true);

-- Update: usuário só atualiza o próprio profile (id canônico)
CREATE POLICY "Allow authenticated users to update own profile"
  ON public.profiles
  FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);
