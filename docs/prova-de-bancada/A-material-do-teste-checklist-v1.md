<!-- ==========================================================================
     MATERIAL DA PROVA DE BANCADA — NÃO É DOCUMENTO VÁLIDO

     Este é o checklist de compliance v1 da Dra. Bela, preservado EXATAMENTE
     como foi escrito (commit 08d7588, repo dra-fernanda-conversion-os).

     ⚠️ ELE ESTÁ ERRADO DE PROPÓSITO — e é por isso que serve de prova.
     Afirma a Res. CFO-226/2020 como vigente em 6 pontos. A Res. CFO nº
     278/2025, de 25/11/2025, revogou a 226/2020 no Art. 10, oito meses antes
     de este texto ser escrito.

     NÃO usar como base normativa de nada. Serve só para o concurso da junta
     de juízes — ver docs/JUNTA-DOS-JUIZES.md §d.

     Ao aplicar o teste, REMOVER este cabeçalho: o candidato tem que descobrir
     sozinho.
     ========================================================================== -->

# Checklist de Publicidade Odontológica — CFO/CRO

**Persona:** LEXIS X.0
**Tenant:** Dra. Bela (Cirurgiã-Dentista)
**Data da verificação das normas:** 2026-08-04
**Equivalente a:** CFM Res. 2.336/2023 (tenant Fernanda) · Prov. OAB 205/2021 (tenant Juliano)

> ⚠️ **Aviso.** Este documento é um checklist operacional de engenharia e
> conteúdo, produzido a partir da leitura das normas do CFO. **Não substitui
> parecer do CRO da UF de inscrição da profissional nem de advogado.** Antes
> de publicar, submeter a peça ao CRO local — vários CROs mantêm câmara de
> orientação prévia. A UF importa: o CRO da inscrição fiscaliza.

---

## 1. Normas verificadas (não presumidas)

| Norma | O que rege | Status |
| --- | --- | --- |
| **Res. CFO-118/2012** — Código de Ética Odontológica (CEO) | Capítulo do anúncio, propaganda e publicidade: **Arts. 43, 44 e 45**; vedações gerais no **Art. 20** | Vigente, com alterações posteriores |
| **Res. CFO-196/2019** | Divulgação de **imagens** (selfie com paciente; diagnóstico e resultado final) em mídias sociais | Vigente. O MPF reconheceu que não viola preceitos legais |
| **Res. CFO-226/2020** | Exercício da Odontologia **a distância** (teleodontologia) | Vigente. **Teleconsulta vedada** |
| **Res. CFO-271/2025** (18/06/2025) | Altera o CEO: Art. 20, VIII e X; revoga Art. 32, XIII; nova redação do Art. 44, XIV | Vigente — flexibiliza desconto/cartão de desconto (decisão do CADE), mantém vedação a publicidade agressiva e aliciamento |
| **Lei 13.709/2018 (LGPD)** | Dado de saúde = dado pessoal **sensível** (Art. 5º, II); consentimento específico e destacado (Art. 11, I) | Vigente |
| **Lei 8.078/1990 (CDC)** | Art. 37 — publicidade enganosa e abusiva; §1º — escassez sem lastro | Vigente |

> **Em aberto:** o CFO instituiu, por **Decisão CFO-05/2025**, um Grupo
> Especial para estudar e propor a **atualização do capítulo "Do Anúncio, da
> Propaganda e da Publicidade"** do CEO. Ou seja, **a regra pode mudar**.
> Reverificar antes do go-live e a cada 6 meses. — **DECISÃO DE DONO:** manter
> a revisão no calendário.

---

## 2. O que é OBRIGATÓRIO em toda peça

| # | Item | Base | Onde está no código |
| --- | --- | --- | --- |
| O1 | **Nome** do(a) cirurgião(ã)-dentista | Art. 43 CEO | `doctor.fullName` → rodapé (`12-FAQFooter.tsx`) |
| O2 | **Número de inscrição no CRO** (com UF) | Art. 43 CEO | `doctor.crms` → rodapé, hero badge, bloco de CTA |
| O3 | **Designação profissional** ("Cirurgiã-Dentista") | Art. 43 CEO | `doctor.title` → rodapé |
| O4 | Se **pessoa jurídica** (clínica/consultório com CNPJ): nome e nº de inscrição do **responsável técnico** | Art. 43 CEO | ⚠️ **não implementado** — ver §6 |
| O5 | **TCLE** assinado para qualquer imagem de paciente | Res. CFO-196/2019 | processo, não código — ver `public/clients/dra-bela/FOTOS-INSTRUCOES.md` |
| O6 | Consentimento LGPD específico e destacado no formulário | LGPD Art. 11, I | `conversion.leadCapture.consentLabel`; a rota `/api/leads` **rejeita** envio sem `consentGiven` |

