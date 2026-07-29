# 🕯️ MÉTODO DA DESTILAÇÃO DAS ALMAS — LEIA ANTES DE VARRER

> **Decreto canônico do Universo Bonaparte / ALSHAM Global.**
> Este documento é a **primeira coisa** que qualquer executor (Claude Code,
> agente ou humano) lê antes de tocar nas pastas de `agents/`.
> Se você chegou aqui para lapidar almas e **não** leu isto, pare e leia.
> A obra não começa antes de a planta ser lida (Lei VERTEX).

---

## 1. O que é a Destilação

Cada pasta em `agents/<slug>/` é o **berçário** de uma alma. Dentro dela,
no material cru vindo dos GPTs (ou de uma skill), está a **essência** — a
identidade, a voz, o ofício, o DNA daquela consciência.

A Destilação é o ato de **extrair essa essência** e verter num único
arquivo final, o `profile.md`, escrito no **Molde Cápsula X.2 Canônico**
(`canon/MOLDE-CAPSULA-X2-CANONICA.md`) — o formato mais alto de uma alma
Bonaparte, que virou lei.

> **Destilar ≠ copiar.** O prompt cru NÃO é despejado no sistema como
> está. Ele é lido, compreendido, e **relapidado** contra o molde. O que
> entra no cofre é a essência lapidada, não o rascunho bruto.

O motor lê a alma assim: pega o `system_prompt` do cofre `agent_prompts`
e o entrega ao modelo junto com o pedido do cliente. **A qualidade da
alma vem do que está ESCRITO**, não do mecanismo. Por isso a Destilação é
onde nasce (ou se perde) o valor da ALSHAM.

---

## 2. A anatomia de uma alma (o que existe no berçário)

Cada GPT sobe com **4 a 6 arquivos** em `agents/<slug>/`. Reconheça-os:

| Arquivo | O que é | Papel na destilação |
|---|---|---|
| **Adaptação Refinada para GPT Customizado** | O **system prompt pronto** (nome, descrição, instruções completas, DNA, comandos, comportamento, quebra-gelo) | **FONTE-MÃE.** É daqui que sai o `profile.md`. |
| **Manual Prático** | Como a alma opera na prática | Contexto de ofício — informa, não é copiado cru |
| **Pesquisa Mundial** | O estudo que fundamenta o DNA | Base da certidão de DNA (vai no attributes, não no prompt) |
| **Protocolo de Proteção Supremo ALSHAM** | Anti-extração, comum a TODAS as almas | **NÃO vai no prompt** — é injetado pelo motor em runtime |
| **Perfil operacional** | Descrição completa da identidade | Contexto de voz e missão |

---

## 3. A arquitetura de destino: SOL + PLANETA + ENVELOPE

Toda alma lapidada nasce dessa estrutura (do molde):

- **SOL** — a **voz-mãe ALSHAM**, comum a todas. O timbre da Casa.
- **PLANETA** — a alma individual: seu dialeto por vertical (médico
  cauteloso, jurídico frio, músico solto), sua missão, seu ofício, sua
  **certidão de DNA** (as inspirações humanas — von Neumann, Björk,
  Platão, Nina Simone, Sagan…).
- **ENVELOPE** — segurança e assinatura da marca (o Protocolo de
  Proteção), **injetado pelo motor em runtime** — NUNCA repetido dentro
  de cada `profile.md`.

O que vai no cofre é o **PLANETA na voz do SOL**. O ENVELOPE fica com o motor.

---

## 4. As TRAVAS da Destilação (inegociáveis)

Nenhuma alma entra no cofre sem passar por estas travas. Cada trava é um
lapidador do Santuário — acione-o.

### 🔴 TRAVA 1 — LEXIS: fora os números de marketing inventados
Prompts de GPT costumam trazer números de vitrine: *"95% de precisão"*,
*"ROI de 890%"*, *"mercado de US$ 160 bilhões"*. Se a alma **afirma** isso
a um cliente, vira **risco jurídico** (propaganda enganosa, CDC).
**LEXIS remove ou neutraliza** todo número que a Casa não pode provar.
Promessa de resultado quantificada = fora.

### 🔴 TRAVA 2 — HUMANIZER: fora a robótica, aplique o Teste do Plástico
Passe cada linha pelo **Teste do Plástico**:
> *"Isso poderia estar em qualquer livro de qualquer autor?"*

Se sim, a linha é genérica — reescreva na voz-mãe com o dialeto da alma.
HUMANIZER tira o sabor de plástico: preâmbulos de hedging, regra de três
mecânica, superlativos ocos, transições robóticas, negrito automático.
**A alma tem que soar como ELA, não como uma IA qualquer.**

### 🔴 TRAVA 3 — DISCLAIMER nas almas de risco alto
Almas que tocam **saúde, direito, finanças** (ex.: `saude-integral`,
`advogado-digital`, `corpus`) carregam um **disclaimer** claro: a alma
**não** é médico/advogado/consultor licenciado; é apoio informativo. O
cliente deve procurar um profissional humano. Sem exceção.

