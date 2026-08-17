// ============================================================================
// FASE 4 — O ESPELHO · autocritica semanal do HUNTER X.1
// ============================================================================
// O cacador olha para as proprias decisoes da semana, cruza o SEU score
// (relevance) com o veredito do TRIBUNAL (verdict), e — se e somente se houver
// evidencia numerica suficiente — PROPOE uma missao v-proxima.
//
// Ele nunca ativa. Nunca abre mina. Nunca mexe em score sozinho.
// LE · MEDE · PROPOE. O juiz e o fundador.
//
// Lei 7: sem amostra, o Espelho diz "amostra insuficiente" e NAO propoe.
// Prestar contas de maos vazias e melhor do que inventar padrao.
// ============================================================================
import {
  db,
  getHuntsSince,
  getFindingsSince,
  getActiveMissionOrThrow,
  maxMissionVersion,
  insertMissionProposal,
  ESPELHO_STATUS_UNICO,
  ESPELHO_AUTOR,
  createIssue,
  type FindingJulgado,
} from "./db.js";
import { writeEspelho, type PorFonte, type Calibracao } from "./espelho-report.js";
import { NL, todayUTC } from "./util.js";

// ── Limiares de evidencia (Lei 7) ───────────────────────────────────────────
// Abaixo disto o Espelho NAO propoe. Numeros escolhidos para que uma unica
// caca ruim nao vire decreto: 20 vereditos no total, 5 por mina para a mina
// ser citada nominalmente.
export const MIN_VEREDITOS_TOTAL = Number(process.env.HUNTER_ESPELHO_MIN_TOTAL || 20);
export const MIN_VEREDITOS_FONTE = Number(process.env.HUNTER_ESPELHO_MIN_FONTE || 5);
const JANELA_DIAS = Number(process.env.HUNTER_ESPELHO_DIAS || 7);

const JULGADOS = ["adopt", "watch", "discard"];

export function medirPorFonte(fs: FindingJulgado[]): PorFonte[] {
  const mapa = new Map<string, PorFonte>();
  for (const f of fs) {
    const cur = mapa.get(f.source) ?? { fonte: f.source, trazidos: 0, julgados: 0, adopt: 0, watch: 0, discard: 0, pending: 0, taxaAdocao: null, taxaDescarte: null, suficiente: false };
    cur.trazidos++;
    if (f.verdict === "pending") cur.pending++;
    if (JULGADOS.includes(f.verdict)) {
      cur.julgados++;
      if (f.verdict === "adopt") cur.adopt++;
      else if (f.verdict === "watch") cur.watch++;
      else cur.discard++;
    }
    mapa.set(f.source, cur);
  }
  for (const v of mapa.values()) {
    v.suficiente = v.julgados >= MIN_VEREDITOS_FONTE;
    // Taxa so existe com denominador. Sem veredito, e null — nunca 0%.
    v.taxaAdocao = v.julgados ? v.adopt / v.julgados : null;
    v.taxaDescarte = v.julgados ? v.discard / v.julgados : null;
  }
  return [...mapa.values()].sort((a, b) => b.trazidos - a.trazidos);
}

export function medirCalibracao(fs: FindingJulgado[]): Calibracao {
  const julgados = fs.filter((f) => JULGADOS.includes(f.verdict));
  // Faixas historicas do HUNTER (a antiga suggest(): >=71 ADOTAR · 41-70 OBSERVAR
  // · <41 DESCARTAR). suggest() foi REMOVIDA — o limiar de 71 ficava abaixo do
  // piso da triagem (72), entao 100% dos achados saiam sugeridos como ADOTAR.
  // As faixas seguem valendo AQUI, onde medem calibracao contra o veredito real
  // do tribunal: e a unica leitura em que o numero tem significado.
  const superestimou = julgados.filter((f) => f.relevance >= 71 && f.verdict === "discard");
  const subestimou = julgados.filter((f) => f.relevance < 41 && f.verdict === "adopt");
  const acertouAlto = julgados.filter((f) => f.relevance >= 71 && f.verdict === "adopt");
  // Regra da missao v2: fonte unica + baixa tracao = teto de OBSERVAR.
  // O schema NAO guarda tracao (estrelas/pontos) — so single_source. Medimos
  // a metade que existe e declaramos a outra como NAO VERIFICAVEL.
  const fonteUnicaAcimaDoTeto = julgados.filter((f) => f.single_source && f.relevance >= 71);
  const fonteUnicaAdotada = fonteUnicaAcimaDoTeto.filter((f) => f.verdict === "adopt");
  return {
    julgados: julgados.length,
    superestimou: superestimou.map((f) => ({ id: f.id, rel: f.relevance, fonte: f.source, titulo: f.title })),
    subestimou: subestimou.map((f) => ({ id: f.id, rel: f.relevance, fonte: f.source, titulo: f.title })),
    acertouAlto: acertouAlto.length,
    fonteUnicaAcimaDoTeto: fonteUnicaAcimaDoTeto.length,
    fonteUnicaAdotada: fonteUnicaAdotada.length,
  };
}

export type Veredito = { propoe: boolean; motivo: string; achados: string[] };

