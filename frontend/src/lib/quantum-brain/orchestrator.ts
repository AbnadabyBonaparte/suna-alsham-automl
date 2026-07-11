// ═══════════════════════════════════════════════════════════════
// ORQUESTRADOR (ORCHESTRATOR ALPHA) - MULTI-AGENTE + SKILLS
// SERVER-ONLY
// ═══════════════════════════════════════════════════════════════
// Recebe um OBJETIVO de alto nível e:
//   1. DECOMPÕE em um plano tipado (passos com dependências) — puro/determinístico
//   2. resolve cada skill → agente especialista tipado
//   3. EXECUTA os passos em ordem, ENCADEANDO a saída de um passo no
//      input do próximo (dependsOn) via executeTask (persistência real)
//   4. SINTETIZA um resultado agregado com rastro auditável
//
// Degradação honesta: sem OPENAI_API_KEY o PLANO completo ainda é
// devolvido; passos determinísticos (ex.: agregação do DATA MINER)
// executam de verdade; passos que precisam de LLM são marcados como
// 'requires_configuration'. Nunca há saída inventada.
// ═══════════════════════════════════════════════════════════════

import { createAdminClient } from '@/lib/supabase/admin';
import { executeTask, type TaskResult } from './task-executor';
import { getBehavior } from './agent-behaviors';
import { SKILLS, resolveAgentForSkill, skillRequiresLLM, type SkillId } from './skills';

const ORCHESTRATOR_ID = 'orchestrator-alpha';
const ORCHESTRATOR_NAME = 'ORCHESTRATOR ALPHA';

// Pipeline canônico de crescimento (ordem de dependência):
// levanta métricas → pontua leads → gera copy → monta sequência.
const PIPELINE: SkillId[] = ['aggregate-stats', 'score-leads', 'generate-copy', 'build-sequence'];

// Palavras-chave que "acionam" cada skill no objetivo.
const SKILL_KEYWORDS: Record<SkillId, string[]> = {
  'aggregate-stats': ['dados', 'stats', 'métrica', 'metrics', 'minerar', 'mineração', 'analisar'],
  'score-leads': ['lead', 'leads', 'pontuar', 'qualificar', 'prospect', 'prospecção'],
  'generate-copy': ['conteúdo', 'copy', 'post', 'artigo', 'content', 'criativo'],
  'build-sequence': ['email', 'e-mail', 'sequência', 'cadência', 'nutrição', 'nurture'],
};

// ─────────────────────────────────────────────────────────────
// Tipos do contrato: Objetivo → Plan → PlanResult
// ─────────────────────────────────────────────────────────────
export interface PlanStep {
  id: string; // 'step-1'
  skill: SkillId;
  agentId: string;
  agentName: string;
  description: string;
  requiresLLM: boolean;
  dependsOn: string[]; // ids de passos cuja saída alimenta este
}

export interface Plan {
  objective: string;
  steps: PlanStep[];
}

export type StepStatus = 'completed' | 'partial' | 'requires_configuration' | 'failed';

export interface StepResult {
  stepId: string;
  skill: SkillId;
  agentId: string;
  agentName: string;
  status: StepStatus;
  requiresLLM: boolean;
  output: unknown; // saída tipada do contrato do agente
  task_id?: string;
  error?: string;
}

export interface PlanResult {
  objective: string;
  plan: Plan;
  steps: StepResult[];
  configured: boolean; // houve execução com LLM?
  summary: string;
  trace: { stepId: string; agentName: string; skill: SkillId; status: StepStatus }[];
}

export interface OrchestrateParams {
  objective: string;
  user_id?: string;
  data?: Record<string, unknown>;
  /** Injeção para testes; por padrão usa o executeTask real. */
  runStep?: typeof executeTask;
}

// ─────────────────────────────────────────────────────────────
// DECOMPOSIÇÃO (pura, determinística) — Objetivo → Plan
// ─────────────────────────────────────────────────────────────
export function decomposeObjective(objective: string): Plan {
  const lower = objective.toLowerCase();

  // Skills acionadas por palavra-chave; se nenhuma casar, plano de
  // crescimento completo (papel padrão do ORCHESTRATOR ALPHA).
  let selected = PIPELINE.filter((s) => SKILL_KEYWORDS[s].some((k) => lower.includes(k)));
  if (selected.length === 0) selected = [...PIPELINE];
  // Mantém a ordem canônica do pipeline.
  selected = PIPELINE.filter((s) => selected.includes(s));

  const steps: PlanStep[] = selected.map((skill, i) => {
    const agentId = resolveAgentForSkill(skill);
    const behavior = getBehavior(agentId);
    return {
      id: `step-${i + 1}`,
      skill,
      agentId,
      agentName: behavior?.agentName ?? agentId,
      description: SKILLS[skill].summary,
      requiresLLM: skillRequiresLLM(skill),
      dependsOn: i > 0 ? [`step-${i}`] : [],
    };
  });

  return { objective, steps };
}

