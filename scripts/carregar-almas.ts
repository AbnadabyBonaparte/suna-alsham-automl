/**
 * ═══════════════════════════════════════════════════════════════════════════
 * CARGA DAS ALMAS — pastas agents/<slug>/ → public.agent_prompts
 * ═══════════════════════════════════════════════════════════════════════════
 * ⛔ NÃO EXECUTADO. Aguarda a DECISÃO DE MAPEAMENTO do fundador (ver §MAPA).
 *
 * Roda só com --confirmar. Sem a flag, faz DRY-RUN e não toca no banco.
 *
 *   npx tsx scripts/carregar-almas.ts                 # dry-run (padrão)
 *   npx tsx scripts/carregar-almas.ts --confirmar     # grava
 *
 * Exige SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY: o cofre `agent_prompts` não
 * tem grant para anon nem authenticated (migration 20260727_agent_prompts_cofre).
 *
 * IDEMPOTENTE: upsert por `agent_id` (PK). Rodar duas vezes não duplica; a
 * segunda passada só reescreve o mesmo conteúdo.
 * ═══════════════════════════════════════════════════════════════════════════
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';

const RAIZ = resolve(process.cwd(), 'agents');
const CONFIRMAR = process.argv.includes('--confirmar');

// ═══════════════════════════════════════════════════════════════════════════
// §MAPA — A DECISÃO QUE FALTA
// ═══════════════════════════════════════════════════════════════════════════
// Preencher DEPOIS do veredito do fundador. Cada entrada casa uma alma (pasta)
// com uma linha de public.agents (agent_id).
//
// Enquanto estiver vazio, o script roda em dry-run e relata "sem mapeamento".
// NÃO invente o casamento: alma trocada = agente com a instrução errada.
const MAPA: Array<{ slug: string; agentId: string }> = [
  // exemplo (NÃO ativo): { slug: 'stylus', agentId: 'orc-alpha' },
];

// ═══════════════════════════════════════════════════════════════════════════
// A FONTE-MÃE de cada linhagem
// ═══════════════════════════════════════════════════════════════════════════
// Medido no repo hoje:
//   · linhagem SKILL  → originais/skill-claude.md   5.4 KB a 15.8 KB de
//                        instrução real. É prompt de verdade.
//   · linhagem NOTION → originais/notion-A*.md      ~1.5 KB de FICHA (26 campos
//                        de metadado). `profile.md` é esqueleto de 280 bytes
//                        com "_(a preencher)_". NÃO é prompt.
function lerAlma(slug: string): { prompt: string; arquivo: string; linhagem: 'skill-claude' | 'notion' } | null {
  const dir = join(RAIZ, slug);
  if (!existsSync(dir)) return null;

  const skill = join(dir, 'originais', 'skill-claude.md');
  if (existsSync(skill)) {
    const bruto = readFileSync(skill, 'utf8');
    // corta o cabeçalho do resgate; o prompt é o SKILL.md a partir do 1º ---
    const i = bruto.indexOf('\n---\n\n');
    return {
      prompt: (i >= 0 ? bruto.slice(i + 6) : bruto).trim(),
      arquivo: `agents/${slug}/originais/skill-claude.md`,
      linhagem: 'skill-claude',
    };
  }

  const originais = join(dir, 'originais');
  const notion = existsSync(originais)
    ? readdirSync(originais).find((f) => f.startsWith('notion-') && f.endsWith('.md'))
    : undefined;
  if (notion) {
    return {
      prompt: readFileSync(join(originais, notion), 'utf8').trim(),
      arquivo: `agents/${slug}/originais/${notion}`,
      linhagem: 'notion',
    };
  }
  return null;
}

async function main() {
  console.log(CONFIRMAR ? '=== CARGA DAS ALMAS (GRAVANDO) ===' : '=== CARGA DAS ALMAS — DRY-RUN (nada será gravado) ===');

  if (MAPA.length === 0) {
    console.log('\n⛔ MAPA VAZIO — o casamento alma→agente ainda não foi decidido.');
    console.log('   Sem ele o script não grava nada. Ver §MAPA no topo do arquivo.\n');
    console.log('   Almas com PROMPT REAL disponíveis hoje (linhagem skill-claude):');
    for (const d of readdirSync(RAIZ)) {
      const a = lerAlma(d);
      if (a?.linhagem === 'skill-claude') {
        console.log(`     · ${d.padEnd(24)} ${String(a.prompt.length).padStart(6)} chars  ${a.arquivo}`);
      }
    }
    process.exit(0);
  }

  // import tardio de propósito: o DRY-RUN não deve exigir dependência alguma.
  const { createClient } = await import('@supabase/supabase-js');
  const sb = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!, {
    auth: { persistSession: false },
  });

  let ok = 0, pulados = 0;
  for (const { slug, agentId } of MAPA) {
    const alma = lerAlma(slug);
    if (!alma) { console.log(`  [PULADO] ${slug}: pasta ou fonte-mãe não encontrada`); pulados++; continue; }
    if (alma.linhagem === 'notion') {
      // Lei 7: ficha de metadado não é instrução. Não vira prompt por decreto.
      console.log(`  [PULADO] ${slug}: linhagem notion — é FICHA, não prompt. Lapidar antes.`);
      pulados++; continue;
    }

    // confere que o agente existe antes de escrever
    const { data: existe } = await sb.from('agents').select('id,name').eq('id', agentId).maybeSingle();
    if (!existe) { console.log(`  [PULADO] ${slug} → ${agentId}: agente inexistente em public.agents`); pulados++; continue; }

    if (!CONFIRMAR) {
      console.log(`  [DRY]    ${slug} → ${agentId} (${existe.name}) · ${alma.prompt.length} chars · ${alma.arquivo}`);
      ok++; continue;
    }

    const { error } = await sb.from('agent_prompts').upsert({
      agent_id: agentId,
      system_prompt: alma.prompt,
      fonte_slug: slug,
      fonte_arquivo: alma.arquivo,
      fonte_linhagem: alma.linhagem,
      atualizado_em: new Date().toISOString(),
      atualizado_por: 'carga-almas',
    }, { onConflict: 'agent_id' });

    if (error) { console.error(`  [ERRO]   ${slug} → ${agentId}: ${error.message}`); pulados++; }
    else { console.log(`  [OK]     ${slug} → ${agentId} (${existe.name}) · ${alma.prompt.length} chars`); ok++; }
  }

  console.log(`\n${CONFIRMAR ? 'gravados' : 'seriam gravados'}: ${ok} · pulados: ${pulados}`);
  if (!CONFIRMAR) console.log('Rode com --confirmar para gravar.');
}

main();
