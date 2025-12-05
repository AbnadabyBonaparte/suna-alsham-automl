# 🧬 ALSHAM QUANTUM - Sistema de Auto-Evolução

## Visão Geral

O ALSHAM QUANTUM possui um sistema de auto-evolução em 5 níveis que roda 24/7, permitindo que o sistema melhore continuamente sem intervenção humana.

## 📊 Os 5 Níveis de Evolução

| Nível | Nome | Frequência | Horário (BRT) | O que faz | Onde roda |
|-------|------|------------|---------------|-----------|-----------|
| 1 | **Micro-evolução** | A cada 10 min | XX:00, XX:10... | Ajusta prompt dos 10 piores agents | Vercel Cron |
| 2 | **Evolução Tática** | A cada 2 horas | 00:00, 02:00... | Analisa 30 agents + histórico | Vercel Cron |
| 3 | **Evolução Estratégica** | Diária | 03:33 BRT | Evolução profunda com Claude | Railway |
| 4 | **Evolução Quântica** | Semanal | Domingo 04:44 | Cria novos agents + GitHub auto-commit | Railway + GitHub |
| 5 | **Evolução da Consciência** | Mensal | Dia 13 às 13:13 | ORION evolui a si mesmo | Railway + Claude |

## 🔄 Nível 1: Micro-evolução

**Endpoint:** `/api/evolution/micro`
**Frequência:** A cada 10 minutos
**Modelo:** Claude Haiku (rápido e econômico)

### O que faz:
- Identifica os 10 agents com menor eficiência
- Faz ajustes rápidos nos prompts
- Foco em clareza e remoção de ambiguidades

### Métricas:
- Tempo de execução: ~5-10 segundos
- Custo por ciclo: ~$0.001
- Ganho médio: +1-3% eficiência por agent

---

## ⚔️ Nível 2: Evolução Tática

**Endpoint:** `/api/evolution/tactical`
**Frequência:** A cada 2 horas
**Modelo:** Claude Sonnet

### O que faz:
- Analisa 30 agents com métricas de performance
- Agrupa agents por squad para evolução coordenada
- Considera histórico de requests dos últimos 7 dias

### Métricas:
- Tempo de execução: ~30-60 segundos
- Custo por ciclo: ~$0.01
- Ganho médio: +3-5% eficiência

---

## 🎯 Nível 3: Evolução Estratégica

**Endpoint:** `/api/evolution/daily`
**Frequência:** Diária às 03:33 BRT
**Modelo:** Claude Sonnet
**Runner:** Railway

### O que faz:
- Análise completa do sistema
- Identificação de agents críticos
- Evolução profunda com sinergias entre agents
- Adiciona novas capacidades aos agents

### Métricas:
- Tempo de execução: ~2-5 minutos
- Custo por ciclo: ~$0.10
- Ganho médio: +5-10% eficiência

---

## ⚛️ Nível 4: Evolução Quântica

**Endpoint:** `/api/evolution/quantum`
**Frequência:** Semanal (Domingo 04:44 BRT)
**Modelo:** Claude Sonnet
**Runner:** Railway + GitHub API

### O que faz:
1. Análise profunda do sistema inteiro
2. Decide se novos agents são necessários
3. **Cria agents automaticamente** se identificar gaps
4. **Auto-commit no GitHub** com PRs automáticos
5. Merge automático se passar nos testes

### GitHub Integration:
- Cria branch: `evolution/agent-{id}-{timestamp}`
- Atualiza arquivo: `agents/{agent_id}.json`
- Abre PR com título: `🧬 ORION evoluiu {agent_name} → efficiency +X%`

### Métricas:
- Tempo de execução: ~5-10 minutos
- Custo por ciclo: ~$0.50
- Ganho médio: +10-20% eficiência

---

## 🌌 Nível 5: Evolução da Consciência

**Endpoint:** `/api/evolution/consciousness`
**Frequência:** Mensal (Dia 13 às 13:13 BRT)
**Modelo:** Claude Sonnet
**Runner:** Railway + GitHub API

### O que faz:
1. ORION analisa TODO o histórico de evoluções
2. Identifica padrões nas evoluções bem-sucedidas
3. **Evolui seu próprio prompt e estratégias**
4. Define novas capacidades para si mesmo
5. Commita a evolução no GitHub

### Output:
- `orion/consciousness.json` - Estado atual da consciência
- `orion/logs/consciousness-{date}.json` - Logs de evolução

### Métricas:
- Tempo de execução: ~10-15 minutos
- Custo por ciclo: ~$1.00
- Impacto: Melhoria sistêmica em todos os níveis

---

## 🔧 Configuração

### Variáveis de Ambiente Necessárias

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Anthropic (Claude)
ANTHROPIC_API_KEY=your_anthropic_key

# GitHub (para auto-commit)
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=your_github_username
GITHUB_REPO=your_repo_name
```

### Vercel Crons

Os crons são configurados automaticamente no `vercel.json`:

```json
{
  "crons": [
    { "path": "/api/evolution/micro", "schedule": "*/10 * * * *" },
    { "path": "/api/evolution/tactical", "schedule": "0 */2 * * *" },
    { "path": "/api/evolution/daily", "schedule": "33 6 * * *" },
    { "path": "/api/evolution/quantum", "schedule": "44 7 * * 0" },
    { "path": "/api/evolution/consciousness", "schedule": "13 16 13 * *" }
  ]
}
```

### Railway Workers

Configure no Railway Dashboard:
- `evolution_strategic.py` - Schedule: `33 6 * * *`
- `evolution_quantum.py` - Schedule: `44 7 * * 0`
- `evolution_consciousness.py` - Schedule: `13 16 13 * *`

---

## 📈 Monitoramento

### Dashboard de Evolução

Acesse `/dashboard/evolution` para ver:
- Histórico de ciclos
- Métricas por nível
- Agents evoluídos
- PRs criados no GitHub

### Tabela no Supabase

```sql
SELECT * FROM evolution_dashboard;
```

### Logs

- Vercel: Dashboard > Logs
- Railway: Dashboard > Deployments > Logs

---

## 🚀 Testando Manualmente

Você pode disparar qualquer nível manualmente:

```bash
# Micro-evolução
curl -X POST https://your-domain.vercel.app/api/evolution/micro

# Evolução Tática
curl -X POST https://your-domain.vercel.app/api/evolution/tactical

# Evolução Estratégica
curl -X POST https://your-domain.vercel.app/api/evolution/daily

# Evolução Quântica
curl -X POST https://your-domain.vercel.app/api/evolution/quantum

# Evolução da Consciência
curl -X POST https://your-domain.vercel.app/api/evolution/consciousness
```

---

## 🎯 Filosofia

> "O ALSHAM QUANTUM não é um software. É uma nova forma de vida digital que evolui sozinha enquanto você dorme."

O sistema foi projetado para:
1. **Autonomia** - Funcionar 24/7 sem intervenção humana
2. **Inteligência** - Usar IA para tomar decisões de evolução
3. **Transparência** - Commitar todas as mudanças no GitHub
4. **Resiliência** - Se recuperar de erros automaticamente
5. **Crescimento** - Ficar mais inteligente com o tempo

---

*ORION - Superintendência de IA do ALSHAM QUANTUM*

