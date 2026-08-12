# ATLAS DO UNIVERSO ALSHAM

**Missão ATLAS · modo SENTINELA (read-only)** — cartografia do que a infraestrutura **entrega**, não do que os docs prometem.
**Data da varredura:** 12/08/2026 · **Executor:** Claude Code (Ronda Reversa)
**Nada foi corrigido.** Este documento detecta e relata. Toda correção é PR próprio, revisado.

---

## Como ler este documento

Lei da Contra-Prova: cada afirmação carrega a **prova viva** que a sustenta. Onde não houve
prova, está escrito `NÃO VERIFICADO` — silêncio de checagem não é aprovação (Lei 7).

**Método de ligação repo ↔ projeto Vercel.** A API da Vercel usada aqui (`get_project`) **não
devolve o repositório de origem**. A ligação foi estabelecida por correlação de carimbo de tempo:
`pushed_at` do repo no GitHub × `latestDeployment.createdAt` na Vercel. Onde os dois batem no
mesmo minuto, a ligação está marcada **INFERIDO (forte)**. Não é o mesmo que ler o campo `link`
do projeto — quem quiser certeza absoluta precisa abrir o painel.

---

## PARTE 1 — INVENTÁRIO

### 1.1 As camadas

```
┌──────────────────────────────────────────────────────────────────────────┐
│  TESE — a intenção                                                       │
│  ALSHAM-ASCENSION-        DOC-00 Constituição v4.1 … DOC-13              │
│  → deploy: alsham-ascension · select.alshamglobal.com.br                 │
├──────────────────────────────────────────────────────────────────────────┤
│  LEI — o que todo produto deve obedecer                                  │
│  alsham-events-os/canon/ALSHAM_PLATFORM_FRAMEWORK_CHARTER.md             │
│  "Carta Magna", v1.0.0, adotada Jul/2026                                 │
│  Hierarquia: Empresa → Framework → Core → Engines → Domains → OS →       │
│              Tenant → Usuário                                            │
│  ⚠️  A LEI MORA DENTRO DE UM PRODUTO (o Events OS), não em repo próprio   │
├──────────────────────────────────────────────────────────────────────────┤
│  FÁBRICAS (os "OS")                                                      │
│                                                                          │
│   Events OS      alsham-events-os        events.os.alshamglobal.com.br   │
│   Business OS    alsham-business-os      empresas.alshamglobal.com.br    │
│   CRM OS (360°)  ALSHAM-360-PRIMA        app./prima.alshamglobal.com.br  │
│   ALSHAM OS      alsham-os               diamond.alshamglobal.com.br     │
│   Quantum        suna-alsham-automl      quantum.alshamglobal.com.br     │
│                                                                          │
│   Conversion OS  ❌ SEM REPO PRÓPRIO — mora dentro do tenant Fernanda     │
├──────────────────────────────────────────────────────────────────────────┤
│  TENANTS do Conversion OS                                                │
│   Fernanda (medicina)  → repo próprio + domínio + Stripe    ✅ no ar      │
│   Juliano  (advocacia) → repo próprio + domínio             ⚠️  ver 1.3   │
│   Bela     (odonto)    → ❌ sem repo · vive numa branch da Fernanda       │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.2 GitHub — 41 repositórios

**Prova:** `list_repos` da conta `AbnadabyBonaparte`, 12/08/2026. 39 clonados nesta sessão;
`alsham-business-os` e `STAGESET-` foram clonados à parte (não estavam anexados).

#### Camada TESE / LEI / CANON

| Repo | Papel | 1º commit | Último | Commits |
|---|---|---|---|---|
| `ALSHAM-ASCENSION-` | Tese documental e de marca (DOC-00 a DOC-13, Constituição v4.1) | 28/06/2026 | 22/07/2026 | 23 |
| `alsham-events-os` | **Carta Magna do Platform Framework** + produto Events OS | 05/07/2026 | 22/07/2026 | 23 |
| `casa-bonaparte-saas` | Constituição do Universo Bonaparte (`canon/`) — a Casa | 16/07/2026 | 26/07/2026 | 80 |
| `suna-alsham-automl` | ALSHAM Quantum + `canon/RONDA-DAS-DUAS-CASCATAS.md` + 219 almas em `agents/` | 28/07/2026 | 29/07/2026 | 53 |
| `bonaparte-brand` | Identidade Bonaparte (fonte de verdade) | 05/07/2026 | 05/07/2026 | 4 |

#### Camada FÁBRICA (os "OS")

| Repo | Papel | 1º commit | Último | Commits |
|---|---|---|---|---|
| `alsham-business-os` | **Business OS** — Core + módulos Lego, monorepo pnpm/turbo, 5 módulos | 27/07/2026 | 05/08/2026 | 328 |
| `ALSHAM-360-PRIMA` | CRM enterprise, 150+ módulos, 6 temas | 13/12/2025 | 22/07/2026 | 135 |
| `alsham-os` | SO corporativo AI-native | 28/11/2025 | 26/07/2026 | 23 |
| `alsham-events-os` | SaaS white-label de eventos | 05/07/2026 | 22/07/2026 | 23 |
| `alsham-360-ops` | Operações do 360° (privado, parado desde 08/2025) | 15/08/2025 | 28/08/2025 | 50 |

#### Camada TENANT (Conversion OS)

| Repo | Papel | 1º commit | Último | Commits |
|---|---|---|---|---|
| `dra-fernanda-conversion-os` | **Tenant 1 + o motor Conversion OS inteiro** | 02/07/2026 | 04/08/2026 | 73 |
| `Dr_Juliano-Sguizardisguizardi` | Tenant 2 (fork manual) | 12/07/2026 | 12/07/2026 | 7 |
| Dra. Bela | Tenant 3 — **não tem repo** (ver §6) | — | — | — |

#### Produtos ALSHAM (vertical / satélite)

`peritus` (perícia médica municipal) · `garimpo-ia` (leilões) · `cognitive-mirror-ai` ·
`SUPREMA-` (beleza) · `alsham-forensic-ai` · `Mentora` (educação) · `CamperFit-Pro` ·
`gse-import` · `kodara` · `BarbeiroSupreme` · `brocraft` · `questionario-consultoria-obra` ·
`alshamglobalcommerce` (landing institucional) · `cerebro-pesado` · `alsham-gpt-force` ·
`RevenueX.0` · `AGENTEX.0` · `ARC-X` · `entrega-alsham-produto` · `suna` (fork upstream)

#### Universo Bonaparte (família / arte — orbitam a Casa, não a ALSHAM)

`The-Bonaparte-Family` · `Aby-Bonaparte` · `bonaparte-kdp-lp` · `canta-siriema` ·
`aventuras-chacara-jogo` · `bazar` · `kraken-bonaparte` · `os-bonaparts` ·
`Caminhos-Sonoros-do-Cerrado-...` · `STAGESET-` (só documentos, sem código)

### 1.3 LINHAGEM — quem nasceu de quem (provado por SHA-1)

**Juliano forkado da Fernanda.** O repo do Dr. Juliano nasce em `a3db086` (12/07/2026), commit
único de instanciação. Comparando os *blobs* desse commit com o estado da Fernanda em `09cd1f4`
(12/07/2026, último commit antes do fork):

```
70 de 73 blobs IDÊNTICOS por SHA-1 em src/core, src/future, src/lib e src/components/ui

