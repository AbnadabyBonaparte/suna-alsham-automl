-- ============================================
-- ALSHAM QUANTUM · HUNTER X.1 — funcao de dedup semantica (Fase 2)
-- Migration: 20260726_hunter_x1_dedup_fn
-- ============================================
-- Usada pelo runtime da caca (passo 'e' da liturgia): dado um embedding,
-- retorna o achado mais parecido acima do limiar. Se vier linha = ja visto.
-- service_role apenas (o runtime); anon NEGADO (mesma lei da memoria).
-- ============================================

create or replace function public.hunter_match_finding(
  query_embedding vector(1024),
  match_threshold float
)
returns table (id bigint, similarity float)
language sql stable
as $$
  select f.id, 1 - (f.embedding <=> query_embedding) as similarity
  from public.hunter_findings f
  where f.embedding is not null
    and 1 - (f.embedding <=> query_embedding) > match_threshold
  order by f.embedding <=> query_embedding
  limit 1;
$$;

revoke all on function public.hunter_match_finding(vector, float) from anon;
grant execute on function public.hunter_match_finding(vector, float) to service_role;