// ─────────────────────────────────────────────────────────────
// Persistência do plano (rastro auditável em agent_logs) — best-effort
// ─────────────────────────────────────────────────────────────
async function logOrchestration(
  eventType: 'orchestration_plan' | 'orchestration_complete',
  message: string,
  metadata: Record<string, unknown>,
): Promise<void> {
  try {
    const supabase = createAdminClient();
    await supabase.from('agent_logs').insert({
      agent_id: ORCHESTRATOR_ID,
      event_type: eventType,
      message,
      metadata,
    });
  } catch (err) {
    // Não deve derrubar a orquestração; apenas registra.
    console.error('[ORCHESTRATOR] log falhou:', err);
  }
}

function isNotConfigured(taskResult: TaskResult): boolean {
  return /OPENAI_API_KEY/.test(taskResult.error_message || '');
}

function buildSummary(objective: string, steps: StepResult[]): string {
  const by: Record<StepStatus, number> = {
    completed: 0,
    partial: 0,
    requires_configuration: 0,
    failed: 0,
  };
  steps.forEach((s) => {
    by[s.status]++;
  });

  const parts = [`Objetivo: "${objective}" — ${steps.length} passo(s)`];
  if (by.completed) parts.push(`${by.completed} concluído(s)`);
  if (by.partial) parts.push(`${by.partial} parcial(is) (saída determinística sem LLM)`);
  if (by.requires_configuration)
    parts.push(`${by.requires_configuration} requer(em) OPENAI_API_KEY`);
  if (by.failed) parts.push(`${by.failed} falhou(aram)`);
  return parts.join(' — ');
}

// ─────────────────────────────────────────────────────────────
// EXECUÇÃO + ENCADEAMENTO + SÍNTESE
// ─────────────────────────────────────────────────────────────
export async function orchestrate(params: OrchestrateParams): Promise<PlanResult> {
  const { objective, user_id, data } = params;
  const runStep = params.runStep ?? executeTask;

  // 1. Decomposição determinística (sempre disponível).
  const plan = decomposeObjective(objective);

  await logOrchestration('orchestration_plan', `Plan: ${objective}`, {
    objective,
    steps: plan.steps,
  });

  // 2. Execução em ordem, encadeando saídas.
  const results: StepResult[] = [];
  const outputsByStep = new Map<string, unknown>();

  for (const step of plan.steps) {
    // Monta o input encadeado a partir das dependências (saída → input).
    const upstream: Record<string, unknown> = {};
    for (const depId of step.dependsOn) {
      const depStep = plan.steps.find((s) => s.id === depId);
      if (depStep) upstream[depStep.skill] = outputsByStep.get(depId) ?? null;
    }
    const stepData: Record<string, unknown> = { objective, ...(data ?? {}), upstream };

    let taskResult: TaskResult;
    try {
      taskResult = await runStep({
        title: `${step.agentName}: ${step.skill}`,
        description: objective,
        data: stepData,
        user_id,
        agent_id: step.agentId,
      });
    } catch (err) {
      const error = err instanceof Error ? err.message : 'Erro desconhecido';
      results.push({
        stepId: step.id,
        skill: step.skill,
        agentId: step.agentId,
        agentName: step.agentName,
        status: 'failed',
        requiresLLM: step.requiresLLM,
        output: null,
        error,
      });
      outputsByStep.set(step.id, null);
      continue;
    }

    // Mapeia o resultado do executor para o status honesto do passo.
    let status: StepStatus;
    if (taskResult.status === 'completed') {
      status = 'completed';
    } else if (isNotConfigured(taskResult)) {
      // Sem LLM: skills determinísticas ainda produzem saída real (partial);
      // as que dependem de LLM ficam pendentes de configuração.
      status = step.requiresLLM ? 'requires_configuration' : 'partial';
    } else {
      status = 'failed';
    }

    results.push({
      stepId: step.id,
      skill: step.skill,
      agentId: step.agentId,
      agentName: step.agentName,
      status,
      requiresLLM: step.requiresLLM,
      output: taskResult.result,
      task_id: taskResult.task_id,
      error: status === 'failed' ? taskResult.error_message : undefined,
    });
    outputsByStep.set(step.id, taskResult.result);
  }

  // 3. Síntese + rastro.
  const configured = results.some((s) => s.status === 'completed');
  const summary = buildSummary(objective, results);
  const trace = results.map((r) => ({
    stepId: r.stepId,
    agentName: r.agentName,
    skill: r.skill,
    status: r.status,
  }));

  await logOrchestration('orchestration_complete', `Done: ${objective}`, {
    objective,
    configured,
    trace,
  });

  return { objective, plan, steps: results, configured, summary, trace };
}

export const ORCHESTRATOR = { id: ORCHESTRATOR_ID, name: ORCHESTRATOR_NAME };