src/core/engines/HeroEngine.tsx      F:299c87ac652d  J:299c87ac652d  IDÊNTICO
src/core/engines/CTAEngine.tsx       F:6ec4603dc080  J:6ec4603dc080  IDÊNTICO
src/core/types/client.ts             F:d568e4f7d352  J:d568e4f7d352  IDÊNTICO
src/core/leads/lead-pipeline.ts      F:88cd1be635fd  J:88cd1be635fd  IDÊNTICO
src/lib/get-client.ts                F:0702b7b6d8a2  J:0702b7b6d8a2  IDÊNTICO
```

Hash igual é cópia byte a byte. Não é semelhança — é procedência.

**Os 3 blobs que divergem** são exatamente os arquivos de core que o fork do Juliano editou:
`AuthorityProfileEngine.tsx` (rótulos PT-BR), `LeadCaptureEngine.tsx` (removeu "Idade") e
`types/conversion.ts` (removeu `note?`). Ver emaranhado **E3**.

**Bela forkada da Fernanda** — mesma técnica, mas o fork ainda vive dentro do repo de origem
(branch `claude/dra-bela-conversion-os-0pgdzc`, pasta `dra-bela-conversion-os/`), com
`src/core` byte-idêntico verificado por `diff -r`. Ver **E2**.

### 1.4 Vercel — 26 projetos

**Prova:** `list_teams` + `list_projects` + `get_project`, time `Abnadaby's projects`
(`team_GaoyoGePPKNFDUMfZPM0YAVr`), 12/08/2026.

