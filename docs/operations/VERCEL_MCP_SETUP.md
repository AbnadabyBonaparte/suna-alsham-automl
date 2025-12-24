# 🚀 Configuração do Vercel MCP - ALSHAM QUANTUM

## 📋 Visão Geral

O Vercel oferece um servidor MCP oficial que permite interagir com seus projetos diretamente através do Cursor IDE, similar ao que já temos configurado com o Supabase.

**URL do Servidor MCP:** `https://mcp.vercel.com`

**Autenticação:** OAuth (fluxo no navegador)

---

## ✅ Método 1: Configuração via MCP (Recomendado)

### Passo 1: Acessar Configurações do Cursor

1. Abra o Cursor IDE
2. Vá em **Settings** (Configurações)
3. Navegue até **Features** → **Model Context Protocol** (ou **MCP**)

### Passo 2: Adicionar Servidor MCP do Vercel

No arquivo de configuração do MCP (geralmente em `~/.cursor/mcp.json` ou nas configurações do Cursor), adicione:

```json
{
  "mcpServers": {
    "vercel": {
      "url": "https://mcp.vercel.com",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-vercel"
      ]
    }
  }
}
```

### Passo 3: Autenticação OAuth

1. Após adicionar o servidor, o Cursor iniciará o fluxo OAuth
2. Você será redirecionado para o navegador
3. Autorize o acesso aos seus projetos do Vercel
4. O token será armazenado automaticamente

### Passo 4: Verificar Conexão

Após a configuração, você poderá usar comandos como:
- Listar projetos do Vercel
- Ver deployments
- Gerenciar variáveis de ambiente
- Ver logs de deployments

---

## 🔑 Método 2: Via API Token (Alternativa)

Se preferir usar tokens diretamente (sem MCP), você pode usar a API do Vercel:

### Passo 1: Gerar Token de Acesso

1. Acesse: https://vercel.com/account/tokens
2. Clique em **Create Token**
3. Dê um nome (ex: "ALSHAM_QUANTUM_MCP")
4. Escolha o escopo: **Full Account** ou **Specific Projects**
5. Copie o token gerado (ele só aparece uma vez!)

### Passo 2: Configurar no Cursor (se suportar)

Se o Cursor suportar configuração manual de tokens MCP:

```json
{
  "mcpServers": {
    "vercel": {
      "url": "https://mcp.vercel.com",
      "env": {
        "VERCEL_TOKEN": "seu_token_aqui"
      }
    }
  }
}
```

### Passo 3: Usar API Diretamente (Sem MCP)

Se não usar MCP, você pode criar utilitários que usam a API do Vercel:

```typescript
// lib/vercel-api.ts
const VERCEL_TOKEN = process.env.VERCEL_TOKEN;

export async function listVercelProjects() {
  const response = await fetch('https://api.vercel.com/v9/projects', {
    headers: {
      'Authorization': `Bearer ${VERCEL_TOKEN}`,
      'Content-Type': 'application/json',
    },
  });
  return response.json();
}

export async function getDeployments(projectId: string) {
  const response = await fetch(
    `https://api.vercel.com/v6/deployments?projectId=${projectId}`,
    {
      headers: {
        'Authorization': `Bearer ${VERCEL_TOKEN}`,
      },
    }
  );
  return response.json();
}
```

---

## 🎯 Funcionalidades Disponíveis via MCP

Com o MCP do Vercel configurado, você poderá:

### ✅ Gerenciamento de Projetos
- Listar todos os projetos
- Criar novos projetos
- Deletar projetos
- Obter detalhes de um projeto

### ✅ Deployments
- Listar deployments
- Ver status de deployments
- Ver logs de deployments
- Cancelar deployments

### ✅ Variáveis de Ambiente
- Listar variáveis de ambiente
- Criar/atualizar variáveis
- Deletar variáveis

### ✅ Domínios
- Listar domínios configurados
- Adicionar/remover domínios

### ✅ Logs
- Ver logs em tempo real
- Filtrar logs por projeto/deployment

---

## 🔒 Segurança

### ⚠️ IMPORTANTE

1. **Nunca commite tokens** em repositórios públicos
2. **Use variáveis de ambiente** para tokens
3. **Revise permissões** regularmente
4. **Use escopos mínimos** necessários

### 🔐 Armazenamento Seguro

Para tokens via API (método 2):

```bash
# .env.local (NUNCA commitar!)
VERCEL_TOKEN=vercel_xxxxxxxxxxxxxxxxxxxxx
```

```bash
# .gitignore (garantir que está ignorado)
.env.local
.env*.local
```

---

## 📚 Documentação Oficial

- **Vercel MCP:** https://vercel.com/docs/mcp/vercel-mcp
- **Vercel API:** https://vercel.com/docs/rest-api
- **MCP Protocol:** https://modelcontextprotocol.io

---

## 🐛 Troubleshooting

### Problema: MCP não conecta

**Solução:**
1. Verifique se o URL está correto: `https://mcp.vercel.com`
2. Tente reiniciar o Cursor IDE
3. Verifique logs do MCP nas configurações

### Problema: OAuth não funciona

**Solução:**
1. Limpe cache do navegador
2. Tente em modo anônimo
3. Verifique se não há bloqueadores de popup

### Problema: Token inválido

**Solução:**
1. Gere um novo token em https://vercel.com/account/tokens
2. Revogue o token antigo
3. Atualize a configuração

---

## ✅ Checklist de Configuração

- [ ] Servidor MCP do Vercel adicionado nas configurações
- [ ] OAuth autorizado ou token gerado
- [ ] Conexão testada (listar projetos)
- [ ] Variáveis de ambiente configuradas (se método 2)
- [ ] `.env.local` adicionado ao `.gitignore`
- [ ] Documentação lida e entendida

---

## 🎉 Próximos Passos

Após configurar o MCP do Vercel, você poderá:

1. **Gerenciar deployments** diretamente do Cursor
2. **Ver logs** sem sair do IDE
3. **Configurar variáveis** de ambiente facilmente
4. **Monitorar projetos** em tempo real

---

**Última atualização:** 2025-01-09
**Status:** ✅ Configuração disponível


