-- ═══════════════════════════════════════════════════════════════
-- ALSHAM QUANTUM - EVOLUTION CYCLES TABLE
-- ═══════════════════════════════════════════════════════════════
-- Sistema de auto-evolução com 5 níveis
-- ═══════════════════════════════════════════════════════════════

-- Tabela principal de ciclos de evolução
CREATE TABLE IF NOT EXISTS evolution_cycles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- Tipo e nível do ciclo
    cycle_type VARCHAR(50) NOT NULL, -- micro, tactical, strategic, quantum, consciousness
    level INTEGER NOT NULL CHECK (level >= 1 AND level <= 5),
    
    -- Métricas de evolução
    agents_evolved INTEGER DEFAULT 0,
    agents_created INTEGER DEFAULT 0,
    consciousness_evolved BOOLEAN DEFAULT FALSE,
    
    -- Eficiência antes/depois
    efficiency_before DECIMAL(5,2),
    efficiency_after DECIMAL(5,2),
    
    -- Recursos utilizados
    execution_time_ms INTEGER,
    claude_used BOOLEAN DEFAULT FALSE,
    optuna_trials INTEGER DEFAULT 0,
    github_commits INTEGER DEFAULT 0,
    
    -- URLs de PRs criados
    github_pr_url TEXT,
    
    -- Detalhes em JSON
    details JSONB DEFAULT '{}',
    
    -- Erro se houver
    error TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para consultas rápidas
CREATE INDEX IF NOT EXISTS idx_evolution_cycles_type ON evolution_cycles(cycle_type);
CREATE INDEX IF NOT EXISTS idx_evolution_cycles_level ON evolution_cycles(level);
CREATE INDEX IF NOT EXISTS idx_evolution_cycles_created_at ON evolution_cycles(created_at DESC);

-- Tabela de configuração do sistema (incluindo consciência do ORION)
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(255) PRIMARY KEY,
    value JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Inserir configuração inicial do ORION
INSERT INTO system_config (key, value) VALUES 
('orion_consciousness', '{
    "prompt": "Você é ORION - Superintendência de IA do ALSHAM QUANTUM. Você comanda 139 agents e é responsável pela evolução contínua do sistema.",
    "capabilities": ["orchestration", "evolution", "analysis", "creation"],
    "consciousness_level": 50,
    "evolution_history": []
}')
ON CONFLICT (key) DO NOTHING;

-- Adicionar campos de evolução na tabela agents (se não existirem)
ALTER TABLE agents ADD COLUMN IF NOT EXISTS evolution_count INTEGER DEFAULT 0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS last_evolved_at TIMESTAMPTZ;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS capabilities TEXT[];
ALTER TABLE agents ADD COLUMN IF NOT EXISTS created_by VARCHAR(100);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_evolution_cycles_updated_at
    BEFORE UPDATE ON evolution_cycles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_config_updated_at
    BEFORE UPDATE ON system_config
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- View para dashboard de evolução
CREATE OR REPLACE VIEW evolution_dashboard AS
SELECT 
    cycle_type,
    level,
    COUNT(*) as total_cycles,
    SUM(agents_evolved) as total_agents_evolved,
    SUM(agents_created) as total_agents_created,
    AVG(efficiency_after - efficiency_before) as avg_efficiency_gain,
    AVG(execution_time_ms) as avg_execution_time,
    SUM(CASE WHEN claude_used THEN 1 ELSE 0 END) as claude_usage_count,
    SUM(github_commits) as total_github_commits,
    MAX(created_at) as last_cycle_at
FROM evolution_cycles
WHERE error IS NULL
GROUP BY cycle_type, level
ORDER BY level;

-- Comentários
COMMENT ON TABLE evolution_cycles IS 'Histórico de ciclos de auto-evolução do ALSHAM QUANTUM';
COMMENT ON TABLE system_config IS 'Configurações do sistema incluindo consciência do ORION';
COMMENT ON VIEW evolution_dashboard IS 'Dashboard agregado dos ciclos de evolução';