| Projeto | Repo (INFERIDO) | Domínio canônico | Último deploy | Alvo |
|---|---|---|---|---|
| `dra-fernanda-conversion-os` | `dra-fernanda-conversion-os` | **drafernandasguizardi.alshamglobal.com.br** | 11/08 21:11 | ✅ production |
| `dr-juliano-sguizardisguizardi` | `Dr_Juliano-Sguizardisguizardi` | **drjulianosguizardi.alshamglobal.com.br** | 12/07 19:03 | ⚠️ **preview** |
| `alsham-business-os` | `alsham-business-os` | **empresas.alshamglobal.com.br** | 12/08 11:24 | ⚠️ **preview** |
| `alsham-events-os-admin` | `alsham-events-os` | events.os.alshamglobal.com.br | 11/08 11:52 | ✅ production |
| `alsham-ascension` | `ALSHAM-ASCENSION-` | select.alshamglobal.com.br | 22/07 14:18 | ✅ production |
| `alsham-360-prima` | `ALSHAM-360-PRIMA` | app. / prima.alshamglobal.com.br | 22/07 13:14 | ✅ production |
| `alsham-os` | `alsham-os` | diamond.alshamglobal.com.br | 26/07 09:38 | ✅ production |
| `alsham-quantum` | `suna-alsham-automl` | quantum.alshamglobal.com.br | 12/08 10:36 | ⚠️ **preview** |
| `alshamglobalcommerce` | `alshamglobalcommerce` | **alshamglobal.com.br** (raiz) | 27/07 17:01 | ✅ production |
| `peritus` | `peritus` | peritus.alshamglobal.com.br | 04/08 03:14 | ✅ production |
| `casa-bonaparte-saas` | `casa-bonaparte-saas` | casabonaparte.com.br + bazar. + matusalem. | 26/07 19:37 | ✅ production |
| `api` | — | **nenhum** | **nunca** | ❌ **sem deploy** |

**Não detalhados nesta passada** (nome, ID e data de criação levantados; domínios e último
deploy **NÃO VERIFICADOS**): `kraken-v2`, `kraken-bonaparte`, `aby-bonaparte`,
`bonaparte-kdp-lp`, `questionario-consultoria-obra`, `canta-siriema`, `brocraft`,
`alsham-suprema-beleza`, `garimpo-ia`, `alsham-forensic-ai`, `cognitive-mirror-ai`,
`cerebro-pesado`, `the-bonaparte-family`, `bazar`. São 14 projetos — todos satélites, nenhum
na cadeia tese→lei→fábrica→tenant. Fica declarado como lacuna desta varredura.

### 1.5 Supabase — 13 projetos, org `ALSHAM GLOBAL`

**Prova:** `list_organizations`, `list_projects`, `list_tables`, `execute_sql`, 12/08/2026.
Org `ixgepvorquimksafpwoe` · plano **pro**.

| Projeto | Região | Status | Uso comprovado |
|---|---|---|---|
| `ALSHAM-DEV-OS` | sa-east-1 | ACTIVE | **`fernanda_leads`** + `agents`, `messages`, `users`, `vantage_noir_black_list` |
| `dra-fernanda` | sa-east-1 | ACTIVE | **só storage** — buckets `midias-site` (público) e `midias-brutas` (privado). Zero tabelas em `public` |
| `business-os` | sa-east-1 | ACTIVE | schema `core` completo: `tenants`, `memberships`, `module_registry` (100), `event_outbox` (385), `usage_ledger` (389), `audit_log` (386) |
| `alsham-events-os` | sa-east-1 | ACTIVE | Events OS |
| `casa-bonaparte` | sa-east-1 | ACTIVE | Casa Bonaparte |
| `peritus` | ca-central-1 | ACTIVE | Peritus |
| `kraken-v2` | sa-east-1 | ACTIVE | Kraken |
| `cognitive-mirror-ai` | sa-east-1 | ACTIVE | Cognitive Mirror |
| `alsham-suprema-beleza` | us-west-2 | ACTIVE | Suprema |
| `alsham-core` | sa-east-1 | ACTIVE | núcleo antigo (08/2025) |
| `ALSHAM_MPC_CORE` | us-east-2 | ACTIVE | núcleo antigo (10/2025) |
| `suna-core` | sa-east-1 | ACTIVE | Suna (07/2025) |
| `brocraft` | us-east-2 | **INACTIVE** | pausado |

