import { z } from "zod";

export type RawItem = {
  source: string;
  url: string;
  title: string;
  rawText: string;
};

export const TriageSchema = z.object({
  results: z.array(
    z.object({
      idx: z.number().int(),
      verdict: z.enum(["lixo", "talvez", "ouro"]),
      score: z.coerce.number().min(0).max(100).catch(0),
      has_personal_data: z.boolean().catch(false),
    })
  ),
});

export const EdgeSchema = z.object({
  subject: z.string(),
  relation: z.string(),
  object: z.string(),
  confidence: z.coerce.number().min(0).max(100).catch(50),
});

// Schema TOLERANTE (Lei 8: falhar barato): a omissao ou o tipo errado de um
// campo secundario nao derruba o achado inteiro. Apenas summary_md e
// obrigatorio de fato — sem resumo, o achado nao serve ao tribunal.
export const AnalysisSchema = z.object({
  kind: z.enum(["tech", "paper", "tool", "pattern", "soul", "threat", "market"]).catch("tech"),
  summary_md: z.string().min(1),
  relevance: z.coerce.number().min(0).max(100).catch(0),
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
