import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { NL } from "./util.js";

export type ReportItem = {
  relevance: number;
  kind: string;
  title: string;
  source: string;
  url: string;
  summary_md: string;
  single_source: boolean;
  license: string | null;
  suggest: string;
};

// Canon (dossie, Parte 6): o relatorio nasce em caca/AAAA-MM-DD.md (com c-cedilha,
// nome = so a data), na raiz do repo. O runtime roda com cwd=hunter/, entao
// subimos um nivel; HUNTER_REPORT_DIR permite override.
export function writeReport(args: {
  date: string;
  itemsSeen: number;
  itemsKept: number;
  itemsQueued: number;
  sourcesOk: number;
  sourcesFail: number;
  failNotes: string[];
  costUsd: number;
  costNote: string;
  status: string;
  gold: string;
  findings: ReportItem[];
}): string {
  const L: string[] = [];
  L.push("# CAÇA — " + args.date);
  L.push("");
  L.push("## Resumo pro fundador (3 linhas)");
  L.push(
    "- " + args.itemsSeen + " itens vistos · " + args.itemsKept + " trazidos · " + args.itemsQueued + " na quarentena · custo US$ " + args.costUsd.toFixed(4) + " · status " + args.status
  );
  L.push("- OURO DO DIA: " + (args.gold || "— sem ouro hoje (dia honesto)"));
  L.push(
    "- Fontes: " + args.sourcesOk + " ok / " + args.sourcesFail + " falhas" + (args.failNotes.length ? " · NÃO VERIFICADO: " + args.failNotes.join("; ") : "")
  );
  L.push("");
  L.push("> tokens: " + args.costNote);
  L.push("");
  L.push("## Fila de julgamento");
  const sorted = args.findings.slice().sort((a, b) => b.relevance - a.relevance);
  if (!sorted.length) L.push("_(nada trazido nesta caça)_");
  for (const f of sorted) {
    L.push("");
    L.push(
      "### [" + f.relevance + "] " + f.title + " — " + f.kind + " · " + f.source + " · contra-prova:" + (f.single_source ? "não (fonte única)" : "sim") + " · licença:" + (f.license ?? "?")
    );
    L.push(f.summary_md);
    L.push(f.url);
    L.push("**veredito sugerido: " + f.suggest + "**");
  }
  L.push("");
  L.push("---");
  L.push("_Gerado pelo HUNTER X.1 · fila do tribunal · o veredito e o merge são do fundador._");
  const md = L.join(NL);

  const outDir = process.env.HUNTER_REPORT_DIR || resolve(process.cwd(), "..", "caça");
  mkdirSync(outDir, { recursive: true });
  writeFileSync(resolve(outDir, args.date + ".md"), md, "utf8");
  return "caça/" + args.date + ".md";
}
