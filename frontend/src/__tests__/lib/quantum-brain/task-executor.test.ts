import OpenAI from 'openai';
import { createAdminClient } from '@/lib/supabase/admin';
import {
  updateAgentStatus,
  incrementNeuralLoad,
  decrementNeuralLoad,
  getAgentById,
} from '@/lib/quantum-brain/agent-router';
import { computeCost, executeTask } from '@/lib/quantum-brain/task-executor';
import type { DataMiningResult } from '@/lib/quantum-brain/agent-behaviors';

jest.mock('openai');
jest.mock('@/lib/supabase/admin', () => ({ createAdminClient: jest.fn() }));
jest.mock('@/lib/quantum-brain/agent-router', () => ({
  routeToAgent: jest.fn(),
  getAgentById: jest.fn(),
  updateAgentStatus: jest.fn().mockResolvedValue(undefined),
  incrementNeuralLoad: jest.fn().mockResolvedValue(undefined),
  decrementNeuralLoad: jest.fn().mockResolvedValue(undefined),
}));

// ── Query-builder mock encadeável para o service-role client ──────────
function createSupabaseMock() {
  let currentTable = '';
  const singleResults: Record<string, unknown> = {
    requests: { data: { id: 'req-1' }, error: null },
    quantum_tasks: { data: { id: 'task-1' }, error: null },
  };
  const manyResults: Record<string, unknown> = {};

  const builder: Record<string, jest.Mock> & {
    single: jest.Mock;
    then: (r: (v: unknown) => unknown) => unknown;
  } = {} as never;
  const chain = ['select', 'insert', 'update', 'delete', 'eq', 'in', 'order', 'limit', 'gte', 'lt'];
  chain.forEach((m) => {
    builder[m] = jest.fn(() => builder);
  });
  builder.single = jest.fn(() =>
    Promise.resolve(singleResults[currentTable] ?? { data: null, error: null }),
  );
  builder.then = (resolve) => resolve(manyResults[currentTable] ?? { data: [], error: null });

  const from = jest.fn((table: string) => {
    currentTable = table;
    return builder;
  });

  return {
    client: { from },
    from,
    setMany: (table: string, value: unknown) => {
      manyResults[table] = value;
    },
  };
}

const mockCreate = jest.fn();
const GENERIC_AGENT = {
  id: 'revenue-hunter',
  name: 'REVENUE HUNTER',
  role: 'SPECIALIST',
  efficiency: 89,
  neural_load: 0,
  metadata: {},
};

describe('computeCost', () => {
  it('calcula custo a partir de tokens de entrada/saída', () => {
    // 200 in * 0.00015/1k + 100 out * 0.0006/1k
    expect(computeCost(200, 100)).toBeCloseTo(0.00003 + 0.00006, 10);
  });
  it('trata valores inválidos como 0', () => {
    expect(computeCost(NaN, -5)).toBe(0);
  });
});

describe('executeTask — transições de estado e custo', () => {
  let sb: ReturnType<typeof createSupabaseMock>;

  beforeEach(() => {
    jest.clearAllMocks();
    process.env.OPENAI_API_KEY = 'test-key';
    sb = createSupabaseMock();
    (createAdminClient as jest.Mock).mockReturnValue(sb.client);
    (getAgentById as jest.Mock).mockResolvedValue(GENERIC_AGENT);
    (OpenAI as unknown as jest.Mock).mockImplementation(() => ({
      chat: { completions: { create: mockCreate } },
    }));
    mockCreate.mockResolvedValue({
      usage: { total_tokens: 300, prompt_tokens: 200, completion_tokens: 100 },
      choices: [{ message: { content: '{"result":"ok"}' } }],
    });
  });

  it('IDLE→PROCESSING→IDLE, calcula custo e conclui', async () => {
    const res = await executeTask({
      title: 'Fechar venda',
      description: 'negociar contrato',
      agent_id: 'revenue-hunter',
      user_id: 'user-1',
    });

    expect(res.status).toBe('completed');
    expect(res.tokens_used).toBe(300);
    expect(res.cost_usd).toBeCloseTo(computeCost(200, 100), 10);

    // Transição de status: PROCESSING primeiro, depois IDLE
    const statuses = (updateAgentStatus as jest.Mock).mock.calls.map((c) => c[1]);
    expect(statuses).toEqual(['PROCESSING', 'IDLE']);
    expect(incrementNeuralLoad).toHaveBeenCalledWith('revenue-hunter', 15);
    expect(decrementNeuralLoad).toHaveBeenCalledWith('revenue-hunter', 15);
    expect(mockCreate).toHaveBeenCalledTimes(1);
  });

  it('marca WARNING e falha quando o LLM lança erro', async () => {
    mockCreate.mockRejectedValueOnce(new Error('boom'));
    const res = await executeTask({
      title: 'X',
      description: 'y',
      agent_id: 'revenue-hunter',
      user_id: 'user-1',
    });
    expect(res.status).toBe('failed');
    expect(res.error_message).toBe('boom');
    const statuses = (updateAgentStatus as jest.Mock).mock.calls.map((c) => c[1]);
    expect(statuses).toEqual(['PROCESSING', 'WARNING']);
    expect(decrementNeuralLoad).toHaveBeenCalled();
  });

  it('degrada com honestidade quando não há OPENAI_API_KEY (sem chamar o LLM)', async () => {
    delete process.env.OPENAI_API_KEY;
    const res = await executeTask({
      title: 'X',
      description: 'y',
      agent_id: 'revenue-hunter',
      user_id: 'user-1',
    });
    expect(res.status).toBe('failed');
    expect(res.error_message).toMatch(/OPENAI_API_KEY/);
    expect(res.tokens_used).toBe(0);
    expect(res.cost_usd).toBe(0);
    // Ainda passa por PROCESSING→IDLE (não WARNING) e não chama o LLM.
    const statuses = (updateAgentStatus as jest.Mock).mock.calls.map((c) => c[1]);
    expect(statuses).toEqual(['PROCESSING', 'IDLE']);
    expect(mockCreate).not.toHaveBeenCalled();
  });

  it('DATA MINER degradado preserva métricas REAIS agregadas do banco', async () => {
    delete process.env.OPENAI_API_KEY;
    sb.setMany('agents', {
      data: [
        { role: 'CORE', status: 'IDLE', efficiency: 90 },
        { role: 'GUARD', status: 'ERROR', efficiency: 80 },
      ],
      error: null,
    });
    (getAgentById as jest.Mock).mockResolvedValue({
      id: 'data-miner',
      name: 'DATA MINER',
      role: 'ANALYST',
      efficiency: 88,
      neural_load: 0,
      metadata: {},
    });

    const res = await executeTask({
      title: 'Minerar',
      description: 'stats',
      agent_id: 'data-miner',
      user_id: 'user-1',
    });

    const output = res.result as DataMiningResult;
    expect(output.task_type).toBe('data_mining');
    expect(output.configured).toBe(false);
    expect(output.metrics.total_agents).toBe(2);
    expect(output.metrics.active_agents).toBe(1); // ERROR não conta
    expect(output.insights).toEqual([]); // sem LLM, sem insights inventados
  });
});
