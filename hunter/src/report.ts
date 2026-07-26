import { mkdirSync, writeFileSync } from "node:fs";
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
  L.push("# CACA — " + args.date);
  L.push("");
  L.push("## Resumo pro fundador (3 linhas)");
  L.push(
    "- " + args.itemsSeen + " itens vistos · " + args.itemsKept + " trazidos · " + args.itemsQueued + " na quarentena · custo US$ " + args.costUsd.toFixed(4) + " · status " + args.status
  );
  L.push("- OURO DO DIA: " + (args.gold || "— sem ouro hoje (dia honesto)"));
  L.push(
    "- Fontes: " + args.sourcesOk + " ok / " + args.sourcesFail + " falhas" + (args.failNotes.length ? " · NAO VERIFICADO: " + args.failNotes.join("; ") : "")
  );
  L.push("");
  L.push("> tokens: " + args.costNote);
  L.push("");
  L.push("## Fila de julgamento");
  const sorted = args.findings.slice().sort((a, b) => b.relevance - a.relevance);
  if (!sorted.length) L.push("_(nada trazido nesta caca)_");
  for (const f of sorted) {
    L.push("");
    L.push(
      "### [" + f.relevance + "] " + f.title + " — " + f.kind + " · " + f.source + " · contra-prova:" + (f.single_source ? "nao (fonte unica)" : "sim") + " · licenca:" + (f.license ?? "?")
    );
    L.push(f.summary_md);
    L.push(f.url);
    L.push("**veredito sugerido: " + f.suggest + "**");
  }
  L.push("");
  L.push("---");
  L.push("_Gerado pelo HUNTER X.1 · fila do tribunal · o veredito e o merge sao do fundador._");
  const md = L.join(NL);
  mkdirSync("cacas", { recursive: true });
  const path = "cacas/caca-" + args.date + ".md";
  writeFileSync(path, md, "utf8");
  return path;
}
