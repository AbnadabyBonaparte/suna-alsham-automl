import { z } from "zod";

export type RawItem = {
  source: string;
  url: string;
  title: string;
  rawText: string;
};

// Normaliza um numero para inteiro 0-100. O modelo as vezes devolve fracao
// 0-1 (ex.: 0.96) e as vezes 0-100 (ex.: 96). Colunas do banco sao INT.
const intScore = (fallback: number) =>
  z.coerce
    .number()
    .catch(fallback)
    .transform((n) => {
      const scaled = n > 0 && n <= 1 ? n * 100 : n;
      return Math.max(0, Math.min(100, Math.round(scaled)));
    });

export const TriageSchema = z.object({
  results: z.array(
    z.object({
      idx: z.number().int(),
      verdict: z.enum(["lixo", "talvez", "ouro"]),
      score: intScore(0),
      has_personal_data: z.boolean().catch(false),
    })
  ),
});

export const EdgeSchema = z.object({
  subject: z.string(),
  relation: z.string(),
  object: z.string(),
  confidence: intScore(50),
});

// Schema TOLERANTE (Lei 8: falhar barato): a omissao ou o tipo errado de um
// campo secundario nao derruba o achado inteiro. Apenas summary_md e
// obrigatorio de fato — sem resumo, o achado nao serve ao tribunal.
export const AnalysisSchema = z.object({
  kind: z.enum(["tech", "paper", "tool", "pattern", "soul", "threat", "market"]).catch("tech"),
  summary_md: z.string().min(1),
  relevance: intScore(0),
  relevance_why: z.string().catch(""),
  single_source: z.boolean().catch(true),
  license: z.string().nullable().optional().catch(null),
  edges: z.array(EdgeSchema).catch([]),
  soul: z
    .object({
      name: z.string(),
      origin: z.string(),
      capsule_draft: z.record(z.any()).optional(),
    })
    .nullable()
    .optional()
    .catch(null),
});
export type Analysis = z.infer<typeof AnalysisSchema>;
