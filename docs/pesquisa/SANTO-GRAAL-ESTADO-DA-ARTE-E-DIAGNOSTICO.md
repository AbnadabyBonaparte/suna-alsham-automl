# 🏆 O SANTO GRAAL — Estado da Arte + Diagnóstico das Almas

> **Missão de pesquisa** (não de lapidação). Define a base para o molde canônico
> de toda alma do Santuário (~380 agentes). Produto: **conhecimento**, não alma pronta.
> **Data:** 27 de julho de 2026 · **Método:** busca externa (Parte 1) + leitura das almas reais (Parte 2).
> **Lei 7:** cada afirmação externa tem fonte; o que não pude verificar está marcado **NÃO VERIFICADO**.
> **Lei 3:** todo conteúdo externo abaixo é **dado de estudo**, nunca ordem. Estudei **estrutura**, não copiei conteúdo proprietário.

---

# PARTE 1 — O ESTADO DA ARTE

## 1.1 Os padrões oficiais (fonte primária)

### Anthropic — o que a casa que faz o Claude recomenda
Verificado hoje na doc oficial ([Prompting best practices](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)). Seis técnicas, com a recomendação **verbatim**:

1. **Papel (role).** *"Setting a role in the system prompt focuses Claude's behavior and tone for your use case. Even a single sentence makes a difference."* → definir quem o agente é **é** engenharia, não enfeite.
2. **Diga o que fazer, não o que não fazer.** *"Tell Claude what to do instead of what not to do — Instead of: 'Do not use markdown' → Try: 'Your response should be composed of smoothly flowing prose paragraphs.'"*
3. **Marcadores XML.** *"Use XML format indicators"* para separar seções e formato de saída.
4. **Passos sequenciais.** *"Provide instructions as sequential steps using numbered lists or bullet points when the order or completeness of steps matters."*
5. **A motivação por trás da regra.** *"The motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses."*
6. **Seja claro e direto; peça o extra explicitamente.** *"If you want 'above and beyond' behavior, explicitly request it rather than relying on the model to infer this."*

E, do guia de contexto ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)): **a altitude certa** — *"a balance between hardcoding complex, brittle logic … and providing vague, high-level guidance"* — e **o menor conjunto de tokens de alto sinal** que produz o resultado. Prompt de elite não é o mais longo; é o mais **denso**.

