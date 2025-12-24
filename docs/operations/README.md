# 🔧 Operações - ALSHAM QUANTUM

**Documentação operacional: deploy, handoff, runbooks.**

---

## 📂 Conteúdo desta Seção

| Documento | Descrição |
|-----------|-----------|
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Guia completo de deploy |
| [HANDOFF.md](./HANDOFF.md) | Transferência de contexto entre sessões |
| [ENVIRONMENT-VARIABLES.md](./ENVIRONMENT-VARIABLES.md) | Mapa de variáveis de ambiente |
| [runbooks/](./runbooks/) | Procedimentos para incidentes |

---

## 🚀 Quick Deploy

```bash
# 1. Testar localmente
cd frontend
npm run dev

# 2. Build
npm run build

# 3. Deploy (automático via Vercel)
git add -A
git commit -m "feat(scope): description"
git push origin main

# 4. Aguardar ~30s e testar em produção
# https://quantum.alshamglobal.com.br
```

---

## 🔗 Links Relacionados

- [Progresso do Projeto](../project/PROGRESS.md)
- [Padrões de Arquitetura](../policies/ARCHITECTURE-STANDARDS.md)
- [ADRs](../architecture/decisions/)

