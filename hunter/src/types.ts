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
      score: z.number().min(0).max(100),
      has_personal_data: z.boolean().default(false),
    })
  ),
});

export const EdgeSchema = z.object({
  subject: z.string(),
  relation: z.string(),
  object: z.string(),
  confidence: z.number().min(0).max(100),
});

export const AnalysisSchema = z.object({
  kind: z.enum(["tech", "paper", "tool", "pattern", "soul", "threat", "market"]),
  summary_md: z.string(),
  relevance: z.number().min(0).max(100),
  relevance_why: z.string(),
  single_source: z.boolean(),
  license: z.string().nullable().optional(),
  edges: z.array(EdgeSchema).default([]),
  soul: z
    .object({
      name: z.string(),
      origin: z.string(),
      capsule_draft: z.record(z.any()).optional(),
    })
    .nullable()
    .optional(),
});
export type Analysis = z.infer<typeof AnalysisSchema>;