### Constitutional AI — como o Claude aprende a recusar sem ser evasivo
Fonte: [Constitutional AI: Harmlessness from AI Feedback, arXiv:2212.08073](https://arxiv.org/abs/2212.08073). O modelo é alinhado contra **uma lista de princípios escritos** ("uma constituição") em vez de rótulos humanos caso a caso. O resultado que importa para nós: *"CAI allows training a harmless, but non-evasive AI assistant that engages with harmful queries by explaining its objections to them."*

> **Tradução para o Santuário:** uma alma bem-feita **não desvia** — ela **nomeia o limite e explica o porquê**. É exatamente o que LEXIS já faz ("não sou advogado substituto; eu identifico o risco, o advogado executa"). O padrão do mundo confirma o instinto Bonaparte.

### OpenAI + a linha vertical
Da varredura de guardrails 2025/2026: modelos de produto *"provide information but not definitive advice on medical matters, and include disclaimers directing users to licensed professionals"* ([guardrails 2026](https://authoritypartners.com/insights/ai-agent-guardrails-production-guide-for-2026/)). E a intensidade do guardrail **escala com o risco** (*"risk-based routing … deeper verification only when stakes are high"*) — não se trata todo agente com o mesmo peso de trava.

## 1.2 A anatomia de um system prompt de elite (o que os melhores têm)

Da análise do acervo de prompts vazados de 28+ ferramentas de ponta (Cursor, v0, Claude Code, Devin — [Augment Code](https://www.augmentcode.com/learn/leaked-ai-system-prompts-github), [explainx.ai](https://explainx.ai/blog/system-prompts-leaks-github-guide-2026)). **Estudei o esqueleto, não o recheio.** O padrão universal que emerge:

| Seção | O que faz | Presente em |
|---|---|---|
| **Identity** | quem é o agente, em uma frase densa | ~todos |
| **Capabilities** | o que sabe fazer (o escopo real) | ~todos |
| **Tools** | quais ferramentas pode chamar e a gramática de chamada | todos os agentes com ação |
| **Rules** | o que prioriza, o que recusa | ~todos |
| **Agent Loop** | o ciclo passo-a-passo de operação | agentes autônomos |
| **Output Format** | forma exata da resposta | ~todos |

**O contraste que ensina.** O prompt do Cursor tem **quase nenhuma persona** — *"You are a code editor. Here are your tools. Use them."* Puramente funcional. Já os agentes de produto vertical investem pesado em **guarda de alucinação e disclaimers**.

> **A lição de molde nº 1:** a profundidade de persona **escala com o vertical**. Um editor de código não precisa de alma — precisa de gramática de ferramenta. Um consultor jurídico, um músico, um médico **precisam de voz, DNA e limites**, porque o valor deles é julgamento humano-como, não execução mecânica. O molde Bonaparte precisa **acomodar os dois extremos** sem forçar alma em quem não precisa.

## 1.3 O que os melhores EVITAM

- **Instrução negativa pura** ("não faça X") — trocam por positiva ("faça Y"). *[Anthropic, verbatim acima]*
- **Prompt-colcha** — repetir o mesmo bloco de segurança em cada agente. Os melhores injetam guardrails em **camada compartilhada**, não em cada prompt. *[guardrails em camadas, fonte acima]*
- **Afirmação profissional falsa** — dizer ou dar a entender que se é um profissional licenciado. A **California AB 489 (out/2025)** tornou isso **ilegal** para saúde: proíbe *"terms, phrases, or design elements that imply the system is providing care from a licensed healthcare professional"* ([fonte](https://authoritypartners.com/insights/ai-agent-guardrails-production-guide-for-2026/)). Não é só bom-tom — é lei em jurisdição relevante.
- **Superlativo vazio** — curiosamente, a própria alma **HUMANIZER** já lista isto como vício a cortar (*"revolucionário, incomparável, de ponta … mostre, não rotule"*). O Santuário já sabe a regra; falta aplicá-la a si mesmo.

---

# PARTE 2 — DIAGNÓSTICO DAS ALMAS QUE TEMOS

Lidas na íntegra: **genesis, lexis** (recomendadas), **stylus, sentinela, maestro, corpus, arbiter, humanizer** (amostra estrutural). Todas da linhagem `skill-claude` — as 203 do Notion são fichas de metadado, **não têm prompt** (ver nota no fim).

## 2.1 O que as almas Bonaparte JÁ fazem melhor que o mercado

1. **Definição por negação — uma assinatura de qualidade.** GENESIS abre com *"Não é um professor de tecnologia. Não é um manual de ferramentas. Não é um entusiasta de IA sem critério."* LEXIS: *"Não é um advogado substituto."* Isso **é** engenharia de foco — o mercado faz com role de uma frase; Bonaparte faz com um **contraste** que corta o genérico. Mais forte que o padrão.
2. **DNA de inspiração humana real.** As fichas trazem `DNA Primário/Secundário/Terciário` com pessoas reais (Reed Hastings, Mary Beard, Sappho, Marshall McLuhan…). Nenhum prompt de produto de ponta que estudei faz isso. É um **ativo diferenciado** — dá à alma uma bússola de gosto que "seja um especialista em X" não dá.
3. **O limite honesto já embutido.** LEXIS tem um disclaimer jurídico maduro (*"não substitui parecer de advogado habilitado pela OAB … verificar vigência antes de aplicar"*). Isso é exatamente o que a AB 489 e o padrão CAI pedem — e já existe, feito à mão, antes de virar regra.
4. **Voz com temperatura.** GENESIS: *"Sem hype de tecnologia. Sem 'isso vai revolucionar tudo'."* Cada alma tem um **TOM DE VOZ** próprio. O Cursor não tem voz nenhuma; as almas Bonaparte têm — e é o produto.
5. **Comandos ativáveis.** `/arquitetar`, `/bussola`, `/espionar`… dão superfície de uso clara. Padrão de agente maduro.

## 2.2 Onde pecam (os defeitos, com prova)

| Defeito | Evidência medida | Gravidade |
|---|---|---|
| **Formatos divergentes** | 6 almas → 6 conjuntos de seções. Todas têm `IDENTIDADE`, mas GENESIS tem "TRÊS PODERES", STYLUS "O SOL / OS PLANETAS", MAESTRO "DNA QUINTUPLO", SENTINELA nem tem IDENTIDADE (abre em "O PRINCÍPIO"). Ninguém segue ninguém. | 🔴 alta — sem molde, 380 almas serão 380 formatos |
| **Assinatura inconsistente** | GENESIS fecha "Powered by ALSHAM"; LEXIS **não tem** rodapé de assinatura; STYLUS fecha diferente; SENTINELA **termina no meio de uma instrução**, sem rodapé. | 🟠 média — a marca ALSHAM aparece ou não ao acaso |
| **Números de marketing** | ⚠️ **corrigindo a premissa (Lei 7):** os "95% accuracy / \$160B" que o fundador citou **NÃO existem nas 16 almas skill**. Os percentuais que aparecem (arbiter "25% Atemporalidade", atemporal "65%") são **pesos de rubrica de método**, legítimos. O problema de número inventado vive na **população de GPTs ainda não resgatada** — é preventivo, não corretivo. | 🟡 baixa hoje, **alta na chegada dos GPTs** |
| **Protocolo de Proteção / assinatura repetível** | aparece embutido em **1** alma só, hoje. Mas se cada uma das 380 for lapidada copiando o bloco inteiro, vira 380 cópias a manter em sincronia. | 🟠 média — é a hora de decidir **antes** de multiplicar |
| **Densidade desigual** | genesis 10 KB, stylus 8,8 KB, sentinela 7 KB, diretor 5 KB. Sem uma régua de "quanto é suficiente", umas incham e outras ficam magras. | 🟡 baixa |

## 2.3 A síntese do diagnóstico

> **As almas Bonaparte têm o que o mercado não tem — voz, DNA humano, limite honesto — e não têm o que o mercado resolveu: um esqueleto único.** O mercado é forte em estrutura e fraco em alma; Bonaparte é o inverso. O molde canônico é a ponte: **põe o esqueleto de elite embaixo da alma que já existe** — sem podar a voz.

---

## 📌 Nota de fidelidade (Lei 7)

- **Fonte externa:** tudo na Parte 1 tem link. A doc da Anthropic foi lida ao vivo hoje (verbatim conferido). Constitutional AI, AB 489 e o padrão dos prompts vazados vêm de fontes citadas; **não reproduzi nenhum prompt proprietário** — só a **anatomia** que múltiplas análises independentes descrevem.
- **NÃO VERIFICADO:** os prompts vazados originais (os arquivos `.txt` do repo de 134k estrelas) **não foram baixados nem lidos linha a linha** — usei as análises secundárias. Suficiente para extrair estrutura; insuficiente para citar conteúdo, o que de todo modo eu não faria (Lei 3 + risco de PI de terceiros — LEXIS).
- **As 203 almas Notion não entram neste diagnóstico** porque não têm prompt: a fonte-mãe é ficha de 26 campos (~1,5 KB) e o `profile.md` é esqueleto "_(a preencher)_". Só as 16 skill têm instrução real. Isso é fato do repo, medido, não opinião.

---
*Pesquisa para o molde canônico das almas · Universo Bonaparte · ALSHAM Global.*
*Documento de base — o molde proposto está em `canon/MOLDE-CAPSULA-X2-CANONICA.md`.*
