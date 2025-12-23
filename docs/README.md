# 📚 ALSHAM QUANTUM - Centro de Documentação

**Versão:** 1.0.0  
**Última Atualização:** 2025-12-23  
**Status:** 🟢 Enterprise-Grade

---

## 🎯 Navegação Rápida

### Para IAs e Assistentes
| Arquivo | Localização | Função |
|---------|-------------|--------|
| [CLAUDE.md](../CLAUDE.md) | Raiz | Instruções para Claude (Anthropic) |
| [.cursorrules](../.cursorrules) | Raiz | Regras para Cursor IDE |
| [copilot-instructions.md](../.github/copilot-instructions.md) | .github/ | Instruções para GitHub Copilot |

### Para Desenvolvedores
| Seção | Conteúdo |
|-------|----------|
| [architecture/](./architecture/) | Arquitetura, decisões técnicas, diagramas |
| [operations/](./operations/) | Deploy, handoff, runbooks |
| [policies/](./policies/) | Políticas e padrões obrigatórios |
| [project/](./project/) | Progresso, changelog, roadmap |

---

## 📂 Estrutura Completa

```
docs/
├── README.md                    ← VOCÊ ESTÁ AQUI
│
├── architecture/                ← Decisões técnicas
│   ├── README.md
│   ├── SYSTEM-ARCHITECTURE.md   ← Visão geral do sistema
│   ├── DATABASE-SCHEMA.md       ← Schema do banco
│   └── decisions/               ← ADRs (Architecture Decision Records)
│       ├── README.md
│       ├── 001-zustand-over-redux.md
│       ├── 002-supabase-over-firebase.md
│       ├── 003-data-honesty-policy.md
│       ├── 004-typescript-strict-mode.md
│       ├── 005-faang-level-standards.md
│       └── 006-no-context-api.md
│
├── operations/                  ← Operações e deploy
│   ├── README.md
│   ├── DEPLOYMENT.md            ← Guia de deploy
│   ├── HANDOFF.md               ← Transferência de contexto
│   ├── ENVIRONMENT-VARIABLES.md ← Mapa de variáveis
│   └── runbooks/                ← Procedimentos de incidentes
│       ├── README.md
│       └── auth-login-failure.md
│
├── policies/                    ← Políticas obrigatórias
│   ├── README.md
│   ├── HONESTY.md               ← Política de dados reais
│   ├── ARCHITECTURE-STANDARDS.md ← Padrões de código
│   └── CODE-REVIEW-CHECKLIST.md ← Checklist de review
│
└── project/                     ← Status do projeto
    ├── README.md
    ├── PROGRESS.md              ← Progresso atual
    ├── CHANGELOG.md             ← Histórico de mudanças
    └── ROADMAP.md               ← Próximos passos
```

---

## 🚀 Quick Start

### Novo Desenvolvedor?
1. Leia [policies/ARCHITECTURE-STANDARDS.md](./policies/ARCHITECTURE-STANDARDS.md)
2. Leia [policies/HONESTY.md](./policies/HONESTY.md)
3. Siga [operations/DEPLOYMENT.md](./operations/DEPLOYMENT.md)

### Nova IA/Assistente?
1. Leia [CLAUDE.md](../CLAUDE.md) ou equivalente
2. Consulte [architecture/decisions/](./architecture/decisions/) para contexto
3. Verifique [project/PROGRESS.md](./project/PROGRESS.md) para estado atual

### Precisa fazer Deploy?
1. [operations/DEPLOYMENT.md](./operations/DEPLOYMENT.md)
2. [operations/ENVIRONMENT-VARIABLES.md](./operations/ENVIRONMENT-VARIABLES.md)

### Incidente em Produção?
1. [operations/runbooks/](./operations/runbooks/)

---

## 📋 Índice de Decisões Arquiteturais (ADRs)

| # | Decisão | Status | Data |
|---|---------|--------|------|
| 001 | [Zustand over Redux](./architecture/decisions/001-zustand-over-redux.md) | ✅ Aceita | 2025-11 |
| 002 | [Supabase over Firebase](./architecture/decisions/002-supabase-over-firebase.md) | ✅ Aceita | 2025-11 |
| 003 | [Data Honesty Policy](./architecture/decisions/003-data-honesty-policy.md) | ✅ Aceita | 2025-11 |
| 004 | [TypeScript Strict Mode](./architecture/decisions/004-typescript-strict-mode.md) | ✅ Aceita | 2025-11 |
| 005 | [FAANG-Level Standards](./architecture/decisions/005-faang-level-standards.md) | ✅ Aceita | 2025-11 |
| 006 | [No Context API](./architecture/decisions/006-no-context-api.md) | ✅ Aceita | 2025-11 |

---

## 🏢 Sobre o Projeto

**ALSHAM QUANTUM** é uma plataforma enterprise de CRM/AutoML com:
- 139 agentes de IA configurados
- 27 tabelas no banco de dados
- 25 páginas no frontend
- Sistema de auto-evolução em 5 níveis
- Padrões FAANG de qualidade

**Filosofia:** Dados reais, código enterprise, zero paliativos.

---

**Mantido por:** ALSHAM GLOBAL  
**Padrão:** Enterprise-Grade (Bilionário)

