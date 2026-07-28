# ⚖️ Checkout jurídico — o que falta VOCÊ decidir

> Os 3 documentos (Termos, Reembolso, Privacidade) estão escritos e no ar em `/terms`, `/refund`, `/privacy`. LEXIS ancorou tudo na lei brasileira real (CDC, LGPD, Marco Civil). Ficaram **8 pontos** que dependem de decisão sua — marcados no texto como `(definir: fundador)`. Enquanto não decidir, o texto honra o mínimo legal e o que a UI já promete.

**Data:** 28/jul/2026. **Empresa:** ALSHAM Global Commerce Ltda. · CNPJ 59.332.265/0001-30 · comercial@alshamglobal.com.br.

---

## As 8 decisões (marcadas no texto)

### Termos de Assinatura (`/terms`)
1. **Antecedência de reajuste de preço** — quanto tempo antes você avisa um aumento? (sugestão LEXIS: 30 dias.)
2. **SLA e horário de suporte por plano** — a UI diz "24/7" no Pro/Enterprise. Isso é real? Defina os canais e horários que você consegue cumprir (Lei 7 — não prometer o que não se honra).
3. **Comarca do foro** — qual comarca de Goiás? (a cidade da sede.)

### Política de Reembolso (`/refund`)
4. **Garantia de 30 dias — integral ou proporcional?** Depois dos 7 dias legais (arrependimento CDC), a garantia de 30 dias devolve o valor **cheio** ou proporcional ao uso?
5. **Garantia de 30 dias — só a 1ª assinatura ou todo ciclo novo?**
6. **Prazo de devolução do estorno** — quanto tempo até o dinheiro voltar? (sugestão: 5 a 10 dias úteis, conforme a operadora do cartão.)

### Política de Privacidade (`/privacy`)
7. **Política de retenção por tipo de dado** — por quanto tempo guardar conta, logs, conteúdo, dados fiscais.
8. **DPO nomeado** — há um encarregado de dados nomeado além do e-mail de contato?

---

## O que um advogado humano deve revisar (obrigatório antes da 1ª venda)

Isto **não é aconselhamento jurídico definitivo**. LEXIS é o primeiro filtro — escreveu o que é sustentável na lei brasileira, mas quem assina o risco é você, com um advogado humano. Peça a um advogado para revisar, em especial:

- A **limitação de responsabilidade** (Termos, cláusula 8) — o teto de 12 meses precisa passar pelo crivo do CDC (cláusulas que limitam direito do consumidor podem ser afastadas).
- A **garantia de 30 dias** vs. arrependimento de 7 dias — a redação final da soma dos dois direitos.
- As cláusulas de **propriedade intelectual e anti-redistribuição** (Termos, cláusula 6) — se cobrem o seu modelo de licença.
- A **base legal LGPD** e o texto sobre **processamento por IA** (Privacidade, cláusula 3) — o alerta de não inserir dado sensível.
- Se a atividade exige **registro de DPO** formal e inscrição de canais junto à ANPD.

---

## Já está pronto (não depende de você)

- ✅ Páginas `/terms`, `/privacy`, `/refund` no ar, na pele do Quantum (obsidian + tokens, zero cor hardcoded).
- ✅ Links no rodapé do `/pricing` corrigidos (antes davam 404).
- ✅ **Checkbox de consentimento** no checkout: o usuário precisa aceitar os 3 documentos antes de assinar, e o aceite (data/hora) é registrado no metadata da sessão Stripe — prova de consentimento que a LGPD e o CDC pedem.

---
*Frente jurídica do checkout · ALSHAM QUANTUM · Universo Bonaparte · ALSHAM Global.*