// A decisao de propor ou nao. Isolada de proposito: e o que o teste crava.
export function decidir(porFonte: PorFonte[], cal: Calibracao): Veredito {
  const achados: string[] = [];
  if (cal.julgados < MIN_VEREDITOS_TOTAL) {
    return {
      propoe: false,
      motivo: "amostra insuficiente: " + cal.julgados + " veredito(s) na janela, minimo " + MIN_VEREDITOS_TOTAL + ". O Espelho nao propoe sem evidencia (Lei 7).",
      achados,
    };
  }
  for (const f of porFonte) {
    if (!f.suficiente) continue;
    if (f.taxaDescarte !== null && f.taxaDescarte >= 0.6)
      achados.push("mina `" + f.fonte + "`: " + Math.round(f.taxaDescarte * 100) + "% de DESCARTE em " + f.julgados + " vereditos — candidata a peso menor na triagem");
    if (f.taxaAdocao !== null && f.taxaAdocao >= 0.6)
      achados.push("mina `" + f.fonte + "`: " + Math.round(f.taxaAdocao * 100) + "% de ADOCAO em " + f.julgados + " vereditos — candidata a peso maior");
  }
  if (cal.superestimou.length >= 3)
    achados.push("calibracao: " + cal.superestimou.length + " achados com relevance>=71 foram DESCARTADOS pelo tribunal — o HUNTER esta pontuando alto demais");
  if (cal.subestimou.length >= 3)
    achados.push("calibracao: " + cal.subestimou.length + " achados com relevance<41 foram ADOTADOS — o HUNTER esta pontuando baixo demais");
  if (cal.fonteUnicaAdotada >= 3)
    achados.push("regra v2 (fonte unica = teto OBSERVAR): " + cal.fonteUnicaAdotada + " achados de fonte unica com relevance>=71 foram ADOTADOS — a regra nao esta segurando");
  if (!achados.length)
    return { propoe: false, motivo: "amostra suficiente (" + cal.julgados + " vereditos), mas nenhum padrao cruzou o limiar. Semana sem proposta — e um resultado, nao uma falha.", achados };
  return { propoe: true, motivo: achados.length + " padrao(oes) com evidencia numerica.", achados };
}

async function main() {
  const sb = db();
  const desde = new Date(Date.now() - JANELA_DIAS * 86400000).toISOString();
  const hoje = todayUTC();

  const missao = await getActiveMissionOrThrow(sb);
  const hunts = await getHuntsSince(sb, desde);
  const finds = await getFindingsSince(sb, desde);

  const porFonte = medirPorFonte(finds);
  const cal = medirCalibracao(finds);
  const v = decidir(porFonte, cal);

  let propostaId: number | null = null;
  let versaoProposta: number | null = null;
  if (v.propoe) {
    const prox = (await maxMissionVersion(sb)) + 1;
    const md = [
      "# Missao v" + prox + " — PROPOSTA do Espelho (nao ativa)",
      "",
      "Gerada em " + hoje + " a partir de " + cal.julgados + " vereditos reais na janela de " + JANELA_DIAS + " dias.",
      "",
      "## Evidencia",
      ...v.achados.map((a) => "- " + a),
      "",
      "## Texto herdado da missao ativa (v" + missao.version + ")",
      "",
      String(missao.mission_md ?? ""),
      "",
      "---",
      "_Proposta do HUNTER. As minas seguem identicas — o Espelho nao abre mina. Ativar e ato do fundador._",
    ].join(NL);
    // sources IDENTICO ao ativo: a trava rejeita qualquer divergencia.
    propostaId = await insertMissionProposal(
      sb,
      { version: prox, status: ESPELHO_STATUS_UNICO, mission_md: md, sources: missao.sources, scoring_rules: missao.scoring_rules, created_by: ESPELHO_AUTOR },
      missao.sources,
      cal.julgados
    );
    versaoProposta = prox;
  }

  const caminho = writeEspelho({
    date: hoje,
    janelaDias: JANELA_DIAS,
    missaoAtiva: missao.version,
    hunts: hunts.map((h: any) => ({ id: h.id, status: h.status, itemsSeen: h.items_seen, itemsKept: h.items_kept, custo: Number(h.cost_usd ?? 0) })),
    totalFindings: finds.length,
    porFonte,
    cal,
    veredito: v,
    propostaId,
    versaoProposta,
    minTotal: MIN_VEREDITOS_TOTAL,
    minFonte: MIN_VEREDITOS_FONTE,
  });

  console.log("Espelho " + hoje + " · " + cal.julgados + " vereditos · propoe=" + v.propoe + (versaoProposta ? " · v" + versaoProposta + " proposed #" + propostaId : "") + " · " + caminho);
  console.log(v.motivo);

  if ((process.env.ESPELHO_OPEN_ISSUE ?? "").toLowerCase() === "true" && v.propoe) {
    await createIssue(
      "[ESPELHO] Proposta de missao v" + versaoProposta + " aguardando juizo",
      ["## 🪞 O Espelho propos uma missao", "", "Status: `proposed` — **nao ativa**. Ativar e ato do fundador.", "", "### Evidencia", ...v.achados.map((a) => "- " + a), "", "Relatorio: `" + caminho + "`"].join(NL)
    );
  }
}

main();
