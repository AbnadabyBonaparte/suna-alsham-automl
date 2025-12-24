# 📋 Architecture Decision Records (ADRs)

**Registro formal de todas as decisões arquiteturais do ALSHAM QUANTUM.**

---

## 🎯 O que são ADRs?

ADRs (Architecture Decision Records) são documentos curtos que capturam decisões arquiteturais importantes. Cada ADR descreve:

- **Contexto:** Por que a decisão foi necessária
- **Decisão:** O que foi decidido
- **Consequências:** Impactos positivos e negativos
- **Status:** Aceita, Substituída, Deprecada

---

## 📂 Índice de ADRs

| # | Título | Status | Data | Impacto |
|---|--------|--------|------|---------|
| [001](./001-zustand-over-redux.md) | Zustand over Redux | ✅ Aceita | 2025-11 | State Management |
| [002](./002-supabase-over-firebase.md) | Supabase over Firebase | ✅ Aceita | 2025-11 | Backend/Database |
| [003](./003-data-honesty-policy.md) | Data Honesty Policy | ✅ Aceita | 2025-11 | Cultura/Dados |
| [004](./004-typescript-strict-mode.md) | TypeScript Strict Mode | ✅ Aceita | 2025-11 | Qualidade |
| [005](./005-faang-level-standards.md) | FAANG-Level Standards | ✅ Aceita | 2025-11 | Padrões |
| [006](./006-no-context-api.md) | No Context API | ✅ Aceita | 2025-11 | State Management |

---

## 📝 Template para Novos ADRs

```markdown
# ADR-XXX: Título da Decisão

**Status:** Proposta | Aceita | Substituída | Deprecada  
**Data:** YYYY-MM-DD  
**Decisores:** [nomes]

## Contexto

[Descreva o problema ou necessidade que motivou esta decisão]

## Decisão

[Descreva a decisão tomada]

## Alternativas Consideradas

1. **Alternativa A:** [descrição]
   - Prós: ...
   - Contras: ...

2. **Alternativa B:** [descrição]
   - Prós: ...
   - Contras: ...

## Consequências

### Positivas
- [consequência positiva 1]
- [consequência positiva 2]

### Negativas
- [consequência negativa 1]
- [consequência negativa 2]

## Referências

- [links relevantes]
```

---

## 🔄 Processo de ADR

1. **Propor:** Criar novo ADR com status "Proposta"
2. **Discutir:** Review com time técnico
3. **Aceitar:** Mudar status para "Aceita"
4. **Implementar:** Seguir a decisão no código
5. **Revisar:** Atualizar se necessário

---

## ⚠️ Regras

- **NUNCA** delete um ADR - marque como "Substituída" ou "Deprecada"
- **SEMPRE** documente alternativas consideradas
- **SEMPRE** liste consequências (positivas E negativas)
- Novos ADRs devem ser numerados sequencialmente

