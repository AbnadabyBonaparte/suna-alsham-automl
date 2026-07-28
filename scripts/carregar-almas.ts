/**
 * ═══════════════════════════════════════════════════════════════════════════
 * CARGA DAS ALMAS — OPÇÃO B — pastas agents/<slug>/ → public.agents (linha
 * nova) + public.agent_prompts (cofre)
 * ═══════════════════════════════════════════════════════════════════════════
 * ⛔ NÃO EXECUTAR sem ordem do fundador. Roda em DRY-RUN por padrão.
 *
 *   npx tsx scripts/carregar-almas.ts                 # dry-run (padrão, sem banco)
 *   npx tsx scripts/carregar-almas.ts --confirmar     # grava (exige service_role)
 *
 * ── DECRETO DO FUNDADOR: OPÇÃO B ────────────────────────────────────────────
 * Cada alma LAPIDADA (profile.md pronto no molde Cápsula X.2) vira uma LINHA
 * NOVA em public.agents, com o nome real da alma. Os 139 registros-fantasma
 * pré-existentes NÃO são tocados — a linha nova nasce com id próprio, prefixo
 * `alma-<slug>`, que não colide com nenhum id de fantasma. Depois, o
 * system_prompt (o conteúdo do profile.md) é gravado no cofre agent_prompts,
 * vinculado a essa linha nova.
 *
 * ── IDEMPOTENTE ─────────────────────────────────────────────────────────────
 * O id é determinístico (`alma-<slug>`). Antes de inserir em agents, o script
 * CHECA se o id já existe — se existe, não duplica (só garante o vínculo no
 * cofre). Rodar duas vezes não cria linha nova nem prompt duplicado.
 *
 * ── FONTE ───────────────────────────────────────────────────────────────────
 * O prompt é o profile.md LAPIDADO (a alma no molde), não a ficha crua. Só
 * entra alma cujo profile.md já saiu do esqueleto (sem "_(a preencher)_" e com
 * as 6 seções fixas). Ficha notion-só e esqueleto ficam de fora — Lei 7.
 *
 * ── SEGURANÇA ───────────────────────────────────────────────────────────────
 * Exige SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY: o cofre não tem grant para
 * anon/authenticated (migration 20260727_agent_prompts_cofre). O DRY-RUN não
 * abre conexão nenhuma — roda em qualquer lugar, só lendo o disco.
 * ═══════════════════════════════════════════════════════════════════════════
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';

const RAIZ = resolve(process.cwd(), 'agents');
const CONFIRMAR = process.argv.includes('--confirmar');

// ═══════════════════════════════════════════════════════════════════════════
// PAPÉIS — public.agents.role tem CHECK (CORE | GUARD | SPECIALIST | ANALYST).
// Default sensato por alma; o fundador pode reclassificar. Não muda a alma.
// ═══════════════════════════════════════════════════════════════════════════
const PAPEL: Record<string, 'CORE' | 'GUARD' | 'SPECIALIST' | 'ANALYST'> = {
  genesis: 'CORE', vertex: 'CORE',
  crivo: 'GUARD', sentinela: 'GUARD', vigil: 'GUARD', arbiter: 'GUARD',
  chronos: 'ANALYST',
  // todo o resto: SPECIALIST (stylus, maestro, lexis, humanizer, corpus,
  // atemporal, auteur, e futuras almas de domínio)
};
const papelDe = (slug: string) => PAPEL[slug] ?? 'SPECIALIST';

// ═══════════════════════════════════════════════════════════════════════════
// LEITURA DA ALMA LAPIDADA (o profile.md no molde)
// ═══════════════════════════════════════════════════════════════════════════
// Uma alma está PRONTA PRA CARGA quando:
//   · agents/<slug>/profile.md existe,
//   · não contém "_(a preencher)_" (não é esqueleto),
//   · tem as seções fixas do molde (marcador "## 1. IDENTIDADE").
// O nome real vem do H1 do profile.md ("# STYLUS X.1" -> "STYLUS X.1").
type Alma = { slug: string; id: string; nome: string; role: string; prompt: string; arquivo: string };

function lerAlmaLapidada(slug: string): Alma | null {
  const arquivoAbs = join(RAIZ, slug, 'profile.md');
  if (!existsSync(arquivoAbs)) return null;
  const bruto = readFileSync(arquivoAbs, 'utf8');
  if (bruto.includes('_(a preencher)_')) return null;          // esqueleto
  if (!/^##\s*1\.\s*IDENTIDADE/m.test(bruto)) return null;      // não está no molde
  const h1 = bruto.match(/^#\s+(.+?)\s*$/m);
  const nome = (h1?.[1] ?? slug.toUpperCase()).trim();
  return {
    slug,
    id: `alma-${slug}`,
    nome,
    role: papelDe(slug),
    prompt: bruto.trim(),
    arquivo: `agents/${slug}/profile.md`,
  };
}

// Classifica TODA pasta de agents/ para o painel honesto (Lei 7).
function classificar(slug: string): 'lapidada' | 'esqueleto' | 'so-notion' | 'aguarda-upload' | 'vazia' {
  const dir = join(RAIZ, slug);
  const profile = join(dir, 'profile.md');
  const originais = join(dir, 'originais');
  if (lerAlmaLapidada(slug)) return 'lapidada';
  const temSkill = existsSync(join(originais, 'skill-claude.md'));
  const temNotion = existsSync(originais) &&
    readdirSync(originais).some((f) => f.startsWith('notion-') && f.endsWith('.md'));
  const temGpt = existsSync(originais) &&
    readdirSync(originais).some((f) => !f.startsWith('notion-') && f !== '_SOBE-AQUI.md' && f !== 'skill-claude.md' && f.endsWith('.md'));
  if (temSkill || temGpt) return 'esqueleto';   // tem prompt cru, falta lapidar
  if (temNotion) return 'so-notion';            // só ficha, aguarda GPT
  if (existsSync(profile)) return 'aguarda-upload';
  return 'vazia';
}

function todosOsSlugs(): string[] {
  return readdirSync(RAIZ, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();
}

async function main() {
  const slugs = todosOsSlugs();
  const prontas = slugs.map(lerAlmaLapidada).filter((a): a is Alma => a !== null);

  console.log(CONFIRMAR
    ? '=== CARGA DAS ALMAS · OPÇÃO B · GRAVANDO ==='
    : '=== CARGA DAS ALMAS · OPÇÃO B · DRY-RUN (nada será gravado, sem conexão) ===');
  console.log(`\nAlmas LAPIDADAS prontas pra carga: ${prontas.length}\n`);
  for (const a of prontas) {
    console.log(`  ${a.slug.padEnd(22)} → agents.id="${a.id}"  role=${a.role.padEnd(10)} ${String(a.prompt.length).padStart(5)} chars  "${a.nome}"`);
  }

  if (!CONFIRMAR) {
    console.log('\n  Cada linha acima seria:');
    console.log('    1. INSERT em public.agents (id, name, role) — só se o id ainda não existir (idempotente).');
    console.log('    2. UPSERT em public.agent_prompts (agent_id=id, system_prompt=profile.md).');
    console.log('    Os 139 registros-fantasma NÃO são tocados: id "alma-<slug>" não colide com eles.');
    console.log('\n  Rode com --confirmar (e service_role no ambiente) para gravar de verdade.');
    process.exit(0);
  }

  // ─── GRAVAÇÃO (só com --confirmar) ────────────────────────────────────────
  const url = process.env.SUPABASE_URL, key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    console.error('\n⛔ Faltam SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY. O cofre só abre com service_role.');
    process.exit(1);
  }
  const { createClient } = await import('@supabase/supabase-js');
  const sb = createClient(url, key, { auth: { persistSession: false } });

  let linhasNovas = 0, jaExistiam = 0, prompts = 0, erros = 0;
  for (const a of prontas) {
    // (1) linha nova em agents — idempotente: checa por id antes de inserir
    const { data: existe, error: eSel } = await sb.from('agents').select('id').eq('id', a.id).maybeSingle();
    if (eSel) { console.error(`  [ERRO]  ${a.slug}: select agents falhou — ${eSel.message}`); erros++; continue; }

    if (!existe) {
      const { error: eIns } = await sb.from('agents').insert({ id: a.id, name: a.nome, role: a.role });
      if (eIns) { console.error(`  [ERRO]  ${a.slug}: insert agents falhou — ${eIns.message}`); erros++; continue; }
      linhasNovas++;
      console.log(`  [NOVA]  agents "${a.id}" (${a.nome}, ${a.role})`);
    } else {
      jaExistiam++;
      console.log(`  [existe] agents "${a.id}" — não duplico`);
    }

    // (2) prompt no cofre — upsert por agent_id (PK) é idempotente
    const { error: eUp } = await sb.from('agent_prompts').upsert({
      agent_id: a.id,
      system_prompt: a.prompt,
      fonte_slug: a.slug,
      fonte_arquivo: a.arquivo,
      fonte_linhagem: 'manual',            // profile.md lapidado (não é a ficha crua)
      atualizado_em: new Date().toISOString(),
      atualizado_por: 'carga-almas-opcao-b',
    }, { onConflict: 'agent_id' });
    if (eUp) { console.error(`  [ERRO]  ${a.slug}: upsert cofre falhou — ${eUp.message}`); erros++; continue; }
    prompts++;
  }

  console.log(`\nlinhas novas em agents: ${linhasNovas} · já existiam: ${jaExistiam} · prompts no cofre: ${prompts} · erros: ${erros}`);
}

main();