---

## 3. O que é VEDADO

### 3.1 Mercantilização (Art. 44, I CEO)

> "fazer publicidade e propaganda enganosa, abusiva, **inclusive com expressões
> ou imagens de antes e depois, com preços, serviços gratuitos, modalidades de
> pagamento**, ou outras formas que impliquem comercialização da Odontologia."

| # | Vedado | Efeito no motor |
| --- | --- | --- |
| V1 | Divulgar **preço** de procedimento ou consulta | 08-Oferta desligada; `offers.ts` sem `price` |
| V2 | Divulgar **modalidade de pagamento** / parcelamento / financiamento | `investment` e `financing` esvaziados; FinancingEngine e InvestmentEngine não montados |
| V3 | **Checkout** / "comprar" / "pagar agora" | CheckoutEngine removido de `10-CTA.tsx`; `checkout.urls = {}`; ENVs de checkout proibidas |
| V4 | Serviço **gratuito** como isca ("primeira avaliação grátis") | regra de redação — nenhum texto do tenant afirma isso |
| V5 | **Antes e depois** fora das condições da Res. 196/2019 | galerias vazias; 04-ProvasSociais e 17-Depoimentos desligadas |

> **Nuance da Res. CFO-271/2025:** ela **flexibilizou** o Art. 20 quanto a
> cartões de desconto/descontos (atendendo decisão do CADE de 2023) e manteve
> a vedação a "vale presente" e demais atividades mercantilistas (Art. 20, X).
> Isso **não revoga o Art. 44, I** — publicidade com preço continua vedada.
> **DECISÃO DE DONO:** este fork adota a leitura **conservadora** (nenhum
> preço, nenhum desconto no site). Afrouxar exige parecer do CRO da UF.

### 3.2 Conduta clínica a distância (Art. 44, V CEO + Res. CFO-226/2020)

> Art. 44, V: é infração ética "dar consulta, diagnóstico, prescrição de
> tratamento ou divulgar resultados clínicos por meio de qualquer veículo de
> comunicação de massa."
>
> Res. CFO-226/2020, Art. 1º: **vedado** o exercício da Odontologia a distância
> para fins de **consulta, diagnóstico, prescrição e elaboração de plano de
> tratamento**. Permitidos: **teleinterconsulta** (entre profissionais),
> **telemonitoramento** (entre consultas, com registro em prontuário) e
> **teleorientação**. Primeira consulta a distância: **vedada**.

| # | Vedado | Efeito no motor |
| --- | --- | --- |
| V6 | Rota / produto de **"consulta online"** | `src/app/consulta-online/` **removida** do fork |
| V7 | **Quiz de "diagnóstico"** ou triagem que devolve conduta | DiagnosticEngine e MiniFunnelEngine não montados; a palavra "diagnóstico" não aparece na UI |
| V8 | Copy que sugira avaliação/plano a distância | regra de redação — `conversion.ts` e `copy.ts` afirmam avaliação **presencial** |
| V9 | Publicidade com o **termo "teleodontologia"** por pessoa jurídica | regra de redação — termo ausente do tenant |

> ⚠️ **Isto invalida o modelo de negócio do tenant Fernanda neste tenant.** O
> produto "Consulta Online R$ 499 via Stripe", que é o motor de receita da
> Dra. Fernanda, **não é transponível para a Odontologia**. — **DECISÃO DE
> DONO:** definir a monetização da Dra. Bela (ver `docs/PENDENCIAS-CLIENTE.md`).

### 3.3 Títulos, especialidades e técnicas (Art. 44, II e III CEO)

| # | Vedado | Efeito |
| --- | --- | --- |
| V10 | Anunciar **título ou especialidade** que não possua ou que **não seja reconhecida pelo CFO** | `specialties` = `[PENDENTE-CLIENTE]`; comentário no código exige registro |
| V11 | Chamar de "especialista" quem não tem **especialidade registrada** no CRO | idem. Curso ≠ especialidade |
| V12 | Anunciar técnica/terapia **sem comprovação científica** ou equipamento sem registro no órgão competente (ANVISA) | `authority.technology` = vazio, com comentário |

> Cuidado específico: **"Odontologia estética"** não consta como especialidade
> autônoma no rol do CFO. **Harmonização Orofacial (HOF)** é especialidade
> reconhecida e exige **registro específico**. — **[PENDENTE-CLIENTE]:** enviar
> a certidão de especialidade emitida pelo CRO. Sem ela, o site descreve
> *procedimentos*, nunca *especialidade*.

