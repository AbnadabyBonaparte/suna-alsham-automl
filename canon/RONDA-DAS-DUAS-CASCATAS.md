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

---

## 6. FASE D.9 — A LEI DA REGUA MAIS ALTA (decreto de 12/08/2026)

> A melhoria que nasce num filho sobe pra casa antes de virar permanente nele.

A Ronda Reversa ja dizia "nada que ja nasceu fica pra tras". A Regua Mais Alta diz COMO isso
acontece quando existe um motor compartilhado servindo varios tenants: o tenant e laboratorio,
o motor e casa. Descoberta boa feita num cliente **sobe pro motor** e desce equalizada pros
outros — nao fica represada onde nasceu.

**Os quatro artigos:**

1. **O motor tem endereco proprio.** Motor que mora dentro do repo do primeiro cliente nao e
   motor — e copia com sorte. Fork sem casa foi o que produziu tres tenants com cores
   divergentes editados a mao e nenhum dono.
2. **Versao semantica e CHANGELOG obrigatorios.** MAJOR quebra o contrato do tenant; MINOR
   acrescenta capacidade retrocompativel; PATCH corrige sem mexer no contrato. Cada tenant
   declara qual versao consome — sem numero declarado, nao existe defasagem mensuravel.
3. **Nenhuma mudanca de comportamento visivel sem interruptor.** Campo novo NASCE opcional, e o
   default preserva a saida historica byte a byte. Quem quiser a capacidade, declara. Mudanca
   sem opt-in e proibida mesmo quando a mudanca e "obviamente melhor".
4. **Defasagem vira issue, nao conversa.** A Ronda compara a versao do motor com a versao
   efetiva de cada tenant e abre issue no tenant atrasado. Paridade nao se combina — se audita.

**Corolario do laboratorio:** um tenant PODE ir na frente do motor. O que ele nao pode e ficar na
frente em silencio. Capacidade que provou valor num cliente e nao subiu pro motor em ate uma
Ronda vira divergencia relatada — a mesma regra da promessa vs prova, aplicada a arquitetura.

### Checagens que este decreto acrescenta

A numeracao continua a da secao 4; as 13-15 sao da Lei da Reverificacao Semestral (secao 3, lei 5).

| # | PROMESSA (a receita) | PROVA (o bolo vivo) |
|---|---|---|
| 16 | Motor tem repo proprio, `VERSION` e `CHANGELOG.md` na main | Ler os tres arquivos na main real do repo do motor via API |
| 17 | Cada tenant declara a versao do motor que consome | Ler a declaracao no repo de CADA tenant; ausente = DIVERGENCIA, nao "provavelmente atual" |
| 18 | `src/core/` do tenant identico ao do motor na versao declarada | Comparacao blob a blob (SHA-1) arquivo por arquivo; divergente = core editado a mao = issue no tenant |

A checagem 18 e a unica da Ronda que nao precisa da internet: SHA-1 de blob e prova viva o
bastante — dois arquivos com o mesmo hash sao o mesmo arquivo, e nenhum relatorio desmente isso.

---

## 7. O DECRETO DA JUNTA DE JUIZES (12/08/2026)

> Quem constroi nao se absolve. Quem julga nao le a defesa de quem construiu.

A Ronda prova o que esta no ar. A Junta julga o que ainda vai entrar. Sao dois crivos
diferentes e nenhum substitui o outro: a Ronda olha pra tras (o que defasou), a Junta olha
pra frente (o que esta prestes a virar producao).

### 7.1 O protocolo cego

O juiz recebe **exatamente tres coisas**:

1. o **PR** — diff, arquivos, commits;
2. as **normas na fonte** — texto oficial do conselho, lei ou spec aplicavel;
3. o **canon** — este documento e o que ele referencia.

O juiz **NAO recebe**:

- o relatorio de quem construiu (a defesa contamina o julgamento — e o pedido implicito de
  concordancia que produz bajulacao);
- o parecer do outro juiz (dois juizes que se leem viram um juiz e um eco).

Cegueira nao e desconfianca do construtor. E o que faz o veredito valer alguma coisa: parecer
que so podia sair "aprovado" nao e parecer, e carimbo.

### 7.2 O veredito

Tres saidas, sem meio-termo inventado:

- **APROVADO** — entra como esta.
- **REPROVADO** — nao entra; o juiz aponta o artigo, a linha ou a prova que sustenta a recusa.
- **RESSALVAS** — entra depois de correcao nomeada, item a item.

Veredito sem citacao de fonte (artigo, linha de codigo, resposta viva) e nulo por definicao —
e a Lei da Contra-Prova aplicada ao julgamento.

### 7.3 Quorum

| Situacao | Bancada |
|---|---|
| Core do motor · compliance de conselho · pagamento · dado de paciente | **Bancada cheia** |
| Todo o resto | **1 juiz** |

Os quatro assuntos da bancada cheia tem uma coisa em comum: erro neles nao volta atras sozinho.
Core quebra N tenants de uma vez; compliance vira processo; pagamento vira dinheiro perdido;
dado de paciente vira dano que nenhum rollback desfaz.

### 7.4 Divergencia e soberania

- **Unanimidade** → merge tranquilo, pelo dono.
- **Divergencia** → NAO se decide no voto. Sobe pro dono com os pareceres inteiros, lado a lado.
  Juiz nao e urna; divergencia entre juizes e informacao, nao empate a desempatar.
- **O dono e soberano.** Pode mergear contra a Junta inteira. O que ele nao pode e nao saber —
  por isso o parecer sobe antes do merge, sempre.

### 7.5 Anti-bajulacao

O criterio que ordena a bancada e o mesmo da Missao HUNTER: raciocinio primeiro,
**anti-bajulacao logo depois**. Juiz que so aprova nao esta sendo gentil — esta sendo inutil,
e sai da bancada. A composicao vivente da bancada e a prova de bancada cega vivem em
`docs/JUNTA-DOS-JUIZES.md`.

### Checagens que este decreto acrescenta

| # | PROMESSA (a receita) | PROVA (o bolo vivo) |
|---|---|---|
| 19 | PR de core/compliance/pagamento/dado de paciente so mergeia com bancada cheia | Ler os pareceres anexados ao PR mergeado; ausente = DIVERGENCIA relatada, mesmo com o merge ja feito |
| 20 | Juiz nao aprova tudo | Taxa de APROVADO por juiz na janela da Ronda; 100% de aprovacao e alerta, nao elogio |