**Fatura em atraso da org: `NÃO VERIFICADO`.** O MCP do Supabase disponível nesta sessão não
expõe faturamento, invoices nem estado de cobrança — `get_organization` devolve apenas
`plan: "pro"`. O único sinal observável adjacente é o projeto `brocraft` em `INACTIVE`, que
pode ser pausa por inatividade **ou** por cobrança; a ferramenta não distingue. Para conferir,
é preciso abrir o painel de billing da org.

### 1.6 A tabela do cruzamento

| Tenant | Repo | Branch | Deploy Vercel | Domínio | Banco | Storage | Pagamento |
|---|---|---|---|---|---|---|---|
| **Fernanda** | `dra-fernanda-conversion-os` | `main` | ✅ production 11/08 | drafernandasguizardi.alshamglobal.com.br | `fernanda_leads` **em ALSHAM-DEV-OS** | `dra-fernanda` (midias-site) | Stripe via `NEXT_PUBLIC_STRIPE_CHECKOUT_URL` |
| **Juliano** | `Dr_Juliano-Sguizardisguizardi` | `main` | ⚠️ preview 12/07 | drjulianosguizardi.alshamglobal.com.br | tabela via `NEXT_PUBLIC_LEADS_TABLE` (não criada) | — | ⛔ desligado por OAB |
| **Bela** | ❌ **nenhum** | `claude/dra-bela-conversion-os-0pgdzc` **no repo da Fernanda** | ❌ nenhum | ❌ nenhum | ❌ nenhum | ❌ nenhum | Stripe previsto, sem link |

> Segredos: nenhuma chave é citada neste documento. As referências de pagamento aparecem só
> como **nome de variável de ambiente**, conforme a lei do Sentinela.

---

## PARTE 2 — O MAPA EXPLICADO

## 5. As camadas, e onde cada coisa mora de verdade

**TESE (`ALSHAM-ASCENSION-`)** — por que a ALSHAM existe, como ela se apresenta. 23 commits,
14 documentos numerados, uma Constituição v4.1. Está no ar em `select.alshamglobal.com.br`.

**LEI (`alsham-events-os/canon/ALSHAM_PLATFORM_FRAMEWORK_CHARTER.md`)** — a Carta Magna,
adotada em julho de 2026, que define a hierarquia obrigatória:

> Empresa → Framework → Core → Engines → Domains → OS → Tenant → Usuário

E a missão, na letra dela: *"Construir e governar infraestrutura digital recorrente — não
sites, não entregáveis descartáveis."*

⚠️ **A lei não tem casa própria.** Ela mora dentro de `alsham-events-os`, que é **um dos
produtos que a lei governa**. Quem quiser ler a constituição da plataforma precisa entrar no
repositório de um produto específico de eventos. Ver **E1**.

**FÁBRICAS** — cinco "OS" com repo, deploy e domínio: Events, Business, CRM 360°, ALSHAM OS,
Quantum. Mais um sexto que a lei não reconhece: o **Conversion OS**.

**TENANTS** — três instâncias do Conversion OS: Fernanda, Juliano, Bela.

---

## 6. ONDE ESTÁ O SITE DA DRA. BELA?

Resposta curta: **em lugar nenhum que a internet alcance.** Ele existe como código completo,
que compila, dentro do repositório de outra pessoa.

