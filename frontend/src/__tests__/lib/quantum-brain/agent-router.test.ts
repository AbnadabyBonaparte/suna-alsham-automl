import { resolveAgentName, resolveRole } from '@/lib/quantum-brain/agent-router';

describe('resolveAgentName (roteamento por especialização — puro)', () => {
  it.each([
    ['preciso qualificar um lead novo', 'LEAD MAGNET'],
    ['montar uma sequência de email', 'EMAIL SEQUENCE BOT'],
    ['gerar conteúdo para o blog', 'CONTENT CREATOR'],
    ['fazer mineração de dados do banco', 'DATA MINER'],
    ['auditar a segurança do sistema', 'SECURITY GUARDIAN'],
    ['otimizar a campanha de ads', 'ADS OPTIMIZER'],
    ['orquestrar o pipeline geral', 'ORCHESTRATOR ALPHA'],
  ])('mapeia "%s" → %s', (desc, expected) => {
    expect(resolveAgentName(desc)).toBe(expected);
  });

  it('é case-insensitive', () => {
    expect(resolveAgentName('QUALIFICAR LEAD')).toBe('LEAD MAGNET');
  });

  it('retorna null quando nenhuma palavra-chave casa', () => {
    expect(resolveAgentName('xyz sem relacao alguma')).toBeNull();
  });
});

describe('resolveRole (roteamento por role — puro)', () => {
  it('escolhe ANALYST para análise/dados/relatório', () => {
    expect(resolveRole('preciso de análise de dados e relatório de performance')).toBe('ANALYST');
  });

  it('escolhe GUARD para segurança/firewall', () => {
    expect(resolveRole('reforçar segurança e configurar firewall')).toBe('GUARD');
  });

  it('escolhe CORE para deploy/api/orquestrar', () => {
    expect(resolveRole('orquestrar o deploy da api no gateway')).toBe('CORE');
  });

  it('escolhe SPECIALIST para venda/marketing/email', () => {
    expect(resolveRole('campanha de marketing e email para venda')).toBe('SPECIALIST');
  });

  it('faz default para CORE sem palavras-chave', () => {
    expect(resolveRole('texto neutro qualquer')).toBe('CORE');
  });

  it('escolhe o role com maior contagem de palavras-chave', () => {
    // 1x GUARD (segurança) vs 3x ANALYST (análise, dados, relatório)
    expect(resolveRole('segurança com análise de dados e relatório')).toBe('ANALYST');
  });
});
