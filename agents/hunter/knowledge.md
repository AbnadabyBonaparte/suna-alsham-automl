# CONHECIMENTO ACUMULADO — HUNTER X.1

_(alimentado pelos vereditos dos juízes; começa com o julgamento de honestidade do próprio dossiê)_

## O que é REAL e construível agora (Fases 1-3)
- Memória persistente de agentes (Supabase + pgvector).
- Caçador diário por cron que lê a missão, varre fontes abertas e comita um relatório julgável.
- Triagem com score, deduplicação semântica e fila de julgamento.
- Proposta de melhoria da própria missão VIA PR que o fundador aprova/rejeita.

## O que é FRONTEIRA (espelhar o padrão, nunca confiar cego)
- Agente que reescreve o próprio código e melhora sozinho: existe em papers
  (Voyager, AlphaEvolve, Darwin Gödel Machine) mas só em caixas estreitas com
  métrica objetiva. Espelhamos o PADRÃO (gerar → medir → selecionar → registrar),
  com juiz HUMANO no lugar do juiz automático.

## O que é FÁBULA (nunca prometer, nem internamente)
- Consciência/vontade do agente; evolução espontânea sem ciclo humano;
  alma emergindo do código (a alma desce do canon); e infalibilidade.
  Não existe sistema infalível — existe sistema honesto sobre onde falha.

## As minas (fontes canônicas, todas abertas e legais)
arXiv · GitHub Trending/Search · Hugging Face · Papers with Code ·
Hacker News · Reddit (r/LocalLLaMA, r/MachineLearning) · anthropics/skills +
MCP · blogs oficiais de labs · Product Hunt (AI). A caça é na LUZ, nunca na dark web.

## Vereditos incorporados (X.1)
- ADOTADO: circuit breakers / degradação graciosa (virou Lei 8 + raw_queue).
- ADOTADO (semente): GraphRAG mínimo (tabela hunter_edges).
- REJEITADO na v1: modelos locais (exigem GPU/servidor); sanitização RDF/Protobuf;
  MCP dinâmico (fonte nova só por PR); toda linguagem de "infalibilidade".