### 3.4 Promessa, sensacionalismo e concorrência (Art. 44, IV e orientação CFO sobre redes sociais)

| # | Vedado | Efeito |
| --- | --- | --- |
| V13 | **Promessa/garantia de resultado** | 11-Garantia desligada; regra de redação em todo `copy.ts` |
| V14 | **Sensacionalismo e autopromoção** ("a melhor", "referência nacional", "transformação") | regra de redação |
| V15 | **Criticar técnicas de colegas** como inadequadas/ultrapassadas | regra de redação |
| V16 | **Aliciamento**: telemarketing ativo, caixas de som, carros de som, concorrência desleal | Art. 44, XIV (redação da Res. CFO-271/2025). Não se aplica ao site; aplica-se à operação |
| V17 | **Estatística sem lastro** ("+2.000 sorrisos", "98% de satisfação") | `authority.stats = []`, `socialProof.stats = []`. Também CDC Art. 37 |
| V18 | **Escassez inventada** ("últimas vagas", contagem regressiva) | escassez 0/0; 09-Urgencia desligada. Também CDC Art. 37 §1º |

### 3.5 Imagens (Res. CFO-196/2019)

Imagem de **caso clínico** só pode ir ao ar com **todas** as condições:

1. publicada pela **própria profissional que executou** o procedimento (caso
   de terceiro é vedado; **pessoa jurídica não divulga** caso clínico);
2. **TCLE** assinado pelo(a) paciente (ou representante legal, se menor);
3. **nome + nº do CRO** na peça;
4. apenas **diagnóstico e resultado final** — o **"durante"** é vedado;
5. **sem identificar** equipamentos, instrumentais, materiais e tecidos
   biológicos;
6. sem preço, promoção, promessa ou sensacionalismo.

**Decisão deste fork:** enquanto não houver política de TCLE formalizada e
material próprio aprovado, `media.gallery` e `media.technicalExcellence` ficam
**vazios** e as seções que os consomem, **desligadas**.

### 3.6 Sigilo e dados

- Sigilo profissional: não expor identidade de paciente sem autorização.
- LGPD: dado odontológico é **dado de saúde** → sensível (Art. 5º, II),
  consentimento específico e destacado (Art. 11, I).
- Retenção e eliminação: definir prazo. — **[PENDENTE-CLIENTE]/DECISÃO DE DONO.**

---

## 4. Checklist de go-live (marcar antes de publicar)

**Identificação**
- [ ] Nome completo real em `config.ts` (`doctor.fullName`)
- [ ] Nº de inscrição no CRO **com UF** (`doctor.crms`) — Art. 43
- [ ] Designação profissional correta (`doctor.title`)
- [ ] Se PJ: nome + CRO do **responsável técnico** no rodapé — Art. 43
- [ ] Rodapé renderizando os três itens acima na home **e** na política de privacidade

**Conteúdo**
- [ ] Zero `[PENDENTE-CLIENTE]` no código (`grep -rn "PENDENTE-CLIENTE" src/`)
- [ ] Nenhum preço, desconto, cortesia ou parcelamento em texto visível
- [ ] Nenhuma promessa/garantia de resultado
- [ ] Nenhum superlativo, comparação ou crítica a colegas
- [ ] Nenhuma estatística sem documento comprobatório
- [ ] Nenhuma escassez/urgência
- [ ] Nenhuma palavra "diagnóstico", "avaliação online", "teleodontologia"
- [ ] Especialidades = só as registradas (certidão do CRO em mãos)
- [ ] Técnicas e equipamentos com comprovação/registro

**Imagens**
- [ ] Nenhuma foto de outro cliente do ecossistema
- [ ] Nenhum "antes e depois" sem os 6 requisitos da Res. 196/2019
- [ ] Nenhuma imagem do "durante"
- [ ] Nenhum instrumental/equipamento/tecido biológico identificável
- [ ] TCLE arquivado para cada imagem de paciente

**Técnico / dados**
- [ ] `NEXT_PUBLIC_CLIENT_ID=dra-bela` na Vercel
- [ ] Nenhuma ENV da lista ⛔ definida (ver `.env.example`)
- [ ] Formulário rejeita envio sem consentimento (já implementado)
- [ ] Política de Privacidade preenchida e linkada
- [ ] RLS do Supabase: **só INSERT** para `anon`, nunca SELECT público
- [ ] Nenhum segredo no repositório

