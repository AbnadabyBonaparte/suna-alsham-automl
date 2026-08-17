// Relatorio do Espelho — caça/espelho-AAAA-MM-DD.md
// O Espelho SEMPRE presta contas, mesmo em semana sem proposta.
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { NL } from "./util.js";

export type PorFonte = {
  fonte: string;
  trazidos: number;
  julgados: number;
  adopt: number;
  watch: number;
  discard: number;
  pending: number;
  taxaAdocao: number | null;
  taxaDescarte: number | null;
  suficiente: boolean;
};

export type Divergencia = { id: number; rel: number; fonte: string; titulo: string };

export type Calibracao = {
  julgados: number;
  superestimou: Divergencia[];
  subestimou: Divergencia[];
  acertouAlto: number;
  fonteUnicaAcimaDoTeto: number;
  fonteUnicaAdotada: number;
};

const pct = (v: number | null) => (v === null ? "—" : Math.round(v * 100) + "%");

// A partir de quantas caças vazias seguidas o Espelho abre alerta vermelho.
export const ESPELHO_STREAK_ALERTA = 3;

// Conta caças vazias consecutivas terminando na MAIS RECENTE. Vazia = nada
// trazido E custo zero.
// `hunts` chega de getHuntsSince ordenado por started_at ASCENDENTE (mais
// antiga primeiro), entao a varredura vai do FIM para o comeco. Ler na ordem
// errada daria streak 0 sempre que a janela comecasse com uma caça boa — o
// alerta nunca dispararia, que e exatamente a cegueira que isto conserta.
export function contarVaziasSeguidas(hunts: { itemsKept: number; custo: number }[]): number {
  let n = 0;
  for (let i = hunts.length - 1; i >= 0; i--) {
    const h = hunts[i];
    if (h.itemsKept === 0 && h.custo === 0) n++;
    else break;
  }
  return n;
}

