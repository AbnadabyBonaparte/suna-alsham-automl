# 🛡️ Garantia com cota — a política anti-vazamento

> O sentimento do fundador: "a pessoa entra, gosta e fica; não gosta, cancela e recebe o dinheiro. Mas ninguém pode gastar meus tokens testando de graça e depois vazar."
> Este documento é o COMO — a prática de mercado que LEXIS + GENESIS escolheram, os números, e a prova de que não sangra.

**Data:** 28/jul/2026.

---

## O modelo (padrão de mercado: free-trial cap + money-back)

Duas camadas, que convivem:

1. **Arrependimento legal — 7 dias (CDC art. 49).** Reembolso **integral e incondicional**. O uso no período fica limitado à cota (o limite é do serviço, não do reembolso — o reembolso continua incondicional).
2. **Garantia comercial — 30 dias.** Reembolso integral **enquanto o uso ≤ cota de avaliação**. Ao atingir a cota, o usuário **confirma que fica** (renuncia à garantia de 30 dias — nunca à legal de 7) e o uso pleno do plano abre. Sem confirmar, segue no limite da cota até o fim da janela.
3. **Após 30 dias:** cliente efetivado, franquia cheia, garantia expirada.
4. **Fundador:** ilimitado sempre.

**A trava:** enquanto qualquer reembolso é possível, o uso nunca passa da cota Q. Logo, **o custo máximo de token de um reembolso é Q execuções**.

---

## Os números que ESCOLHEMOS (e por quê)

Cota de avaliação por plano, durante a janela de garantia:

| Plano | Cota Q | Franquia mensal do plano | Q é ~ |
|---|---|---|---|
| Starter | **100 execuções** | 1.000 req/mês | 10% |
| Pro | **300 execuções** | 10.000 req/mês | 3% |
| Enterprise | **500 execuções** | ilimitado | teto de avaliação |

**Por quê:** 100–500 execuções é suficiente para avaliar de verdade (dezenas de tarefas reais, cada uma com vários passos), mas limita a exposição a reembolso-abuso. É a faixa que trials de SaaS usam para "money-back se usou pouco".

---

## Custo de honrar um reembolso (não sangra) — prova em dry-run

Custo de token medido no próprio sistema: uma execução de agente (gpt-4o-mini) ≈ **R$ 0,007**; uma mensagem no chat ORION (Claude) ≈ **R$ 0,083**. Pior caso = usuário gasta a cota inteira e pede reembolso:

| Plano | Q | Pior caso (agentes) | Pior caso (tudo ORION) | % do valor do plano |
|---|---|---|---|---|
| Starter | 100 | R$ 0,74 | R$ 8,25 | 0,07% – 0,83% |
| Pro | 300 | R$ 2,23 | R$ 24,75 | 0,05% – 0,51% |
| Enterprise | 500 | R$ 3,71 | R$ 41,25 | 0,04% – 0,42% |

Reproduza: `npx tsx scripts/prova-cota-garantia.ts` (não gasta token, não toca banco).

---

## Como funciona no código (a trava real)

- **Medidor:** a tabela `requests` já registra `user_id` + `created_at`. O uso na janela = contagem de `requests` desde `guarantee_started_at`. Sem duplicar fonte de verdade; só um índice novo para a contagem ser barata.
- **Âncora da janela:** o webhook do Stripe grava `profiles.guarantee_started_at` na **primeira ativação** (uma vez).
- **Decisão:** `frontend/src/lib/quota.ts` (`evaluateUsage`) — função **pura**, recebe estado e devolve `{allowed, quota, usage, refundEligible, canWaive, ...}`.
- **Aplicação:** `POST /api/quantum/brain/execute` chama a cota **antes de gastar token**; sobre a cota → HTTP 429, nenhuma chamada de IA. Vale para os dois caminhos de token (agentes e chat ORION).
- **Confirmar permanência:** `POST /api/subscription/confirm-stay` grava `guarantee_waived = true` (só tem efeito após os 7 dias legais).

**O que falta o fundador fazer:** aplicar a migration `20260728_quota_garantia.sql` (aditiva, idempotente) e — quando ligar o Stripe — o teste único de ponta a ponta (ver `ATIVAR-CHECKOUT.md`).

---

## Limites honestos (Lei 7)

- A migration **não foi aplicada** aqui (o MCP do banco caiu no meio da missão). É aditiva e segura; aplicar é ato do fundador ou de um passo seguinte.
- A UI de `/pricing` diz **"Suporte 24/7"**. Os Termos adotam suporte por e-mail em horário comercial (realista). **Decisão de honestidade:** ou o fundador passa a oferecer 24/7 de verdade, ou o texto "24/7" na UI deve ser ajustado. Sinalizado, não corrigido sozinho.
- A cota bloqueia o **caminho autenticado**. O chat ORION acessível a **anônimo** (sem login) é uma exposição pré-existente e separada — recomenda-se exigir login no chat.

---
*Política de garantia com cota · ALSHAM QUANTUM · Universo Bonaparte · ALSHAM Global.*