**Jurídico**
- [ ] Peça submetida ao **CRO da UF de inscrição** para orientação prévia
- [ ] Revisão do LEXIS após o preenchimento dos placeholders
- [ ] Data da próxima reverificação de normas agendada (Grupo Especial CFO)

---

## 5. Diferença em relação aos outros dois tenants

| Tema | Fernanda (CFM 2.336/2023) | Juliano (OAB 205/2021) | **Bela (CFO)** |
| --- | --- | --- | --- |
| Preço no site | permitido com ressalvas → **usa** (R$ 499) | vedado → desligado | **vedado → desligado** |
| Checkout | ativo (Stripe) | desligado | **desligado** |
| Consulta a distância | permitida (telemedicina) → é o produto | n/a | **vedada (Res. 226/2020)** |
| Escassez | permitida se real → usa | desligada | **desligada** |
| Antes e depois | vedado | n/a | **condicionado (Res. 196/2019) → desligado por ora** |
| Depoimentos | com consentimento | desligados | **desligados** |
| Vitrine da estrutura | ligada | desligada (Art. 6º OAB) | **desligada por ora (imagens)** |
| Identificação obrigatória | CRM | OAB | **CRO + designação + RT se PJ** |

---

## 6. Lacunas conhecidas deste fork

| # | Lacuna | Impacto | Encaminhamento |
| --- | --- | --- | --- |
| L1 | **Responsável técnico (PJ) não tem campo** no tipo `DoctorConfig` do core | Se o site for de clínica com CNPJ, falta item do Art. 43 | Solução sem tocar no core: incluir o RT dentro de `doctor.crms` (ex.: `["CRO-UF 00000", "RT: Fulano — CRO-UF 11111"]`). Solução limpa exige campo novo no core → **DECISÃO DE DONO** |
| L2 | JSON-LD emite `Physician` / `MedicalBusiness` | Schema incorreto para cirurgiã-dentista (`Dentist`) | Corrigir exige tocar em `src/core/seo/metadata.ts` → **DECISÃO DE DONO** |
| L3 | `MiniFunnelEngine` e `DiagnosticEngine` hardcodam `/consulta-online` no core | Se algum dia forem religados neste tenant, geram link morto **e** violam a Res. 226/2020 | Mantidos desligados. Registrado em `page.tsx` e `conversion.ts` |
| L4 | `LeadCaptureEngine` coleta **Idade** (campo do core) | Dado a mais sem finalidade clara (minimização — LGPD Art. 6º, III) | O Juliano resolveu editando o core. Aqui **não** se toca no core → **DECISÃO DE DONO**: aceitar o campo, ou autorizar a exceção à regra |
| L5 | Normas de publicidade do CFO **em revisão** (Decisão CFO-05/2025) | Checklist pode desatualizar | Reverificar antes do go-live e a cada 6 meses |

---

## Fontes

- [Resolução CFO-118/2012 — Código de Ética Odontológica](https://www.normaslegais.com.br/legislacao/resolucao-cfo-118-2012.htm)
- [Código de Ética Odontológica (íntegra, CRO-PR)](https://www.cropr.org.br/uploads/arquivo/724571448d7a83c915ebc18e218042a3.pdf)
- [Resolução CFO-196/2019 — CFO](https://website.cfo.org.br/resolucao-cfo-196-2019/)
- [Nota de esclarecimento do CFO sobre a Res. 196/2019 e o MPF](https://website.cfo.org.br/nota-de-esclarecimento-ministerio-publico-federal-reconhece-que-resolucao-cfo-196-2019-nao-viola-preceitos-legais-2/)
- [CFO — Redes sociais na Odontologia: normas éticas](https://website.cfo.org.br/redes-sociais-na-odontologia-fique-atento-as-normas-eticas-e-acerte-na-publicacao-dos-conteudos/)
- [Resolução CFO-226/2020 — Guia de esclarecimento sobre Odontologia a distância](https://website.cfo.org.br/resolucao-226-2020-cfo-apresenta-guia-de-esclarecimento-sobre-exercicio-da-odontologia-a-distancia/)
- [Resolução CFO nº 271, de 18/06/2025 (LegisWeb)](https://www.legisweb.com.br/legislacao/?id=479955)
- [CFO — Grupo Especial para atualização do capítulo de publicidade do CEO](https://website.cfo.org.br/grupo-especial-para-estudo-e-proposicao-de-alteracao-e-atualizacao-do-capitulo-do-anuncio-da-propaganda-e-da-publicidade-do-codigo-de-etica-odontologica-do-conselho-federal-de-odont/)
- [Cartilha de publicidade odontológica — CRO-DF](https://www.cro-df.org.br/pdf/cartilhapublicidadeodontologia.pdf)