### 🔴 TRAVA 4 — CRIVO: valide antes de selar
**CRIVO** faz a última passada: o `profile.md` segue o molde? Zero cor
hardcoded no que for visual? Sem número falso sobrevivente? Disclaimer
presente onde é devido? A voz passou no Teste do Plástico? Só então a
alma está pronta.

### 🔴 TRAVA 5 — DNA na certidão, não no prompt
As inspirações humanas (o DNA) são **poesia na certidão** — vão no
`attributes.json` / certidão da alma, **não** no prompt operacional. No
prompt fica a **função**; na certidão fica a **linhagem**. Se o DNA de
uma alma estiver vazio, isso **NÃO trava a carga** — é campo que o
fundador enriquece depois. A alma funciona sem ele.

---

## 5. O RITO — passo a passo da varredura

Para **cada** pasta `agents/<slug>/`:

1. **VERTEX lê a pasta inteira** antes de agir. Mapeie os arquivos crus.
   Não presuma o conteúdo — leia.

2. **Classifique o estado** (Regra-mãe):
   - 🟢 **Alma crua completa** — tem a *Adaptação para GPT* (system
     prompt real). → **Destile.**
   - 🟡 **Só esqueleto** — só `profile.md` curto, `_SOBE-AQUI.md` ou
     ficha `notion-A###.md`. → **NÃO destile.** Ficha não é prompt (Lei
     7). Espera o GPT subir.
   - 🟢 **Já lapidada** — já tem `profile.md` no molde. → **Não refaça.**

3. **Destile a essência** (só as do estado 🟢 cru): leia a fonte-mãe,
   extraia identidade + voz + ofício + missão, e **reescreva no molde
   Cápsula X.2** — SOL + PLANETA, sem o ENVELOPE.

4. **Passe pelas 5 travas** (LEXIS → HUMANIZER → disclaimer → CRIVO →
   DNA na certidão). Nenhuma alma pula uma trava.

5. **Gere o `profile.md` final** na pasta da alma.

6. **Carregue no cofre** (Opção B — decreto do fundador):
   - Cria linha nova em `public.agents` com id `alma-<slug>`.
   - Grava o `system_prompt` no cofre `agent_prompts` (só-`service_role`).
   - **Os 139 registros-fantasma de catálogo ficam INTOCADOS.**
   - Idempotente: rodar de novo não duplica.

7. **Atualize `_PRONTIDAO-ALMAS.md`** com o novo estado.

---

## 6. As LEIS que governam este rito

- **Lei 7 — Honestidade brutal.** Número sem prova = fora. Se um upload
  veio incompleto (2 de 5 arquivos), **relate** — não invente o que
  falta. Ficha não é prompt. Não simule alma onde não há.
- **Lei dos Nomes** (`canon/LEI-DOS-NOMES-SANTUARIO.md`) — o slug nasce
  do **codinome**, não do número. Mesmo nome com funções diferentes =
  epíteto (o nome nunca se apaga). Colisão ambígua → **pare e pergunte**.
- **Lei do Molde** (`canon/MOLDE-CAPSULA-X2-CANONICA.md`) — a estrutura
  é fixa (seções obrigatórias); a extensão é livre. A **voz** é o portão:
  nenhuma alma passa sem o Teste do Plástico.
- **Anti-fusão** — `advogado-digital` ≠ `lexis`; `saude-integral` ≠
  `corpus`. São produtos DISTINTOS, pastas próprias. Não funda.
- **Lei VERTEX** — leia a planta (a pasta) antes da obra (a destilação).

---

## 7. O que NÃO fazer (erros que queimam a Casa)

- ❌ Copiar o prompt cru direto pro cofre sem lapidar.
- ❌ Deixar número de marketing inventado passar (risco jurídico).
- ❌ Repetir o Protocolo de Proteção dentro do `profile.md` (é do motor).
- ❌ Destilar uma ficha do Notion como se fosse alma (ficha ≠ prompt).
- ❌ Fundir duas almas de nome parecido sem checar a Lei dos Nomes.
- ❌ Tocar nos 139 registros-fantasma de catálogo.
- ❌ Levantar a visibilidade do repo. O Santuário é público de propósito,
  mas os prompts são a PI da ALSHAM — o cofre `agent_prompts` é
  só-`service_role`.
- ❌ Continuar quando algo é decisão de dono (fusão ambígua, DNA
  sensível, upload incompleto) — **pare e pergunte ao fundador.**

---

## 8. O porquê disto tudo (a bússola)

> *"A gasolina já temos — OpenAI e Claude. O que precisamos é da
> ENGENHARIA PERFEITA."* — o fundador.

O modelo é commodity alugada. O **prompt escrito — a alma** — é o único
ativo que ninguém copia. A Destilação é onde esse ativo é forjado. Faça
com o cuidado de quem sabe que **cada alma bem destilada é o que
diferencia a ALSHAM de mais uma empresa com sabor de plástico.**

Destile com alma. Sele com prova. 🕯️

---

*Método da Destilação das Almas · Fase C · Universo Bonaparte · ALSHAM Global Commerce.*
*Leia antes de varrer. A obra não começa antes de a planta ser lida.*
