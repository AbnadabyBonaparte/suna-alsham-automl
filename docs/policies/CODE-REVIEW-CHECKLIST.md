# ✅ Code Review Checklist - ALSHAM QUANTUM

**Checklist obrigatório para aprovação de PRs.**

---

## 🚨 Regra de Ouro

**Se QUALQUER item falhar → PR REJEITADO**

Sem exceções. Sem "vou arrumar depois". Sem "é só um fix rápido".

---

## 📋 Checklist Completo

### 1. TypeScript
- [ ] Build passa sem erros (`npm run build`)
- [ ] Zero uso de `any`
- [ ] Zero uso de `@ts-ignore`
- [ ] Zero uso de `!` sem null check prévio
- [ ] Tipos de retorno explícitos em funções públicas
- [ ] Interfaces/Types para objetos complexos

### 2. State Management
- [ ] Zustand para estado compartilhado
- [ ] Não usa Context API para state
- [ ] Não usa useState para dados globais
- [ ] Store tem middleware devtools
- [ ] Actions nomeadas para rastreabilidade

### 3. Data Honesty
- [ ] Zero dados hardcoded/fake
- [ ] Todas as métricas vêm de queries reais
- [ ] Mostra 0 quando é 0 (não esconde)
- [ ] Não mistura dados de demo com produção

### 4. Error Handling
- [ ] Try/catch em todas operações async
- [ ] Erros logados com contexto
- [ ] Usuário notificado de erros (toast/alert)
- [ ] Fallbacks para estados de erro

### 5. Performance
- [ ] useMemo para cálculos pesados
- [ ] React.memo para componentes puros
- [ ] Debounce em inputs de busca
- [ ] Lazy loading para componentes pesados
- [ ] Sem re-renders desnecessários

### 6. Segurança
- [ ] Nenhuma key/secret no código
- [ ] Inputs validados
- [ ] RLS ativo em novas tabelas
- [ ] Sem console.log com dados sensíveis

### 7. Code Style
- [ ] ESLint passa sem erros
- [ ] Naming conventions seguidas
  - [ ] PascalCase para componentes
  - [ ] camelCase para funções/hooks
  - [ ] UPPER_SNAKE para constantes
- [ ] Imports organizados
- [ ] Sem código comentado

### 8. Git
- [ ] Commit message segue conventional commits
- [ ] Um commit = uma mudança lógica
- [ ] Branch name descritivo
- [ ] Sem arquivos desnecessários (node_modules, .env.local)

### 9. Documentação
- [ ] Funções complexas têm JSDoc
- [ ] README atualizado se necessário
- [ ] ADR criado para decisões arquiteturais
- [ ] PROGRESS.md atualizado se feature nova

### 10. Testes (quando aplicável)
- [ ] Testes unitários para lógica crítica
- [ ] Testes passam localmente
- [ ] Cobertura não diminuiu

---

## 🔍 Como Usar

### Para Autor do PR
1. Antes de abrir PR, passe por cada item
2. Marque os itens como completos
3. Se algum não se aplica, justifique no PR

### Para Reviewer
1. Verifique cada item
2. Comente especificamente qual item falhou
3. Não aprove até todos passarem

---

## 📝 Template de PR

```markdown
## Descrição
[O que esta PR faz]

## Tipo de Mudança
- [ ] feat: Nova feature
- [ ] fix: Bug fix
- [ ] refactor: Refatoração
- [ ] docs: Documentação
- [ ] chore: Manutenção

## Checklist
- [ ] Build passa
- [ ] Zero `any`
- [ ] Zustand para state
- [ ] Dados reais (não fake)
- [ ] Try/catch em async
- [ ] Conventional commit

## Screenshots (se UI)
[Imagens]

## Como Testar
1. [Passo 1]
2. [Passo 2]
```

---

## ❌ Motivos Comuns de Rejeição

| Problema | Exemplo | Solução |
|----------|---------|---------|
| Uso de `any` | `function f(x: any)` | Tipar corretamente |
| Dados fake | `const count = 42` | Query ao banco |
| Context API | `createContext()` | Usar Zustand |
| Sem try/catch | `await fetch()` | Envolver em try/catch |
| Commit ruim | `"fix stuff"` | `"fix(auth): resolve X"` |

---

## 🏆 Padrão de Excelência

Um PR excelente:
- ✅ Passa em todos os itens
- ✅ Tem descrição clara
- ✅ Inclui screenshots se UI
- ✅ Tem testes se lógica complexa
- ✅ Atualiza documentação relevante

---

**Lembre-se:** Somos uma empresa bilionária. Nosso código reflete isso.