export function writeEspelho(a: {
  date: string;
  janelaDias: number;
  missaoAtiva: number;
  hunts: { id: number; status: string; itemsSeen: number; itemsKept: number; custo: number }[];
  totalFindings: number;
  porFonte: PorFonte[];
  cal: Calibracao;
  veredito: { propoe: boolean; motivo: string; achados: string[] };
  propostaId: number | null;
  versaoProposta: number | null;
  minTotal: number;
  minFonte: number;
}): string {
  const L: string[] = [];
  L.push("# ESPELHO — " + a.date);
  L.push("");

  // ALERTA VERMELHO — anti-cegueira (licao da 1a Curadoria Mensal, 17/08/2026).
  // A janela de 2026-08-01 a 2026-08-17 teve 17 caças seguidas com 0 trazidos e
  // custo US$ 0,0000 — e o Espelho daquela semana nao gritou, porque so olhava
  // taxa de adocao por mina. Sem colheita nao ha o que calibrar: a autocritica
  // precisa dizer PRIMEIRO que o cacador parou de caçar.
  const vazias = contarVaziasSeguidas(a.hunts);
  if (vazias >= ESPELHO_STREAK_ALERTA) {
    L.push("> ## 🔴 ALERTA VERMELHO — O CAÇADOR ESTÁ CEGO");
    L.push("> ");
    L.push("> **" + vazias + " caças seguidas trouxeram ZERO** com custo **US$ 0,0000**.");
    L.push("> Custo zero prova que a etapa de análise não chegou a rodar — não é caça pobre, é caça que não aconteceu.");
    L.push("> ");
    L.push("> Enquanto isso a caça fecha como `partial`, sai com exit 0 e abre PR diário: **verde em todo lugar, nada no banco.**");
    L.push("> Ler `hunter_hunts.notes` e `hunter_raw_queue.queued_reason` antes de qualquer leitura de calibração — as taxas abaixo estão medindo o vazio.");
    L.push("");
  }

  L.push("_Autocritica semanal do HUNTER X.1. O caçador olha as próprias decisões e presta contas._");
  L.push("_Ele **lê, mede e propõe**. Nunca ativa, nunca abre mina, nunca muda score sozinho._");
  L.push("");
  L.push("## Resumo pro fundador");
  L.push("- Janela: **" + a.janelaDias + " dias** · missão ativa: **v" + a.missaoAtiva + "**");
  L.push("- **" + a.hunts.length + " caça(s)** · **" + a.totalFindings + " achado(s)** · **" + a.cal.julgados + " veredito(s)** do tribunal");
  L.push("- Proposta de missão: **" + (a.veredito.propoe ? "SIM — v" + a.versaoProposta + " gravada como `proposed` (id " + a.propostaId + ")" : "NÃO") + "**");
  L.push("- " + a.veredito.motivo);
  L.push("");

  L.push("## Caças da janela");
  if (!a.hunts.length) L.push("_(nenhuma caça na janela)_");
  else {
    L.push("| Caça | Status | Vistos | Trazidos | Custo US$ |");
    L.push("|---|---|---|---|---|");
    for (const h of a.hunts) L.push("| #" + h.id + " | " + h.status + " | " + h.itemsSeen + " | " + h.itemsKept + " | " + h.custo.toFixed(4) + " |");
  }
  L.push("");

  L.push("## Por mina — quem traz ouro, quem traz lixo");
  L.push("");
  L.push("`—` = sem denominador. Taxa sem veredito não é 0%, é ausência de dado (Lei 7).");
  L.push("Mina com menos de **" + a.minFonte + "** vereditos não é citada como padrão.");
  L.push("");
  L.push("| Mina | Trazidos | Julgados | Adotar | Observar | Descartar | Pendentes | Taxa adoção | Taxa descarte | Amostra |");
  L.push("|---|---|---|---|---|---|---|---|---|---|");
  if (!a.porFonte.length) L.push("| _(nenhum achado na janela)_ | | | | | | | | | |");
  for (const f of a.porFonte)
    L.push("| `" + f.fonte + "` | " + f.trazidos + " | " + f.julgados + " | " + f.adopt + " | " + f.watch + " | " + f.discard + " | " + f.pending + " | " + pct(f.taxaAdocao) + " | " + pct(f.taxaDescarte) + " | " + (f.suficiente ? "suficiente" : "**insuficiente**") + " |");
  L.push("");

  L.push("## Calibração — HUNTER × tribunal");
  L.push("");
  L.push("- Vereditos na janela: **" + a.cal.julgados + "** (mínimo para propor: **" + a.minTotal + "**)");
  L.push("- Acertos no topo (`relevance>=71` → ADOTAR): **" + a.cal.acertouAlto + "**");
  L.push("- **Superestimou** (`relevance>=71` mas DESCARTADO): **" + a.cal.superestimou.length + "**");
  for (const d of a.cal.superestimou) L.push("  - `#" + d.id + "` [" + d.rel + "] " + d.titulo + " — `" + d.fonte + "`");
  L.push("- **Subestimou** (`relevance<41` mas ADOTADO): **" + a.cal.subestimou.length + "**");
  for (const d of a.cal.subestimou) L.push("  - `#" + d.id + "` [" + d.rel + "] " + d.titulo + " — `" + d.fonte + "`");
  L.push("");

  L.push("## Aderência à regra da missão v2 (fonte única = teto OBSERVAR)");
  L.push("");
  L.push("- Fonte única com `relevance>=71` (acima do teto): **" + a.cal.fonteUnicaAcimaDoTeto + "**");
  L.push("- Desses, **ADOTADOS** pelo tribunal: **" + a.cal.fonteUnicaAdotada + "**");
  L.push("");
  L.push("> ⚠️ **NÃO VERIFICÁVEL (Lei 7):** a regra fala em *fonte única **+ baixa tração***. O schema");
  L.push("> `hunter_findings` guarda `single_source`, mas **não guarda tração** (estrelas, pontos, votos).");
  L.push("> Só a metade `single_source` foi medida. Medir tração exige coluna nova — decisão de dono.");
  L.push("");

  L.push("## Veredito do Espelho");
  L.push("");
  if (a.veredito.propoe) {
    L.push("**PROPÕE missão v" + a.versaoProposta + "** — gravada em `hunter_missions` com `status='proposed'`.");
    L.push("");
    for (const x of a.veredito.achados) L.push("- " + x);
    L.push("");
    L.push("A proposta **não está ativa** e não entra em vigor sozinha. O juiz é o fundador.");
  } else {
    L.push("**NÃO PROPÕE.** " + a.veredito.motivo);
    L.push("");
    L.push("Prestar contas de mãos vazias é o comportamento correto: sem evidência, proposta seria chute.");
  }
  L.push("");
  L.push("---");
  L.push("_Gerado pelo ESPELHO · HUNTER X.1 · o caçador se audita; o veredito é do fundador._");

  const outDir = process.env.HUNTER_REPORT_DIR || resolve(process.cwd(), "..", "caça");
  mkdirSync(outDir, { recursive: true });
  const nome = "espelho-" + a.date + ".md";
  writeFileSync(resolve(outDir, nome), L.join(NL), "utf8");
  return "caça/" + nome;
}