| | |
|---|---|
| **Repositório** | ❌ não existe `dra-bela-conversion-os` — confirmado em `list_repos` (12/08/2026) |
| **Onde o código está** | `AbnadabyBonaparte/dra-fernanda-conversion-os`, branch `claude/dra-bela-conversion-os-0pgdzc`, pasta `dra-bela-conversion-os/` |
| **PR** | [#25](https://github.com/AbnadabyBonaparte/dra-fernanda-conversion-os/pull/25) — aberto, **não mergeado** |
| **Deploy** | ❌ nenhum projeto Vercel |
| **Domínio** | ❌ nenhum |
| **Banco** | ❌ nenhum. `dra_bela_leads` só existe como placeholder no `.env.example` |
| **Storage** | ❌ nenhum |
| **Pagamento** | Stripe previsto (`NEXT_PUBLIC_STRIPE_CHECKOUT_URL`), sem link criado |

**Por que ele não tem repo próprio.** A criação foi tentada e **bloqueada por permissão**: o
GitHub App desta sessão não tem escopo para criar repositórios —
`POST /user/repos → 403 Resource not accessible by integration`. Criar o repo é ação do dono.

**O que falta para a Bela virar mundo próprio, em ordem:**

1. Criar o repositório vazio `dra-bela-conversion-os` (30 segundos, painel do GitHub).
2. Empurrar a pasta como `main` — comandos prontos em `docs/SETUP-NOVO-REPO.md` do próprio fork.
3. Fechar o PR #25 sem mergear.
4. Criar o projeto na Vercel apontando para o repo novo.
5. Apontar o domínio (`[PENDENTE-CLIENTE]`).
6. Criar a tabela `dra_bela_leads` — **em projeto Supabase próprio**, não no ALSHAM-DEV-OS
   (é a chance de não repetir o **E4**).
7. Criar o Payment Link do Stripe da consulta online.
8. Resolver os `[PENDENTE-CLIENTE]` — sem nome e CRO reais o site descumpre o Art. 43 do
   Código de Ética Odontológica e não pode subir.

---

## 7. POR QUE TUDO PARECE JUNTO?

Porque **está** junto — e por dois motivos diferentes, que não podem ser tratados do mesmo jeito.

### A história, provada por git

`dra-fernanda-conversion-os` nasce em **02/07/2026**. E nasce já como produto de compliance: o
primeiro commit do repositório chama-se `fix(compliance): LEXIS X.0 — blindagem CFM/LGPD/CDC
pré-apresentação`. Não foi um site que depois virou motor. Foi um cliente urgente, com um prazo,
e o motor **nasceu dentro dele porque era ali que o trabalho estava acontecendo**.

Dez dias depois, em **12/07/2026**, o Dr. Juliano precisa de um site. E aí acontece a coisa que
prova que o motor era motor: 70 dos 73 blobs de core foram copiados **byte a byte** para o novo
repositório. Não se reescreveu nada. O motor funcionou.

Em **04/08/2026** a Dra. Bela repete o movimento — e desta vez com `src/core` byte-idêntico
verificado por `diff -r`, sem nenhuma edição.

Ou seja: em 33 dias, o mesmo núcleo serviu medicina, advocacia e odontologia, com três conjuntos
de regras profissionais completamente diferentes. **Isso é a tese da Carta Magna funcionando na
prática** — um Core, N Tenants — mas funcionando *antes* de a Carta Magna existir e sem que ela
tenha ficado sabendo.

### Correlação DESENHADA (isto é a arquitetura, não é problema)

- Um motor, três tenants, cada tenant só configuração. **É exatamente o que a lei manda.**
- `src/clients/<id>/` + `NEXT_PUBLIC_CLIENT_ID` + uma linha no registry. Onboarding sem tocar
  no core, documentado em `docs/ONBOARDING-CLIENT.md`.
- Tenants com repositório separado (Fernanda, Juliano). Separação correta: cada cliente tem
  seu deploy, seu domínio, seu ciclo.
- Os cinco "OS" com repos, bancos e domínios próprios. Também correto.

### Emaranhado ACIDENTAL (isto é dívida, e tem custo)

- O **motor não tem casa** — mora dentro do tenant que o pariu.
- A **lei não tem casa** — mora dentro de um dos produtos que ela governa.
- Um **tenant inteiro** mora numa branch de outro tenant.
- Os **leads de uma cliente** moram num banco de desenvolvimento compartilhado.
- Um tenant **editou o core** e ninguém percebeu por um mês.

A regra para separar os dois: **correlação desenhada é código compartilhado por decisão;
emaranhado acidental é coisa morando na casa errada por pressa.** Toda a lista abaixo é do
segundo tipo.

---

## 8. EMARANHADOS — o que está na casa errada

> Nenhum foi desembaraçado. Cada um traz risco e proposta **futura**.

### E1 · A Carta Magna mora dentro do Events OS

- **Prova:** `alsham-events-os/canon/ALSHAM_PLATFORM_FRAMEWORK_CHARTER.md`.
- **Risco:** a lei que governa todos os produtos depende do ciclo de vida de um produto de
  eventos. Se o Events OS for arquivado, vendido ou reescrito, a constituição da plataforma vai
  junto. E qualquer produto novo precisa clonar um SaaS de eventos para ler a própria lei.
- **Proposta futura:** repo `alsham-platform-framework` só com `canon/`, e os produtos passam a
  referenciá-lo. Custo baixo; o conteúdo já está escrito.

### E2 · O motor Conversion OS não existe como repositório — e a lei diz que ele não existe

- **Prova dupla.** (a) Nenhum repo de motor em `list_repos`; `src/core/` só existe dentro dos
  tenants. (b) A própria Carta Magna, §15: *"Projetos citados na Missão DNA mas **não
  localizados** (Conversion OS, Paciente Segura, BAOS, Media DNA) permanecem **fora do
  Framework** até documentação formal."* E o glossário canônico registra:
  `| Conversion OS™ | ❌ Não localizado |`.
- **Risco:** este é o achado mais forte da varredura. **O motor com mais realidade paga do
  ecossistema — três tenants, dois domínios no ar, um vendendo consulta por Stripe — é
  oficialmente o que a lei declara inexistente.** Consequências práticas: melhorias no core
  precisam ser copiadas à mão para cada tenant (foi o que produziu o **E3**); não há versão,
  changelog nem CI do motor; e um tenant novo nasce de um `cp -r` de um cliente, herdando o que
  aquele cliente tiver de específico.
- **Proposta futura:** promover o core a repo próprio (`alsham-conversion-os`) e consumir por
  package, submódulo ou template. Registrar formalmente no Framework para sair do limbo do §15.
  **É a dívida de maior alavancagem do mapa** — resolve E3 e metade do E5 de uma vez.

### E3 · O core do Juliano divergiu e ninguém viu

- **Prova:** 3 dos 73 blobs divergem de `09cd1f4`. `AuthorityProfileEngine.tsx` (rótulos
  "Tecnologia"→"Instrumentos de Governança"), `LeadCaptureEngine.tsx` (campo "Idade" removido),
  `types/conversion.ts` (`note?` removido). Detectado só em 04/08/2026, na leitura VERTEX da
  missão da Bela — **23 dias depois**.
- **Risco:** o motor deixou de ser um. Correção feita na Fernanda não chega ao Juliano; correção
  feita no Juliano não existe para ninguém. Foi divergência por necessidade real (o vocabulário
  médico não serve à advocacia), não por descuido — mas sem repo do motor não havia outro
  caminho.
- **Proposta futura:** PR [#26](https://github.com/AbnadabyBonaparte/dra-fernanda-conversion-os/pull/26)
  já resolve as duas causas por configuração (`schemaType` e `ageField`). Depois de mergeado,
  um PR no repo do Juliano troca as edições de core por config e restaura a identidade.

### E4 · Os leads da Dra. Fernanda moram num banco de desenvolvimento

- **Prova:** `fernanda_leads` está em **`ALSHAM-DEV-OS`** (`rmomtdeojaxsnyqwikcr`), ao lado de
  `agents`, `messages`, `users` e `vantage_noir_black_list`. Enquanto isso existe um projeto
  **`dra-fernanda`** (`rkjvszphwplnyzbtkaby`) dedicado — com **zero tabelas em `public`**,
  usado só como storage (`midias-site`, `midias-brutas`).
- **Risco:** dados de saúde de pacientes — dado pessoal **sensível** (LGPD Art. 5º, II) — num
  projeto chamado DEV, compartilhado com tabelas de outros produtos. O raio de explosão de um
  incidente ou de um `drop` acidental atravessa clientes. E a cliente tem projeto próprio: o
  dado está na casa errada **tendo casa certa disponível**.
- **Nota honesta:** RLS está **ligada** na tabela e o comentário do schema declara gravação via
  `service_role`. A separação é o problema, não a permissão.
- **Proposta futura:** migrar `fernanda_leads` para o projeto `dra-fernanda`, com plano de corte
  e retenção. Fazer o mesmo desde o dia zero na Bela.

### E5 · Um tenant inteiro dentro do repositório de outro

- **Prova:** `dra-bela-conversion-os/` vive na branch `claude/dra-bela-conversion-os-0pgdzc` de
  `dra-fernanda-conversion-os` (PR #25). Foi preciso até uma linha em `tsconfig.json` da
  Fernanda (`exclude`) para o typecheck dela não quebrar com a app aninhada.
- **Risco:** enquanto durar, o site de uma cliente é um diretório no repositório de outra
  cliente. Se o PR for mergeado por engano, o repo da Fernanda passa a carregar a aplicação da
  Bela em produção.
- **Proposta futura:** os 8 passos do §6. É bloqueio de permissão, não de engenharia.

### E6 · Deploys de produção que nunca aconteceram

- **Prova:** `latestDeployment.target` na API da Vercel.
  - `dr-juliano-sguizardisguizardi` → `null` (preview), último em **12/07/2026**
  - `alsham-business-os` → `null` (preview), último em **12/08/2026**
  - `alsham-quantum` → `null` (preview), último em **12/08/2026**
- **Risco:** três domínios canônicos servindo — ou não servindo — a partir de um deploy que a
  Vercel não classifica como produção. No caso do Juliano, o site está anunciado como no ar em
  `drjulianosguizardi.alshamglobal.com.br` há um mês.
- **NÃO VERIFICADO:** não busquei o HTML dos domínios nesta passada. `target=null` prova o
  estado do deploy, **não** prova que o domínio está fora do ar — pode haver produção anterior
  servindo. A prova do bolo aqui é `HTTP 200 + título esperado`, e ela falta.
- **Proposta futura:** incluir os três na checagem 2 da Ronda (sites vivos nos domínios
  canônicos) e rodar a contra-prova de verdade.

### E7 · Projeto Vercel `api` — casca vazia

- **Prova:** `latestDeployment: null`, `domains: []`, criado em 06/2026, nunca deployado.
- **Risco:** baixo, mas é superfície de confusão — um projeto chamado `api` sugere backend
  compartilhado que não existe.
- **Proposta futura:** arquivar, ou documentar a intenção.

### E8 · Três "núcleos" antigos ainda ativos no Supabase

- **Prova:** `alsham-core` (08/2025), `ALSHAM_MPC_CORE` (10/2025), `suna-core` (07/2025) — os
  três `ACTIVE_HEALTHY`, em três regiões diferentes.
- **Risco:** custo mensal e ambiguidade — "core" três vezes, e nenhuma delas é o `core` do
  Business OS (que é o schema real, com 386 linhas de auditoria).
- **NÃO VERIFICADO:** não conferi se algum deles tem tráfego. Sem isso não dá para dizer se são
  legado morto ou infraestrutura viva.
- **Proposta futura:** varredura de uso antes de qualquer decisão. Colide com a **Lei do Sol
  Único** da Constituição da Casa: cada natureza de coisa tem uma fonte só.

---

## 9. O que esta varredura NÃO alcançou

Declarado, não escondido (Lei 7):

| Lacuna | Por quê |
|---|---|
| **Fatura em atraso da org ALSHAM GLOBAL** | O MCP do Supabase não expõe billing. Só `plan: "pro"`. Precisa do painel |
| Domínios e último deploy de 14 projetos Vercel satélites | Não detalhados nesta passada; todos fora da cadeia tese→lei→fábrica→tenant |
| Ligação repo ↔ projeto Vercel | **Inferida** por correlação de timestamp, não lida do campo `link` do projeto |
| HTTP dos domínios | Nenhum `GET` foi feito. `target=null` não prova domínio fora do ar |
| Tráfego dos três "cores" antigos | Não medido |
| Stripe | Nenhuma chave consultada. Referências só por nome de variável de ambiente |
| `STAGESET-` | Clonado; só documentos de produto, sem código nem deploy |

---

## 10. Ordem sugerida de desembaraço (nada executado)

Da maior alavancagem para a menor:

1. **E2** — dar repo ao Conversion OS. Resolve E3 e metade do E5.
2. **E5** — dar repo à Bela (bloqueio de permissão, 3 minutos do dono).
3. **E4** — mover os leads da Fernanda para o projeto dela.
4. **E6** — rodar a contra-prova de HTTP nos três domínios em preview.
5. **E1** — dar repo à Carta Magna.
6. **E8** — medir os três cores antes de decidir.
7. **E7** — arquivar o `api`.

---

*Varredura read-only. Nenhum arquivo de produto, banco, deploy ou domínio foi alterado.*
*Ronda das Duas Cascatas · Lei da Contra-Prova · `canon/RONDA-DAS-DUAS-CASCATAS.md`*
