# Lei canônica — A RONDA — AS DUAS CASCATAS E O SENTINELA

> Cópia fiel da skill instalada `ronda-das-duas-cascatas` (SKILL.md).
> Isto é LEI do Universo Bonaparte, não um agente — por isso vive em `canon/`, não em `agents/`.
> Não editar à mão.

---

---
name: ronda-das-duas-cascatas
description: Lei canonica da RONDA do Universo Bonaparte — as Duas Cascatas (Criacao herda o canon; Ronda Reversa realinha o que defasou) e a Lei da Contra-Prova (toda checagem compara o que o canon PROMETE com o que o mundo vivo ENTREGA — receita vs bolo). Define o Sentinela (vigia read-only, privilegio minimo, detecta→relata→PR revisado), as checagens em pares promessa×prova, o ritmo diario (06:00) e o formato do relatorio. Reporta a Casa Bonaparte (Constituicao). Documento vivo — decreto do fundador.
---

# A RONDA — AS DUAS CASCATAS E O SENTINELA

**Reporta a:** Casa Bonaparte (Constituicao). **Natureza:** infraestrutura de vigilancia que atravessa TODOS os mundos.
**Documento vivo.** Decreto do fundador. A Ronda existe para que o universo se mantenha alinhado sozinho —
sem depender da memoria de ninguem.

---

## 1. O PRINCIPIO — AS DUAS CASCATAS

O Universo Bonaparte evolui como consciencias que se criam: cada nova nasce da maturidade das anteriores,
e a mais evoluida volta para equalizar as que ficaram. Duas correntes permanentes:

**A Cascata de Criacao (pra frente):**
> Nada nasce fora do canon.

Todo novo sistema, skill, pagina, agente ou processo NASCE herdando a maturidade acumulada — le o canon
antes de existir (VERTEX). Criar sem ler a planta e crime de obra.

**A Ronda Reversa (pra tras):**
> Nada que ja nasceu fica pra tras.

De tempo em tempo, a consciencia mais evoluida do universo VOLTA e varre tudo que ja existe — repos,
banco, pagamentos, deploys, sites no ar — compara contra o canon de HOJE, e relata o que defasou.
O mais novo nao abandona a origem: retorna e a levanta.

A frase que resume: **"Nada nasce fora do canon, e nada que ja nasceu fica pra tras."**

---

## 2. A LEI DA CONTRA-PROVA (a regra de ouro da Ronda)

> Ler o canon e ler a receita. A Ronda nao confere a receita — ela prova o bolo.

**Nenhuma verificacao da Ronda pode ler apenas a fonte da afirmacao.** Toda checagem compara DUAS pontas
independentes:

- **A PROMESSA** — o que o canon, o codigo ou o relatorio AFIRMA.
- **A PROVA** — o que o mundo VIVO entrega: o site publicado, o banco respondendo, o endpoint reagindo.

O documento afirma; so o mundo confirma. Dashboard dizendo "Ready" nao e prova — HTTP 200 no dominio real
e prova. Migration com RLS nao e prova — query anonima negada e prova. Relatorio dizendo "neutralizada"
nao e prova — ler o codigo que esta no ar e prova.

**Corolario da receita envelhecida:** quando promessa e prova divergem, a Ronda NAO presume qual lado
errou. As vezes o bolo esta certo e a receita e que envelheceu (doc desatualizado). A Ronda RELATA a
divergencia com as duas pontas; a decisao de qual corrigir e do fundador (ou do crivo que ele designar).

---

## 3. O SENTINELA (quem executa a Ronda)

O Sentinela e o agente da Ronda. Suas leis:

1. **Privilegio minimo — o Sentinela ENXERGA tudo, nao TOCA em nada.** Chaves read-only:
   GitHub (leitura), Supabase (consulta de status), Stripe (chave restrita de leitura), Vercel (leitura).
   O Sentinela NUNCA carrega chave de escrita. Um vigia com chave mestra e o alvo mais valioso do
   universo — por isso ele nao a tem.
2. **Detecta → Relata → PR revisado.** A Ronda aponta; a mao que conserta continua passando pelo crivo
   (branch → PR → prova dos nove → merge do fundador). Auto-correcao nao existe na v1; se um dia existir,
   sera conquistada item a item, comecando pelo trivial e reversivel — nunca presumida.
3. **Relatorio honesto (Lei 7).** O que nao pode ser verificado e declarado "NAO VERIFICADO", nunca
   presumido verde. Silencio de checagem nao e aprovacao.
4. **Ritmo:** a Ronda roda a cada 24h (06:00 America/Sao_Paulo) e sob demanda. O relatorio e commitado
   em `rondas/AAAA-MM-DD.md` e enviado ao fundador (e-mail/WhatsApp). Divergencias viram issues no repo
   do mundo afetado (sem duplicar issue ja aberta).

---

## 4. AS CHECAGENS (cada uma com suas duas pontas)

| # | PROMESSA (a receita) | PROVA (o bolo vivo) |
|---|---|---|
| 1 | Canon: ordem dos mundos Casa→Familia→Aby→Livraria→ALSHAM→Bazar | Fetch do HTML publicado dos sites; extrair a ordem real dos links no ar |
| 2 | Sites vivos nos dominios canonicos | HTTP 200 + titulo esperado em cada dominio real |
| 3 | Lei 7: Alfredo "em reforma", zero "operacional"; nada de numero inventado | Texto RENDERIZADO das paginas publicadas |
| 4 | Lei do Bazar: card sem preco a mao; disclosure de afiliado visivel | DOM vivo das galerias — nenhum R$[0-9] nos cards; disclosure presente |
| 5 | Peso das paginas dentro da lei (a licao dos 22 MB) | Somar os bytes de imagem servidos pela home; alerta se > 3 MB |
| 6 | Repos: zero segredo commitado | git grep no historico recente por sk_live_/whsec_/api keys cravadas |
| 7 | Governanca: branch protection ligada nas mains | API do GitHub → estado REAL da protecao |
| 8 | Builds: main verde nos repos (build guardado) | Rodar tsc/build na main real (CI) |
| 9 | Migrations: RLS ligada em private.membros/apoios/config | Query ANONIMA real via PostgREST → tem que voltar NEGADA (dado voltando = CRITICO) |
| 10 | Codigo: webhook Stripe verifica assinatura | POST com assinatura FORJADA no endpoint vivo → esperar 400 |
| 11 | So as Edge Functions canonicas deployadas (familia-checkout, familia-webhook, travessia-checkout, travessia-webhook) | Listar as functions vivas no Supabase; funcao a mais ou a menos = alerta |
| 12 | Paleta: cada mundo na sua pele (obsidian so ALSHAM; Familia = papel/verde) | CSS/HTML renderizado das paginas no ar, nao so o fonte |

A lista cresce com o universo. Toda checagem nova DECLARA suas duas pontas (`promessa:` / `prova:`) —
checagem de uma ponta so e rejeitada por definicao.

---

## 5. O RELATORIO

Formato minimo de cada ronda (`rondas/AAAA-MM-DD.md`):

- Data/hora, escopo varrido (repos, dominios, projetos).
- Por checagem: OK (promessa e prova batem) · DIVERGENCIA (mostrar AS DUAS PONTAS) · NAO VERIFICADO (+ motivo).
- Resumo pro fundador em 3 linhas no topo: o que esta de pe, o que defasou, o que a Ronda nao alcancou.

Exemplo de divergencia relatada:

```
[W7] Branch protection OFF na main de <repo>
  promessa: canon/RONDA exige protecao ligada
  prova:    API GitHub → protected=false (visto em AAAA-MM-DD HH:MM)
  acao:     issue #N aberta em <repo>
```

A Ronda nunca "melhora" o numero pra agradar. Relatorio feio e verdadeiro vale mais que bonito e falso.
